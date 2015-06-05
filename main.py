"""
Wrapper for interfacing with the Thorlabs Wavefront Sensor (WFS)
"""

from wfs import WFS

def loop_images(n):
    for i in xrange(n):
        wfs._take_spotfield_image_auto_exposure()
        wfs._get_spotfield_image()
        wfs._calc_spots_centroid_diameter_intensity()
        wfs._get_spot_centroids()
        wfs._calc_beam_centroid_diameter()
        wfs._calc_spot_to_reference_deviations()
        wfs._get_spot_deviations()
        wfs._calc_wavefront()
        wfs._calc_wavefront_statistics()
        wfs._zernike_lsf()

wfs = WFS()
wfs._revision_query()
wfs._get_instrument_list_len()
wfs._get_instrument_list_info()
wfs._init()
wfs._get_instrument_info()
wfs._get_mla_count()
wfs._get_mla_data()
wfs._select_mla()
wfs._configure_cam()
wfs._get_status()
wfs._set_reference_place(0)
wfs._get_reference_plane()
wfs._set_pupil()
wfs._get_pupil()
wfs._get_status()
wfs._take_spotfield_image_auto_exposure()
wfs._get_status()
wfs._take_spotfield_image_auto_exposure()
wfs._get_status()
wfs._take_spotfield_image_auto_exposure()
wfs._get_status()
wfs._take_spotfield_image_auto_exposure()
wfs._get_status()
wfs._take_spotfield_image_auto_exposure()
wfs._get_status()

loop_images(10)

wfs._close()
print(wfs.PUPIL_DIA_MAX_MM)