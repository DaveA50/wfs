"""
Wrapper for interfacing with the Thorlabs Wavefront Sensor (WFS)
"""
from __future__ import print_function
import os
import subprocess
import sys

from wfs import WFS

__version__ = '0.1.0'
PY2 = sys.version_info[0] == 2

if 'pyside' in sys.argv[1]:
    from PySide import QtCore, QtGui
    Signal = QtCore.Signal
    Slot = QtCore.Slot
    subprocess.call("pyside-uic.exe gui/design.ui -o gui/design.py")  # Compile .py from .ui
    import gui
    design_ui, design_base = gui.design.Ui_main_window, QtGui.QMainWindow
    debug_ui, debug_base = gui.debug.Ui_Form, QtGui.QMainWindow
else:
    from PyQt4 import QtCore, QtGui, uic
    Signal = QtCore.pyqtSignal
    Slot = QtCore.pyqtSlot
    subprocess.call("pyuic4.bat gui/design.ui -o gui/design.py")  # Compile .py from .ui
    subprocess.call("pyuic4.bat gui/debug.ui -o gui/debug.py")  # Compile .py from .ui
    abs_path = os.path.dirname(os.path.abspath(__file__))
    gui_path = os.path.join(abs_path, 'gui')
    design_path = os.path.join(gui_path, 'design.ui')
    design_ui, design_base = uic.loadUiType(design_path)
    debug_path = os.path.join(gui_path, 'debug.ui')
    debug_ui, debug_base = uic.loadUiType(debug_path)


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
        if self.debug_window is None:
            self.debug_window = WFSDebugApp(wfs=self.wfs)
        self.debug_window.show()

    @Slot()
    def on_debug_click(self):
        self.wfs._get_instrument_list_len()
        self.wfs._get_instrument_list_info()
        self.wfs._init(resource_name=b'USB::0x1313::0x0000::1', id_query=1, reset_device=1)
        self.wfs._revision_query()
        self.wfs.allow_auto_exposure.value = 1
        # print(self.wfs.WFS_DRIVER_STATUS)
        # for i in range(5):
        #     self.wfs.update()
        # self.wfs._convert_wavefront_waves(wavelength=405)


