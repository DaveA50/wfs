# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Workspace\Code\wfs\gui\debug.ui'
#
# Created: Mon Mar 14 10:53:41 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1059, 750)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.config_groupbox = QtGui.QGroupBox(Form)
        self.config_groupbox.setObjectName("config_groupbox")
        self.gridLayout_9 = QtGui.QGridLayout(self.config_groupbox)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_8 = QtGui.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.btn_configure_cam = QtGui.QPushButton(self.config_groupbox)
        self.btn_configure_cam.setObjectName("btn_configure_cam")
        self.gridLayout_8.addWidget(self.btn_configure_cam, 0, 1, 1, 1)
        self.btn_set_reference_plane = QtGui.QPushButton(self.config_groupbox)
        self.btn_set_reference_plane.setObjectName("btn_set_reference_plane")
        self.gridLayout_8.addWidget(self.btn_set_reference_plane, 9, 1, 1, 1)
        self.btn_get_master_gain_range = QtGui.QPushButton(self.config_groupbox)
        self.btn_get_master_gain_range.setObjectName("btn_get_master_gain_range")
        self.gridLayout_8.addWidget(self.btn_get_master_gain_range, 2, 2, 1, 1)
        self.btn_get_exposure_time = QtGui.QPushButton(self.config_groupbox)
        self.btn_get_exposure_time.setObjectName("btn_get_exposure_time")
        self.gridLayout_8.addWidget(self.btn_get_exposure_time, 2, 1, 1, 1)
        self.btn_check_highspeed_centroids = QtGui.QPushButton(self.config_groupbox)
        self.btn_check_highspeed_centroids.setEnabled(False)
        self.btn_check_highspeed_centroids.setObjectName("btn_check_highspeed_centroids")
        self.gridLayout_8.addWidget(self.btn_check_highspeed_centroids, 1, 1, 1, 1)
        self.btn_set_aoi = QtGui.QPushButton(self.config_groupbox)
        self.btn_set_aoi.setObjectName("btn_set_aoi")
        self.gridLayout_8.addWidget(self.btn_set_aoi, 8, 0, 1, 1)
        self.btn_get_reference_plane = QtGui.QPushButton(self.config_groupbox)
        self.btn_get_reference_plane.setObjectName("btn_get_reference_plane")
        self.gridLayout_8.addWidget(self.btn_get_reference_plane, 9, 2, 1, 1)
        self.btn_set_trigger_mode = QtGui.QPushButton(self.config_groupbox)
        self.btn_set_trigger_mode.setObjectName("btn_set_trigger_mode")
        self.gridLayout_8.addWidget(self.btn_set_trigger_mode, 4, 1, 1, 1)
        self.btn_get_mla_data = QtGui.QPushButton(self.config_groupbox)
        self.btn_get_mla_data.setObjectName("btn_get_mla_data")
        self.gridLayout_8.addWidget(self.btn_get_mla_data, 7, 0, 1, 1)
        self.btn_get_trigger_mode = QtGui.QPushButton(self.config_groupbox)
        self.btn_get_trigger_mode.setObjectName("btn_get_trigger_mode")
        self.gridLayout_8.addWidget(self.btn_get_trigger_mode, 4, 2, 1, 1)
        self.btn_set_highspeed_mode = QtGui.QPushButton(self.config_groupbox)
        self.btn_set_highspeed_mode.setEnabled(False)
        self.btn_set_highspeed_mode.setObjectName("btn_set_highspeed_mode")
        self.gridLayout_8.addWidget(self.btn_set_highspeed_mode, 0, 2, 1, 1)
        self.btn_get_mla_data2 = QtGui.QPushButton(self.config_groupbox)
        self.btn_get_mla_data2.setObjectName("btn_get_mla_data2")
        self.gridLayout_8.addWidget(self.btn_get_mla_data2, 7, 1, 1, 1)
        self.btn_get_pupil = QtGui.QPushButton(self.config_groupbox)
        self.btn_get_pupil.setObjectName("btn_get_pupil")
        self.gridLayout_8.addWidget(self.btn_get_pupil, 9, 0, 1, 1)
        self.btn_get_exposure_time_range = QtGui.QPushButton(self.config_groupbox)
        self.btn_get_exposure_time_range.setObjectName("btn_get_exposure_time_range")
        self.gridLayout_8.addWidget(self.btn_get_exposure_time_range, 1, 2, 1, 1)
        self.btn_set_pupil = QtGui.QPushButton(self.config_groupbox)
        self.btn_set_pupil.setObjectName("btn_set_pupil")
        self.gridLayout_8.addWidget(self.btn_set_pupil, 8, 2, 1, 1)
        self.btn_select_mla = QtGui.QPushButton(self.config_groupbox)
        self.btn_select_mla.setObjectName("btn_select_mla")
        self.gridLayout_8.addWidget(self.btn_select_mla, 7, 2, 1, 1)
        self.btn_set_exposure_time = QtGui.QPushButton(self.config_groupbox)
        self.btn_set_exposure_time.setObjectName("btn_set_exposure_time")
        self.gridLayout_8.addWidget(self.btn_set_exposure_time, 2, 0, 1, 1)
        self.btn_get_black_level_offset = QtGui.QPushButton(self.config_groupbox)
        self.btn_get_black_level_offset.setObjectName("btn_get_black_level_offset")
        self.gridLayout_8.addWidget(self.btn_get_black_level_offset, 4, 0, 1, 1)
        self.btn_set_black_level_offset = QtGui.QPushButton(self.config_groupbox)
        self.btn_set_black_level_offset.setObjectName("btn_set_black_level_offset")
        self.gridLayout_8.addWidget(self.btn_set_black_level_offset, 3, 2, 1, 1)
        self.btn_get_aoi = QtGui.QPushButton(self.config_groupbox)
        self.btn_get_aoi.setObjectName("btn_get_aoi")
        self.gridLayout_8.addWidget(self.btn_get_aoi, 8, 1, 1, 1)
        self.btn_get_master_gain = QtGui.QPushButton(self.config_groupbox)
        self.btn_get_master_gain.setObjectName("btn_get_master_gain")
        self.gridLayout_8.addWidget(self.btn_get_master_gain, 3, 1, 1, 1)
        self.btn_get_mla_count = QtGui.QPushButton(self.config_groupbox)
        self.btn_get_mla_count.setObjectName("btn_get_mla_count")
        self.gridLayout_8.addWidget(self.btn_get_mla_count, 5, 2, 1, 1)
        self.btn_get_instrument_info = QtGui.QPushButton(self.config_groupbox)
        self.btn_get_instrument_info.setObjectName("btn_get_instrument_info")
        self.gridLayout_8.addWidget(self.btn_get_instrument_info, 0, 0, 1, 1)
        self.btn_get_highspeed_windows = QtGui.QPushButton(self.config_groupbox)
        self.btn_get_highspeed_windows.setEnabled(False)
        self.btn_get_highspeed_windows.setObjectName("btn_get_highspeed_windows")
        self.gridLayout_8.addWidget(self.btn_get_highspeed_windows, 1, 0, 1, 1)
        self.btn_set_master_gain = QtGui.QPushButton(self.config_groupbox)
        self.btn_set_master_gain.setObjectName("btn_set_master_gain")
        self.gridLayout_8.addWidget(self.btn_set_master_gain, 3, 0, 1, 1)
        self.btn_set_trigger_delay = QtGui.QPushButton(self.config_groupbox)
        self.btn_set_trigger_delay.setObjectName("btn_set_trigger_delay")
        self.gridLayout_8.addWidget(self.btn_set_trigger_delay, 5, 0, 1, 1)
        self.btn_get_trigger_delay_range = QtGui.QPushButton(self.config_groupbox)
        self.btn_get_trigger_delay_range.setObjectName("btn_get_trigger_delay_range")
        self.gridLayout_8.addWidget(self.btn_get_trigger_delay_range, 5, 1, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_8, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.config_groupbox, 1, 0, 1, 1)
        self.args_groupbox = QtGui.QGroupBox(Form)
        self.args_groupbox.setObjectName("args_groupbox")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.args_groupbox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_arg1 = QtGui.QLabel(self.args_groupbox)
        self.label_arg1.setObjectName("label_arg1")
        self.verticalLayout.addWidget(self.label_arg1)
        self.line_arg1 = QtGui.QLineEdit(self.args_groupbox)
        self.line_arg1.setObjectName("line_arg1")
        self.verticalLayout.addWidget(self.line_arg1)
        self.label_arg2 = QtGui.QLabel(self.args_groupbox)
        self.label_arg2.setObjectName("label_arg2")
        self.verticalLayout.addWidget(self.label_arg2)
        self.line_arg2 = QtGui.QLineEdit(self.args_groupbox)
        self.line_arg2.setObjectName("line_arg2")
        self.verticalLayout.addWidget(self.line_arg2)
        self.label_arg3 = QtGui.QLabel(self.args_groupbox)
        self.label_arg3.setObjectName("label_arg3")
        self.verticalLayout.addWidget(self.label_arg3)
        self.line_arg3 = QtGui.QLineEdit(self.args_groupbox)
        self.line_arg3.setObjectName("line_arg3")
        self.verticalLayout.addWidget(self.line_arg3)
        self.label_arg4 = QtGui.QLabel(self.args_groupbox)
        self.label_arg4.setObjectName("label_arg4")
        self.verticalLayout.addWidget(self.label_arg4)
        self.line_arg4 = QtGui.QLineEdit(self.args_groupbox)
        self.line_arg4.setObjectName("line_arg4")
        self.verticalLayout.addWidget(self.line_arg4)
        self.label_arg5 = QtGui.QLabel(self.args_groupbox)
        self.label_arg5.setObjectName("label_arg5")
        self.verticalLayout.addWidget(self.label_arg5)
        self.line_arg5 = QtGui.QLineEdit(self.args_groupbox)
        self.line_arg5.setObjectName("line_arg5")
        self.verticalLayout.addWidget(self.line_arg5)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addWidget(self.args_groupbox, 6, 0, 1, 1)
        self.utility_groupbox = QtGui.QGroupBox(Form)
        self.utility_groupbox.setObjectName("utility_groupbox")
        self.gridLayout_11 = QtGui.QGridLayout(self.utility_groupbox)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.btn_convert_wavefront_waves = QtGui.QPushButton(self.utility_groupbox)
        self.btn_convert_wavefront_waves.setObjectName("btn_convert_wavefront_waves")
        self.gridLayout_6.addWidget(self.btn_convert_wavefront_waves, 4, 0, 1, 1)
        self.btn_get_xy_scale = QtGui.QPushButton(self.utility_groupbox)
        self.btn_get_xy_scale.setObjectName("btn_get_xy_scale")
        self.gridLayout_6.addWidget(self.btn_get_xy_scale, 3, 1, 1, 1)
        self.btn_error_message = QtGui.QPushButton(self.utility_groupbox)
        self.btn_error_message.setObjectName("btn_error_message")
        self.gridLayout_6.addWidget(self.btn_error_message, 2, 0, 1, 1)
        self.btn_revision_query = QtGui.QPushButton(self.utility_groupbox)
        self.btn_revision_query.setObjectName("btn_revision_query")
        self.gridLayout_6.addWidget(self.btn_revision_query, 1, 0, 1, 1)
        self.btn_reset = QtGui.QPushButton(self.utility_groupbox)
        self.btn_reset.setEnabled(False)
        self.btn_reset.setObjectName("btn_reset")
        self.gridLayout_6.addWidget(self.btn_reset, 0, 1, 1, 1)
        self.btn_self_test = QtGui.QPushButton(self.utility_groupbox)
        self.btn_self_test.setEnabled(False)
        self.btn_self_test.setObjectName("btn_self_test")
        self.gridLayout_6.addWidget(self.btn_self_test, 0, 0, 1, 1)
        self.btn_error_query = QtGui.QPushButton(self.utility_groupbox)
        self.btn_error_query.setEnabled(False)
        self.btn_error_query.setObjectName("btn_error_query")
        self.gridLayout_6.addWidget(self.btn_error_query, 1, 1, 1, 1)
        self.btn_get_instrument_list_info = QtGui.QPushButton(self.utility_groupbox)
        self.btn_get_instrument_list_info.setObjectName("btn_get_instrument_list_info")
        self.gridLayout_6.addWidget(self.btn_get_instrument_list_info, 3, 0, 1, 1)
        self.btn_get_instrument_list_len = QtGui.QPushButton(self.utility_groupbox)
        self.btn_get_instrument_list_len.setObjectName("btn_get_instrument_list_len")
        self.gridLayout_6.addWidget(self.btn_get_instrument_list_len, 2, 1, 1, 1)
        self.btn_flip_2d_array = QtGui.QPushButton(self.utility_groupbox)
        self.btn_flip_2d_array.setObjectName("btn_flip_2d_array")
        self.gridLayout_6.addWidget(self.btn_flip_2d_array, 4, 1, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_6, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.utility_groupbox, 2, 0, 1, 1)
        self.data_groupbox = QtGui.QGroupBox(Form)
        self.data_groupbox.setObjectName("data_groupbox")
        self.gridLayout_10 = QtGui.QGridLayout(self.data_groupbox)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.gridLayout_7 = QtGui.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.btn_average_image = QtGui.QPushButton(self.data_groupbox)
        self.btn_average_image.setObjectName("btn_average_image")
        self.gridLayout_7.addWidget(self.btn_average_image, 1, 1, 1, 1)
        self.btn_take_spotfield_image = QtGui.QPushButton(self.data_groupbox)
        self.btn_take_spotfield_image.setObjectName("btn_take_spotfield_image")
        self.gridLayout_7.addWidget(self.btn_take_spotfield_image, 0, 0, 1, 1)
        self.btn_average_image_rolling = QtGui.QPushButton(self.data_groupbox)
        self.btn_average_image_rolling.setObjectName("btn_average_image_rolling")
        self.gridLayout_7.addWidget(self.btn_average_image_rolling, 1, 2, 1, 1)
        self.btn_calc_mean_rms_noise = QtGui.QPushButton(self.data_groupbox)
        self.btn_calc_mean_rms_noise.setObjectName("btn_calc_mean_rms_noise")
        self.gridLayout_7.addWidget(self.btn_calc_mean_rms_noise, 2, 2, 1, 1)
        self.btn_zernike_lsf = QtGui.QPushButton(self.data_groupbox)
        self.btn_zernike_lsf.setObjectName("btn_zernike_lsf")
        self.gridLayout_7.addWidget(self.btn_zernike_lsf, 6, 2, 1, 1)
        self.btn_get_spotfield_image_copy = QtGui.QPushButton(self.data_groupbox)
        self.btn_get_spotfield_image_copy.setObjectName("btn_get_spotfield_image_copy")
        self.gridLayout_7.addWidget(self.btn_get_spotfield_image_copy, 1, 0, 1, 1)
        self.btn_cut_image_noise_floor = QtGui.QPushButton(self.data_groupbox)
        self.btn_cut_image_noise_floor.setObjectName("btn_cut_image_noise_floor")
        self.gridLayout_7.addWidget(self.btn_cut_image_noise_floor, 2, 0, 1, 1)
        self.btn_get_line = QtGui.QPushButton(self.data_groupbox)
        self.btn_get_line.setObjectName("btn_get_line")
        self.gridLayout_7.addWidget(self.btn_get_line, 3, 0, 1, 1)
        self.btn_get_spotfield_image = QtGui.QPushButton(self.data_groupbox)
        self.btn_get_spotfield_image.setObjectName("btn_get_spotfield_image")
        self.gridLayout_7.addWidget(self.btn_get_spotfield_image, 0, 2, 1, 1)
        self.btn_calc_spots_centroid_diameter_intensity = QtGui.QPushButton(self.data_groupbox)
        self.btn_calc_spots_centroid_diameter_intensity.setObjectName("btn_calc_spots_centroid_diameter_intensity")
        self.gridLayout_7.addWidget(self.btn_calc_spots_centroid_diameter_intensity, 4, 0, 1, 1)
        self.btn_get_spot_diameters_statistics = QtGui.QPushButton(self.data_groupbox)
        self.btn_get_spot_diameters_statistics.setObjectName("btn_get_spot_diameters_statistics")
        self.gridLayout_7.addWidget(self.btn_get_spot_diameters_statistics, 5, 0, 1, 1)
        self.btn_get_spot_diameters = QtGui.QPushButton(self.data_groupbox)
        self.btn_get_spot_diameters.setObjectName("btn_get_spot_diameters")
        self.gridLayout_7.addWidget(self.btn_get_spot_diameters, 4, 2, 1, 1)
        self.btn_calc_spot_to_reference_deviations = QtGui.QPushButton(self.data_groupbox)
        self.btn_calc_spot_to_reference_deviations.setObjectName("btn_calc_spot_to_reference_deviations")
        self.gridLayout_7.addWidget(self.btn_calc_spot_to_reference_deviations, 5, 2, 1, 1)
        self.btn_get_spot_intensities = QtGui.QPushButton(self.data_groupbox)
        self.btn_get_spot_intensities.setObjectName("btn_get_spot_intensities")
        self.gridLayout_7.addWidget(self.btn_get_spot_intensities, 5, 1, 1, 1)
        self.btn_get_spot_centroids = QtGui.QPushButton(self.data_groupbox)
        self.btn_get_spot_centroids.setObjectName("btn_get_spot_centroids")
        self.gridLayout_7.addWidget(self.btn_get_spot_centroids, 4, 1, 1, 1)
        self.btn_take_spotfield_image_auto_exposure = QtGui.QPushButton(self.data_groupbox)
        self.btn_take_spotfield_image_auto_exposure.setObjectName("btn_take_spotfield_image_auto_exposure")
        self.gridLayout_7.addWidget(self.btn_take_spotfield_image_auto_exposure, 0, 1, 1, 1)
        self.btn_calc_beam_centroid_diameter = QtGui.QPushButton(self.data_groupbox)
        self.btn_calc_beam_centroid_diameter.setObjectName("btn_calc_beam_centroid_diameter")
        self.gridLayout_7.addWidget(self.btn_calc_beam_centroid_diameter, 3, 2, 1, 1)
        self.btn_get_line_view = QtGui.QPushButton(self.data_groupbox)
        self.btn_get_line_view.setObjectName("btn_get_line_view")
        self.gridLayout_7.addWidget(self.btn_get_line_view, 3, 1, 1, 1)
        self.btn_get_spot_reference_positions = QtGui.QPushButton(self.data_groupbox)
        self.btn_get_spot_reference_positions.setObjectName("btn_get_spot_reference_positions")
        self.gridLayout_7.addWidget(self.btn_get_spot_reference_positions, 6, 0, 1, 1)
        self.btn_calc_fourier_optometric = QtGui.QPushButton(self.data_groupbox)
        self.btn_calc_fourier_optometric.setObjectName("btn_calc_fourier_optometric")
        self.gridLayout_7.addWidget(self.btn_calc_fourier_optometric, 7, 0, 1, 1)
        self.btn_calc_wavefront = QtGui.QPushButton(self.data_groupbox)
        self.btn_calc_wavefront.setObjectName("btn_calc_wavefront")
        self.gridLayout_7.addWidget(self.btn_calc_wavefront, 7, 2, 1, 1)
        self.btn_calc_reconstructed_deviations = QtGui.QPushButton(self.data_groupbox)
        self.btn_calc_reconstructed_deviations.setObjectName("btn_calc_reconstructed_deviations")
        self.gridLayout_7.addWidget(self.btn_calc_reconstructed_deviations, 7, 1, 1, 1)
        self.btn_get_spot_deviations = QtGui.QPushButton(self.data_groupbox)
        self.btn_get_spot_deviations.setObjectName("btn_get_spot_deviations")
        self.gridLayout_7.addWidget(self.btn_get_spot_deviations, 6, 1, 1, 1)
        self.btn_calc_image_min_max = QtGui.QPushButton(self.data_groupbox)
        self.btn_calc_image_min_max.setObjectName("btn_calc_image_min_max")
        self.gridLayout_7.addWidget(self.btn_calc_image_min_max, 2, 1, 1, 1)
        self.btn_calc_wavefront_statistics = QtGui.QPushButton(self.data_groupbox)
        self.btn_calc_wavefront_statistics.setObjectName("btn_calc_wavefront_statistics")
        self.gridLayout_7.addWidget(self.btn_calc_wavefront_statistics, 8, 0, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_7, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.data_groupbox, 1, 1, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.calibration_groupbox = QtGui.QGroupBox(Form)
        self.calibration_groupbox.setObjectName("calibration_groupbox")
        self.gridLayout_3 = QtGui.QGridLayout(self.calibration_groupbox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.btn_set_spots_to_user_reference = QtGui.QPushButton(self.calibration_groupbox)
        self.btn_set_spots_to_user_reference.setObjectName("btn_set_spots_to_user_reference")
        self.gridLayout.addWidget(self.btn_set_spots_to_user_reference, 0, 0, 1, 1)
        self.btn_do_spherical_reference = QtGui.QPushButton(self.calibration_groupbox)
        self.btn_do_spherical_reference.setObjectName("btn_do_spherical_reference")
        self.gridLayout.addWidget(self.btn_do_spherical_reference, 1, 2, 1, 1)
        self.btn_save_user_reference_file = QtGui.QPushButton(self.calibration_groupbox)
        self.btn_save_user_reference_file.setObjectName("btn_save_user_reference_file")
        self.gridLayout.addWidget(self.btn_save_user_reference_file, 1, 0, 1, 1)
        self.btn_create_default_user_reference = QtGui.QPushButton(self.calibration_groupbox)
        self.btn_create_default_user_reference.setObjectName("btn_create_default_user_reference")
        self.gridLayout.addWidget(self.btn_create_default_user_reference, 0, 2, 1, 1)
        self.btn_load_user_reference_file = QtGui.QPushButton(self.calibration_groupbox)
        self.btn_load_user_reference_file.setObjectName("btn_load_user_reference_file")
        self.gridLayout.addWidget(self.btn_load_user_reference_file, 1, 1, 1, 1)
        self.btn_set_calc_spots_to_user_reference = QtGui.QPushButton(self.calibration_groupbox)
        self.btn_set_calc_spots_to_user_reference.setObjectName("btn_set_calc_spots_to_user_reference")
        self.gridLayout.addWidget(self.btn_set_calc_spots_to_user_reference, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.calibration_groupbox)
        self.action_groupbox = QtGui.QGroupBox(Form)
        self.action_groupbox.setObjectName("action_groupbox")
        self.gridLayout_5 = QtGui.QGridLayout(self.action_groupbox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.btn_init = QtGui.QPushButton(self.action_groupbox)
        self.btn_init.setObjectName("btn_init")
        self.gridLayout_4.addWidget(self.btn_init, 0, 0, 1, 1)
        self.btn_close = QtGui.QPushButton(self.action_groupbox)
        self.btn_close.setObjectName("btn_close")
        self.gridLayout_4.addWidget(self.btn_close, 0, 2, 1, 1)
        self.btn_get_status = QtGui.QPushButton(self.action_groupbox)
        self.btn_get_status.setObjectName("btn_get_status")
        self.gridLayout_4.addWidget(self.btn_get_status, 0, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.action_groupbox)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 2, 1, 1, 1)
        self.text_display = QtGui.QTextBrowser(Form)
        self.text_display.setObjectName("text_display")
        self.gridLayout_2.addWidget(self.text_display, 6, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Debug", None, QtGui.QApplication.UnicodeUTF8))
        self.config_groupbox.setTitle(QtGui.QApplication.translate("Form", "Configuration Functions", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_configure_cam.setText(QtGui.QApplication.translate("Form", "configure_cam", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_set_reference_plane.setText(QtGui.QApplication.translate("Form", "set_reference_plane", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_master_gain_range.setText(QtGui.QApplication.translate("Form", "get_master_gain_range", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_exposure_time.setText(QtGui.QApplication.translate("Form", "get_exposure_time", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_check_highspeed_centroids.setText(QtGui.QApplication.translate("Form", "check_highspeed_centroids", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_set_aoi.setText(QtGui.QApplication.translate("Form", "set_aoi", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_reference_plane.setText(QtGui.QApplication.translate("Form", "get_reference_plane", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_set_trigger_mode.setText(QtGui.QApplication.translate("Form", "set_trigger_mode", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_mla_data.setText(QtGui.QApplication.translate("Form", "get_mla_data", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_trigger_mode.setText(QtGui.QApplication.translate("Form", "get_trigger_mode", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_set_highspeed_mode.setText(QtGui.QApplication.translate("Form", "set_highspeed_mode", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_mla_data2.setText(QtGui.QApplication.translate("Form", "get_mla_data2", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_pupil.setText(QtGui.QApplication.translate("Form", "get_pupil", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_exposure_time_range.setText(QtGui.QApplication.translate("Form", "get_exposure_time_range", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_set_pupil.setText(QtGui.QApplication.translate("Form", "set_pupil", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_select_mla.setText(QtGui.QApplication.translate("Form", "select_mla", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_set_exposure_time.setText(QtGui.QApplication.translate("Form", "set_exposure_time", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_black_level_offset.setText(QtGui.QApplication.translate("Form", "get_black_level_offset", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_set_black_level_offset.setText(QtGui.QApplication.translate("Form", "set_black_level_offset", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_aoi.setText(QtGui.QApplication.translate("Form", "get_aoi", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_master_gain.setText(QtGui.QApplication.translate("Form", "get_master_gain", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_mla_count.setText(QtGui.QApplication.translate("Form", "get_mla_count", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_instrument_info.setText(QtGui.QApplication.translate("Form", "get_instrument_info", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_highspeed_windows.setText(QtGui.QApplication.translate("Form", "get_highspeed_windows", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_set_master_gain.setText(QtGui.QApplication.translate("Form", "set_master_gain", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_set_trigger_delay.setText(QtGui.QApplication.translate("Form", "set_trigger_delay", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_trigger_delay_range.setText(QtGui.QApplication.translate("Form", "get_trigger_delay_range", None, QtGui.QApplication.UnicodeUTF8))
        self.args_groupbox.setTitle(QtGui.QApplication.translate("Form", "Arguments", None, QtGui.QApplication.UnicodeUTF8))
        self.label_arg1.setText(QtGui.QApplication.translate("Form", "arg1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_arg2.setText(QtGui.QApplication.translate("Form", "arg2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_arg3.setText(QtGui.QApplication.translate("Form", "arg3", None, QtGui.QApplication.UnicodeUTF8))
        self.label_arg4.setText(QtGui.QApplication.translate("Form", "arg4", None, QtGui.QApplication.UnicodeUTF8))
        self.label_arg5.setText(QtGui.QApplication.translate("Form", "arg5 (instrument_handle)", None, QtGui.QApplication.UnicodeUTF8))
        self.utility_groupbox.setTitle(QtGui.QApplication.translate("Form", "Utility Functions", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_convert_wavefront_waves.setText(QtGui.QApplication.translate("Form", "convert_wavefront_waves", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_xy_scale.setText(QtGui.QApplication.translate("Form", "get_xy_scale", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_error_message.setText(QtGui.QApplication.translate("Form", "error_message", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_revision_query.setText(QtGui.QApplication.translate("Form", "revision_query", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_reset.setText(QtGui.QApplication.translate("Form", "reset", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_self_test.setText(QtGui.QApplication.translate("Form", "self_test", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_error_query.setText(QtGui.QApplication.translate("Form", "error_query", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_instrument_list_info.setText(QtGui.QApplication.translate("Form", "get_instrument_list_info", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_instrument_list_len.setText(QtGui.QApplication.translate("Form", "get_instrument_list_len", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_flip_2d_array.setText(QtGui.QApplication.translate("Form", "flip_2d_array", None, QtGui.QApplication.UnicodeUTF8))
        self.data_groupbox.setTitle(QtGui.QApplication.translate("Form", "Data Functions", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_average_image.setText(QtGui.QApplication.translate("Form", "average_image", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_take_spotfield_image.setText(QtGui.QApplication.translate("Form", "take_spotfield_image", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_average_image_rolling.setText(QtGui.QApplication.translate("Form", "average_image_rolling", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_calc_mean_rms_noise.setText(QtGui.QApplication.translate("Form", "calc_mean_rms_noise", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_zernike_lsf.setText(QtGui.QApplication.translate("Form", "zernike_lsf", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_spotfield_image_copy.setText(QtGui.QApplication.translate("Form", "get_spotfield_image_copy", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cut_image_noise_floor.setText(QtGui.QApplication.translate("Form", "cut_image_noise_floor", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_line.setText(QtGui.QApplication.translate("Form", "get_line", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_spotfield_image.setText(QtGui.QApplication.translate("Form", "get_spotfield_image", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_calc_spots_centroid_diameter_intensity.setText(QtGui.QApplication.translate("Form", "calc_spots_centroid_diameter_intensity", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_spot_diameters_statistics.setText(QtGui.QApplication.translate("Form", "get_spot_diameters_statistics", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_spot_diameters.setText(QtGui.QApplication.translate("Form", "get_spot_diameters", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_calc_spot_to_reference_deviations.setText(QtGui.QApplication.translate("Form", "calc_spot_to_reference_deviations", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_spot_intensities.setText(QtGui.QApplication.translate("Form", "get_spot_intensities", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_spot_centroids.setText(QtGui.QApplication.translate("Form", "get_spot_centroids", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_take_spotfield_image_auto_exposure.setText(QtGui.QApplication.translate("Form", "take_spotfield_image_auto_exposure", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_calc_beam_centroid_diameter.setText(QtGui.QApplication.translate("Form", "calc_beam_centroid_diameter", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_line_view.setText(QtGui.QApplication.translate("Form", "get_line_view", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_spot_reference_positions.setText(QtGui.QApplication.translate("Form", "get_spot_reference_positions", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_calc_fourier_optometric.setText(QtGui.QApplication.translate("Form", "calc_fourier_optometric", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_calc_wavefront.setText(QtGui.QApplication.translate("Form", "calc_wavefront", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_calc_reconstructed_deviations.setText(QtGui.QApplication.translate("Form", "calc_reconstructed_deviations", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_spot_deviations.setText(QtGui.QApplication.translate("Form", "get_spot_deviations", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_calc_image_min_max.setText(QtGui.QApplication.translate("Form", "_calc_image_min_max", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_calc_wavefront_statistics.setText(QtGui.QApplication.translate("Form", "calc_wavefront_statistics", None, QtGui.QApplication.UnicodeUTF8))
        self.calibration_groupbox.setTitle(QtGui.QApplication.translate("Form", "Calibration Functions", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_set_spots_to_user_reference.setText(QtGui.QApplication.translate("Form", "set_spots_to_user_reference", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_do_spherical_reference.setText(QtGui.QApplication.translate("Form", "do_spherical_reference", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_save_user_reference_file.setText(QtGui.QApplication.translate("Form", "save_user_reference_file", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_create_default_user_reference.setText(QtGui.QApplication.translate("Form", "create_default_user_reference", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_load_user_reference_file.setText(QtGui.QApplication.translate("Form", "load_user_reference_file", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_set_calc_spots_to_user_reference.setText(QtGui.QApplication.translate("Form", "set_calc_spots_to_user_reference", None, QtGui.QApplication.UnicodeUTF8))
        self.action_groupbox.setTitle(QtGui.QApplication.translate("Form", "Action Functions", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_init.setText(QtGui.QApplication.translate("Form", "init", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_close.setText(QtGui.QApplication.translate("Form", "close", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_get_status.setText(QtGui.QApplication.translate("Form", "get_status", None, QtGui.QApplication.UnicodeUTF8))

