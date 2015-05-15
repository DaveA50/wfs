"""
Wrapper for interfacing with the Thorlabs Wavefront Sensor (WFS)
"""

__author__ = 'David Amrhein'
__version__ = '0.0.1'

from wfs import WFS


def loop_images(n):
    for i in xrange(n):
        wfs.take_spotfield_image_auto_exposure()
        wfs.get_spotfield_image()
        wfs.calc_spots_centroid_diameter_intensity()
        wfs.get_spot_centroids()
        wfs.calc_beam_centroid_diameter()
        wfs.calc_spot_to_reference_deviations()
        wfs.get_spot_deviations()
        wfs.calc_wavefront()
        wfs.calc_wavefront_statistics()
        wfs.zernike_lsf()

wfs = WFS()
wfs.version()
wfs.get_instrument_list_len()
wfs.get_instrument_list_info()
wfs.init()
wfs.get_instrument_info()
wfs.get_mla_count()
wfs.get_mla_data()
wfs.select_mla()
wfs.configure_cam()
wfs.get_status()
wfs.set_reference_place(0)
wfs.get_reference_plane()
wfs.set_pupil()
wfs.get_pupil()
wfs.get_status()
wfs.take_spotfield_image_auto_exposure()
wfs.get_status()
wfs.take_spotfield_image_auto_exposure()
wfs.get_status()
wfs.take_spotfield_image_auto_exposure()
wfs.get_status()
wfs.take_spotfield_image_auto_exposure()
wfs.get_status()
wfs.take_spotfield_image_auto_exposure()
wfs.get_status()

loop_images(100)

wfs.close()