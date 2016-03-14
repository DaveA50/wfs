# -*- coding: utf-8 -*-

"""
Wrapper for interfacing with the Thorlabs Wavefront Sensor (WFS)
"""

from __future__ import print_function
from __future__ import absolute_import
import os
import subprocess
import sys

from wfs import WFS

__version__ = '0.2.0'
PY2 = sys.version_info[0] == 2

abs_path = os.path.dirname(os.path.abspath(__file__))
gui_path = os.path.join(abs_path, 'gui')
design_path = os.path.join(gui_path, 'design.ui')
debug_path = os.path.join(gui_path, 'debug.ui')
if 'pyside' in sys.argv[1]:
    from PySide import QtCore, QtGui
    import pysideuic as uic
    Signal = QtCore.Signal
    Slot = QtCore.Slot
    try:
        subprocess.call("pyside-uic.exe gui/design.ui -o gui/design.py")  # Compile .py from .ui
    except (WindowsError, FileNotFoundError):
        pass
    # uic.compileUi()
    with open(os.path.join(gui_path, 'design.py'), 'w') as outfile:
        uic.compileUi(design_path, outfile, from_imports=True)
    with open(os.path.join(gui_path, 'debug.py'), 'w') as outfile:
        uic.compileUi(debug_path, outfile, from_imports=True)
    import gui
    design_ui, design_base = gui.design.Ui_main_window, QtGui.QMainWindow
    debug_ui, debug_base = gui.debug.Ui_Form, QtGui.QMainWindow
else:
    from PyQt4 import QtCore, QtGui, uic
    Signal = QtCore.pyqtSignal
    Slot = QtCore.pyqtSlot
    try:
        subprocess.call("pyuic4.bat gui/design.ui -o gui/design.py")  # Compile .py from .ui
        subprocess.call("pyuic4.bat gui/debug.ui -o gui/debug.py")  # Compile .py from .ui
    except (WindowsError, FileNotFoundError):
        pass
    design_ui, design_base = uic.loadUiType(design_path)
    debug_ui, debug_base = uic.loadUiType(debug_path)


class WFSThread(QtCore.QThread):
    def __init__(self, parent=None, wfs=WFS()):
        super(WFSThread, self).__init__(parent)
        self.wfs = wfs
        self.roc_ready = Signal(str)

    def __del__(self):
        self.wait()

    def update(self):  # A slot takes no params
        self.wfs.update()
        roc = str(self.wfs.roc_mm.value)
        self.roc_ready.emit(roc)
        self.terminate()


class WFSApp(design_base, design_ui):
    def __init__(self, parent=None, wfs=WFS()):
        super(WFSApp, self).__init__(parent)
        self.setupUi(self)
        self.wfs = wfs

        self.debug_window = None

        self.action_quit.triggered.connect(self.on_quit_trigger)
        self.action_connect.triggered.connect(self.on_connect_click)
        self.action_disconnect.triggered.connect(self.on_disconnect_click)
        self.btn_settings.clicked.connect(lambda: self.on_settings_click('Settings'))
        self.action_settings.triggered.connect(lambda: self.on_settings_click('Settings'))
        self.btn_debug.clicked.connect(self.on_debug_click)
        self.btn_test.clicked.connect(self.on_test_click)

        self.worker = WFSThread()
        # self.worker.roc_ready.connect(self.on_test_click)
        # self.worker.finished.connect(self.on_test_click)
        self.worker.start()

    @Slot()
    def on_quit_trigger(self):
        self.close()

    @Slot()
    def on_connect_click(self):
        self.wfs.connect()
        self.action_disconnect.setEnabled(True)
        self.action_connect.setEnabled(False)

    @Slot()
    def on_disconnect_click(self):
        if self.wfs._close() == 0:
            self.action_connect.setEnabled(True)
            self.action_disconnect.setEnabled(False)

    @Slot(str)
    def on_settings_click(self, arg1):
        print(arg1)

    @Slot()
    def on_test_click(self):
        for i in range(3):
            self.wfs.update()
            roc = str(self.wfs.roc_mm.value)
            self.text_browser.append(roc)

    @Slot()
    def on_debug_click(self):
        if self.debug_window is None:
            self.debug_window = WFSDebugApp(wfs=self.wfs)
        self.debug_window.show()


