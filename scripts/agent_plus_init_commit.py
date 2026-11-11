"""Publish staged Agent+ controls without replacing project files."""

import ctypes
import errno
import os
import shutil
import signal
import stat
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

INTERRUPTS = (signal.SIGHUP, signal.SIGINT, signal.SIGTERM)
DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
EXCLUSIVE_ROOTS = {".cursor", ".agent-plus", ".planning"}
LIBC = ctypes.CDLL(None, use_errno=True)


class InterruptedInstall(Exception):
    def __init__(self, signum: int):
        self.signum = signum


def interrupt(signum, _frame):
    raise InterruptedInstall(signum)


@contextmanager
def record_mutation():
    # Defer signals until the syscall and its ownership record are both complete.
    previous = signal.pthread_sigmask(signal.SIG_BLOCK, INTERRUPTS)
    try:
        yield
    finally:
        signal.pthread_sigmask(signal.SIG_SETMASK, previous)


def directory_rename():
    """Return the native no-replace rename on the supported installer hosts."""
    libc = LIBC
    if sys.platform == "darwin":
        rename, flag = libc.renameatx_np, 0x00000004  # RENAME_EXCL
    elif sys.platform == "linux" and hasattr(libc, "renameat2"):
        rename, flag = libc.renameat2, 1  # RENAME_NOREPLACE
    else:
        raise OSError("Agent+ initialization requires a no-replace directory rename")
    rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    rename.restype = ctypes.c_int

    def publish_directory(source_fd, target_fd, name):
        encoded = os.fsencode(name)
        if rename(source_fd, encoded, target_fd, encoded, flag) != 0:
            error = ctypes.get_errno()
            raise OSError(error, os.strerror(error), name)

    return publish_directory


def read_native_buffer(read):
    size = read(None, 0)
    if size < 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))
    buffer = ctypes.create_string_buffer(size)
    actual = read(buffer, size)
    if actual < 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))
    if actual != size:
        raise OSError("File metadata changed during inspection")
    return buffer.raw[:size]


def extended_metadata(fd):
    if sys.platform != "darwin":
        return tuple((name, os.getxattr(fd, name)) for name in sorted(os.listxattr(fd)))

    LIBC.flistxattr.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int]
    LIBC.flistxattr.restype = ctypes.c_ssize_t
    LIBC.fgetxattr.argtypes = [
        ctypes.c_int, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint32, ctypes.c_int,
    ]
    LIBC.fgetxattr.restype = ctypes.c_ssize_t
    names = read_native_buffer(lambda buffer, size: LIBC.flistxattr(fd, buffer, size, 0))
    attributes = tuple(
        (name, read_native_buffer(
            lambda buffer, size, name=name: LIBC.fgetxattr(fd, name, buffer, size, 0, 0),
        ))
        for name in sorted(names.split(b"\0")) if name
    )
    LIBC.acl_get_fd_np.argtypes = [ctypes.c_int, ctypes.c_int]
    LIBC.acl_get_fd_np.restype = ctypes.c_void_p
    LIBC.acl_to_text.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    LIBC.acl_to_text.restype = ctypes.c_void_p
    LIBC.acl_free.argtypes = [ctypes.c_void_p]
    LIBC.acl_free.restype = ctypes.c_int
    acl = LIBC.acl_get_fd_np(fd, 0x100)  # ACL_TYPE_EXTENDED
    if not acl:
        error = ctypes.get_errno()
        if error == errno.ENOENT:
            return attributes, b""
        raise OSError(error, os.strerror(error))
    text = None
    try:
        text = LIBC.acl_to_text(acl, None)
        if not text:
            error = ctypes.get_errno()
            raise OSError(error, os.strerror(error))
        return attributes, ctypes.string_at(text)
    finally:
        if text:
            LIBC.acl_free(text)
        LIBC.acl_free(acl)


def snapshot(fd):
    before = os.fstat(fd)
    attributes = (
        before.st_mode, before.st_uid, before.st_gid,
        getattr(before, "st_flags", 0), getattr(before, "st_birthtime", None),
        extended_metadata(fd),
    )
    contents = None
    if stat.S_ISREG(before.st_mode):
        os.lseek(fd, 0, os.SEEK_SET)
        with os.fdopen(os.dup(fd), "rb") as file:
            contents = file.read(before.st_size + 1)
        attributes += (before.st_mtime_ns,)
    elif not stat.S_ISDIR(before.st_mode):
        raise OSError("Cannot inspect a nonregular install entry")
    after = os.fstat(fd)
    if before.st_ctime_ns != after.st_ctime_ns or before.st_mtime_ns != after.st_mtime_ns:
        raise OSError("Install entry changed during inspection")
    return before, attributes, contents


def unchanged(parent, name, original):
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
    try:
        expected, attributes, contents = original
        opened = os.fstat(fd)
        if not os.path.samestat(opened, expected) or (
            contents is not None and opened.st_size != len(contents)
        ):
            return False
        current = snapshot(fd)
        return (
            os.path.samestat(current[0], expected)
            and current[1:] == (attributes, contents)
            and os.path.samestat(os.stat(name, dir_fd=parent, follow_symlinks=False), current[0])
            and os.fstat(fd).st_ctime_ns == current[0].st_ctime_ns
        )
    finally:
        os.close(fd)


