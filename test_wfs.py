# -*- coding: utf-8 -*-

"""Test module for the WFS"""

import pytest

from wfs import WFS


# noinspection PyMissingOrEmptyDocstring
class TestWFS(object):
    """Test class for the WFS"""

    @pytest.fixture(scope='class')
    def wfs(self):
        _wfs = WFS()
        return _wfs

    def test_get_instrument_list_len(self, wfs):
        assert wfs._get_instrument_list_len()[0] == 0

    def test_get_instrument_list_info(self, wfs):
        assert wfs._get_instrument_list_info()[0] == 0

    def test_init(self, wfs):
        assert wfs._init()[0] == 0

    def test_revision_query(self, wfs):
        assert wfs._revision_query()[0] == 0

    def test_get_instrument_info(self, wfs):
        assert wfs._get_instrument_info()[0] == 0

    def test_get_mla_count(self, wfs):
        assert wfs._get_mla_count()[0] == 0

    def test_get_mla_data(self, wfs):
        assert wfs._get_mla_data()[0] == 0

    def test_get_mla_data2(self, wfs):
        assert wfs._get_mla_data2()[0] == 0

    def test_select_mla(self, wfs):
        assert wfs._select_mla() == 0
        # Parameter 2 out of range! # -1074003966
        assert wfs._select_mla(1) == wfs.WFS_ERROR_PARAMETER2
        assert wfs._select_mla(0) == 0

    def test_configure_cam(self, wfs):
        assert wfs._configure_cam()[0] == 0

    def test_get_status(self, wfs):
        assert wfs._get_status()[0] == 0

    def test_set_highspeed_mode(self, wfs):
        # Highspeed mode is not supported! # -1074001641
        assert wfs._set_highspeed_mode() == wfs.WFS_ERROR_NO_HIGHSPEED

    def test_get_highspeed_windows(self, wfs):
        # Highspeed Mode is not active! # -1074001639
        assert wfs._get_highspeed_windows()[0] == wfs.WFS_ERROR_HIGHSPEED_NOT_ACTIVE

    def test_check_highspeed_centroids(self, wfs):
        # Highspeed Mode is not active! # -1074001639
        assert wfs._check_highspeed_centroids() == wfs.WFS_ERROR_HIGHSPEED_NOT_ACTIVE

    def test_get_exposure_time_range(self, wfs):
        assert wfs._get_exposure_time_range()[0] == 0

    def test_set_exposure_time(self, wfs):
        assert wfs._set_exposure_time()[0] == 0
        # Parameter 2 out of range! # -1074003966
        assert wfs._set_exposure_time(0.01)[0] == wfs.WFS_ERROR_PARAMETER2
        assert wfs._set_exposure_time(0.1)[0] == 0
        assert wfs._set_exposure_time(10)[0] == 0
        # Parameter 2 out of range! # -1074003966
        assert wfs._set_exposure_time(67)[0] == wfs.WFS_ERROR_PARAMETER2
        assert wfs._set_exposure_time(1)[0] == 0

    def test_get_exposure_time(self, wfs):
        assert wfs._get_exposure_time()[0] == 0

    def test_get_master_gain_range(self, wfs):
        assert wfs._get_master_gain_range()[0] == 0

    def test_set_master_gain(self, wfs):
        assert wfs._set_master_gain()[0] == 0
        # Parameter 2 out of range! # -1074003966
        assert wfs._set_master_gain(0)[0] == wfs.WFS_ERROR_PARAMETER2
        # Parameter 2 out of range! # -1074003966
        assert wfs._set_master_gain(10)[0] == wfs.WFS_ERROR_PARAMETER2
        assert wfs._set_master_gain(1.5)[0] == 0
        assert wfs._set_master_gain(1)[0] == 0

    def test_get_master_gain(self, wfs):
        assert wfs._get_master_gain()[0] == 0

    def test_set_black_level_offset(self, wfs):
        assert wfs._set_black_level_offset() == 0
        assert wfs._set_black_level_offset(255) == 0
        # Parameter 2 out of range! # -1074003966
        assert wfs._set_black_level_offset(256) == wfs.WFS_ERROR_PARAMETER2
        assert wfs._set_black_level_offset(0) == 0

    def test_get_black_level_offset(self, wfs):
        assert wfs._get_black_level_offset()[0] == 0

    def test_set_trigger_mode(self, wfs):
        assert wfs._set_trigger_mode() == 0
        assert wfs._set_trigger_mode(1) == 0  # WFS_HW_TRIGGER_HL
        assert wfs._set_trigger_mode(2) == 0  # WFS_HW_TRIGGER_LH
        assert wfs._set_trigger_mode(3) == 0  # Why does this pass?
        # Parameter 2 out of range! # -1074003966
        assert wfs._set_trigger_mode(4) == wfs.WFS_ERROR_PARAMETER2
        assert wfs._set_trigger_mode(0) == 0  # WFS_HW_TRIGGER_OFF

    def test_get_trigger_mode(self, wfs):
        assert wfs._get_trigger_mode()[0] == 0

    def test_set_trigger_delay(self, wfs):
        assert wfs._set_trigger_delay()[0] == 0
        # Parameter 2 out of range! # -1074003966
        assert wfs._set_trigger_delay(14)[0] == wfs.WFS_ERROR_PARAMETER2
        assert wfs._set_trigger_delay(4000000)[0] == 0
        # Parameter 2 out of range! # -1074003966
        assert wfs._set_trigger_delay(4000001)[0] == wfs.WFS_ERROR_PARAMETER2
        assert wfs._set_trigger_delay(15)[0] == 0

    def test_get_trigger_delay_range(self, wfs):
        assert wfs._get_trigger_delay_range()[0] == 0

    def test_set_aoi(self, wfs):
        # Resolution: 1280x1024
        # Pixel Size: 4.65 (µm)
        # Sensor Size: 5.952x4.7616 (mm)
        # Sensor Size Center +/-: 2.976x2.3808 (mm)
        assert wfs._set_aoi() == 0
        # Parameter 2 out of range! # -1074003966
        assert wfs._set_aoi(-2.977, 0, 0, 0) == wfs.WFS_ERROR_PARAMETER2
        assert wfs._set_aoi(-2.976, 0, 0, 0) == 0
        # Parameter 2 out of range! # -1074003966
        assert wfs._set_aoi(2.977, 0, 0, 0) == wfs.WFS_ERROR_PARAMETER2
        assert wfs._set_aoi(2.976, 0, 0, 0) == 0
        # Parameter 3 out of range! # -1074003965
        assert wfs._set_aoi(0, -2.3809, 0, 0) == wfs.WFS_ERROR_PARAMETER3
        assert wfs._set_aoi(0, -2.3808, 0, 0) == 0
        # Parameter 3 out of range! # -1074003965
        assert wfs._set_aoi(0, 2.3809, 0, 0) == wfs.WFS_ERROR_PARAMETER3
        assert wfs._set_aoi(0, 2.3808, 0, 0) == 0
        # Parameter 4 out of range! # -1074003964
        assert wfs._set_aoi(0, 0, 5.953, 0) == wfs.WFS_ERROR_PARAMETER4
        assert wfs._set_aoi(0, 0, 5.952, 0) == 0
        # Parameter 5 out of range! # -1074003963
        assert wfs._set_aoi(0, 0, 0, 4.7617) == wfs.WFS_ERROR_PARAMETER5
        assert wfs._set_aoi(0, 0, 0, 4.7616) == 0
        assert wfs._set_aoi(0, 0, 0, 0) == 0

    def test_get_aoi(self, wfs):
        assert wfs._get_aoi()[0] == 0

    def test_set_pupil(self, wfs):
        # Pupil center range: -5.0 mm to +5.0 mm
        # Pupil diameter range: 0.1 mm to 10.0 mm
        assert wfs._set_pupil() == 0
        # Parameter 2 out of range! # -1074003966
        assert wfs._set_pupil(-5.1, 0, 4, 4) == wfs.WFS_ERROR_PARAMETER2
        # Parameter 2 out of range! # -1074003966
        assert wfs._set_pupil(5.1, 0, 4, 4) == wfs.WFS_ERROR_PARAMETER2
        # Parameter 3 out of range! # -1074003965
        assert wfs._set_pupil(0, -5.1, 4, 4) == wfs.WFS_ERROR_PARAMETER3
        # Parameter 3 out of range! # -1074003965
        assert wfs._set_pupil(0, 5.1, 4, 4) == wfs.WFS_ERROR_PARAMETER3
        # Parameter 4 out of range! # -1074003964
        assert wfs._set_pupil(0, 0, 0.09, 4) == wfs.WFS_ERROR_PARAMETER4
        # Parameter 4 out of range! # -1074003964
        assert wfs._set_pupil(0, 0, 10.1, 4) == wfs.WFS_ERROR_PARAMETER4
        # Parameter 5 out of range! # -1074003963
        assert wfs._set_pupil(0, 0, 4, 0.09) == wfs.WFS_ERROR_PARAMETER5
        # Parameter 5 out of range! # -1074003963
        assert wfs._set_pupil(0, 0, 4, 10.1) == wfs.WFS_ERROR_PARAMETER5
        assert wfs._set_pupil(-5, -5, 4, 4) == 0
        assert wfs._set_pupil(5, 5, 4, 4) == 0
        assert wfs._set_pupil(0, 0, 0.1, 0.1) == 0
        assert wfs._set_pupil(0, 0, 10.0, 10.0) == 0
        assert wfs._set_pupil(0, 0, 4, 4) == 0

    def test_get_pupil(self, wfs):
        assert wfs._get_pupil()[0] == 0

    def test_set_reference_plane(self, wfs):
        assert wfs._set_reference_plane() == 0
        # No User Reference available! # -1074001643
        assert wfs._set_reference_plane(1) in (0, wfs.WFS_ERROR_NO_USER_REFERENCE)
        assert wfs._set_reference_plane(0) == 0

    def test_get_reference_plane(self, wfs):
        assert wfs._get_reference_plane()[0] == 0

    # Data Functions
    # def test_take_spotfield_image(self, wfs):
    #     assert wfs._take_spotfield_image() == 0
    #
    # def test_take_spotfield_image_auto_exposure(self, wfs):
    #     assert wfs._take_spotfield_image_auto_exposure()[0] == 0
    #     assert wfs._take_spotfield_image_auto_exposure()[0] == 0
    #     assert wfs._take_spotfield_image_auto_exposure()[0] == 0
    #     assert wfs._take_spotfield_image_auto_exposure()[0] == 0
    #     assert wfs._take_spotfield_image_auto_exposure()[0] == 0
    #
    # def test_get_spotfield_image(self, wfs):
    #     assert wfs._get_spotfield_image()[0] == 0
    #
    # def test_get_spotfield_image_copy(self, wfs):
    #     assert wfs._get_spotfield_image_copy()[0] == 0
    #
    # def test_average_image(self, wfs):
    #     # TODO Try multiple average counts
    #     assert wfs._average_image()[0] == 0
    #
    # def test_average_image_rolling(self, wfs):
    #     # TODO Try multiple average counts
    #     assert wfs._average_image_rolling() == 0
    #
    # def test_cut_image_noise_floor(self, wfs):
    #     assert wfs._cut_image_noise_floor() == 0
    #     assert wfs._cut_image_noise_floor(0) == 0
    #     assert wfs._cut_image_noise_floor(1) == 0
    #     assert wfs._cut_image_noise_floor(256) == 0
    #     # Parameter 2 out of range! # -1074003966
    #     assert wfs._cut_image_noise_floor(257) == wfs.WFS_ERROR_PARAMETER2
    #     assert wfs._cut_image_noise_floor(10) == 0
    #
    # def test_calc_image_min_max(self, wfs):
    #     assert wfs._calc_image_min_max()[0] == 0
    #
    # def test_calc_mean_rms_noise(self, wfs):
    #     assert wfs._calc_mean_rms_noise()[0] == 0
    #
    # def test_get_line(self, wfs):
    #     assert wfs._get_line()[0] == 0
    #     assert wfs._get_line(1023)[0] == 0
    #     # Parameter 2 out of range! # -1074003966
    #     assert wfs._get_line(1024)[0] == wfs.WFS_ERROR_PARAMETER2
    #     assert wfs._get_line(0)[0] == 0
    #
    # def test_get_line_view(self, wfs):
    #     assert wfs._get_line_view()[0] == 0
    #
    # def test_calc_spots_centroid_diameter_intensity(self, wfs):
    #     assert wfs._calc_spots_centroid_diameter_intensity() == 0
    #     assert wfs._calc_spots_centroid_diameter_intensity(0, 0) == 0
    #     assert wfs._calc_spots_centroid_diameter_intensity(0, 1) == 0
    #     assert wfs._calc_spots_centroid_diameter_intensity(1, 0) == 0
    #     assert wfs._calc_spots_centroid_diameter_intensity(1, 1) == 0
    #
    # def test_get_spot_centroids(self, wfs):
    #     assert wfs._get_spot_centroids()[0] == 0
    #
    # def test_calc_beam_centroid_diameter(self, wfs):
    #     assert wfs._calc_beam_centroid_diameter()[0] == 0
    #
    # def test_calc_spot_to_reference_deviations(self, wfs):
    #     assert wfs._calc_spot_to_reference_deviations() == 0
    #
    # def test_get_spot_diameters(self, wfs):
    #     assert wfs._get_spot_diameters()[0] == 0
    #
    # def test_get_spot_intensities(self, wfs):
    #     assert wfs._get_spot_intensities()[0] == 0
    #
    # def test_get_spot_reference_positions(self, wfs):
    #     assert wfs._get_spot_reference_positions()[0] == 0
    #
    # def test_get_spot_deviations(self, wfs):
    #     assert wfs._get_spot_deviations()[0] == 0
    #
    # def test_zernike_lsf(self, wfs):
    #     assert wfs._zernike_lsf()[0] == 0
    #
    # def test_calc_fourier_optometric(self, wfs):
    #     assert wfs._calc_fourier_optometric()[0] == 0
    #
    # def test_calc_reconstructed_deviations(self, wfs):
    #     assert wfs._calc_reconstructed_deviations()[0] == 0
    #
    # def test_calc_wavefront(self, wfs):
    #     assert wfs._calc_wavefront()[0] == 0
    #
    # def test_calc_wavefront_statistics(self, wfs):
    #     assert wfs._calc_wavefront_statistics()[0] == 0
    #
    # def test_get_spot_diameters_statistics(self, wfs):
    #     assert wfs._get_spot_diameters_statistics()[0] == 0
    #
    # def test_get_xy_scale(self, wfs):
    #     assert wfs._get_xy_scale()[0] == 0
    #
    # def test_convert_wavefront_waves(self, wfs):
    #     assert wfs._convert_wavefront_waves()[0] == 0
    #
    # def test_flip_2d_array(self, wfs):
    #     assert wfs._flip_2d_array()[0] == 0

    # Utility Functions
    def test_self_test(self, wfs):
        # Self-test not supported
        assert wfs._self_test()[0] == 1073479939

    def test_reset(self, wfs):
        # Reset not supported
        assert wfs._reset() == 1073479938

    def test_error_query(self, wfs):
        # Error query not supported
        assert wfs._error_query()[0] == 1073479940

    def test_error_message(self, wfs):
        assert wfs._error_message(wfs.WFS_ERROR_PARAMETER1) == (0, 'Parameter 1 out of range!')
        assert wfs._error_message(wfs.WFS_ERROR_PARAMETER2) == (0, 'Parameter 2 out of range!')
        assert wfs._error_message(wfs.WFS_ERROR_PARAMETER3) == (0, 'Parameter 3 out of range!')
        assert wfs._error_message(wfs.WFS_ERROR_PARAMETER4) == (0, 'Parameter 4 out of range!')
        assert wfs._error_message(wfs.WFS_ERROR_PARAMETER5) == (0, 'Parameter 5 out of range!')
        assert wfs._error_message(wfs.WFS_ERROR_PARAMETER6) == (0, 'Parameter 6 out of range!')
        assert wfs._error_message(wfs.WFS_ERROR_PARAMETER7) == (0, 'Parameter 7 out of range!')
        assert wfs._error_message(wfs.WFS_ERROR_PARAMETER8) == (0, 'Parameter 8 out of range!')
        assert wfs._error_message(wfs.WFS_ERROR_NO_SENSOR_CONNECTED) == (0, 'No Wavefront Sensor connected!')
        assert wfs._error_message(wfs.WFS_ERROR_OUT_OF_MEMORY) == (0, 'Out of memory!')
        assert wfs._error_message(wfs.WFS_ERROR_INVALID_HANDLE) == (0, 'Wrong Instrument handle!')
        # Reports unknown error instead of cam not configured
        assert wfs._error_message(wfs.WFS_ERROR_CAM_NOT_CONFIGURED)[0] == 0
        assert wfs._error_message(wfs.WFS_ERROR_PIXEL_FORMAT) == (0, 'Pixel format not supported!')
        assert wfs._error_message(wfs.WFS_ERROR_EEPROM_CHECKSUM) == (0, 'Wrong EEPROM checksum!')
        assert wfs._error_message(wfs.WFS_ERROR_EEPROM_CAL_DATA) == (0, 'Wrong calibration data in EEPROM!')
        # noinspection PyPep8
        assert wfs._error_message(wfs.WFS_ERROR_OLD_REF_FILE) == (0, 'Only old reference file for unspecific MLA found!')
        assert wfs._error_message(wfs.WFS_ERROR_NO_REF_FILE) == (0, 'No reference file found!')
        assert wfs._error_message(wfs.WFS_ERROR_CORRUPT_REF_FILE) == (0, 'Corrupt reference file!')
        assert wfs._error_message(wfs.WFS_ERROR_WRITE_FILE) == (0, 'Reference file write error!')
        assert wfs._error_message(wfs.WFS_ERROR_INSUFF_SPOTS_FOR_ZERNFIT) == (0, 'Insufficient spots for Zernike fit!')
        assert wfs._error_message(wfs.WFS_ERROR_TOO_MANY_SPOTS_FOR_ZERNFIT) == (0, 'Too many spots for Zernike fit!')
        assert wfs._error_message(wfs.WFS_ERROR_FOURIER_ORDER) == (0, 'Fourier order must not exceed Zernike order!')
        # noinspection PyPep8
        assert wfs._error_message(wfs.WFS_ERROR_NO_RECON_DEVIATIONS) == (0, 'Reconstructed spot deviations not yet calculated!')
        assert wfs._error_message(wfs.WFS_ERROR_NO_PUPIL_DEFINED) == (0, 'Pupil not yet defined!')
        assert wfs._error_message(wfs.WFS_ERROR_WRONG_PUPIL_DIA) == (0, 'Pupil diameter out of range!')
        assert wfs._error_message(wfs.WFS_ERROR_WRONG_PUPIL_CTR) == (0, 'Pupil center out of range!')
        assert wfs._error_message(wfs.WFS_ERROR_INVALID_CAL_DATA) == (0, 'MLA calibration data invalid!')
        # Seems to be the real cam not configured error
        assert wfs._error_message(wfs.WFS_ERROR_INTERNAL_REQUIRED)[0] == 0
        assert wfs._error_message(wfs.WFS_ERROR_ROC_RANGE) == (0, 'RoC out of range!')
        assert wfs._error_message(wfs.WFS_ERROR_NO_USER_REFERENCE) == (0, 'No User Reference available!')
        assert wfs._error_message(wfs.WFS_ERROR_AWAITING_TRIGGER) == (0, 'Function is awaiting a hardware trigger!')
        assert wfs._error_message(wfs.WFS_ERROR_NO_HIGHSPEED) == (0, 'Highspeed mode is not supported!')
        assert wfs._error_message(wfs.WFS_ERROR_HIGHSPEED_ACTIVE) == (0, 'Highspeed mode is active!')
        assert wfs._error_message(wfs.WFS_ERROR_HIGHSPEED_NOT_ACTIVE) == (0, 'Highspeed Mode is not active!')
        # noinspection PyPep8
        assert wfs._error_message(wfs.WFS_ERROR_HIGHSPEED_WINDOW_MISMATCH) == (0, 'Highspeed Mode centroid window mismatch!')
        assert wfs._error_message(wfs.WFS_ERROR_NOT_SUPPORTED) == (0, 'Function is not supported by WFS!')
        # Has the same value as above as per documentation
        assert wfs._error_message(wfs.WFS_ERROR_SPOT_TRUNCATED)[0] == 0
        assert wfs._error_message(wfs.WFS_ERROR_NO_SPOT_DETECTED) == (0, 'Spot not detectable!')
        assert wfs._error_message(wfs.WFS_ERROR_TILT_CALCULATION) == (0, 'Lenslet/Pin tilt calculation failed!')
        assert wfs._error_message(wfs.WFS_WARN_NSUP_ID_QUERY) == (0, 'Identification query not supported!')
        assert wfs._error_message(wfs.WFS_WARN_NSUP_RESET) == (0, 'Reset not supported!')
        assert wfs._error_message(wfs.WFS_WARN_NSUP_SELF_TEST) == (0, 'Self-test not supported!')
        assert wfs._error_message(wfs.WFS_WARN_NSUP_ERROR_QUERY) == (0, 'Error query not supported!')
        assert wfs._error_message(wfs.WFS_WARN_NSUP_REV_QUERY) == (0, 'Instrument revision query not supported!')

    # Calibration Functions
    # def test_set_spots_to_user_reference(self, wfs):
    #     # TODO
    #     assert wfs._set_spots_to_user_reference() == 0
    #
    # def test_set_calc_spots_to_user_reference(self, wfs):
    #     # TODO
    #     assert wfs._set_calc_spots_to_user_reference() == 0
    #
    # def test_create_default_user_reference(self, wfs):
    #     # TODO
    #     assert wfs._create_default_user_reference() == 0
    #
    # def test_do_spherical_reference(self, wfs):
    #     # TODO
    #     assert wfs._do_spherical_reference() in (wfs.WFS_ERROR_ROC_RANGE, 0)
    #
    # def test_save_user_reference_file(self, wfs):
    #     # TODO
    #     assert wfs._save_user_reference_file() in (wfs.WFS_ERROR_WRITE_FILE, 0)
    #
    # def test_load_user_reference_file(self, wfs):
    #     # TODO
    #     assert wfs._load_user_reference_file() in (wfs.WFS_ERROR_OLD_REF_FILE, wfs.WFS_ERROR_NO_REF_FILE,
    #                                                wfs.WFS_ERROR_CORRUPT_REF_FILE, 0)

    def test_close(self, wfs):
        assert wfs._close() == 0
