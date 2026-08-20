from __future__ import annotations

import logging
from pathlib import Path

from redsun.containers import declare_device, declare_presenter, declare_view
from redsun.qt import QtAppContainer

_CONFIG = Path(__file__).parent / "arh_full_configuration.yaml"


def run_arh_container() -> None:
    """Run the full ARH microscope with pre-shipped configuration."""
    # devices
    from redsun_mimir.device.mmcore import (
        MMASIFilterWheel,
        MMASIFWController,
        MMASIXYStage,
        MMASIZStage,
        MMHamamatsuCamera,
        MMSerialDevice,
        MMSpectraShutteredDevice,
    )
    from redsun_mimir.presenter.acquisition import AcquisitionPresenter
    from redsun_mimir.presenter.detector import DetectorPresenter
    from redsun_mimir.presenter.filterwheel import FilterWheelPresenter
    from redsun_mimir.presenter.light import LightPresenter
    from redsun_mimir.presenter.median import MedianPresenter
    from redsun_mimir.presenter.motor import MotorPresenter

    # presenters
    from redsun_mimir.presenter.storage import FileStoragePresenter

    # views
    from redsun_mimir.view.acquisition import AcquisitionView
    from redsun_mimir.view.detector import DetectorView
    from redsun_mimir.view.filterwheel import FilterWheelView
    from redsun_mimir.view.image import ImageView
    from redsun_mimir.view.light import LightView
    from redsun_mimir.view.motor import MotorView
    from redsun_mimir.view.storage import FileStorageView

    logging.getLogger("redsun").setLevel(logging.DEBUG)

    class ARHMicroscope(QtAppContainer, config=_CONFIG):
        # devices
        serial = declare_device(MMSerialDevice, from_config="serial")
        serial25 = declare_device(MMSerialDevice, from_config="serial25")
        iscat = declare_device(MMHamamatsuCamera, from_config="camera")
        stage_xy = declare_device(MMASIXYStage, from_config="stage_xy")
        stage_z = declare_device(MMASIZStage, from_config="stage_z")
        spectra = declare_device(MMSpectraShutteredDevice, from_config="spectra")
        fw_controller = declare_device(MMASIFWController, from_config="fw_controller")
        filterwheel = declare_device(MMASIFilterWheel, from_config="filterwheel")

        # presenters
        storage_ctrl = declare_presenter(FileStoragePresenter, from_config="storage_ctrl")
        median_ctrl = declare_presenter(MedianPresenter, from_config="median_ctrl")
        det_ctrl = declare_presenter(DetectorPresenter, from_config="det_ctrl")
        acq_ctrl = declare_presenter(AcquisitionPresenter, from_config="acq_ctrl")
        light_ctrl = declare_presenter(LightPresenter, from_config="light_ctrl")
        motor_ctrl = declare_presenter(MotorPresenter, from_config="motor_ctrl")
        fw_ctrl = declare_presenter(FilterWheelPresenter, from_config="fw_ctrl")

        # views
        acq_widget = declare_view(AcquisitionView, from_config="acq_widget")
        img_widget = declare_view(ImageView, from_config="img_widget")
        det_widget = declare_view(DetectorView, from_config="det_widget")
        light_widget = declare_view(LightView, from_config="light_widget")
        motor_widget = declare_view(MotorView, from_config="motor_widget")
        storage_widget = declare_view(FileStorageView, from_config="storage_widget")
        fw_widget = declare_view(FilterWheelView, from_config="fw_widget")

    ARHMicroscope().run()
