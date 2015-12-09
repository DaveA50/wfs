import pytest

from wfs import WFS


@pytest.fixture(scope='module')
def wfs(request):
    _wfs = WFS()
    #
    # def test_close():
    #     print('Closing wfs')
    #     assert _wfs._close() == 0
    # request.addfinalizer(test_close)
    #
    return _wfs


def test_revision_query(wfs):
    assert wfs._revision_query() == 0


def test_get_instrument_list_len(wfs):
    assert wfs._get_instrument_list_len() == 0


def test_get_instrument_list_info(wfs):
    assert wfs._get_instrument_list_info() == 0


def test_init(wfs):
    assert wfs._init() == 0


def test_get_instrument_info(wfs):
    assert wfs._get_instrument_info() == 0


def test_get_mla_count(wfs):
    assert wfs._get_mla_count() == 0


def test_get_mla_data(wfs):
    assert wfs._get_mla_data() == 0


def test_get_mla_data2(wfs):
    assert wfs._get_mla_data2() == 0


def test_select_mla(wfs):
    assert wfs._select_mla() == 0


def test_configure_cam(wfs):
    assert wfs._configure_cam() == 0


def test_get_status(wfs):
    assert wfs._get_status() == 0


def test_set_highspeed_mode(wfs):
    # assert wfs._set_highspeed_mode() == 0
    pass  # Not able to test on WFS150


def test_get_highspeed_windows(wfs):
    # assert wfs._get_highspeed_windows() == 0
    pass  # Not able to test on WFS150


def test_check_highspeed_centroids(wfs):
    # assert wfs._check_highspeed_centroids() == 0
    pass  # Not able to test on WFS150


# def test_get_exposure_time_range(wfs):
#     assert wfs._get_exposure_time_range() == 0
#
#
# def test_set_exposure_time(wfs):
#     assert wfs._set_exposure_time() == 0
#
#
# def test_get_exposure_time(wfs):
#     assert wfs._get_exposure_time() == 0
#
#
# def test_get_master_gain_range(wfs):
#     assert wfs._get_master_gain_range() == 0
#
#
# def test_set_master_gain_time(wfs):
#     assert wfs._set_master_gain_time() == 0
#
#
# def test_get_master_gain_time(wfs):
#     assert wfs._get_master_gain_time() == 0
#
#
# def test_set_black_level_offset(wfs):
#     assert wfs._set_black_level_offset() == 0
#
#
# def test_get_black_level_offset(wfs):
#     assert wfs._get_black_level_offset() == 0
#
#
# def test_set_trigger_mode(wfs):
#     assert wfs._set_trigger_mode() == 0
#
#
# def test_get_trigger_mode(wfs):
#     assert wfs._get_trigger_mode() == 0
#
#
# def test_set_trigger_delay(wfs):
#     assert wfs._set_trigger_delay() == 0
#
#
# def test_get_trigger_delay_range(wfs):
#     assert wfs._get_trigger_delay_range() == 0
#
#
# def test_set_aoi(wfs):
#     assert wfs._set_aoi() == 0
#
#
# def test_get_aoi(wfs):
#     assert wfs._get_aoi() == 0
#
#
def test_set_pupil(wfs):
    assert wfs._set_pupil() == 0


def test_get_pupil(wfs):
    assert wfs._get_pupil() == 0


def test_set_reference_place(wfs):
    assert wfs._set_reference_place(0) == 0


def test_get_reference_plane(wfs):
    assert wfs._get_reference_plane() == 0


def test_take_spotfield_image(wfs):
    assert wfs._take_spotfield_image() == 0


def test_take_spotfield_image_auto_exposure(wfs):
    assert wfs._take_spotfield_image_auto_exposure() == 0


def test_get_spotfield_image(wfs):
    assert wfs._get_spotfield_image() == 0


# def test_get_spotfield_image_copy(wfs):
#     assert wfs._get_spotfield_image_copy() == 0
#

# def test_average_image(wfs):
#     assert wfs._average_image() == 0
#
#
# def test_average_image_rolling(wfs):
#     assert wfs._average_image_rolling() == 0
#
#
# def test_cut_image_noise_floor(wfs):
#     assert wfs._cut_image_noise_floor() == 0
#
#
# def test_calc_image_min_max(wfs):
#     assert wfs._calc_image_min_max() == 0
#
#
# def test_calc_mean_rms_noise(wfs):
#     assert wfs._calc_mean_rms_noise() == 0
#
#
# def test_get_line(wfs):
#     assert wfs._get_line() == 0
#
#
# def test_get_line_view(wfs):
#     assert wfs._get_line_view() == 0
#
#
def test_calc_beam_centroid_diameter(wfs):
    assert wfs._calc_beam_centroid_diameter() == 0


def test_calc_spots_centroid_diameter_intensity(wfs):
    assert wfs._calc_spots_centroid_diameter_intensity() == 0


def test_get_spot_centroids(wfs):
    assert wfs._get_spot_centroids() == 0


# def test_get_spot_diameters(wfs):
#     assert wfs._get_spot_diameters() == 0
#
#
# def test_get_spot_diameters_statistics(wfs):
#     assert wfs._get_spot_diameters_statistics() == 0
#
#
# def test_get_spot_intensities(wfs):
#     assert wfs._get_spot_intensities() == 0
#
#
def test_calc_spot_to_reference_deviations(wfs):
    assert wfs._calc_spot_to_reference_deviations() == 0


# def test_get_spot_reference_positions(wfs):
#     assert wfs._get_spot_reference_positions() == 0
#
#
def test_get_spot_deviations(wfs):
    assert wfs._get_spot_deviations() == 0


def test_zernike_lsf(wfs):
    assert wfs._zernike_lsf() == 0


# def test_calc_fourier_optometric(wfs):
#     assert wfs._calc_fourier_optometric() == 0
#
#
# def test_calc_reconstructed_deviations(wfs):
#     assert wfs._calc_reconstructed_deviations() == 0
#
#
def test_calc_wavefront(wfs):
    assert wfs._calc_wavefront() == 0


def test_calc_wavefront_statistics(wfs):
    assert wfs._calc_wavefront_statistics() == 0


# def test_self_test(wfs):
#     assert wfs._self_test() == 0
#
#
# def test_reset(wfs):
#     assert wfs._reset() == 0
#
#
# def test_error_query(wfs):
#     assert wfs._error_query() == 0
#
#
# def test_error_message(wfs):
#     assert wfs._error_message() == 0
#
#
# def test_get_xy_scale(wfs):
#     assert wfs._get_xy_scale() == 0
#
#
# def test_convert_wavefront_waves(wfs):
#     assert wfs._convert_wavefront_waves() == 0
#
#
# def test_flip_2d_array(wfs):
#     assert wfs._flip_2d_array() == 0
#
#
# def test_set_spots_to_user_reference(wfs):
#     assert wfs._set_spots_to_user_reference() == 0
#
#
# def test_set_calc_spots_to_user_reference(wfs):
#     assert wfs._set_calc_spots_to_user_reference() == 0
#
#
# def test_create_default_user_reference(wfs):
#     assert wfs._create_default_user_reference() == 0
#
#
# def test_save_user_reference_file(wfs):
#     assert wfs._save_user_reference_file() == 0
#
#
# def test_load_user_reference_file(wfs):
#     assert wfs._load_user_reference_file() == 0
#
#
# def test_do_spherical_reference(wfs):
#     assert wfs._do_spherical_reference() == 0


def test_close(wfs):
    print('Closing wfs')
    assert wfs._close() == 0