class WFSDebugApp(debug_base, debug_ui):
    def __init__(self, parent=None, wfs=WFS()):
        super(WFSDebugApp, self).__init__(parent)
        self.setupUi(self)
        self.wfs = wfs

        self.btn_get_instrument_info.clicked.connect(self.on_get_instrument_info_click)
        self.btn_configure_cam.clicked.connect(self.on_configure_cam_click)
        self.btn_set_highspeed_mode.clicked.connect(self.on_set_highspeed_mode_click)
        self.btn_get_highspeed_windows.clicked.connect(self.on_get_highspeed_windows_click)
        self.btn_check_highspeed_centroids.clicked.connect(self.on_check_highspeed_centroids_click)
        self.btn_get_exposure_time_range.clicked.connect(self.on_get_exposure_time_range_click)
        self.btn_set_exposure_time.clicked.connect(self.on_set_exposure_time_click)
        self.btn_get_exposure_time.clicked.connect(self.on_get_exposure_time_click)
        self.btn_get_master_gain_range.clicked.connect(self.on_get_master_gain_range_click)
        self.btn_set_master_gain.clicked.connect(self.on_set_master_gain_click)
        self.btn_get_master_gain.clicked.connect(self.on_get_master_gain_click)
        self.btn_set_black_level_offset.clicked.connect(self.on_set_black_level_offset_click)
        self.btn_get_black_level_offset.clicked.connect(self.on_get_black_level_offset_click)
        self.btn_set_trigger_mode.clicked.connect(self.on_set_trigger_mode_click)
        self.btn_get_trigger_mode.clicked.connect(self.on_get_trigger_mode_click)
        self.btn_get_trigger_delay_range.clicked.connect(self.on_get_trigger_delay_range_click)
        self.btn_set_trigger_delay.clicked.connect(self.on_set_trigger_delay_click)
        self.btn_get_mla_count.clicked.connect(self.on_get_mla_count_click)
        self.btn_get_mla_data.clicked.connect(self.on_get_mla_data_click)
        self.btn_get_mla_data2.clicked.connect(self.on_get_mla_data2_click)
        self.btn_select_mla.clicked.connect(self.on_select_mla_click)
        self.btn_set_aoi.clicked.connect(self.on_set_aoi_click)
        self.btn_get_aoi.clicked.connect(self.on_get_aoi_click)
        self.btn_set_pupil.clicked.connect(self.on_set_pupil_click)
        self.btn_get_pupil.clicked.connect(self.on_get_pupil_click)
        self.btn_set_reference_plane.clicked.connect(self.on_set_reference_plane_click)
        self.btn_get_reference_plane.clicked.connect(self.on_get_reference_plane_click)
        self.btn_take_spotfield_image.clicked.connect(self.on_take_spotfield_image_click)
        self.btn_take_spotfield_image_auto_exposure.clicked.connect(self.on_take_spotfield_image_auto_exposure_click)
        self.btn_get_spotfield_image.clicked.connect(self.on_get_spotfield_image_click)
        self.btn_get_spotfield_image_copy.clicked.connect(self.on_get_spotfield_image_copy_click)
        self.btn_average_image.clicked.connect(self.on_average_image_click)
        self.btn_average_image_rolling.clicked.connect(self.on_average_image_rolling_click)
        self.btn_cut_image_noise_floor.clicked.connect(self.on_cut_image_noise_floor_click)
        self.btn_calc_image_min_max.clicked.connect(self.on_calc_image_min_max_click)
        self.btn_calc_mean_rms_noise.clicked.connect(self.on_calc_mean_rms_noise_click)
        self.btn_get_line.clicked.connect(self.on_get_line_click)
        self.btn_get_line_view.clicked.connect(self.on_get_line_view_click)
        self.btn_calc_beam_centroid_diameter.clicked.connect(self.on_calc_beam_centroid_diameter_click)
        self.btn_calc_spots_centroid_diameter_intensity.clicked.connect(
            self.on_calc_spots_centroid_diameter_intensity_click)
        self.btn_get_spot_centroids.clicked.connect(self.on_get_spot_centroids_click)
        self.btn_get_spot_diameters.clicked.connect(self.on_get_spot_diameters_click)
        self.btn_get_spot_diameters_statistics.clicked.connect(self.on_get_spot_diameters_statistics_click)
        self.btn_get_spot_intensities.clicked.connect(self.on_get_spot_intensities_click)
        self.btn_calc_spot_to_reference_deviations.clicked.connect(self.on_calc_spot_to_reference_deviations_click)
        self.btn_get_spot_reference_positions.clicked.connect(self.on_get_spot_reference_positions_click)
        self.btn_get_spot_deviations.clicked.connect(self.on_get_spot_deviations_click)
        self.btn_zernike_lsf.clicked.connect(self.on_zernike_lsf_click)
        self.btn_calc_fourier_optometric.clicked.connect(self.on_calc_fourier_optometric_click)
        self.btn_calc_reconstructed_deviations.clicked.connect(self.on_calc_reconstructed_deviations_click)
        self.btn_calc_wavefront.clicked.connect(self.on_calc_wavefront_click)
        self.btn_calc_wavefront_statistics.clicked.connect(self.on_calc_wavefront_statistics_click)
        self.btn_self_test.clicked.connect(self.on_self_test_click)
        self.btn_reset.clicked.connect(self.on_reset_click)
        self.btn_revision_query.clicked.connect(self.on_revision_query_click)
        self.btn_error_query.clicked.connect(self.on_error_query_click)
        self.btn_error_message.clicked.connect(self.on_error_message_click)
        self.btn_get_instrument_list_len.clicked.connect(self.on_get_instrument_list_len_click)
        self.btn_get_instrument_list_info.clicked.connect(self.on_get_instrument_list_info_click)
        self.btn_get_xy_scale.clicked.connect(self.on_get_xy_scale_click)
        self.btn_convert_wavefront_waves.clicked.connect(self.on_convert_wavefront_waves_click)
        self.btn_flip_2d_array.clicked.connect(self.on_flip_2d_array_click)
        self.btn_set_spots_to_user_reference.clicked.connect(self.on_set_spots_to_user_reference_click)
        self.btn_set_calc_spots_to_user_reference.clicked.connect(self.on_set_calc_spots_to_user_reference_click)
        self.btn_create_default_user_reference.clicked.connect(self.on_create_default_user_reference_click)
        self.btn_save_user_reference_file.clicked.connect(self.on_save_user_reference_file_click)
        self.btn_load_user_reference_file.clicked.connect(self.on_load_user_reference_file_click)
        self.btn_do_spherical_reference.clicked.connect(self.on_do_spherical_reference_click)
        self.btn_init.clicked.connect(self.on_init_click)
        self.btn_get_status.clicked.connect(self.on_get_status_click)
        self.btn_close.clicked.connect(self.on_close_click)

    @Slot()
    def on_get_instrument_info_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_instrument_info(instrument_handle=arg5)

    @Slot()
    def on_configure_cam_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg2 = str(self.line_arg2.text())
        if arg2 == '':
            arg2 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._configure_cam(cam_resolution_index=arg1,
                                pixel_format=arg2,
                                instrument_handle=arg5)

    @Slot()
    def on_set_highspeed_mode_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg2 = str(self.line_arg2.text())
        if arg2 == '':
            arg2 = None
        arg3 = str(self.line_arg3.text())
        if arg3 == '':
            arg3 = None
        arg4 = str(self.line_arg4.text())
        if arg4 == '':
            arg4 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._set_highspeed_mode(highspeed_mode=arg1,
                                     adapt_centroids=arg2,
                                     subtract_offset=arg3,
                                     allow_auto_exposure=arg4,
                                     instrument_handle=arg5)

    @Slot()
    def on_get_highspeed_windows_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_highspeed_windows(instrument_handle=arg5)

    @Slot()
    def on_check_highspeed_centroids_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._check_highspeed_centroids(instrument_handle=arg5)

    @Slot()
    def on_get_exposure_time_range_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_exposure_time_range(instrument_handle=arg5)

    @Slot()
    def on_set_exposure_time_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._set_exposure_time(exposure_time_set=arg1,
                                    instrument_handle=arg5)

    @Slot()
    def on_get_exposure_time_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_exposure_time(instrument_handle=arg5)

    @Slot()
    def on_get_master_gain_range_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_master_gain_range(instrument_handle=arg5)

    @Slot()
    def on_set_master_gain_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._set_master_gain(master_gain_set=arg1,
                                  instrument_handle=arg5)

    @Slot()
    def on_get_master_gain_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_master_gain(instrument_handle=arg5)

    @Slot()
    def on_set_black_level_offset_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._set_black_level_offset(black_level_offset_set=arg1,
                                         instrument_handle=arg5)

    @Slot()
    def on_get_black_level_offset_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_black_level_offset(instrument_handle=arg5)

    @Slot()
    def on_set_trigger_mode_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._set_trigger_mode(trigger_mode=arg1,
                                   instrument_handle=arg5)

    @Slot()
    def on_get_trigger_mode_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_trigger_mode(instrument_handle=arg5)

    @Slot()
    def on_set_trigger_delay_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._set_trigger_delay(trigger_delay_set=arg1,
                                    instrument_handle=arg5)

    @Slot()
    def on_get_trigger_delay_range_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_trigger_delay_range(instrument_handle=arg5)

    @Slot()
    def on_get_mla_count_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_mla_count(instrument_handle=arg5)

    @Slot()
    def on_get_mla_data_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_mla_data(mla_index=arg1,
                               instrument_handle=arg5)

    @Slot()
    def on_get_mla_data2_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_mla_data2(mla_index=arg1,
                                instrument_handle=arg5)

    @Slot()
    def on_select_mla_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._select_mla(mla_index=arg1,
                             instrument_handle=arg5)

    @Slot()
    def on_set_aoi_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg2 = str(self.line_arg2.text())
        if arg2 == '':
            arg2 = None
        arg3 = str(self.line_arg3.text())
        if arg3 == '':
            arg3 = None
        arg4 = str(self.line_arg4.text())
        if arg4 == '':
            arg4 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._set_aoi(aoi_center_x_mm=arg1,
                          aoi_center_y_mm=arg2,
                          aoi_size_x_mm=arg3,
                          aoi_size_y_mm=arg4,
                          instrument_handle=arg5)

    @Slot()
    def on_get_aoi_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_aoi(instrument_handle=arg5)

    @Slot()
    def on_set_pupil_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg2 = str(self.line_arg2.text())
        if arg2 == '':
            arg2 = None
        arg3 = str(self.line_arg3.text())
        if arg3 == '':
            arg3 = None
        arg4 = str(self.line_arg4.text())
        if arg4 == '':
            arg4 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._set_pupil(pupil_center_x_mm=arg1,
                            pupil_center_y_mm=arg2,
                            pupil_diameter_x_mm=arg3,
                            pupil_diameter_y_mm=arg4,
                            instrument_handle=arg5)

    @Slot()
    def on_get_pupil_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_pupil(instrument_handle=arg5)

    @Slot()
    def on_set_reference_plane_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._set_reference_plane(reference_index=arg1,
                                      instrument_handle=arg5)

    @Slot()
    def on_get_reference_plane_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_reference_plane(instrument_handle=arg5)

    @Slot()
    def on_take_spotfield_image_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._take_spotfield_image(instrument_handle=arg5)

    @Slot()
    def on_take_spotfield_image_auto_exposure_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._take_spotfield_image_auto_exposure(instrument_handle=arg5)

    @Slot()
    def on_get_spotfield_image_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_spotfield_image(instrument_handle=arg5)

    @Slot()
    def on_get_spotfield_image_copy_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_spotfield_image_copy(instrument_handle=arg5)

    @Slot()
    def on_average_image_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._average_image(average_count=arg1,
                                instrument_handle=arg5)

    @Slot()
    def on_average_image_rolling_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg2 = str(self.line_arg2.text())
        if arg2 == '':
            arg2 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._average_image_rolling(average_count=arg1,
                                        rolling_reset=arg2,
                                        instrument_handle=arg5)

    @Slot()
    def on_cut_image_noise_floor_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._cut_image_noise_floor(intensity_limit=arg1,
                                        instrument_handle=arg5)

    @Slot()
    def on_calc_image_min_max_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._calc_image_min_max(instrument_handle=arg5)

    @Slot()
    def on_calc_mean_rms_noise_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._calc_mean_rms_noise(instrument_handle=arg5)

    @Slot()
    def on_get_line_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_line(line=arg1,
                           instrument_handle=arg5)

    @Slot()
    def on_get_line_view_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_line_view(instrument_handle=arg5)

    @Slot()
    def on_calc_beam_centroid_diameter_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._calc_beam_centroid_diameter(instrument_handle=arg5)

    @Slot()
    def on_calc_spots_centroid_diameter_intensity_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg2 = str(self.line_arg2.text())
        if arg2 == '':
            arg2 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._calc_spots_centroid_diameter_intensity(dynamic_noise_cut=arg1,
                                                         calculate_diameters=arg2,
                                                         instrument_handle=arg5)

    @Slot()
    def on_get_spot_centroids_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_spot_centroids(instrument_handle=arg5)

    @Slot()
    def on_get_spot_diameters_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_spot_diameters(instrument_handle=arg5)

    @Slot()
    def on_get_spot_diameters_statistics_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_spot_diameters_statistics(instrument_handle=arg5)

    @Slot()
    def on_get_spot_intensities_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_spot_intensities(instrument_handle=arg5)

    @Slot()
    def on_calc_spot_to_reference_deviations_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._calc_spot_to_reference_deviations(cancel_wavefront_tilt=arg1,
                                                    instrument_handle=arg5)

    @Slot()
    def on_get_spot_reference_positions_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_spot_reference_positions(instrument_handle=arg5)

    @Slot()
    def on_get_spot_deviations_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_spot_deviations(instrument_handle=arg5)

    @Slot()
    def on_zernike_lsf_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._zernike_lsf(instrument_handle=arg5)

    @Slot()
    def on_calc_fourier_optometric_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg2 = str(self.line_arg2.text())
        if arg2 == '':
            arg2 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._calc_fourier_optometric(zernike_orders=arg1,
                                          fourier_orders=arg2,
                                          instrument_handle=arg5)

    @Slot()
    def on_calc_reconstructed_deviations_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg2 = str(self.line_arg2.text())
        if arg2 == '':
            arg2 = None
        else:
            # print('Array input not implemented')
            arg2 = None
        arg3 = str(self.line_arg3.text())
        if arg3 == '':
            arg3 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._calc_reconstructed_deviations(zernike_orders=arg1,
                                                array_zernike_reconstructed=arg2,
                                                do_spherical_reference=arg3,
                                                instrument_handle=arg5)

    @Slot()
    def on_calc_wavefront_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg2 = str(self.line_arg2.text())
        if arg2 == '':
            arg2 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._calc_wavefront(wavefront_type=arg1,
                                 limit_to_pupil=arg2,
                                 instrument_handle=arg5)

    @Slot()
    def on_calc_wavefront_statistics_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._calc_wavefront_statistics(instrument_handle=arg5)

    @Slot()
    def on_self_test_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._self_test(instrument_handle=arg5)

    @Slot()
    def on_reset_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._reset(instrument_handle=arg5)

    @Slot()
    def on_revision_query_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._revision_query(instrument_handle=arg5)

    @Slot()
    def on_error_query_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._error_query(instrument_handle=arg5)

    @Slot()
    def on_error_message_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._error_message(error_code=arg1,
                                instrument_handle=arg5)

    @Slot()
    def on_get_instrument_list_len_click(self):
        self.wfs._get_instrument_list_len()

    @Slot()
    def on_get_instrument_list_info_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        self.wfs._get_instrument_list_info(instrument_index=arg1)

    @Slot()
    def on_get_xy_scale_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_xy_scale(instrument_handle=arg5)

    @Slot()
    def on_convert_wavefront_waves_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg2 = str(self.line_arg2.text())
        if arg2 == '':
            arg2 = None
        else:
            # print('Array input not implemented')
            arg2 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._convert_wavefront_waves(wavelength=arg1,
                                          array_wavefront=arg2,
                                          instrument_handle=arg5)

    @Slot()
    def on_flip_2d_array_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        else:
            # print('Array input not implemented')
            arg1 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._flip_2d_array(array_wavefront_yx=arg1,
                                instrument_handle=arg5)

    @Slot()
    def on_set_spots_to_user_reference_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._set_spots_to_user_reference(instrument_handle=arg5)

    @Slot()
    def on_set_calc_spots_to_user_reference_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg2 = str(self.line_arg2.text())
        if arg2 == '':
            arg2 = None
        else:
            # print('Array input not implemented')
            arg2 = None
        arg3 = str(self.line_arg3.text())
        if arg3 == '':
            arg3 = None
        else:
            # print('Array input not implemented')
            arg3 = None
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._set_calc_spots_to_user_reference(spot_ref_type=arg1,
                                                   array_reference_x=arg2,
                                                   array_reference_y=arg3,
                                                   instrument_handle=arg5)

    @Slot()
    def on_create_default_user_reference_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._create_default_user_reference(instrument_handle=arg5)

    @Slot()
    def on_save_user_reference_file_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._save_user_reference_file(instrument_handle=arg5)

    @Slot()
    def on_load_user_reference_file_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._load_user_reference_file(instrument_handle=arg5)

    @Slot()
    def on_do_spherical_reference_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._do_spherical_reference(instrument_handle=arg5)

    @Slot()
    def on_init_click(self):
        arg1 = str(self.line_arg1.text())
        if arg1 == '':
            arg1 = None
        arg2 = str(self.line_arg2.text())
        if arg2 == '':
            arg2 = None
        arg3 = str(self.line_arg3.text())
        if arg3 == '':
            arg3 = None
        self.wfs._init(resource_name=arg1,
                       id_query=arg2,
                       reset_device=arg3)

    @Slot()
    def on_get_status_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._get_status(instrument_handle=arg5)

    @Slot()
    def on_close_click(self):
        arg5 = str(self.line_arg5.text())
        if arg5 == '':
            arg5 = None
        self.wfs._close(instrument_handle=arg5)


def main(wfs):
    app = QtGui.QApplication(sys.argv)
    form = WFSApp(wfs=wfs)
    form.show()
    app.exec_()

if __name__ == '__main__':
    wfs = WFS()
    main(wfs)
