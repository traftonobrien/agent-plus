"""Synthetic interface-consumer smoke for an installed Agent+ project."""

from scripts.interface_consumer_guard import INTERFACE_CONSUMER_SCHEMA_VERSION


def test_interface_consumer_schema_version_is_available() -> None:
    assert INTERFACE_CONSUMER_SCHEMA_VERSION == "agent-plus-interface-consumer-closure/v1"