class WFSDebugApp(debug_base, debug_ui):
    def __init__(self, parent=None, wfs=WFS()):
        super(WFSDebugApp, self).__init__(parent)
        self.setupUi(self)
        self.wfs = wfs

        # self.btn.clicked.connect(self.on_click)
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
        self.btn_calc_spots_centroid_diameter_intensity.clicked.connect(self.on_calc_spots_centroid_diameter_intensity_click)
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

    # @Slot()
    # def on_click(self):
    #     self.wfs.()

    @Slot()
    def on_get_instrument_info_click(self):
        self.wfs._get_instrument_info()

    @Slot()
    def on_configure_cam_click(self):
        self.wfs._configure_cam()

    @Slot()
    def on_set_highspeed_mode_click(self):
        self.wfs._set_highspeed_mode()

    @Slot()
    def on_get_highspeed_windows_click(self):
        self.wfs._get_highspeed_windows()

    @Slot()
    def on_check_highspeed_centroids_click(self):
        self.wfs._check_highspeed_centroids()

    @Slot()
    def on_get_exposure_time_range_click(self):
        self.wfs._get_exposure_time_range()

    @Slot()
    def on_set_exposure_time_click(self):
        self.wfs._set_exposure_time()

    @Slot()
    def on_get_exposure_time_click(self):
        self.wfs._get_exposure_time()

    @Slot()
    def on_get_master_gain_range_click(self):
        self.wfs._get_master_gain_range()

    @Slot()
    def on_set_master_gain_click(self):
        self.wfs._set_master_gain()

    @Slot()
    def on_get_master_gain_click(self):
        self.wfs._get_master_gain()

    @Slot()
    def on_set_black_level_offset_click(self):
        self.wfs._set_black_level_offset()

    @Slot()
    def on_get_black_level_offset_click(self):
        self.wfs._get_black_level_offset()

    @Slot()
    def on_set_trigger_mode_click(self):
        self.wfs._set_trigger_mode()

    @Slot()
    def on_get_trigger_mode_click(self):
        self.wfs._get_trigger_mode()

    @Slot()
    def on_get_trigger_delay_range_click(self):
        self.wfs._get_trigger_delay_range()

    @Slot()
    def on_set_trigger_delay_click(self):
        self.wfs._set_trigger_delay()

    @Slot()
    def on_get_mla_count_click(self):
        self.wfs._get_mla_count()

    @Slot()
    def on_get_mla_data_click(self):
        self.wfs._get_mla_data()

    @Slot()
    def on_get_mla_data2_click(self):
        self.wfs._get_mla_data2()

    @Slot()
    def on_select_mla_click(self):
        self.wfs._select_mla()

    @Slot()
    def on_set_aoi_click(self):
        self.wfs._set_aoi()

    @Slot()
    def on_get_aoi_click(self):
        self.wfs._get_aoi()

    @Slot()
    def on_set_pupil_click(self):
        self.wfs._set_pupil()

    @Slot()
    def on_get_pupil_click(self):
        self.wfs._get_pupil()

    @Slot()
    def on_set_reference_plane_click(self):
        self.wfs._set_reference_plane()

    @Slot()
    def on_get_reference_plane_click(self):
        self.wfs._get_reference_plane()

    @Slot()
    def on_take_spotfield_image_click(self):
        self.wfs._take_spotfield_image()

    @Slot()
    def on_take_spotfield_image_auto_exposure_click(self):
        self.wfs._take_spotfield_image_auto_exposure()

    @Slot()
    def on_get_spotfield_image_click(self):
        self.wfs._get_spotfield_image()

    @Slot()
    def on_get_spotfield_image_copy_click(self):
        self.wfs._get_spotfield_image_copy()

    @Slot()
    def on_average_image_click(self):
        self.wfs._average_image()

    @Slot()
    def on_average_image_rolling_click(self):
        self.wfs._average_image_rolling()

    @Slot()
    def on_cut_image_noise_floor_click(self):
        self.wfs._cut_image_noise_floor()

    @Slot()
    def on_calc_image_min_max_click(self):
        self.wfs._calc_image_min_max()

    @Slot()
    def on_calc_mean_rms_noise_click(self):
        self.wfs._calc_mean_rms_noise()

    @Slot()
    def on_get_line_click(self):
        self.wfs._get_line()

    @Slot()
    def on_get_line_view_click(self):
        self.wfs._get_line_view()

    @Slot()
    def on_calc_beam_centroid_diameter_click(self):
        self.wfs._calc_beam_centroid_diameter()

    @Slot()
    def on_calc_spots_centroid_diameter_intensity_click(self):
        self.wfs._calc_spots_centroid_diameter_intensity()

    @Slot()
    def on_get_spot_centroids_click(self):
        self.wfs._get_spot_centroids()

    @Slot()
    def on_get_spot_diameters_click(self):
        self.wfs._get_spot_diameters()

    @Slot()
    def on_get_spot_diameters_statistics_click(self):
        self.wfs._get_spot_diameters_statistics()

    @Slot()
    def on_get_spot_intensities_click(self):
        self.wfs._get_spot_intensities()

    @Slot()
    def on_calc_spot_to_reference_deviations_click(self):
        self.wfs._calc_spot_to_reference_deviations()

    @Slot()
    def on_get_spot_reference_positions_click(self):
        self.wfs._get_spot_reference_positions()

    @Slot()
    def on_get_spot_deviations_click(self):
        self.wfs._get_spot_deviations()

    @Slot()
    def on_zernike_lsf_click(self):
        self.wfs._zernike_lsf()

    @Slot()
    def on_calc_fourier_optometric_click(self):
        self.wfs._calc_fourier_optometric()

    @Slot()
    def on_calc_reconstructed_deviations_click(self):
        self.wfs._calc_reconstructed_deviations()

    @Slot()
    def on_calc_wavefront_click(self):
        self.wfs._calc_wavefront()

    @Slot()
    def on_calc_wavefront_statistics_click(self):
        self.wfs._calc_wavefront_statistics()

    @Slot()
    def on_self_test_click(self):
        self.wfs._self_test()

    @Slot()
    def on_reset_click(self):
        self.wfs._reset()

    @Slot()
    def on_revision_query_click(self):
        self.wfs._revision_query()

    @Slot()
    def on_error_query_click(self):
        self.wfs._error_query()

    @Slot()
    def on_error_message_click(self):
        self.wfs._error_message()

    @Slot()
    def on_get_instrument_list_len_click(self):
        self.wfs._get_instrument_list_len()

    @Slot()
    def on_get_instrument_list_info_click(self):
        self.wfs._get_instrument_list_info()

    @Slot()
    def on_get_xy_scale_click(self):
        self.wfs._get_xy_scale()

    @Slot()
    def on_convert_wavefront_waves_click(self):
        self.wfs._convert_wavefront_waves()

    @Slot()
    def on_flip_2d_array_click(self):
        self.wfs._flip_2d_array()

    @Slot()
    def on_set_spots_to_user_reference_click(self):
        self.wfs._set_spots_to_user_reference()

    @Slot()
    def on_set_calc_spots_to_user_reference_click(self):
        self.wfs._set_calc_spots_to_user_reference()

    @Slot()
    def on_create_default_user_reference_click(self):
        self.wfs._create_default_user_reference()

    @Slot()
    def on_save_user_reference_file_click(self):
        self.wfs._save_user_reference_file()

    @Slot()
    def on_load_user_reference_file_click(self):
        self.wfs._load_user_reference_file()

    @Slot()
    def on_do_spherical_reference_click(self):
        self.wfs._do_spherical_reference()

    @Slot()
    def on_init_click(self):
        self.wfs._init()

    @Slot()
    def on_get_status_click(self):
        self.wfs._get_status()

    @Slot()
    def on_close_click(self):
        self.wfs._close()


def main(wfs):
    app = QtGui.QApplication(sys.argv)
    form = WFSApp(wfs=wfs)
    form.show()
    app.exec_()

if __name__ == '__main__':
    wfs = WFS()
    main(wfs)