def inventory(stage):
    directories = []
    files = []

    def visit(folder):
        for source in sorted(folder.iterdir()):
            relative = source.relative_to(stage)
            details = source.lstat()
            if stat.S_ISDIR(details.st_mode):
                if relative.parent in (Path("scripts"), Path("tests")):
                    if source.name == "__pycache__":
                        continue
                    raise ValueError(f"Unsafe staged directory: {relative}")
                directories.append(relative)
                visit(source)
            elif stat.S_ISREG(details.st_mode):
                with source.open("rb") as file:
                    files.append((relative, snapshot(file.fileno())))
            else:
                raise ValueError(f"Unsafe staged entry: {relative}")

    visit(stage)
    files.sort(key=lambda entry: entry[0] == Path(".agent-plus/install-manifest.json"))
    return directories, files


def rollback(entries):
    for parent, name, original in reversed(entries):
        is_directory = original[2] is None
        try:
            if not unchanged(parent, name, original):
                continue
            if is_directory:
                os.rmdir(name, dir_fd=parent)
            else:
                os.unlink(name, dir_fd=parent)
        except FileNotFoundError:
            continue
        except OSError as error:
            if not is_directory or error.errno not in (errno.ENOTEMPTY, errno.EEXIST):
                print(f"Could not roll back Agent+ entry {name}: {error}", file=sys.stderr)


def publish(stage, target):
    directories, files = inventory(stage)
    rename = directory_rename()
    scratch = tempfile.mkdtemp(dir=stage)
    scratch_fd = os.open(scratch, DIRECTORY_FLAGS)
    handles = {}
    owned_directories = []
    created = []
    try:
        handles[Path(".")] = os.open(target, DIRECTORY_FLAGS)
        for relative in directories:
            parent = handles[relative.parent]
            name = relative.name
            with record_mutation():
                os.mkdir(name, dir_fd=scratch_fd)
                owned_fd = os.open(name, DIRECTORY_FLAGS, dir_fd=scratch_fd)
                owned_directories.append(owned_fd)
                original = snapshot(owned_fd)
                details = original[0]
                try:
                    rename(scratch_fd, parent, name)
                except FileExistsError:
                    if relative.parts[0] in EXCLUSIVE_ROOTS:
                        raise
                    os.rmdir(name, dir_fd=scratch_fd)
                    details = None
                else:
                    created.append((parent, name, original))
                handles[relative] = os.open(name, DIRECTORY_FLAGS, dir_fd=parent)
                if details is not None and not os.path.samestat(os.fstat(handles[relative]), details):
                    raise ValueError(f"Destination directory changed during install: {relative}")
        for relative, original in files:
            parent = handles[relative.parent]
            with record_mutation():
                os.link(stage / relative, relative.name, dst_dir_fd=parent, follow_symlinks=False)
                created.append((parent, relative.name, original))
        for relative in directories:
            current = os.stat(relative.name, dir_fd=handles[relative.parent], follow_symlinks=False)
            if not os.path.samestat(current, os.fstat(handles[relative])):
                raise ValueError(f"Destination directory changed during install: {relative}")
        signal.pthread_sigmask(signal.SIG_BLOCK, INTERRUPTS)
    except BaseException:
        signal.pthread_sigmask(signal.SIG_BLOCK, INTERRUPTS)
        rollback(created)
        raise
    finally:
        os.close(scratch_fd)
        for descriptor in owned_directories:
            os.close(descriptor)
        for descriptor in reversed(handles.values()):
            os.close(descriptor)


def main():
    stage, target = map(Path, sys.argv[1:3])
    profile = sys.argv[3]
    if stage.parent != target or not stage.name.startswith(".agent-plus-init.") or stage.is_symlink():
        print("Unsafe Agent+ staging directory", file=sys.stderr)
        return 1
    original_stage = stage.lstat()
    for signum in INTERRUPTS:
        signal.signal(signum, interrupt)
    try:
        publish(stage, target)
    except InterruptedInstall as error:
        print("Agent+ installation interrupted.", file=sys.stderr)
        return 128 + error.signum
    except FileExistsError as error:
        print(f"Agent+ destination already exists: {error}", file=sys.stderr)
        return 1
    except (OSError, ValueError) as error:
        print(f"Agent+ installation failed: {error}", file=sys.stderr)
        return 1
    finally:
        signal.pthread_sigmask(signal.SIG_BLOCK, INTERRUPTS)
        if stage.exists() and os.path.samestat(stage.lstat(), original_stage):
            shutil.rmtree(stage)
    print(f"Initialized Agent+ {profile} profile at {target}")
    print(f'Next: cd "{target}" && scripts/agent-plus-doctor.sh --target .')
    print("Then: use $agent-plus-discovery-grill if the decision is unclear; otherwise draft the first contract.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
