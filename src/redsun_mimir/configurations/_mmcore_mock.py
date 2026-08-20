from __future__ import annotations

import logging
from pathlib import Path

from redsun.containers import declare_device, declare_presenter, declare_view
from redsun.qt import QtAppContainer

_CONFIG = Path(__file__).parent / "mmcore_mock_configuration.yaml"


def create_mmcore_mock_container() -> QtAppContainer:
    """Create the hardware-free MMCore test container."""
    from redsun_mimir.device.mmcore import (
        MockMMASIFilterWheel,
        MockMMASIFWController,
        MockMMSerialDevice,
        MockMMSpectraShutteredDevice,
    )
    from redsun_mimir.presenter.filterwheel import FilterWheelPresenter
    from redsun_mimir.presenter.light import LightPresenter
    from redsun_mimir.view.filterwheel import FilterWheelView
    from redsun_mimir.view.light import LightView

    logging.getLogger("redsun").setLevel(logging.DEBUG)

    class MMCoreMockApp(QtAppContainer, config=_CONFIG):
        serial = declare_device(MockMMSerialDevice, from_config="serial")
        serial25 = declare_device(MockMMSerialDevice, from_config="serial25")
        spectra = declare_device(MockMMSpectraShutteredDevice, from_config="spectra")
        fw_controller = declare_device(
            MockMMASIFWController, from_config="fw_controller"
        )
        filterwheel = declare_device(MockMMASIFilterWheel, from_config="filterwheel")

        light_ctrl = declare_presenter(LightPresenter, from_config="light_ctrl")
        fw_ctrl = declare_presenter(FilterWheelPresenter, from_config="fw_ctrl")

        light_widget = declare_view(LightView, from_config="light_widget")
        fw_widget = declare_view(FilterWheelView, from_config="fw_widget")

    return MMCoreMockApp()


def run_mmcore_mock_container() -> None:
    """Run hardware-free MMCore serial, shutter, and filter-wheel controls."""
    create_mmcore_mock_container().run()
