from __future__ import annotations

from typing import TYPE_CHECKING

from ophyd_async.core import StandardReadable
from pymmcore_plus import CMMCorePlus as Core
from redsun.device import DeviceMap
from redsun.log import Loggable

from ._backend import mm_position_signal
from ._common import MMAdapterInfo, MMSerialAdapterInfo

if TYPE_CHECKING:
    from ophyd_async.core import SignalRW


class MMDemoXYStage(StandardReadable, Loggable):
    """Demo stage device."""

    def __init__(self, name: str, *, units: str = "um") -> None:
        adapter_info = MMAdapterInfo(
            adapter="DemoCamera",
            device="DXYStage",
        )
        self.core = Core.instance()
        self.core.loadDevice(name, adapter_info.adapter, adapter_info.device)
        self.core.initializeDevice(name)
        with self.add_children_as_readables():
            self.x = mm_position_signal(self.core, name, "x", units)
            self.y = mm_position_signal(self.core, name, "y", units)
        self.axis = DeviceMap({"x": self.x, "y": self.y})
        super().__init__(name)

class MMASIXYStage(StandardReadable):
    """ASI XY stage device."""

    axis: DeviceMap[SignalRW[float]]

    def __init__(self, name: str, *, units: str = "um") -> None:
        adapter_info = MMSerialAdapterInfo(
            adapter="ASIStage",
            device="XYStage",
            port="COM3",
            baudrate=115200
        )
        self.core = Core.instance()
        self.core.loadDevice(name, adapter_info.adapter, adapter_info.device)
        if adapter_info.port:
            self.core.setProperty(name, "Port", adapter_info.port)
        self.core.initializeDevice(name)
        with self.add_children_as_readables():
            self.x = mm_position_signal(self.core, name, "x", units)
            self.y = mm_position_signal(self.core, name, "y", units)
        self.axis = DeviceMap({"x": self.x, "y": self.y})
        super().__init__(name)

class MMDemoZStage(StandardReadable):
    """Demo stage device."""

    axis: DeviceMap[SignalRW[float]]

    def __init__(self, name: str, *, units: str = "um") -> None:
        adapter_info = MMAdapterInfo(
            adapter="DemoCamera",
            device="DStage",
        )
        self.core = Core.instance()
        self.core.loadDevice(name, adapter_info.adapter, adapter_info.device)
        self.core.initializeDevice(name)
        with self.add_children_as_readables():
            self.z = mm_position_signal(self.core, name, "z", units)
        self.axis = DeviceMap({"z": self.z})
        super().__init__(name)

class MMASIZStage(StandardReadable):
    """ASI Z stage device."""

    axis: DeviceMap[SignalRW[float]]

    def __init__(self, name: str, *, units: str = "um") -> None:
        adapter_info = MMSerialAdapterInfo(
            adapter="ASIStage",
            device="ZStage",
            port="COM3",
            baudrate=115200
        )
        self.core = Core.instance()
        self.core.loadDevice(name, adapter_info.adapter, adapter_info.device)
        if adapter_info.port:
            self.core.setProperty(name, "Port", adapter_info.port)
        self.core.initializeDevice(name)
        with self.add_children_as_readables():
            self.z = mm_position_signal(self.core, name, "z", units)
        self.axis = DeviceMap({"z": self.z})
        super().__init__(name)