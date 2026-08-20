"""Tests for hardware-free MMCore device stand-ins."""

from __future__ import annotations

import pytest

from redsun_mimir.configurations._mmcore_mock import create_mmcore_mock_container
from redsun_mimir.device.mmcore import (
    MockMMASIFilterWheel,
    MockMMASIFWController,
    MockMMSerialDevice,
    MockMMSpectraShutteredDevice,
)


async def test_mock_serial_configuration() -> None:
    serial = MockMMSerialDevice("serial", port="MOCK_COM3", baudrate=115200)
    await serial.connect(mock=True)

    configuration = await serial.read_configuration()

    assert configuration["serial-port"]["value"] == "MOCK_COM3"
    assert configuration["serial-baudrate"]["value"] == 115200
    assert configuration["serial-answer_timeout"]["value"] == pytest.approx(500.0)


async def test_mock_filter_wheel_uses_production_labels_and_presets() -> None:
    wheel = MockMMASIFilterWheel("filterwheel", initial_position=3)
    await wheel.connect(mock=True)

    await wheel.set_label("closed")
    assert await wheel.position.get_value() == 4

    await wheel.apply_color_preset("470_cyan")
    assert await wheel.position.get_value() == 6

    with pytest.raises(ValueError, match="Unknown label"):
        await wheel.set_label("missing")


async def test_mock_filter_wheel_controller_configuration() -> None:
    controller = MockMMASIFWController("fw_controller", port="serial")
    await controller.connect(mock=True)

    configuration = await controller.read_configuration()

    assert configuration["fw_controller-port"]["value"] == "serial"


async def test_mock_spectra_shutter_and_channels() -> None:
    spectra = MockMMSpectraShutteredDevice("spectra")
    await spectra.connect(mock=True)

    assert await spectra.enabled.get_value() is False
    await spectra.trigger()
    assert await spectra.enabled.get_value() is True

    await spectra.apply_full_preset("640_red", power_overrides={"Red": 42})
    assert await spectra.red_enable.get_value() == "1"
    assert await spectra.cyan_enable.get_value() == "0"
    assert await spectra.red_level.get_value() == 42


def test_mock_configuration_builds_without_hardware() -> None:
    container = create_mmcore_mock_container()

    container.build()
    container.connect_devices(mock=True)

    assert set(container.devices) == {
        "serial",
        "serial25",
        "spectra",
        "fw_controller",
        "filterwheel",
    }
    assert isinstance(container.devices["serial"], MockMMSerialDevice)
    assert isinstance(container.devices["spectra"], MockMMSpectraShutteredDevice)
    assert isinstance(container.devices["filterwheel"], MockMMASIFilterWheel)

    container.shutdown()
