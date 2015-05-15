"""
Wrapper for interfacing with the Thorlabs Wavefront Sensor (WFS)
"""

__author__ = 'David Amrhein'
__version__ = '0.0.1'
# $Source$

import ctypes
from ctypes.util import find_library
import logging
import logging.config
import os
import yaml


def setup_logging(path='logging.yaml', level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration

    """
    path = path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)

setup_logging()
logger_camera = logging.getLogger('camera')
logger_wfs = logging.getLogger('wfs')


libname = 'WFS_32'
lib = find_library(libname)
if lib is None:
    if os.name == 'posix':
        logger_wfs.critical('No WFS_32 library exists')
        raise ImportError
    if os.name == 'nt':
        logger_wfs.critical('WFS_32.dll not found')
        raise ImportError
if os.name == 'nt':
    lib_wfs = ctypes.windll.LoadLibrary(lib)
    logger_wfs.debug('WFS_32.dll loaded')


class ViSession(ctypes.c_ulong):
    pass  # long unsigned int


class ViBoolean(ctypes.c_ushort):
    pass  # short unsigned int


class ViRsrc(ctypes.c_char_p):
    pass  # char*


class ViReal64(ctypes.c_double):
    pass  # double
    pass  # char*


class ViPReal64(ctypes.c_double):
    pass  # double Pointer


class ViStatus(ctypes.c_long):
    pass  # long int


class ViUInt8(ctypes.c_ubyte):
    pass  # !Binary8 unsigned char


class ViAUInt8(ctypes.c_ubyte):
    pass  # !Binary8 unsigned char


class ViInt16(ctypes.c_int):
    pass  # Binary16 short int


class ViInt32(ctypes.c_long):
    pass  # Binary32 long int


class ViPInt32(ctypes.c_long):
    pass  # Binary32 long int Pointer


def ViAChar(n):
    """Create a ctypes char array of size n
    :param n: size of char array
    :rtype : ctypes char array
    """
    return ctypes.create_string_buffer(n)


class WFS(ViSession):

    # _WFS_ERROR = (-2147483647L-1)  # 0x80000000
    # WFS_INSTR_WARNING_OFFSET = 0x3FFC0900L
    # WFS_INSTR_ERROR_OFFSET = _WFS_ERROR + 0x3FFC0900L  # 0xBFFC0900

    # def CALL(self, name, *args):
    #     func_name = 'WFS_' + name
    #     func = getattr(lib_wfs, func_name)
    #     new_args = []
    #     for a in args:
    #         if isinstance(a, unicode):
    #             logger.debug(name, 'argument',a, 'is unicode')
    #             new_args.append(str (a))
    #         else:
    #              new_args.append(a)
    #     status = func(*new_args)
    #     return status
    MAX_SPOTS_X = 50
    MAX_SPOTS_Y = 40
    MAX_ZERNIKE_MODES = 66
    MAX_ZERNIKE_ORDERS = 10

    def __init__(self):
        self.instrument_handle = 0

    def init(self,
             resource_name='USB::0x1313::0x0000::1',
             id_query=0,
             reset_device=0,
             instrument_handle=0):
        self.resource_name = ViRsrc(resource_name)
        self.id_query = ViBoolean(id_query)
        self.reset_device = ViBoolean(reset_device)
        self.instrument_handle = ViSession(instrument_handle)
        status = lib_wfs.WFS_init(resource_name,
                                  id_query,
                                  reset_device,
                                  ctypes.byref(self.instrument_handle))
        logger_camera.info('Instrument Handle: {0}'.format(self.instrument_handle.value))
        return status

    def reset(self):
        status = lib_wfs.WFS_reset(self.instrument_handle)
        return status

    def close(self):
        status = lib_wfs.WFS_close(self.instrument_handle)
        return status

    def get_instrument_info(self):
        manufacturer_name = ViAChar(256)
        instrument_name_wfs = ViAChar(256)
        serial_number_wfs = ViAChar(256)
        serial_number_camera = ViAChar(256)
        status = lib_wfs.WFS_GetInstrumentInfo(self.instrument_handle,
                                               manufacturer_name,
                                               instrument_name_wfs,
                                               serial_number_wfs,
                                               serial_number_camera)
        logger_camera.info('Manufacturer Name: {0}'.format(manufacturer_name.value))
        logger_camera.info('Instrument Name WFS: {0}'.format(instrument_name_wfs.value))
        logger_camera.info('Serial Number WFS: {0}'.format(serial_number_wfs.value))
        logger_camera.info('Serial Number Camera: {0}'.format(serial_number_camera.value))
        return status

    def get_mla_count(self):
        MLACount = ViPInt32()
        status = lib_wfs.WFS_GetMlaCount(self.instrument_handle,
                                         ctypes.byref(MLACount))
        logger_camera.info('Micro Lens Array: {0}'.format(MLACount.value))
        self.mla_index = ViInt32(MLACount.value - 1)
        return status

    def get_mla_data(self):
        mla_name = ViAChar(256)
        camPitchm = ViPReal64()
        lensletPitchm = ViPReal64()
        spotOffsetX = ViPReal64()
        spotOffsetY = ViPReal64()
        lensletFm = ViPReal64()
        grdCorr0 = ViPReal64()
        grdCorr45 = ViPReal64()
        status = lib_wfs.WFS_GetMlaData(self.instrument_handle,
                                        self.mla_index,
                                        mla_name,
                                        ctypes.byref(camPitchm),
                                        ctypes.byref(lensletPitchm),
                                        ctypes.byref(spotOffsetX),
                                        ctypes.byref(spotOffsetY),
                                        ctypes.byref(lensletFm),
                                        ctypes.byref(grdCorr0),
                                        ctypes.byref(grdCorr45))

        logger_camera.info('MLA Name: {0}'.format(mla_name.value))
        logger_camera.info('MLA camPitchm: {0}'.format(camPitchm.value))
        logger_camera.info('MLA lensletPitchm: {0}'.format(lensletPitchm.value))
        logger_camera.info('MLA spotOffsetX: {0}'.format(spotOffsetX.value))
        logger_camera.info('MLA spotOffsetY: {0}'.format(spotOffsetY.value))
        logger_camera.info('MLA lensletFm: {0}'.format(lensletFm.value))
        logger_camera.info('MLA grdCorr0: {0}'.format(grdCorr0.value))
        logger_camera.info('MLA grdCorr45: {0}'.format(grdCorr45.value))
        return status

    def get_mla_data2(self):
        MLAName = ViAChar(256)
        camPitchm = ViPReal64()
        lensletPitchm = ViPReal64()
        spotOffsetX = ViPReal64()
        spotOffsetY = ViPReal64()
        lensletFm = ViPReal64()
        grdCorr0 = ViPReal64()
        grdCorr45 = ViPReal64()
        grdCorrRot = ViPReal64()
        grdCorrPitch = ViPReal64()
        status = lib_wfs.WFS_GetMlaData2(self.instrument_handle,
                                        self.mla_index,
                                        MLAName,
                                        ctypes.byref(camPitchm),
                                        ctypes.byref(lensletPitchm),
                                        ctypes.byref(spotOffsetX),
                                        ctypes.byref(spotOffsetY),
                                        ctypes.byref(lensletFm),
                                        ctypes.byref(grdCorr0),
                                        ctypes.byref(grdCorr45),
                                        ctypes.byref(grdCorrRot),
                                        ctypes.byref(grdCorrPitch))

        logger_camera.info('MLA Name: {0}'.format(MLAName.value))
        logger_camera.info('MLA camPitchm: {0}'.format(camPitchm.value))
        logger_camera.info('MLA lensletPitchm: {0}'.format(lensletPitchm.value))
        logger_camera.info('MLA spotOffsetX: {0}'.format(spotOffsetX.value))
        logger_camera.info('MLA spotOffsetY: {0}'.format(spotOffsetY.value))
        logger_camera.info('MLA lensletFm: {0}'.format(lensletFm.value))
        logger_camera.info('MLA grdCorr0: {0}'.format(grdCorr0.value))
        logger_camera.info('MLA grdCorr45: {0}'.format(grdCorr45.value))
        logger_camera.info('MLA grdCorrRot: {0}'.format(grdCorrRot.value))
        logger_camera.info('MLA grdCorrPitch: {0}'.format(grdCorrPitch.value))
        return status

    def select_mla(self):
        status = lib_wfs.WFS_SelectMla(self.instrument_handle,
                                       self.mla_index)
        if status ==0:
            logger_camera.info('MLA selection: {0}'.format(self.mla_index.value))
            pass
        return status

    def configure_cam(self):
        pixelFormat = ViInt32(0)
        camResolIndex = ViInt32(0)
        self.spotsX = ViPInt32()
        self.spotsY = ViPInt32()
        status = lib_wfs.WFS_ConfigureCam(self.instrument_handle,
                                              pixelFormat,
                                              camResolIndex,
                                              ctypes.byref(self.spotsX),
                                              ctypes.byref(self.spotsY))
        logger_camera.info('Spots X: {0}'.format(self.spotsX.value))
        logger_camera.info('Spots Y: {0}'.format(self.spotsY.value))
        return status

    def version(self,
                instrumentHandle=0,
                instrumentDriverRevision=256,
                firmwareRevision=256):
        self.instrument_handle = ViSession.__init__(self, instrumentHandle)
        self.instrumentDriverRevision = ViAChar(instrumentDriverRevision)
        self.firmwareRevision = ViAChar(firmwareRevision)
        status = lib_wfs.WFS_revision_query(self.instrument_handle,
                                            self.instrumentDriverRevision,
                                            self.firmwareRevision)
        logger_camera.info('Instrument Driver Version: {0}'.format(self.instrumentDriverRevision.value))
        logger_camera.info('Instrument Firmware Version: {0}'.format(self.firmwareRevision.value))
        return status

    def get_instrument_list_len(self, instrumentHandle=0, instrumentCount=0):
        self.instrument_handle = ViSession.__init__(self, instrumentHandle)
        instrumentCount = ViInt32(instrumentCount)
        status = lib_wfs.WFS_GetInstrumentListLen(self.instrument_handle,
                                                  ctypes.byref(instrumentCount))
        self.instrument_index = ViInt32(instrumentCount.value - 1)
        logger_camera.info('Instrument Index: {0}'.format(self.instrument_index.value))
        return status

    def get_instrument_list_info(self,
                              handle=ViSession(0),
                              device_id=0,
                              in_use=0,
                              instrument_name=256,
                              serial_number_wfs=256,
                              resourceName=256):
        self.device_id = ViInt32(device_id)
        self.in_use = ViInt32(in_use)
        self.instrument_name = ViAChar(instrument_name)
        self.serial_number_wfs = ViAChar(serial_number_wfs)
        self.resource_name = ViAChar(resourceName)
        status = lib_wfs.WFS_GetInstrumentListInfo(handle,
                                                   self.instrument_index,
                                                   ctypes.byref(self.device_id),
                                                   ctypes.byref(self.in_use),
                                                   self.instrument_name,
                                                   self.serial_number_wfs,
                                                   self.resource_name)
        logger_camera.info('Device ID: {0}'.format(self.device_id.value))
        logger_camera.info('In Use: {0}'.format(self.in_use.value))
        logger_camera.info('Instrument Name: {0}'.format(self.instrument_name.value))
        logger_camera.info('Serial Number WFS: {0}'.format(self.serial_number_wfs.value))
        logger_camera.info('Resource Name: {0}'.format(self.resource_name.value))
        return status

    def get_status(self):
        deviceStatus = ViInt32()
        status = lib_wfs.WFS_GetStatus(self.instrument_handle,
                                   ctypes.byref(deviceStatus))
        logger_camera.info('Device Status: {0}'.format(deviceStatus.value))
        return status

    def self_test(self):
        # selfTestResult = ViInt16()
        # selfTestMessage = ViAChar(256)
        # status = lib_wfs.WFS_self_test(self.instrumentHandle,
        #                                ctypes.byref(selfTestResult),
        #                                selfTestMessage)
        # logger.info('Self Test Result: {0}'.format(selfTestResult.value))
        # logger.info('Self Test Message: {0}'.format(selfTestMessage.value))
        # return status
        pass

    def error_query(self):
        handle = ViSession.__init__(self, 0)
        errorCode = ViInt32()
        errorMessage = ViAChar(256)
        status = lib_wfs.WFS_error_query(handle,
                                         ctypes.byref(errorCode),
                                         errorMessage)
        return status

    def error_message(self):
        handle = ViSession.__init__(self, 0)
        error_code = ViStatus()
        error_message = ViAChar(256)
        status = lib_wfs.WFS_error_message(handle,
                                           error_code,
                                           error_message)
        return status

    def set_reference_place(self, reference_index=0):
        self.reference_index = ViInt32(reference_index)
        status = lib_wfs.WFS_SetReferencePlane(self.instrument_handle,
                                               self.reference_index)
        logger_camera.info('Set Reference Index: {0}'.format(self.reference_index.value))
        return status

    def get_reference_plane(self):
        status = lib_wfs.WFS_GetReferencePlane(self.instrument_handle,
                                               ctypes.byref(self.reference_index))
        logger_camera.info('Get Reference Index: {0}'.format(self.reference_index.value))
        return status

    def set_pupil(self, pupil_center_x_mm=0, pupil_center_y_mm=0, pupil_diameter_x_mm=4.76, pupil_diameter_y_mm=4.76):
        self.pupil_center_x_mm = ViReal64(pupil_center_x_mm)
        self.pupil_center_y_mm = ViReal64(pupil_center_y_mm)
        self.pupil_diameter_x_mm = ViReal64(pupil_diameter_x_mm)
        self.pupil_diameter_y_mm = ViReal64(pupil_diameter_y_mm)
        status = lib_wfs.WFS_SetPupil(self.instrument_handle,
                                      self.pupil_center_x_mm,
                                      self.pupil_center_y_mm,
                                      self.pupil_diameter_x_mm,
                                      self.pupil_diameter_y_mm)
        logger_camera.info('Set Pupil Centroid X [mm]: {0}'.format(self.pupil_center_x_mm.value))
        logger_camera.info('Set Pupil Centroid Y [mm]: {0}'.format(self.pupil_center_y_mm.value))
        logger_camera.info('Set Pupil Diameter X [mm]: {0}'.format(self.pupil_diameter_x_mm.value))
        logger_camera.info('Set Pupil Diameter Y [mm]: {0}'.format(self.pupil_diameter_y_mm.value))
        return status

    def get_pupil(self):
        status = lib_wfs.WFS_GetPupil(self.instrument_handle,
                                      ctypes.byref(self.pupil_center_x_mm),
                                      ctypes.byref(self.pupil_center_y_mm),
                                      ctypes.byref(self.pupil_diameter_x_mm),
                                      ctypes.byref(self.pupil_diameter_y_mm))
        logger_camera.info('Get Pupil Centroid X [mm]: {0}'.format(self.pupil_center_x_mm.value))
        logger_camera.info('Get Pupil Centroid Y [mm]: {0}'.format(self.pupil_center_y_mm.value))
        logger_camera.info('Get Pupil Diameter X [mm]: {0}'.format(self.pupil_diameter_x_mm.value))
        logger_camera.info('Get Pupil Diameter Y [mm]: {0}'.format(self.pupil_diameter_y_mm.value))
        return status

    def take_spotfield_image_auto_exposure(self):
        exposure_time_act = ViPReal64()
        master_gain_act = ViPReal64()
        status = lib_wfs.WFS_TakeSpotfieldImageAutoExpos(self.instrument_handle,
                                                         ctypes.byref(exposure_time_act),
                                                         ctypes.byref(master_gain_act))
        logger_camera.info('Exposure Time Act: {0}'.format(exposure_time_act.value))
        logger_camera.info('Master Gain Act: {0}'.format(master_gain_act.value))
        return status

    def get_spotfield_image(self):
        image_buffer = (ctypes.c_uint)()
        rows = ViInt32()
        columns = ViInt32()
        status = lib_wfs.WFS_GetSpotfieldImage(self.instrument_handle,
                                               ctypes.byref(image_buffer),
                                               ctypes.byref(rows),
                                               ctypes.byref(columns))
        logger_camera.info('Image Buffer: {0}'.format(image_buffer.value))
        logger_camera.info('Rows: {0}'.format(rows.value))
        logger_camera.info('Columns: {0}'.format(columns.value))
        return status

    def calc_spots_centroid_diameter_intensity(self):
        dynamic_noise_cut = ViInt32(1)
        calculate_diameters = ViInt32(0)
        status = lib_wfs.WFS_CalcSpotsCentrDiaIntens(self.instrument_handle,
                                                     dynamic_noise_cut,
                                                     calculate_diameters)
        return status

    def calc_spot_to_reference_deviations(self):
        cancel_wavefront_tilt = ViInt32(1)
        status = lib_wfs.WFS_CalcSpotToReferenceDeviations(self.instrument_handle,
                                                           cancel_wavefront_tilt)
        return status

    def get_spot_centroids(self):
        array_centroid_x = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        array_centroid_y = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        status = lib_wfs.WFS_GetSpotCentroids(self.instrument_handle,
                                              array_centroid_x,
                                              array_centroid_y)
        logger_camera.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in array_centroid_x]))
        logger_camera.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in array_centroid_y]))
        return status

    def calc_wavefront(self):
        array_wavefront = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        wavefront_type = ViInt32(0)
        limit_to_pupil = ViInt32(0)
        status = lib_wfs.WFS_CalcWavefront(self.instrument_handle,
                                           wavefront_type,
                                           limit_to_pupil,
                                           array_wavefront)
        logger_camera.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in array_wavefront]))
        return status

    def calc_wavefront_statistics(self):
        min_ = ViPReal64(0)
        max_ = ViPReal64(0)
        diff = ViPReal64(0)
        mean = ViPReal64(0)
        rms = ViPReal64(0)
        weighted_rms = ViPReal64(0)
        status = lib_wfs.WFS_CalcWavefrontStatistics(self.instrument_handle,
                                                     ctypes.byref(min_),
                                                     ctypes.byref(max_),
                                                     ctypes.byref(diff),
                                                     ctypes.byref(mean),
                                                     ctypes.byref(rms),
                                                     ctypes.byref(weighted_rms))
        logger_camera.info('Min: {0}'.format(min_.value))
        logger_camera.info('Max: {0}'.format(max_.value))
        logger_camera.info('Diff: {0}'.format(diff.value))
        logger_camera.info('Mean: {0}'.format(mean.value))
        logger_camera.info('RMS: {0}'.format(rms.value))
        logger_camera.info('Weighted RMS: {0}'.format(weighted_rms.value))
        return status

    def zernike_lsf(self):
        zernike_orders = ViPInt32(4)
        array_zernike_um = (ctypes.c_float*(self.MAX_ZERNIKE_MODES+1))()
        array_zernike_orders_um = (ctypes.c_float*(self.MAX_ZERNIKE_ORDERS+1))()
        roc_mm = ViPReal64(0)
        status = lib_wfs.WFS_ZernikeLsf(self.instrument_handle,
                                        ctypes.byref(zernike_orders),
                                        array_zernike_um,
                                        array_zernike_orders_um,
                                        ctypes.byref(roc_mm))

        logger_camera.info('Zernike Um:' + ''.join(['{:18}'.format(item) for item in array_zernike_um]))
        logger_camera.info('Zernike Orders Um:' + ''.join(['{:18}'.format(item) for item in array_zernike_orders_um]))
        logger_camera.info('Zernike Orders: {0}'.format(zernike_orders.value))
        logger_camera.info('RoC [mm]: {0}'.format(roc_mm.value))
        return status

    def calc_beam_centroid_diameter(self):
        beam_centroid_x_mm = ViPReal64()
        beam_centroid_y_mm = ViPReal64()
        beam_diameter_x_mm = ViPReal64()
        beam_diameter_y_mm = ViPReal64()
        status = lib_wfs.WFS_CalcBeamCentroidDia(self.instrument_handle,
                                                 ctypes.byref(beam_centroid_x_mm),
                                                 ctypes.byref(beam_centroid_y_mm),
                                                 ctypes.byref(beam_diameter_x_mm),
                                                 ctypes.byref(beam_diameter_y_mm))
        logger_camera.info('Beam Centroid X [mm]: {0}'.format(beam_centroid_x_mm.value))
        logger_camera.info('Beam Diameter X [mm]: {0}'.format(beam_diameter_y_mm.value))
        logger_camera.info('Beam Centroid Y [mm]: {0}'.format(beam_centroid_y_mm.value))
        logger_camera.info('Beam Diameter Y [mm]: {0}'.format(beam_diameter_x_mm.value))
        return status

    def get_spot_deviations(self):
        array_deviations_x = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        array_deviations_y = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        status = lib_wfs.WFS_GetSpotDeviations(self.instrument_handle,
                                               array_deviations_x,
                                               array_deviations_y)
        logger_camera.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in array_deviations_x]))
        logger_camera.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in array_deviations_y]))
        return status


if __name__ == '__main__':
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
    wfs.get_spotfield_image()
    wfs.calc_spots_centroid_diameter_intensity()
    wfs.get_spot_centroids()
    wfs.calc_beam_centroid_diameter()
    wfs.calc_spot_to_reference_deviations()
    wfs.get_spot_deviations()
    wfs.calc_wavefront()
    wfs.calc_wavefront_statistics()
    wfs.zernike_lsf()
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

    wfs.close()
