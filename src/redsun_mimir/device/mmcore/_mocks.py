"""Hardware-free stand-ins for the Micro-Manager devices."""

from __future__ import annotations

from ophyd_async.core import (
    AsyncStatus,
    StandardReadable,
    StandardReadableFormat,
    soft_signal_rw,
)

from ._serial import MMSerialDevice
from ._shuttered import MMSpectraShutteredDevice
from ._stated import MMASIFilterWheel, MMASIFWController


class MockMMSerialDevice(MMSerialDevice):
    """In-memory replacement for :class:`MMSerialDevice`.

    The constructor deliberately does not create a ``CMMCorePlus`` instance or
    open a serial port.  Its configuration signals mirror the properties
    exposed by the hardware-backed device.
    """

    def __init__(
        self,
        name: str,
        *,
        port: str = "MOCK",
        baudrate: int = 115200,
        device: str | None = None,
        answer_timeout: int = 500,
    ) -> None:
        with self.add_children_as_readables(StandardReadableFormat.CONFIG_SIGNAL):
            self.port = soft_signal_rw(str, initial_value=port)
            self.device = soft_signal_rw(str, initial_value=device or port)
            self.baudrate = soft_signal_rw(int, initial_value=baudrate)
            self.answer_timeout = soft_signal_rw(int, initial_value=answer_timeout)

        StandardReadable.__init__(self, name=name)


class MockMMASIFWController(MMASIFWController):
    """In-memory replacement for the ASI filter-wheel serial controller."""

    def __init__(self, name: str, *, port: str = "serial") -> None:
        with self.add_children_as_readables(StandardReadableFormat.CONFIG_SIGNAL):
            self.port = soft_signal_rw(str, initial_value=port)

        StandardReadable.__init__(self, name=name)


class MockMMASIFilterWheel(MMASIFilterWheel):
    """In-memory ASI wheel with the production labels and colour presets."""

    def __init__(
        self,
        name: str,
        *,
        wheel_number: int = 0,
        num_positions: int = 8,
        initial_position: int = 0,
    ) -> None:
        if num_positions <= 0:
            raise ValueError("num_positions must be greater than zero")
        if not 0 <= initial_position < num_positions:
            raise ValueError(
                "initial_position must be within the configured position range"
            )

        with self.add_children_as_readables():
            self.position = soft_signal_rw(int, initial_value=initial_position)

        with self.add_children_as_readables(StandardReadableFormat.CONFIG_SIGNAL):
            self.wheel_number = soft_signal_rw(int, initial_value=wheel_number)
            self.num_positions = soft_signal_rw(int, initial_value=num_positions)

        StandardReadable.__init__(self, name=name)


class MockMMSpectraShutteredDevice(MMSpectraShutteredDevice):
    """In-memory Lumencor Spectra shutter and channel controls."""

    def __init__(
        self,
        name: str,
        *,
        port: str = "serial25",
        setle_type: str = "SpectraX",
        wavelength: int = 0,
    ) -> None:
        with self.add_children_as_readables():
            self.enabled = soft_signal_rw(bool, initial_value=False)
            self.intensity = soft_signal_rw(float, initial_value=0.0)
            for channel in self.channel_names:
                setattr(
                    self,
                    f"{channel.lower()}_enable",
                    soft_signal_rw(str, initial_value="0"),
                )
                setattr(
                    self,
                    f"{channel.lower()}_level",
                    soft_signal_rw(int, initial_value=0),
                )

        with self.add_children_as_readables(StandardReadableFormat.CONFIG_SIGNAL):
            self.port = soft_signal_rw(str, initial_value=port)
            self.setle_type = soft_signal_rw(str, initial_value=setle_type)
            self.wavelength = soft_signal_rw(int, initial_value=wavelength)
            self.egu = soft_signal_rw(str, initial_value="%")

        StandardReadable.__init__(self, name=name)

    @AsyncStatus.wrap
    async def trigger(self) -> None:
        """Toggle the simulated shutter state."""
        current = await self.enabled.get_value()
        await self.enabled.set(not current)
