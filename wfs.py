# -*- coding: utf-8 -*-

"""
Wrapper for interfacing with the Thorlabs Wavefront Sensor (WFS)
"""

from __future__ import print_function

import ctypes
from ctypes.util import find_library
import logging
import logging.config
import os
import sys

import yaml


def setup_logging(path='logging.yaml', level=logging.INFO, env_key='LOG_CFG'):
    """
    Setup logging configuration
    uses logging.yaml for the default configuration
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

is_64bits = sys.maxsize > 2**32
if is_64bits:
    libname = 'WFS_64'
else:
    libname = 'WFS_32'
lib = find_library(libname)
if lib is None:
    if os.name == 'posix':
        logger_wfs.critical('No WFS_32/64 library exists')
        raise ImportError('No WFS_32/64 library exists')
    if os.name == 'nt' and is_64bits:
        logger_wfs.critical('WFS_64.dll not found')
        raise ImportError('WFS_64.dll not found')
    if os.name == 'nt' and not is_64bits:
        logger_wfs.critical('WFS_32.dll not found')
        raise ImportError('WFS_32.dll not found')
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
    """
    Create a ctypes char array of size n

    :param n: size of char array
    :rtype: ctypes char array
    """
    return ctypes.create_string_buffer(n)


class WFS(object):
    # Constants declared in WFS.h header file
    # Buffers
    WFS_BUFFER_SIZE = 256  # General buffer size
    WFS_ERR_DESCR_BUFFER_SIZE = 512  # Buffer size for error messages

    # Error/Warning Codes
    # max errors from camera driver
    MAX_CAM_DRIVER_ERRORS = 2000  # camera driver errors in range 1 .. MAX_CAM_DRIVER_ERRORS
    MAX_WFS_DEVICES = 5  # max 5 cams at the same time connected
    MAX_MLA_CALS = 7  # max. 7 MLA cals per device

    # Offsets
    _WFS_ERROR = (-2147483647L-1)  # 0x80000000
    WFS_INSTR_WARNING_OFFSET = 0x3FFC0900L
    WFS_INSTR_ERROR_OFFSET = _WFS_ERROR + 0x3FFC0900L  # 0xBFFC0900

    # WFS Driver Error Codes; error texts defined in WFS_ErrorMessage()
    WFS_SUCCESS = 0

    WFS_ERROR_PARAMETER1 = _WFS_ERROR+0x3FFC0001L
    WFS_ERROR_PARAMETER2 = _WFS_ERROR+0x3FFC0002L
    WFS_ERROR_PARAMETER3 = _WFS_ERROR+0x3FFC0003L
    WFS_ERROR_PARAMETER4 = _WFS_ERROR+0x3FFC0004L
    WFS_ERROR_PARAMETER5 = _WFS_ERROR+0x3FFC0005L
    WFS_ERROR_PARAMETER6 = _WFS_ERROR+0x3FFC0006L
    WFS_ERROR_PARAMETER7 = _WFS_ERROR+0x3FFC0007L
    WFS_ERROR_PARAMETER8 = _WFS_ERROR+0x3FFC0008L
    WFS_ERROR_PARAMETER9 = _WFS_ERROR+0x3FFC0009L

    WFS_ERROR_NO_SENSOR_CONNECTED = WFS_INSTR_ERROR_OFFSET + 0x00
    WFS_ERROR_OUT_OF_MEMORY = WFS_INSTR_ERROR_OFFSET + 0x01
    WFS_ERROR_INVALID_HANDLE = WFS_INSTR_ERROR_OFFSET + 0x02
    WFS_ERROR_CAM_NOT_CONFIGURED = WFS_INSTR_ERROR_OFFSET + 0x13
    WFS_ERROR_PIXEL_FORMAT = WFS_INSTR_ERROR_OFFSET + 0x04
    WFS_ERROR_EEPROM_CHECKSUM = WFS_INSTR_ERROR_OFFSET + 0x05
    WFS_ERROR_EEPROM_CAL_DATA = WFS_INSTR_ERROR_OFFSET + 0x06
    WFS_ERROR_OLD_REF_FILE = WFS_INSTR_ERROR_OFFSET + 0x07
    WFS_ERROR_NO_REF_FILE = WFS_INSTR_ERROR_OFFSET + 0x08
    WFS_ERROR_CORRUPT_REF_FILE = WFS_INSTR_ERROR_OFFSET + 0x09
    WFS_ERROR_WRITE_FILE = WFS_INSTR_ERROR_OFFSET + 0x0a
    WFS_ERROR_INSUFF_SPOTS_FOR_ZERNFIT = WFS_INSTR_ERROR_OFFSET + 0x0b
    WFS_ERROR_TOO_MANY_SPOTS_FOR_ZERNFIT = WFS_INSTR_ERROR_OFFSET + 0x0c
    WFS_ERROR_FOURIER_ORDER = WFS_INSTR_ERROR_OFFSET + 0x0d
    WFS_ERROR_NO_RECON_DEVIATIONS = WFS_INSTR_ERROR_OFFSET + 0x0e
    WFS_ERROR_NO_PUPIL_DEFINED = WFS_INSTR_ERROR_OFFSET + 0x0f
    WFS_ERROR_WRONG_PUPIL_DIA = WFS_INSTR_ERROR_OFFSET + 0x10
    WFS_ERROR_WRONG_PUPIL_CTR = WFS_INSTR_ERROR_OFFSET + 0x11
    WFS_ERROR_INVALID_CAL_DATA = WFS_INSTR_ERROR_OFFSET + 0x12
    WFS_ERROR_INTERNAL_REQUIRED = WFS_INSTR_ERROR_OFFSET + 0x13
    WFS_ERROR_ROC_RANGE = WFS_INSTR_ERROR_OFFSET + 0x14
    WFS_ERROR_NO_USER_REFERENCE = WFS_INSTR_ERROR_OFFSET + 0x15
    WFS_ERROR_AWAITING_TRIGGER = WFS_INSTR_ERROR_OFFSET + 0x16
    WFS_ERROR_NO_HIGHSPEED = WFS_INSTR_ERROR_OFFSET + 0x17
    WFS_ERROR_HIGHSPEED_ACTIVE = WFS_INSTR_ERROR_OFFSET + 0x18
    WFS_ERROR_HIGHSPEED_NOT_ACTIVE = WFS_INSTR_ERROR_OFFSET + 0x19
    WFS_ERROR_HIGHSPEED_WINDOW_MISMATCH = WFS_INSTR_ERROR_OFFSET + 0x1a
    WFS_ERROR_NOT_SUPPORTED = WFS_INSTR_ERROR_OFFSET + 0x1b

    # returned from non-exported functions
    WFS_ERROR_SPOT_TRUNCATED = WFS_INSTR_ERROR_OFFSET + 0x1b
    WFS_ERROR_NO_SPOT_DETECTED = WFS_INSTR_ERROR_OFFSET + 0x1c
    WFS_ERROR_TILT_CALCULATION = WFS_INSTR_ERROR_OFFSET + 0x1d

    # WFS Driver Warning Codes
    WFS_WARNING = WFS_INSTR_WARNING_OFFSET + 0x00

    WFS_WARN_NSUP_ID_QUERY = 0x3FFC0101L
    WFS_WARN_NSUP_RESET = 0x3FFC0102L
    WFS_WARN_NSUP_SELF_TEST = 0x3FFC0103L
    WFS_WARN_NSUP_ERROR_QUERY = 0x3FFC0104L
    WFS_WARN_NSUP_REV_QUERY = 0x3FFC0105L

    # Driver Status reporting (lower 24 bits)
    WFS_STATBIT_CON = 0x00000001  # USB connection lost, set by driver
    WFS_STATBIT_PTH = 0x00000002  # Power too high (cam saturated)
    WFS_STATBIT_PTL = 0x00000004  # Power too low (low cam digits)
    WFS_STATBIT_HAL = 0x00000008  # High ambient light
    WFS_STATBIT_SCL = 0x00000010  # Spot contrast too low
    WFS_STATBIT_ZFL = 0x00000020  # Zernike fit failed because of not enough detected spots
    WFS_STATBIT_ZFH = 0x00000040  # Zernike fit failed because of too much detected spots
    WFS_STATBIT_ATR = 0x00000080  # Camera is still awaiting a trigger
    WFS_STATBIT_CFG = 0x00000100  # Camera is configured, ready to use
    WFS_STATBIT_PUD = 0x00000200  # Pupil is defined
    WFS_STATBIT_SPC = 0x00000400  # No. of spots or pupil or aoi has been changed
    WFS_STATBIT_RDA = 0x00000800  # Reconstructed spot deviations available
    WFS_STATBIT_URF = 0x00001000  # User reference data available
    WFS_STATBIT_HSP = 0x00002000  # Camera is in Highspeed Mode
    WFS_STATBIT_MIS = 0x00004000  # Mismatched centroids in Highspeed Mode
    WFS_STATBIT_LOS = 0x00008000  # low number of detected spots, warning: reduced Zernike accuracy
    WFS_STATBIT_FIL = 0x00010000  # pupil is badly filled with spots, warning: reduced Zernike accuracy

    # Timeout
    # * 10 ms = 24 hours, given to is_SetTimeout, after that time is_IsVideoFinish returns 'finish' without error
    WFS_TRIG_TIMEOUT = 100*60*60*24
    WFS_TIMEOUT_CAPTURE_NORMAL = 1.0  # in seconds
    WFS_TIMEOUT_CAPTURE_TRIGGER = 0.1  # in seconds, allow fast return of functions WFS_TakeSpotfieldImage...
    WFS10_TIMEOUT_CAPTURE_NORMAL = 4000  # in ms, allow 500 ms exposure time + reserve
    WFS10_TIMEOUT_CAPTURE_TRIGGER = 100  # in ms, allow fast return of functions WFS_TakeSpotfieldImage...
    WFS20_TIMEOUT_CAPTURE_NORMAL = 4000  # in ms, allow 84 ms exposure time + reserve
    WFS20_TIMEOUT_CAPTURE_TRIGGER = 100  # in ms, allow fast return of functions WFS_TakeSpotfieldImage...

    # Exported constants
    WFS_TRUE = 1
    WFS_FALSE = 0

    # Defines for WFS camera
    MAX_FRAMERATE = 15  # not higher for wider exposure range

    EXPOSURE_MANUAL = 0
    EXPOSURE_AUTO = 1

    MASTER_GAIN_MIN_WFS = 1.0  # real gain factor, not 0..100% percent
    MASTER_GAIN_MIN_WFS10 = 1.5  # 1.0 prevents ADC from saturation on overexposure
    MASTER_GAIN_MIN_WFS20 = 1.0
    MASTER_GAIN_MAX_WFS20 = 1.0
    MASTER_GAIN_MAX = 13.66
    MASTER_GAIN_MAX_DISPLAY = 5.0  # dark signal is too noisy for higher amplification
    MASTER_GAIN_EXPONENT = 38.26  # based on natural logarithm

    NOISE_LEVEL_MIN = 0  # level for cutting spotfield
    NOISE_LEVEL_MAX = 255

    BLACK_LEVEL_MIN = 0
    BLACK_LEVEL_MAX = 255
    BLACK_LEVEL_WFS_DEF = 100  # lower values causes problems with auto-exposure and trigger (WFS)
    BLACK_LEVEL_WFS10_DEF = 100  # for cam shifted to 0 .. +15
    BLACK_LEVEL_WFS20_DEF = 0

    # Pixel format defines
    PIXEL_FORMAT_MONO8 = 0
    PIXEL_FORMAT_MONO16 = 1

    # pre-defined image sizes for WFS instruments
    CAM_RES_1280 = 0  # 1280x1024
    CAM_RES_1024 = 1  # 1024x1024
    CAM_RES_768 = 2  # 768x768
    CAM_RES_512 = 3  # 512x512
    CAM_RES_320 = 4  # 320x320 smallest!
    CAM_RES_MAX_IDX = 4

    # pre-defined image sizes for WFS10 instruments
    CAM_RES_WFS10_640 = 0  # 640x480
    CAM_RES_WFS10_480 = 1  # 480x480
    CAM_RES_WFS10_360 = 2  # 360x360
    CAM_RES_WFS10_260 = 3  # 260x260
    CAM_RES_WFS10_180 = 4  # 180x180 smallest!
    CAM_RES_WFS10_MAX_IDX = 4

    # pre-defined image sizes for WFS20 instruments
    CAM_RES_WFS20_1440 = 0  # 1440x1080
    CAM_RES_WFS20_1080 = 1  # 1080x1080
    CAM_RES_WFS20_768 = 2  # 768x768
    CAM_RES_WFS20_512 = 3  # 512x512
    CAM_RES_WFS20_360 = 4  # 360x360 smallest!
    CAM_RES_WFS20_720_BIN2 = 5  # 720x540, binning 2x2
    CAM_RES_WFS20_540_BIN2 = 6  # 540x540, binning 2x2
    CAM_RES_WFS20_384_BIN2 = 7  # 384x384, binning 2x2
    CAM_RES_WFS20_256_BIN2 = 8  # 256x256, binning 2x2
    CAM_RES_WFS20_180_BIN2 = 9  # 180x180, binning 2x2
    CAM_RES_WFS20_MAX_IDX = 9

    # Hardware trigger modes
    WFS_HW_TRIGGER_OFF = 0
    WFS_HW_TRIGGER_HL = 1
    WFS_HW_TRIGGER_LH = 2
    WFS_TRIGGER_MODE_MIN = WFS_HW_TRIGGER_OFF
    WFS_TRIGGER_MODE_MAX = WFS_HW_TRIGGER_LH

    # Averaging
    AVERAGE_COUNT_MAX = 256

    # Pupil
    PUPIL_DIA_MIN_MM = 0.1  # for coarse check only
    PUPIL_DIA_MAX_MM = 10.0
    PUPIL_CTR_MIN_MM = -5.0
    PUPIL_CTR_MAX_MM = 5.0

    # Wavefront types
    WAVEFRONT_MEAS = 0
    WAVEFRONT_REC = 1
    WAVEFRONT_DIFF = 2

    # Max number of detectable spots
    MAX_SPOTS_X = 50  # WFS20: 1440*5/150 = 48
    MAX_SPOTS_Y = 40  # WFS20: 1080*5/150 = 36
    # MAX_SPOTS_X = 41  # max for 1280x1024 with 4.65µm pixels and 150µm lenslet pitch (WFSx)
    #                   # also for 640x480 with 9.9µm pixels and 150µm lenslet pitch (WFS10x)
    # MAX_SPOTS_Y = 33  # determines also 3D display size

    # Reference
    WFS_REF_INTERNAL = 0
    WFS_REF_USER = 1

    # Spots ref types
    WFS_REF_TYPE_REL = 0
    WFS_REF_TYPE_ABS = 1

    # Spherical reference
    ROC_CAL_MIN_MM = 100.0
    ROC_CAL_MAX_MM = 5000.0

    # Zernike polynomials
    MIN_NUMDOTS_FIT = 5
    MAX_NUMDOTS_FIT = MAX_SPOTS_X * MAX_SPOTS_Y  # max number of spots used for Zernike fit
    MAX_NUM_ROWS_B = 2 * MAX_NUMDOTS_FIT + 1  # max number of rows in Matrix containing x and y deviations and a piston

    ZERNIKE_ORDERS_AUTO = 0
    MIN_ZERNIKE_ORDERS = 2
    MAX_ZERNIKE_ORDERS = 10
    MIN_ZERNIKE_MODES = 6  # min number of modes in Zernike fit
    MAX_ZERNIKE_MODES = 66  # max number of modes in Zernike fit
    ZERNIKE_WARNING_LEVEL = 1.3  # 30% more spots than desired Zernike modes should be detected for good accuracy

    # for conversion pixel - mm
    NOT_CENTERED = 0
    CENTERED = 1

    def __init__(self):
        self.instrument_handle = 0
        self.resource_name = ViRsrc('')  # resource_name='USB::0x1313::0x0000::1'
        self.id_query = ViBoolean(0)
        self.reset_device = ViBoolean(0)
        self.instrument_handle = ViSession(0)

    # # Vi Types
    # # class ViSession(ctypes.c_ulong):
    # #     pass  # long unsigned int
    # def vi_session(self, n):
    #     return ctypes.c_ulong(n)
    #
    # # class ViBoolean(ctypes.c_ushort):
    # #     pass  # short unsigned int
    # def vi_boolean(self, n):
    #     return ctypes.c_ushort(n)
    #
    # # class ViRsrc(ctypes.c_char_p):
    # #     pass  # char*
    # def vi_rsrc(self, n):
    #     return ctypes.c_char_p(n)
    #
    # # class ViReal64(ctypes.c_double):
    # #     pass  # double
    # #     pass  # char*
    # def vi_real_64(self, n):
    #     return ctypes.c_double(n)
    #
    # # class ViPReal64(ctypes.c_double):
    # #     pass  # double Pointer
    # def vi_p_real_64(self, n):
    #     return ctypes.c_double(n)
    #
    # # class ViStatus(ctypes.c_long):
    # #     pass  # long int
    # def vi_status(self, n):
    #     return ctypes.c_long(n)
    #
    # # class ViUInt8(ctypes.c_ubyte):
    # #     pass  # !Binary8 unsigned char
    # def vi_u_int_8(self, n):
    #     return ctypes.c_ubyte(n)
    #
    # # class ViAUInt8(ctypes.c_ubyte):
    # #     pass  # !Binary8 unsigned char
    # def vi_au_int_8(self, n):
    #     return ctypes.c_ubyte(n)
    #
    # # class ViInt16(ctypes.c_int):
    # #     pass  # Binary16 short int
    # def vi_int_16(self, n):
    #     return ctypes.c_int(n)
    #
    # # class ViInt32(ctypes.c_long):
    # #     pass  # Binary32 long int
    # def vi_int_32(self, n):
    #     return ctypes.c_long(n)
    #
    # # class ViPInt32(ctypes.c_long):
    # #     pass  # Binary32 long int Pointer
    # def vi_p_int_32(self, n):
    #     return ctypes.c_long(n)
    #
    # def ViAChar(n):
    #     """Create a ctypes char array of size n
    #     :param n: size of char array
    #     :rtype : ctypes char array
    #     """
    #     return ctypes.create_string_buffer(n)

    # WFS Functions
    def _init(self, **kwargs):
        """
        WFS_init

        ViStatus WFS_init (ViRsrc resourceName, ViBoolean IDQuery, ViBoolean resetDevice, ViPSession instrumentHandle);

        Purpose
        This function initializes the instrument driver session and performs the
        following initialization actions:

        (1) Opens a session to the Default Resource Manager resource and a
        session to the selected device using the Resource Name.
        (2) Performs an identification query on the Instrument.
        (3) Resets the instrument to a known state.
        (4) Sends initialization commands to the instrument.
        (5) Returns an instrument handle which is used to differentiate between
        different sessions of this instrument driver.

        Notes:
        (1) Each time this function is invoked an unique session is opened.

        Parameter List

        resourceName

            Variable Type       ViRsrc

            This parameter specifies the interface of the device that is to be
            initialized.The resource name has to follow the syntax:

            "USB::0x1313::0x0000::" followed by the Device ID.

            The Device ID can be get with the function
            "WFS_GetInstrumentListInfo". E.g. "USB::0x1313::0x0000::1"

        IDQuery

            Variable Type       ViBoolean

            Performs an In-System Verification.
            Checks if the resource matches the vendor and product id.

        resetDevice

            Variable Type       ViBoolean

            Performs Reset operation and places the instrument in a pre-defined
            reset state.

        instrumentHandle

            Variable Type       ViSession (passed by reference)

            This parameter returns an instrument handle that is used in all
            subsequent calls to distinguish between different sessions of this
            instrument driver.

        Return Value

            Operational return status. Contains either a completion code or an
            error code. Instrument driver specific codes that may be returned in
            addition to the VISA error codes defined in VPP-4.3 and vendor
            specific codes, are as follows.

            Completion Codes
            ----------------------------------------------------------------
            VI_SUCCESS              Initialization successful
            VI_WARN_NSUP_ID_QUERY   Identification query not supported
            VI_WARN_NSUP_RESET      Reset not supported

            Error Codes
            ----------------------------------------------------------------
            VI_ERROR_FAIL_ID_QUERY  Instrument identification query failed

            Vendor Specific Codes
            ----------------------------------------------------------------
            For error codes and descriptions see <Error Message>.

        Keyword arguments
        :param resource_name:
        :param id_query:
        :param reset_device:
        :param instrument_handle:
        :return vi_status:
        """
        if 'resource_name' in kwargs:
            self.resource_name = ViRsrc(kwargs['resource_name'])
        if 'id_query' in kwargs:
            self.resource_name = ViBoolean(kwargs['id_query'])
        if 'reset_device' in kwargs:
            self.resource_name = ViBoolean(kwargs['reset_device'])
        if 'instrument_handle' in kwargs:
            self.resource_name = ViSession(kwargs['instrument_handle'])

        vi_status = lib_wfs.WFS_init(self.resource_name,
                                     self.id_query,
                                     self.reset_device,
                                     ctypes.byref(self.instrument_handle))
        logger_camera.info('Instrument Handle: {0}'.format(self.instrument_handle.value))
        return vi_status

    def _close(self):
        vi_status = lib_wfs.WFS_close(self.instrument_handle)
        return vi_status

    # Configuration Functions
    def _get_instrument_info(self):
        manufacturer_name = ViAChar(256)
        instrument_name_wfs = ViAChar(256)
        serial_number_wfs = ViAChar(256)
        serial_number_camera = ViAChar(256)
        vi_status = lib_wfs.WFS_GetInstrumentInfo(self.instrument_handle,
                                                  manufacturer_name,
                                                  instrument_name_wfs,
                                                  serial_number_wfs,
                                                  serial_number_camera)
        logger_camera.info('Manufacturer Name: {0}'.format(manufacturer_name.value))
        logger_camera.info('Instrument Name WFS: {0}'.format(instrument_name_wfs.value))
        logger_camera.info('Serial Number WFS: {0}'.format(serial_number_wfs.value))
        logger_camera.info('Serial Number Camera: {0}'.format(serial_number_camera.value))
        return vi_status

    def _configure_cam(self):
        pixel_format = ViInt32(0)
        cam_resolution_index = ViInt32(0)
        self.spotsX = ViPInt32()
        self.spotsY = ViPInt32()
        vi_status = lib_wfs.WFS_ConfigureCam(self.instrument_handle,
                                             pixel_format,
                                             cam_resolution_index,
                                             ctypes.byref(self.spotsX),
                                             ctypes.byref(self.spotsY))
        logger_camera.info('Spots X: {0}'.format(self.spotsX.value))
        logger_camera.info('Spots Y: {0}'.format(self.spotsY.value))
        return vi_status

    def _set_highspeed_mode(self):
        pass

    def _get_highspeed_windows(self):
        pass

    def _check_highspeed_centroids(self):
        pass

    def _get_exposure_time_range(self):
        pass

    def _set_exposure_time(self):
        pass

    def _get_exposure_time(self):
        pass

    def _get_master_gain_range(self):
        pass

    def _set_master_gain_time(self):
        pass

    def _get_master_gain_time(self):
        pass

    def _set_black_level_offset(self):
        pass

    def _get_black_level_offset(self):
        pass

    def _set_trigger_mode(self):
        pass

    def _get_trigger_mode(self):
        pass

    def _set_trigger_delay(self):
        pass

    def _get_trigger_delay_range(self):
        pass

    def _get_mla_count(self):
        mla_count = ViPInt32()
        vi_status = lib_wfs.WFS_GetMlaCount(self.instrument_handle,
                                            ctypes.byref(mla_count))
        logger_camera.info('Micro Lens Array: {0}'.format(mla_count.value))
        self.mla_index = ViInt32(mla_count.value - 1)
        return vi_status

    def _get_mla_data(self):
        mla_name = ViAChar(256)
        cam_pitch_um = ViPReal64()
        lenslet_pitch_um = ViPReal64()
        spot_offset_x = ViPReal64()
        spot_offset_y = ViPReal64()
        lenslet_focal_length_um = ViPReal64()
        grid_correction_0 = ViPReal64()
        grid_correction_45 = ViPReal64()
        vi_status = lib_wfs.WFS_GetMlaData(self.instrument_handle,
                                           self.mla_index,
                                           mla_name,
                                           ctypes.byref(cam_pitch_um),
                                           ctypes.byref(lenslet_pitch_um),
                                           ctypes.byref(spot_offset_x),
                                           ctypes.byref(spot_offset_y),
                                           ctypes.byref(lenslet_focal_length_um),
                                           ctypes.byref(grid_correction_0),
                                           ctypes.byref(grid_correction_45))

        logger_camera.info('MLA Name: {0}'.format(mla_name.value))
        logger_camera.info('MLA cam_pitch_um: {0}'.format(cam_pitch_um.value))
        logger_camera.info('MLA lenslet_pitch_um: {0}'.format(lenslet_pitch_um.value))
        logger_camera.info('MLA spot_offset_x: {0}'.format(spot_offset_x.value))
        logger_camera.info('MLA spot_offset_y: {0}'.format(spot_offset_y.value))
        logger_camera.info('MLA lenslet_focal_length_um: {0}'.format(lenslet_focal_length_um.value))
        logger_camera.info('MLA grid_correction_0: {0}'.format(grid_correction_0.value))
        logger_camera.info('MLA grid_correction_45: {0}'.format(grid_correction_45.value))
        return vi_status

    def _get_mla_data2(self):
        mla_name = ViAChar(256)
        cam_pitch_um = ViPReal64()
        lenslet_pitch_um = ViPReal64()
        spot_offset_x = ViPReal64()
        spot_offset_y = ViPReal64()
        lenslet_focal_length_um = ViPReal64()
        grid_correction_0 = ViPReal64()
        grid_correction_45 = ViPReal64()
        grid_correction_rotation = ViPReal64()
        grid_correction_pitch = ViPReal64()
        vi_status = lib_wfs.WFS_GetMlaData2(self.instrument_handle,
                                            self.mla_index,
                                            mla_name,
                                            ctypes.byref(cam_pitch_um),
                                            ctypes.byref(lenslet_pitch_um),
                                            ctypes.byref(spot_offset_x),
                                            ctypes.byref(spot_offset_y),
                                            ctypes.byref(lenslet_focal_length_um),
                                            ctypes.byref(grid_correction_0),
                                            ctypes.byref(grid_correction_45),
                                            ctypes.byref(grid_correction_rotation),
                                            ctypes.byref(grid_correction_pitch))

        logger_camera.info('MLA Name: {0}'.format(mla_name.value))
        logger_camera.info('MLA cam_pitch_um: {0}'.format(cam_pitch_um.value))
        logger_camera.info('MLA lenslet_pitch_um: {0}'.format(lenslet_pitch_um.value))
        logger_camera.info('MLA spot_offset_x: {0}'.format(spot_offset_x.value))
        logger_camera.info('MLA spot_offset_y: {0}'.format(spot_offset_y.value))
        logger_camera.info('MLA lenslet_focal_length_um: {0}'.format(lenslet_focal_length_um.value))
        logger_camera.info('MLA grid_correction_0: {0}'.format(grid_correction_0.value))
        logger_camera.info('MLA grid_correction_45: {0}'.format(grid_correction_45.value))
        logger_camera.info('MLA grid_correction_rotation: {0}'.format(grid_correction_rotation.value))
        logger_camera.info('MLA grid_correction_pitch: {0}'.format(grid_correction_pitch.value))
        return vi_status

    def _select_mla(self):
        vi_status = lib_wfs.WFS_SelectMla(self.instrument_handle, self.mla_index)
        if vi_status == 0:
            logger_camera.info('MLA selection: {0}'.format(self.mla_index.value))
            pass
        return vi_status

    def _set_aoi(self):
        pass

    def _get_aoi(self):
        pass

    def _set_pupil(self, pupil_center_x_mm=0, pupil_center_y_mm=0, pupil_diameter_x_mm=4.76, pupil_diameter_y_mm=4.76):
        self.pupil_center_x_mm = ViReal64(pupil_center_x_mm)
        self.pupil_center_y_mm = ViReal64(pupil_center_y_mm)
        self.pupil_diameter_x_mm = ViReal64(pupil_diameter_x_mm)
        self.pupil_diameter_y_mm = ViReal64(pupil_diameter_y_mm)
        vi_status = lib_wfs.WFS_SetPupil(self.instrument_handle,
                                         self.pupil_center_x_mm,
                                         self.pupil_center_y_mm,
                                         self.pupil_diameter_x_mm,
                                         self.pupil_diameter_y_mm)
        logger_camera.info('Set Pupil Centroid X [mm]: {0}'.format(self.pupil_center_x_mm.value))
        logger_camera.info('Set Pupil Centroid Y [mm]: {0}'.format(self.pupil_center_y_mm.value))
        logger_camera.info('Set Pupil Diameter X [mm]: {0}'.format(self.pupil_diameter_x_mm.value))
        logger_camera.info('Set Pupil Diameter Y [mm]: {0}'.format(self.pupil_diameter_y_mm.value))
        return vi_status

    def _get_pupil(self):
        vi_status = lib_wfs.WFS_GetPupil(self.instrument_handle,
                                         ctypes.byref(self.pupil_center_x_mm),
                                         ctypes.byref(self.pupil_center_y_mm),
                                         ctypes.byref(self.pupil_diameter_x_mm),
                                         ctypes.byref(self.pupil_diameter_y_mm))
        logger_camera.info('Get Pupil Centroid X [mm]: {0}'.format(self.pupil_center_x_mm.value))
        logger_camera.info('Get Pupil Centroid Y [mm]: {0}'.format(self.pupil_center_y_mm.value))
        logger_camera.info('Get Pupil Diameter X [mm]: {0}'.format(self.pupil_diameter_x_mm.value))
        logger_camera.info('Get Pupil Diameter Y [mm]: {0}'.format(self.pupil_diameter_y_mm.value))
        return vi_status

    def _set_reference_place(self, reference_index=0):
        self.reference_index = ViInt32(reference_index)
        vi_status = lib_wfs.WFS_SetReferencePlane(self.instrument_handle,
                                                  self.reference_index)
        logger_camera.info('Set Reference Index: {0}'.format(self.reference_index.value))
        return vi_status

    def _get_reference_plane(self):
        vi_status = lib_wfs.WFS_GetReferencePlane(self.instrument_handle,
                                                  ctypes.byref(self.reference_index))
        logger_camera.info('Get Reference Index: {0}'.format(self.reference_index.value))
        return vi_status

    # Action/Status Functions
    def _get_status(self):
        device_status = ViInt32()
        vi_status = lib_wfs.WFS_GetStatus(self.instrument_handle,
                                          ctypes.byref(device_status))
        logger_camera.info('Device Status: {0}'.format(device_status.value))
        return vi_status

    # Data Functions
    def _take_spotfield_image(self):
        vi_status = lib_wfs.WFS_TakeSpotfieldImage(self.instrument_handle)
        return vi_status

    def _take_spotfield_image_auto_exposure(self):
        exposure_time_act = ViPReal64()
        master_gain_act = ViPReal64()
        vi_status = lib_wfs.WFS_TakeSpotfieldImageAutoExpos(self.instrument_handle,
                                                            ctypes.byref(exposure_time_act),
                                                            ctypes.byref(master_gain_act))
        logger_camera.info('Exposure Time Act: {0}'.format(exposure_time_act.value))
        logger_camera.info('Master Gain Act: {0}'.format(master_gain_act.value))
        return vi_status

    def _get_spotfield_image(self):
        image_buffer = ctypes.c_uint()
        rows = ViInt32()
        columns = ViInt32()
        vi_status = lib_wfs.WFS_GetSpotfieldImage(self.instrument_handle,
                                                  ctypes.byref(image_buffer),
                                                  ctypes.byref(rows),
                                                  ctypes.byref(columns))
        logger_camera.info('Image Buffer: {0}'.format(image_buffer.value))
        logger_camera.info('Rows: {0}'.format(rows.value))
        logger_camera.info('Columns: {0}'.format(columns.value))
        return vi_status

    def _get_spotfield_image_copy(self):
        # image_buffer = (ctypes.c_uint)()
        # rows = ViInt32()
        # columns = ViInt32()
        # vi_status = lib_wfs.WFS_GetSpotfieldImage(self.instrument_handle,
        #                                           ctypes.byref(image_buffer),
        #                                           ctypes.byref(rows),
        #                                           ctypes.byref(columns))
        # logger_camera.info('Image Buffer: {0}'.format(image_buffer.value))
        # logger_camera.info('Rows: {0}'.format(rows.value))
        # logger_camera.info('Columns: {0}'.format(columns.value))
        # return vi_status
        pass

    def _average_image(self):
        pass

    def _average_image_rolling(self):
        pass

    def _cut_image_noise_floor(self):
        pass

    def _calc_image_min_max(self):
        pass

    def _calc_mean_rms_noise(self):
        pass

    def _get_line(self):
        pass

    def _get_line_view(self):
        pass

    def _calc_beam_centroid_diameter(self):
        beam_centroid_x_mm = ViPReal64()
        beam_centroid_y_mm = ViPReal64()
        beam_diameter_x_mm = ViPReal64()
        beam_diameter_y_mm = ViPReal64()
        vi_status = lib_wfs.WFS_CalcBeamCentroidDia(self.instrument_handle,
                                                    ctypes.byref(beam_centroid_x_mm),
                                                    ctypes.byref(beam_centroid_y_mm),
                                                    ctypes.byref(beam_diameter_x_mm),
                                                    ctypes.byref(beam_diameter_y_mm))
        logger_camera.info('Beam Centroid X [mm]: {0}'.format(beam_centroid_x_mm.value))
        logger_camera.info('Beam Diameter X [mm]: {0}'.format(beam_diameter_y_mm.value))
        logger_camera.info('Beam Centroid Y [mm]: {0}'.format(beam_centroid_y_mm.value))
        logger_camera.info('Beam Diameter Y [mm]: {0}'.format(beam_diameter_x_mm.value))
        return vi_status

    def _calc_spots_centroid_diameter_intensity(self):
        dynamic_noise_cut = ViInt32(1)
        calculate_diameters = ViInt32(0)
        vi_status = lib_wfs.WFS_CalcSpotsCentrDiaIntens(self.instrument_handle,
                                                        dynamic_noise_cut,
                                                        calculate_diameters)
        return vi_status

    def _get_spot_centroids(self):
        array_centroid_x = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        array_centroid_y = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        vi_status = lib_wfs.WFS_GetSpotCentroids(self.instrument_handle,
                                                 array_centroid_x,
                                                 array_centroid_y)
        logger_camera.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in array_centroid_x]))
        logger_camera.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in array_centroid_y]))
        return vi_status

    def _get_spot_diameters(self):
        pass

    def _get_spot_diameters_statistics(self):
        pass

    def _get_spot_intensities(self):
        pass

    def _calc_spot_to_reference_deviations(self):
        cancel_wavefront_tilt = ViInt32(1)
        vi_status = lib_wfs.WFS_CalcSpotToReferenceDeviations(self.instrument_handle,
                                                              cancel_wavefront_tilt)
        return vi_status

    def _get_spot_reference_positions(self):
        pass

    def _get_spot_deviations(self):
        array_deviations_x = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        array_deviations_y = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        vi_status = lib_wfs.WFS_GetSpotDeviations(self.instrument_handle,
                                                  array_deviations_x,
                                                  array_deviations_y)
        logger_camera.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in array_deviations_x]))
        logger_camera.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in array_deviations_y]))
        return vi_status

    def _zernike_lsf(self):
        zernike_orders = ViPInt32(4)
        array_zernike_um = (ctypes.c_float*(self.MAX_ZERNIKE_MODES+1))()
        array_zernike_orders_um = (ctypes.c_float*(self.MAX_ZERNIKE_ORDERS+1))()
        roc_mm = ViPReal64(0)
        vi_status = lib_wfs.WFS_ZernikeLsf(self.instrument_handle,
                                           ctypes.byref(zernike_orders),
                                           array_zernike_um,
                                           array_zernike_orders_um,
                                           ctypes.byref(roc_mm))
        logger_camera.info('Zernike Um:' + ''.join(['{:18}'.format(item) for item in array_zernike_um]))
        logger_camera.info('Zernike Orders Um:' + ''.join(['{:18}'.format(item) for item in array_zernike_orders_um]))
        logger_camera.info('Zernike Orders: {0}'.format(zernike_orders.value))
        logger_camera.info('RoC [mm]: {0}'.format(roc_mm.value))
        return vi_status

    def _calc_fourier_optometric(self):
        pass

    def _calc_reconstructed_deviations(self):
        pass

    def _calc_wavefront(self):
        array_wavefront = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        wavefront_type = ViInt32(0)
        limit_to_pupil = ViInt32(0)
        vi_status = lib_wfs.WFS_CalcWavefront(self.instrument_handle,
                                              wavefront_type,
                                              limit_to_pupil,
                                              array_wavefront)
        logger_camera.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in array_wavefront]))
        return vi_status

    def _calc_wavefront_statistics(self):
        min_ = ViPReal64(0)
        max_ = ViPReal64(0)
        diff = ViPReal64(0)
        mean = ViPReal64(0)
        rms = ViPReal64(0)
        weighted_rms = ViPReal64(0)
        vi_status = lib_wfs.WFS_CalcWavefrontStatistics(self.instrument_handle,
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
        return vi_status

    # Utility Functions
    def _self_test(self):
        # selfTestResult = ViInt16()
        # selfTestMessage = ViAChar(256)
        # vi_status = lib_wfs.WFS_self_test(self.instrumentHandle,
        #                                   ctypes.byref(selfTestResult),
        #                                   selfTestMessage)
        # logger.info('Self Test Result: {0}'.format(selfTestResult.value))
        # logger.info('Self Test Message: {0}'.format(selfTestMessage.value))
        # return vi_status
        pass

    def _reset(self):
        vi_status = lib_wfs.WFS_reset(self.instrument_handle)
        return vi_status

    def _revision_query(self,
                        instrument_handle=0,
                        instrument_driver_revision=256,
                        firmware_revision=256):
        self.instrument_handle = ViSession(instrument_handle)
        self.instrumentDriverRevision = ViAChar(instrument_driver_revision)
        self.firmwareRevision = ViAChar(firmware_revision)
        vi_status = lib_wfs.WFS_revision_query(self.instrument_handle,
                                               self.instrumentDriverRevision,
                                               self.firmwareRevision)
        logger_camera.info('Instrument Driver Version: {0}'.format(self.instrumentDriverRevision.value))
        logger_camera.info('Instrument Firmware Version: {0}'.format(self.firmwareRevision.value))
        return vi_status

    def _error_query(self):
        error_code = ViInt32()
        error_message = ViAChar(256)
        vi_status = lib_wfs.WFS_error_query(self.instrument_handle,
                                            ctypes.byref(error_code),
                                            error_message)
        return vi_status

    def _error_message(self):
        error_code = ViStatus()
        error_message = ViAChar(256)
        vi_status = lib_wfs.WFS_error_message(self.instrument_handle,
                                              error_code,
                                              error_message)
        return vi_status

    def _get_instrument_list_len(self, instrument_handle=0, instrument_count=0):
        self.instrument_handle = ViSession(instrument_handle)
        instrument_count = ViInt32(instrument_count)
        vi_status = lib_wfs.WFS_GetInstrumentListLen(self.instrument_handle,
                                                     ctypes.byref(instrument_count))
        self.instrument_index = ViInt32(instrument_count.value - 1)
        logger_camera.info('Instrument Index: {0}'.format(self.instrument_index.value))
        return vi_status

    def _get_instrument_list_info(self,
                                  handle=ViSession(0),
                                  device_id=0,
                                  in_use=0,
                                  instrument_name=256,
                                  serial_number_wfs=256,
                                  resource_name=256):
        self.device_id = ViInt32(device_id)
        self.in_use = ViInt32(in_use)
        self.instrument_name = ViAChar(instrument_name)
        self.serial_number_wfs = ViAChar(serial_number_wfs)
        self.resource_name = ViAChar(resource_name)
        vi_status = lib_wfs.WFS_GetInstrumentListInfo(handle,
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
        return vi_status

    def _get_xy_scale(self):
        pass

    def _convert_wavefront_waves(self):
        pass

    def _flip_2d_array(self):
        pass

    # Calibration Functions
    def _set_spots_to_user_reference(self):
        pass

    def _set_calc_spots_to_user_reference(self):
        pass

    def _create_default_user_reference(self):
        pass

    def _save_user_reference_file(self):
        pass

    def _load_user_reference_file(self):
        pass

    def _do_spherical_reference(self):
        pass

    def test(self):
        pass


if __name__ == '__main__':
    wfs = WFS()
