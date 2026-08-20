from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MMAdapterInfo:
    """Information about a Micro-Manager adapter and its devices."""

    adapter: str
    """Adapter name as recognized by the Micro-Manager Core."""

    device: str
    """Device name as recognized by the Micro-Manager Core."""


@dataclass
class MMSerialAdapterInfo(MMAdapterInfo):
    """Legacy serial-adapter metadata retained for ARH donor devices."""

    port: str
    """Serial port used by the adapter."""

    baudrate: int
    """Serial baud rate."""
