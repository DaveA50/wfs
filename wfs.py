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

__version__ = '0.1.1'
PY2 = sys.version_info[0] == 2


def setup_logging(path='logging.yaml', level=logging.INFO, env_key='LOG_CFG'):
    """
    Setup logging configuration
    uses logging.yaml for the default configuration

    Args:
        env_key:
        level:
        path:
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
log_wfs = logging.getLogger('WFS')
log_ui = logging.getLogger('UI')

is_64bits = sys.maxsize > 2 ** 32
if is_64bits:
    libname = 'WFS_64'
else:
    libname = 'WFS_32'
lib = find_library(libname)
if lib is None:
    if os.name == 'posix':
        log_wfs.critical('No WFS_32/64 library exists')
        raise ImportError('No WFS_32/64 library exists')
    if os.name == 'nt' and is_64bits:
        log_wfs.critical('WFS_64.dll not found')
        raise ImportError('WFS_64.dll not found')
    if os.name == 'nt' and not is_64bits:
        log_wfs.critical('WFS_32.dll not found')
        raise ImportError('WFS_32.dll not found')
if os.name == 'nt':
    lib_wfs = ctypes.windll.LoadLibrary(lib)
    log_wfs.debug('WFS_32.dll loaded')


class Vi:
    true = 1
    false = 0
    null = 0
    success = 0

    def __init__(self):
        pass

    @staticmethod
    def char(n):
        """
        Create a ctypes char array of size n

        Args:
            n: size of char array
        """
        return ctypes.create_string_buffer(n)

    @staticmethod
    def int8(n):
        """
        Args:
            n: Binary8 char
        """
        return ctypes.c_byte(n)

    @staticmethod
    def uint8(n):
        """
        Args:
            n: Binary8 unsigned char
        """
        return ctypes.c_ubyte(n)

    @staticmethod
    def int16(n):
        """
        Args:
            n: Binary16 short int
        """
        return ctypes.c_short(n)

    @staticmethod
    def uint16(n):
        """
        Args:
            n: Binary16 unsigned short int
        """
        return ctypes.c_ushort(n)

    @staticmethod
    def int32(n):
        """
        Args:
            n: Binary32 long int
        """
        return ctypes.c_long(n)

    @staticmethod
    def uint32(n):
        """
        Args:
            n: Binary32 long int
        """
        return ctypes.c_ulong(n)

    @staticmethod
    def real32(n):
        """
        Args:
            n: float, char*
        """
        return ctypes.c_float(n)

    @staticmethod
    def real64(n):
        """
        Args:
            n: double, char*
        """
        return ctypes.c_double(n)

    @staticmethod
    def boolean(n):
        if n is True:
            n = Vi.true
        elif n is False:
            n = Vi.false
        return Vi.uint16(n)

    @staticmethod
    def object(n):
        return Vi.uint32(n)

    @staticmethod
    def rsrc(s):
        return Vi.string(s)

    @staticmethod
    def session(n):
        return Vi.object(n)

    @staticmethod
    def status(n):
        return Vi.int32(n)

    @staticmethod
    def string(s):
        # return Vi.char(s)    :
        return ctypes.c_char_p(s)

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
    WFS_ERROR = (-2147483647 - 1)  # 0x80000000
    WFS_INSTR_WARNING_OFFSET = 0x3FFC0900
    WFS_INSTR_ERROR_OFFSET = WFS_ERROR + 0x3FFC0900  # 0xBFFC0900

    # WFS Driver Error Codes; error texts defined in WFS_ErrorMessage()
    WFS_SUCCESS = 0

    WFS_ERROR_PARAMETER1 = WFS_ERROR + 0x3FFC0001
    WFS_ERROR_PARAMETER2 = WFS_ERROR + 0x3FFC0002
    WFS_ERROR_PARAMETER3 = WFS_ERROR + 0x3FFC0003
    WFS_ERROR_PARAMETER4 = WFS_ERROR + 0x3FFC0004
    WFS_ERROR_PARAMETER5 = WFS_ERROR + 0x3FFC0005
    WFS_ERROR_PARAMETER6 = WFS_ERROR + 0x3FFC0006
    WFS_ERROR_PARAMETER7 = WFS_ERROR + 0x3FFC0007
    WFS_ERROR_PARAMETER8 = WFS_ERROR + 0x3FFC0008
    # WFS_ERROR_PARAMETER9 = WFS_ERROR + 0x3FFC0009

    WFS_ERROR_NO_SENSOR_CONNECTED = WFS_INSTR_ERROR_OFFSET + 0x00
    WFS_ERROR_OUT_OF_MEMORY = WFS_INSTR_ERROR_OFFSET + 0x01
    WFS_ERROR_INVALID_HANDLE = WFS_INSTR_ERROR_OFFSET + 0x02
    WFS_ERROR_CAM_NOT_CONFIGURED = WFS_INSTR_ERROR_OFFSET + 0x03
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
    WFS_WARN_NSUP_ID_QUERY = 0x3FFC0101
    WFS_WARN_NSUP_RESET = 0x3FFC0102
    WFS_WARN_NSUP_SELF_TEST = 0x3FFC0103
    WFS_WARN_NSUP_ERROR_QUERY = 0x3FFC0104
    WFS_WARN_NSUP_REV_QUERY = 0x3FFC0105

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
    WFS_DRIVER_STATUS = {WFS_STATBIT_CON: 'USB connection lost, set by driver',
                         WFS_STATBIT_PTH: 'Power too high (cam saturated)',
                         WFS_STATBIT_PTL: 'Power too low (low cam digits)',
                         WFS_STATBIT_HAL: 'High ambient light',
                         WFS_STATBIT_SCL: 'Spot contrast too low',
                         WFS_STATBIT_ZFL: 'Zernike fit failed because of not enough detected spots',
                         WFS_STATBIT_ZFH: 'Zernike fit failed because of too many detected spots',
                         WFS_STATBIT_ATR: 'Camera is still awaiting a trigger',
                         WFS_STATBIT_CFG: 'Camera is configured, ready to use',
                         WFS_STATBIT_PUD: 'Pupil is defined',
                         WFS_STATBIT_SPC: 'Number of spots or pupil or aoi has been changed',
                         WFS_STATBIT_RDA: 'Reconstructed spot deviations available',
                         WFS_STATBIT_URF: 'User reference data available',
                         WFS_STATBIT_HSP: 'Camera is in Highspeed Mode',
                         WFS_STATBIT_MIS: 'Mismatched centroids in Highspeed Mode',
                         WFS_STATBIT_LOS: 'Low number of detected spots, warning: reduced Zernike accuracy',
                         WFS_STATBIT_FIL: 'Pupil is badly filled with spots, warning: reduced Zernike accuracy'}

    # Timeout
    # * 10 ms = 24 hours, given to is_SetTimeout, after that time is_IsVideoFinish returns 'finish' without error
    WFS_TRIG_TIMEOUT = 100 * 60 * 60 * 24
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
    # MAX_SPOTS_X = 50  # WFS20: 1440*5/150 = 48
    # MAX_SPOTS_Y = 40  # WFS20: 1080*5/150 = 36
    MAX_SPOTS_X = 41  # max for 1280x1024 with 4.65µm pixels and 150µm lenslet pitch (WFSx)
                      # also for 640x480 with 9.9µm pixels and 150µm lenslet pitch (WFS10x)
    MAX_SPOTS_Y = 33  # determines also 3D display size

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
        self.adapt_centroids = Vi.int32(0)
        self.allow_auto_exposure = Vi.int32(0)
        self.array_centroid_x = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        self.array_centroid_y = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        self.array_deviations_x = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        self.array_deviations_y = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        self.array_diameter_x = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        self.array_diameter_y = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        self.array_intensity = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        self.array_reference_x = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        self.array_reference_y = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        self.array_scale_x = (ctypes.c_float * self.MAX_SPOTS_X)()
        self.array_scale_y = (ctypes.c_float * self.MAX_SPOTS_Y)()
        self.array_wavefront = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        self.array_wavefront_waves = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        self.array_wavefront_xy = ((ctypes.c_float * self.MAX_SPOTS_Y) * self.MAX_SPOTS_X)()
        self.array_wavefront_yx = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        self.array_zernike_orders_um = (ctypes.c_float * (self.MAX_ZERNIKE_ORDERS + 1))()
        self.array_zernike_reconstructed = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
        self.array_zernike_um = (ctypes.c_float * (self.MAX_ZERNIKE_MODES + 1))()
        self.average_count = Vi.int32(0)
        self.average_data_ready = Vi.int32(0)
        self.aoi_center_x_mm = Vi.real64(0)
        self.aoi_center_y_mm = Vi.real64(0)
        self.aoi_size_x_mm = Vi.real64(0)
        self.aoi_size_y_mm = Vi.real64(0)
        self.beam_centroid_x_mm = Vi.real64(0)
        self.beam_centroid_y_mm = Vi.real64(0)
        self.beam_diameter_x_mm = Vi.real64(0)
        self.beam_diameter_y_mm = Vi.real64(0)
        self.black_level_offset_actual = Vi.int32(0)
        self.black_level_offset_set = Vi.int32(0)
        self.calculate_diameters = Vi.int32(0)
        self.cam_pitch_um = Vi.real64(0)
        self.cam_resolution_index = Vi.int32(0)
        self.cancel_wavefront_tilt = Vi.int32(1)
        self.device_id = Vi.int32(0)
        self.device_status = Vi.int32(0)
        self.diameter_max = Vi.real64(0)
        self.diameter_mean = Vi.real64(0)
        self.diameter_min = Vi.real64(0)
        self.do_spherical_reference = Vi.int32(0)
        self.dynamic_noise_cut = Vi.int32(1)
        self.error_code = Vi.int32(0)
        self.error_message = Vi.char(self.WFS_ERR_DESCR_BUFFER_SIZE)
        self.exposure_time_actual = Vi.real64(0)
        self.exposure_time_increment = Vi.real64(0)
        self.exposure_time_max = Vi.real64(0)
        self.exposure_time_min = Vi.real64(0)
        self.exposure_time_set = Vi.real64(0)
        self.firmware_revision = Vi.char(self.WFS_BUFFER_SIZE)
        self.fit_error_mean = Vi.real64(0)
        self.fit_error_stdev = Vi.real64(0)
        self.fourier_j0 = Vi.real64(0)
        self.fourier_j45 = Vi.real64(0)
        self.fourier_m = Vi.real64(0)
        self.fourier_orders = Vi.int32(2)  # 2, 4, 6 only valid settings
        self.grid_correction_0 = Vi.real64(0)
        self.grid_correction_45 = Vi.real64(0)
        self.grid_correction_pitch = Vi.real64(0)
        self.grid_correction_rotation = Vi.real64(0)
        self.highspeed_mode = Vi.int32(0)
        self.id_query = Vi.boolean(0)
        # self.image_buffer = ctypes.c_uint(0)
        self.image_buffer = Vi.uint8(0)
        self.intensity_limit = Vi.int32(0)
        self.intensity_max = Vi.int32(0)
        self.intensity_mean = Vi.int32(0)
        self.intensity_min = Vi.int32(0)
        self.intensity_rms = Vi.int32(0)
        self.in_use = Vi.int32(0)
        self.instrument_count = Vi.int32(0)
        self.instrument_driver_revision = Vi.char(self.WFS_BUFFER_SIZE)
        self.instrument_handle = Vi.session(0)
        self.instrument_index = Vi.int32(0)
        self.instrument_name_wfs = Vi.char(self.WFS_BUFFER_SIZE)
        self.lenslet_focal_length_um = Vi.real64(0)
        self.lenslet_pitch_um = Vi.real64(0)
        self.limit_to_pupil = Vi.int32(0)
        self.line = Vi.int32(0)
        # self.line_max = Vi.real32(0)  # TODO Float Array
        self.line_max = (ctypes.c_float * 1280)()
        # self.line_min = Vi.real32(0)  # TODO Float Array
        self.line_min = (ctypes.c_float * 1280)()
        # self.line_selected = Vi.real32(0)  # TODO Float Array
        self.line_selected = (ctypes.c_float * 1280)()
        self.manufacturer_name = Vi.char(self.WFS_BUFFER_SIZE)
        self.master_gain_actual = Vi.real64(0)
        self.master_gain_max = Vi.real64(0)
        self.master_gain_min = Vi.real64(0)
        self.master_gain_set = Vi.real64(0)
        self.mla_count = Vi.int32(0)
        self.mla_index = Vi.int32(0)
        self.mla_name = Vi.char(self.WFS_BUFFER_SIZE)
        self.optometric_axis = Vi.real64(0)
        self.optometric_cylinder = Vi.real64(0)
        self.optometric_sphere = Vi.real64(0)
        self.pixel_format = Vi.int32(self.PIXEL_FORMAT_MONO8)
        self.pupil_center_x_mm = Vi.real64(0)
        self.pupil_center_y_mm = Vi.real64(0)
        self.pupil_diameter_x_mm = Vi.real64(4.76)  # Max diameter without clipping edges
        self.pupil_diameter_y_mm = Vi.real64(4.76)  # Max diameter without clipping edges
        self.reference_index = Vi.int32(0)
        self.reset = Vi.int32(0)
        self.reset_device = Vi.boolean(0)
        # self.resource_name = Vi.rsrc(b'')  # resource_name='USB::0x1313::0x0000::1'
        self.resource_name = Vi.char(self.WFS_BUFFER_SIZE)
        self.resource_name.value = b'USB::0x1313::0x0000::1'
        self.roc_mm = Vi.real64(0)
        self.saturated_pixels_percent = Vi.real64(0)
        self.serial_number_camera = Vi.char(self.WFS_BUFFER_SIZE)
        self.serial_number_wfs = Vi.char(self.WFS_BUFFER_SIZE)
        self.spot_offset_x = Vi.real64(0)
        self.spot_offset_y = Vi.real64(0)
        self.spot_ref_type = Vi.int32(0)
        self.spotfield_columns = Vi.int32(0)
        self.spotfield_rows = Vi.int32(0)
        self.spots_x = Vi.int32(0)
        self.spots_y = Vi.int32(0)
        self.subtract_offset = Vi.int32(0)
        self.test_message = Vi.int16(0)
        self.test_result = Vi.char(self.WFS_BUFFER_SIZE)
        self.trigger_delay_actual = Vi.int32(0)
        self.trigger_delay_increment = Vi.int32(0)
        self.trigger_delay_max = Vi.int32(0)
        self.trigger_delay_min = Vi.int32(0)
        self.trigger_delay_set = Vi.int32(0)
        self.trigger_mode = Vi.int32(0)
        self.wavefront_diff = Vi.real64(0)
        self.wavefront_max = Vi.real64(0)
        self.wavefront_mean = Vi.real64(0)
        self.wavefront_min = Vi.real64(0)
        self.wavefront_rms = Vi.real64(0)
        self.wavefront_type = Vi.int32(0)
        self.wavefront_weighted_rms = Vi.real64(0)
        self.wavelength = Vi.real64(532)
        self.zernike_orders = Vi.int32(4)
        self.window_count_x = Vi.int32(0)
        self.window_count_y = Vi.int32(0)
        self.window_size_x = Vi.int32(0)
        self.window_size_y = Vi.int32(0)
        self.window_start_position_x = Vi.int32(0)
        self.window_start_position_y = Vi.int32(0)

    # WFS Functions
    def _init(self, resource_name=None, id_query=None, reset_device=None):
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
        :return status:
        """
        if resource_name is not None:
            try:
                self.resource_name = Vi.char(self.WFS_BUFFER_SIZE)
                self.resource_name.value = resource_name
            except TypeError:
                self.resource_name = resource_name
        if id_query is not None:
            try:
                self.id_query = Vi.boolean(id_query)
            except TypeError:
                self.id_query = id_query
        if reset_device is not None:
            try:
                self.reset_device = Vi.boolean(reset_device)
            except TypeError:
                self.reset_device = reset_device
        lib_wfs.WFS_init.argtypes = [ctypes.c_char_p,
                                     ctypes.c_ushort,
                                     ctypes.c_ushort,
                                     ctypes.POINTER(ctypes.c_ulong)]
        lib_wfs.WFS_init.restypes = ctypes.c_long
        status = lib_wfs.WFS_init(self.resource_name,
                                  self.id_query,
                                  self.reset_device,
                                  ctypes.byref(self.instrument_handle))
        log_wfs.info('Init: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Resource Name: {0}'.format(self.resource_name.value))
        log_wfs.info('ID Query: {0}'.format(self.id_query.value))
        log_wfs.info('Reset Device: {0}'.format(self.reset_device.value))
        self._error_message(status)
        return status

    def _get_status(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetStatus(self.instrument_handle,
                                       ctypes.byref(self.device_status))
        log_wfs.debug('Get Status: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Device Status: {0}'.format(self.device_status.value))
        # self.device_status.value -= 1788  # Some unknown offset? TODO
        # self.device_status.value -= 1792  # Some unknown offset? TODO
        if self.device_status.value in self.WFS_DRIVER_STATUS:
            log_wfs.info('Device Status: {0}'.format(self.WFS_DRIVER_STATUS[self.device_status.value]))
        else:
            log_wfs.info('Device Status: Unknown/OK')
        self._error_message(status)
        return status

    def _close(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        if self.instrument_handle.value is not 0:
            status = lib_wfs.WFS_close(self.instrument_handle)
            log_wfs.info('Close: {0}'.format(self.instrument_handle.value))
            self.instrument_handle.value = 0
        else:
            status = 0
        self._error_message(status)
        return status

    # Configuration Functions
    def _get_instrument_info(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetInstrumentInfo(self.instrument_handle,
                                               self.manufacturer_name,
                                               self.instrument_name_wfs,
                                               self.serial_number_wfs,
                                               self.serial_number_camera)
        log_wfs.debug('Get Instrument Info: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Manufacturer Name: {0}'.format(self.manufacturer_name.value))
        log_wfs.info('Instrument Name WFS: {0}'.format(self.instrument_name_wfs.value))
        log_wfs.info('Serial Number WFS: {0}'.format(self.serial_number_wfs.value))
        log_wfs.info('Serial Number Camera: {0}'.format(self.serial_number_camera.value))
        self._error_message(status)
        return status

    def _configure_cam(self, instrument_handle=None, pixel_format=None, cam_resolution_index=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        if pixel_format is not None:
            try:
                self.pixel_format = Vi.int32(pixel_format)
            except TypeError:
                self.pixel_format = pixel_format
        if cam_resolution_index is not None:
            try:
                self.cam_resolution_index = Vi.int32(cam_resolution_index)
            except TypeError:
                self.cam_resolution_index = cam_resolution_index
        status = lib_wfs.WFS_ConfigureCam(self.instrument_handle,
                                          self.pixel_format,
                                          self.cam_resolution_index,
                                          ctypes.byref(self.spots_x),
                                          ctypes.byref(self.spots_y))
        log_wfs.debug('Configure Cam: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Pixel Format: {0}'.format(self.pixel_format.value))
        log_wfs.info('Camera Resolution Index: {0}'.format(self.cam_resolution_index.value))
        log_wfs.info('Spots X: {0}'.format(self.spots_x.value))
        log_wfs.info('Spots Y: {0}'.format(self.spots_y.value))
        self._error_message(status)
        return status

    def _set_highspeed_mode(self, instrument_handle=None, highspeed_mode=None,
                            adapt_centroids=None, subtract_offset=None, allow_auto_exposure=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        if highspeed_mode is not None:
            try:
                self.highspeed_mode = Vi.int32(highspeed_mode)
            except TypeError:
                self.highspeed_mode = highspeed_mode
        if adapt_centroids is not None:
            try:
                self.adapt_centroids = Vi.int32(adapt_centroids)
            except TypeError:
                self.adapt_centroids = adapt_centroids
        if subtract_offset is not None:
            try:
                self.subtract_offset = Vi.int32(subtract_offset)
            except TypeError:
                self.subtract_offset = subtract_offset
        if allow_auto_exposure is not None:
            try:
                self.allow_auto_exposure = Vi.int32(allow_auto_exposure)
            except TypeError:
                self.allow_auto_exposure = allow_auto_exposure
        status = lib_wfs.WFS_SetHighspeedMode(self.instrument_handle,
                                              self.highspeed_mode,
                                              self.adapt_centroids,
                                              self.subtract_offset,
                                              self.allow_auto_exposure)
        log_wfs.debug('Set Highspeed Mode: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Highspeed Mode: {0}'.format(self.highspeed_mode.value))
        log_wfs.info('Adapt Centroids: {0}'.format(self.adapt_centroids.value))
        log_wfs.info('Subtract Offset: {0}'.format(self.subtract_offset.value))
        log_wfs.info('Allow Auto Exposure: {0}'.format(self.allow_auto_exposure.value))
        self._error_message(status)
        return status

    def _get_highspeed_windows(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetHighspeedWindows(self.instrument_handle,
                                                 ctypes.byref(self.window_count_x),
                                                 ctypes.byref(self.window_count_y),
                                                 ctypes.byref(self.window_size_x),
                                                 ctypes.byref(self.window_size_y),
                                                 self.window_start_position_x,
                                                 self.window_start_position_y)
        log_wfs.debug('Get Highspeed Windows: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Window Count X: {0}'.format(self.window_count_x.value))
        log_wfs.info('Window Count Y: {0}'.format(self.window_count_y.value))
        log_wfs.info('Window Size X: {0}'.format(self.window_size_x.value))
        log_wfs.info('Window Size Y: {0}'.format(self.window_size_y.value))
        log_wfs.info('Window Start Position X: {0}'.format(self.window_start_position_x.value))
        log_wfs.info('Window Start Position Y: {0}'.format(self.window_start_position_y.value))
        self._error_message(status)
        return status

    def _check_highspeed_centroids(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_CheckHighspeedCentroids(self.instrument_handle)
        log_wfs.debug('Check Highspeed Centroids: {0}'.format(self.instrument_handle.value))
        self._error_message(status)
        return status

    def _get_exposure_time_range(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetExposureTimeRange(self.instrument_handle,
                                                  ctypes.byref(self.exposure_time_min),
                                                  ctypes.byref(self.exposure_time_max),
                                                  ctypes.byref(self.exposure_time_increment))
        log_wfs.debug('Get Exposure Time Range: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Exposure Time Minimum (ms): {0}'.format(self.exposure_time_min.value))
        log_wfs.info('Exposure Time Maximum (ms): {0}'.format(self.exposure_time_max.value))
        log_wfs.info('Exposure Time Increment (ms): {0}'.format(self.exposure_time_increment.value))
        self._error_message(status)
        return status

    def _set_exposure_time(self, instrument_handle=None, exposure_time_set=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        if exposure_time_set is not None:
            try:
                self.exposure_time_set = Vi.real64(exposure_time_set)
            except TypeError:
                self.exposure_time_set = exposure_time_set
        status = lib_wfs.WFS_SetExposureTime(self.instrument_handle,
                                             self.exposure_time_set,
                                             ctypes.byref(self.exposure_time_actual))
        log_wfs.debug('Set Exposure Time: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Exposure Time Set (ms): {0}'.format(self.exposure_time_set.value))
        log_wfs.info('Exposure Time Actual (ms): {0}'.format(self.exposure_time_actual.value))
        self._error_message(status)
        return status

    def _get_exposure_time(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetExposureTime(self.instrument_handle,
                                             ctypes.byref(self.exposure_time_actual))
        log_wfs.debug('Get Exposure Time (ms): {0}'.format(self.instrument_handle.value))
        log_wfs.info('Exposure Time Actual (ms): {0}'.format(self.exposure_time_actual.value))
        self._error_message(status)
        return status

    def _get_master_gain_range(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetMasterGainRange(self.instrument_handle,
                                                ctypes.byref(self.master_gain_min),
                                                ctypes.byref(self.master_gain_max))
        log_wfs.debug('Get Master Gain Range: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Master Gain Minimum: {0}'.format(self.master_gain_min.value))
        log_wfs.info('Master Gain Maximum: {0}'.format(self.master_gain_max.value))
        self._error_message(status)
        return status

    def _set_master_gain(self, instrument_handle=None, master_gain_set=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        if master_gain_set is not None:
            try:
                self.master_gain_set = Vi.real64(master_gain_set)
            except TypeError:
                self.master_gain_set = master_gain_set
        status = lib_wfs.WFS_SetMasterGain(self.instrument_handle,
                                           self.master_gain_set,
                                           ctypes.byref(self.master_gain_actual))
        log_wfs.debug('Get Exposure Time: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Master Gain Set: {0}'.format(self.master_gain_set.value))
        log_wfs.info('Master Gain Actual: {0}'.format(self.master_gain_actual.value))
        self._error_message(status)
        return status

    def _get_master_gain(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetMasterGain(self.instrument_handle,
                                           ctypes.byref(self.master_gain_actual))
        log_wfs.debug('Get Exposure Time: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Master Gain Actual: {0}'.format(self.master_gain_actual.value))
        self._error_message(status)
        return status

    def _set_black_level_offset(self, instrument_handle=None, black_level_offset_set=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        if black_level_offset_set is not None:
            try:
                self.black_level_offset_set = Vi.int32(black_level_offset_set)
            except TypeError:
                self.black_level_offset_set = black_level_offset_set
        status = lib_wfs.WFS_SetBlackLevelOffset(self.instrument_handle,
                                                 self.black_level_offset_set)
        log_wfs.debug('Set Black Level Offset: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Black Level Offset Set: {0}'.format(self.black_level_offset_set.value))
        self._error_message(status)
        return status

    def _get_black_level_offset(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetBlackLevelOffset(self.instrument_handle,
                                                 ctypes.byref(self.black_level_offset_actual))
        log_wfs.debug('Get Black Level Offset: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Black Level Offset Actual: {0}'.format(self.black_level_offset_actual.value))
        self._error_message(status)
        return status

    def _set_trigger_mode(self, instrument_handle=None, trigger_mode=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        if trigger_mode is not None:
            try:
                self.trigger_mode = Vi.int32(trigger_mode)
            except TypeError:
                self.trigger_mode = trigger_mode
        status = lib_wfs.WFS_SetTriggerMode(self.instrument_handle,
                                            self.trigger_mode)
        log_wfs.debug('Set Trigger Mode: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Trigger Mode: {0}'.format(self.trigger_mode.value))
        self._error_message(status)
        return status

    def _get_trigger_mode(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetTriggerMode(self.instrument_handle,
                                            ctypes.byref(self.trigger_mode))
        log_wfs.debug('Get Trigger Mode: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Trigger Mode: {0}'.format(self.trigger_mode.value))
        self._error_message(status)
        return status

    def _set_trigger_delay(self, instrument_handle=None, trigger_delay_set=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        if trigger_delay_set is not None:
            try:
                self.trigger_delay_set = Vi.int32(trigger_delay_set)
            except TypeError:
                self.trigger_delay_set = trigger_delay_set
        status = lib_wfs.WFS_SetTriggerDelay(self.instrument_handle,
                                             self.trigger_delay_set,
                                             ctypes.byref(self.trigger_delay_actual))
        log_wfs.debug('Set Trigger Delay: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Trigger Delay Set (µs): {0}'.format(self.trigger_delay_set.value))
        log_wfs.info('Trigger Delay Actual (µs): {0}'.format(self.trigger_delay_actual.value))
        self._error_message(status)
        return status

    def _get_trigger_delay_range(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetTriggerDelayRange(self.instrument_handle,
                                                  ctypes.byref(self.trigger_delay_min),
                                                  ctypes.byref(self.trigger_delay_max),
                                                  ctypes.byref(self.trigger_delay_increment))
        log_wfs.debug('Get Trigger Delay Range: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Trigger Delay Minimum (µs): {0}'.format(self.trigger_delay_min.value))
        log_wfs.info('Trigger Delay Maximum (µs): {0}'.format(self.trigger_delay_max.value))
        log_wfs.info('Trigger Delay Increment (µs): {0}'.format(self.trigger_delay_increment.value))
        self._error_message(status)
        return status

    def _get_mla_count(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetMlaCount(self.instrument_handle,
                                         ctypes.byref(self.mla_count))
        self.mla_index = Vi.int32(self.mla_count.value - 1)
        log_wfs.debug('Get MLA Count: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Micro Lens Array Count: {0}'.format(self.mla_count.value))
        log_wfs.info('Micro Lens Array Index: {0}'.format(self.mla_index.value))
        self._error_message(status)
        return status

    def _get_mla_data(self, instrument_handle=None, mla_index=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        if mla_index is not None:
            try:
                self.mla_index = Vi.int32(mla_index)
            except TypeError:
                self.mla_index = mla_index
        status = lib_wfs.WFS_GetMlaData(self.instrument_handle,
                                        self.mla_index,
                                        self.mla_name,
                                        ctypes.byref(self.cam_pitch_um),
                                        ctypes.byref(self.lenslet_pitch_um),
                                        ctypes.byref(self.spot_offset_x),
                                        ctypes.byref(self.spot_offset_y),
                                        ctypes.byref(self.lenslet_focal_length_um),
                                        ctypes.byref(self.grid_correction_0),
                                        ctypes.byref(self.grid_correction_45))
        log_wfs.debug('Get MLA Data: {0}'.format(self.instrument_handle.value))
        log_wfs.info('MLA Index: {0}'.format(self.mla_index.value))
        log_wfs.info('MLA Name: {0}'.format(self.mla_name.value))
        log_wfs.info('MLA Camera Pitch (µm): {0}'.format(self.cam_pitch_um.value))
        log_wfs.info('MLA Lenslet Pitch (µm): {0}'.format(self.lenslet_pitch_um.value))
        log_wfs.info('MLA Spot Offset X: {0}'.format(self.spot_offset_x.value))
        log_wfs.info('MLA Spot Offset Y: {0}'.format(self.spot_offset_y.value))
        log_wfs.info('MLA Lenslet Focal length (µm): {0}'.format(self.lenslet_focal_length_um.value))
        log_wfs.info('MLA Grid Correction 0°'.format(self.grid_correction_0.value))
        log_wfs.info('MLA Grid Correction 45°'.format(self.grid_correction_45.value))
        self._error_message(status)
        return status

    def _get_mla_data2(self, instrument_handle=None, mla_index=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        if mla_index is not None:
            try:
                self.mla_index = Vi.int32(mla_index)
            except TypeError:
                self.mla_index = mla_index
        status = lib_wfs.WFS_GetMlaData2(self.instrument_handle,
                                         self.mla_index,
                                         self.mla_name,
                                         ctypes.byref(self.cam_pitch_um),
                                         ctypes.byref(self.lenslet_pitch_um),
                                         ctypes.byref(self.spot_offset_x),
                                         ctypes.byref(self.spot_offset_y),
                                         ctypes.byref(self.lenslet_focal_length_um),
                                         ctypes.byref(self.grid_correction_0),
                                         ctypes.byref(self.grid_correction_45),
                                         ctypes.byref(self.grid_correction_rotation),
                                         ctypes.byref(self.grid_correction_pitch))
        log_wfs.debug('Get MLA Data2: {0}'.format(self.instrument_handle.value))
        log_wfs.info('MLA Index: {0}'.format(self.mla_index.value))
        log_wfs.info('MLA Name: {0}'.format(self.mla_name.value))
        log_wfs.info('MLA Camera Pitch (µm): {0}'.format(self.cam_pitch_um.value))
        log_wfs.info('MLA Lenslet Pitch (µm): {0}'.format(self.lenslet_pitch_um.value))
        log_wfs.info('MLA Spot Offset X: {0}'.format(self.spot_offset_x.value))
        log_wfs.info('MLA Spot Offset Y: {0}'.format(self.spot_offset_y.value))
        log_wfs.info('MLA Lenslet Focal length (µm): {0}'.format(self.lenslet_focal_length_um.value))
        log_wfs.info('MLA Grid Correction 0°'.format(self.grid_correction_0.value))
        log_wfs.info('MLA Grid Correction 45°'.format(self.grid_correction_45.value))
        log_wfs.info('MLA Grid Correction Rotation: {0}'.format(self.grid_correction_rotation.value))
        log_wfs.info('MLA Grid Correction Pitch: {0}'.format(self.grid_correction_pitch.value))
        self._error_message(status)
        return status

    def _select_mla(self, instrument_handle=None, mla_index=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        if mla_index is not None:
            try:
                self.mla_index = Vi.int32(mla_index)
            except TypeError:
                self.mla_index = mla_index
        status = lib_wfs.WFS_SelectMla(self.instrument_handle,
                                       self.mla_index)
        log_wfs.debug('Select MLA: {0}'.format(self.instrument_handle.value))
        log_wfs.info('MLA selection: {0}'.format(self.mla_index.value))
        self._error_message(status)
        return status

    def _set_aoi(self, instrument_handle=None,
                 aoi_center_x_mm=None, aoi_center_y_mm=None,
                 aoi_size_x_mm=None, aoi_size_y_mm=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        if aoi_center_x_mm is not None:
            try:
                self.aoi_center_x_mm = Vi.real64(aoi_center_x_mm)
            except TypeError:
                self.aoi_center_x_mm = aoi_center_x_mm
        if aoi_center_y_mm is not None:
            try:
                self.aoi_center_y_mm = Vi.real64(aoi_center_y_mm)
            except TypeError:
                self.aoi_center_y_mm = aoi_center_y_mm
        if aoi_size_x_mm is not None:
            try:
                self.aoi_size_x_mm = Vi.real64(aoi_size_x_mm)
            except TypeError:
                self.aoi_size_x_mm = aoi_size_x_mm
        if aoi_size_y_mm is not None:
            try:
                self.aoi_size_y_mm = Vi.real64(aoi_size_y_mm)
            except TypeError:
                self.aoi_size_y_mm = aoi_size_y_mm
        status = lib_wfs.WFS_SetAoi(self.instrument_handle,
                                    self.aoi_center_x_mm,
                                    self.aoi_center_y_mm,
                                    self.aoi_size_x_mm,
                                    self.aoi_size_y_mm)
        log_wfs.debug('Set AoI: {0}'.format(self.instrument_handle.value))
        log_wfs.info('AoI Center X (mm): {0}'.format(self.aoi_center_x_mm.value))
        log_wfs.info('AoI Center y (mm): {0}'.format(self.aoi_center_y_mm.value))
        log_wfs.info('AoI Size X (mm): {0}'.format(self.aoi_size_x_mm.value))
        log_wfs.info('AoI Size Y (mm): {0}'.format(self.aoi_size_y_mm.value))
        self._error_message(status)
        return status

    def _get_aoi(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetAoi(self.instrument_handle,
                                    ctypes.byref(self.aoi_center_x_mm),
                                    ctypes.byref(self.aoi_center_y_mm),
                                    ctypes.byref(self.aoi_size_x_mm),
                                    ctypes.byref(self.aoi_size_y_mm))
        log_wfs.debug('Set AoI: {0}'.format(self.instrument_handle.value))
        log_wfs.info('AoI Center X (mm): {0}'.format(self.aoi_center_x_mm.value))
        log_wfs.info('AoI Center y (mm): {0}'.format(self.aoi_center_y_mm.value))
        log_wfs.info('AoI Size X (mm): {0}'.format(self.aoi_size_x_mm.value))
        log_wfs.info('AoI Size Y (mm): {0}'.format(self.aoi_size_y_mm.value))
        self._error_message(status)
        return status

    def _set_pupil(self, instrument_handle=None,
                   pupil_center_x_mm=None, pupil_center_y_mm=None,
                   pupil_diameter_x_mm=None, pupil_diameter_y_mm=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        if pupil_center_x_mm is not None:
            try:
                self.pupil_center_x_mm = Vi.real64(pupil_center_x_mm)
            except TypeError:
                self.pupil_center_x_mm = pupil_center_x_mm
        if pupil_center_y_mm is not None:
            try:
                self.pupil_center_y_mm = Vi.real64(pupil_center_y_mm)
            except TypeError:
                self.pupil_center_y_mm = pupil_center_y_mm
        if pupil_diameter_x_mm is not None:
            try:
                self.pupil_diameter_x_mm = Vi.real64(pupil_diameter_x_mm)
            except TypeError:
                self.pupil_diameter_x_mm = pupil_diameter_x_mm
        if pupil_diameter_y_mm is not None:
            try:
                self.pupil_diameter_y_mm = Vi.real64(pupil_diameter_y_mm)
            except TypeError:
                self.pupil_diameter_y_mm = pupil_diameter_y_mm

        status = lib_wfs.WFS_SetPupil(self.instrument_handle,
                                      self.pupil_center_x_mm,
                                      self.pupil_center_y_mm,
                                      self.pupil_diameter_x_mm,
                                      self.pupil_diameter_y_mm)
        log_wfs.debug('Set Pupil: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Set Pupil Centroid X (mm): {0}'.format(self.pupil_center_x_mm.value))
        log_wfs.info('Set Pupil Centroid Y (mm): {0}'.format(self.pupil_center_y_mm.value))
        log_wfs.info('Set Pupil Diameter X (mm): {0}'.format(self.pupil_diameter_x_mm.value))
        log_wfs.info('Set Pupil Diameter Y (mm): {0}'.format(self.pupil_diameter_y_mm.value))
        self._error_message(status)
        return status

    def _get_pupil(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetPupil(self.instrument_handle,
                                      ctypes.byref(self.pupil_center_x_mm),
                                      ctypes.byref(self.pupil_center_y_mm),
                                      ctypes.byref(self.pupil_diameter_x_mm),
                                      ctypes.byref(self.pupil_diameter_y_mm))
        log_wfs.debug('Get Pupil: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Get Pupil Centroid X (mm): {0}'.format(self.pupil_center_x_mm.value))
        log_wfs.info('Get Pupil Centroid Y (mm): {0}'.format(self.pupil_center_y_mm.value))
        log_wfs.info('Get Pupil Diameter X (mm): {0}'.format(self.pupil_diameter_x_mm.value))
        log_wfs.info('Get Pupil Diameter Y (mm): {0}'.format(self.pupil_diameter_y_mm.value))
        self._error_message(status)
        return status

    def _set_reference_plane(self, instrument_handle=None, reference_index=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        if reference_index is not None:
            try:
                self.reference_index = Vi.int32(reference_index)
            except TypeError:
                self.reference_index = reference_index
        self.reference_index = Vi.int32(reference_index)
        status = lib_wfs.WFS_SetReferencePlane(self.instrument_handle,
                                               self.reference_index)
        log_wfs.debug('Set Reference Plane: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Set Reference Index: {0}'.format(self.reference_index.value))
        self._error_message(status)
        return status

    def _get_reference_plane(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetReferencePlane(self.instrument_handle,
                                               ctypes.byref(self.reference_index))
        log_wfs.debug('Get Reference Plane: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Get Reference Index: {0}'.format(self.reference_index.value))
        self._error_message(status)
        return status

    # Data Functions
    def _take_spotfield_image(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_TakeSpotfieldImage(self.instrument_handle)
        log_wfs.debug('Take Spotfield Image: {0}'.format(self.instrument_handle.value))
        self._error_message(status)
        return status

    def _take_spotfield_image_auto_exposure(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_TakeSpotfieldImageAutoExpos(self.instrument_handle,
                                                         ctypes.byref(self.exposure_time_actual),
                                                         ctypes.byref(self.master_gain_actual))
        log_wfs.debug('Take Spotfield Image Auto Exposure: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Exposure Time Actual: {0}'.format(self.exposure_time_actual.value))
        log_wfs.info('Master Gain Actual: {0}'.format(self.master_gain_actual.value))
        self._error_message(status)
        return status

    def _get_spotfield_image(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetSpotfieldImage(self.instrument_handle,
                                               ctypes.byref(self.image_buffer),
                                               ctypes.byref(self.spotfield_rows),
                                               ctypes.byref(self.spotfield_columns))
        log_wfs.debug('Get Spotfield Image: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Image Buffer: {0}'.format(self.image_buffer.value))
        log_wfs.info('Rows: {0}'.format(self.spotfield_rows.value))
        log_wfs.info('Columns: {0}'.format(self.spotfield_columns.value))
        self._error_message(status)
        return status

    def _get_spotfield_image_copy(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        # TODO
        status = lib_wfs.WFS_GetSpotfieldImageCopy(self.instrument_handle,
                                                   self.image_buffer,
                                                   ctypes.byref(self.spotfield_rows),
                                                   ctypes.byref(self.spotfield_columns))
        log_wfs.debug('Get Spotfield Image Copy: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Image Buffer: {0}'.format(self.image_buffer.value))
        log_wfs.info('Rows: {0}'.format(self.spotfield_rows.value))
        log_wfs.info('Columns: {0}'.format(self.spotfield_columns.value))
        self._error_message(status)
        return status

    def _average_image(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_AverageImage(self.instrument_handle,
                                          self.average_count,
                                          ctypes.byref(self.average_data_ready))
        log_wfs.debug('Average Image: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Average Count: {0}'.format(self.average_count.value))
        log_wfs.info('Average Data Ready: {0}'.format(self.average_data_ready.value))
        self._error_message(status)
        return status

    def _average_image_rolling(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_AverageImageRolling(self.instrument_handle,
                                                 self.average_count,
                                                 self.reset)
        log_wfs.debug('Average Image Rolling: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Average Count: {0}'.format(self.average_count.value))
        log_wfs.info('Reset: {0}'.format(self.reset.value))
        self._error_message(status)
        return status

    def _cut_image_noise_floor(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_CutImageNoiseFloor(self.instrument_handle,
                                                self.intensity_limit)
        log_wfs.debug('Cut Image Noise Floor: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Intensity Limit: {0}'.format(self.intensity_limit.value))
        self._error_message(status)
        return status

    def _calc_image_min_max(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_CalcImageMinMax(self.instrument_handle,
                                             ctypes.byref(self.intensity_min),
                                             ctypes.byref(self.intensity_max),
                                             ctypes.byref(self.saturated_pixels_percent))
        log_wfs.debug('Calc Image Min Max: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Intensity Minimum: {0}'.format(self.intensity_min.value))
        log_wfs.info('Intensity Maximum: {0}'.format(self.intensity_max.value))
        log_wfs.info('Saturated Pixels Percent: {0}'.format(self.saturated_pixels_percent.value))
        self._error_message(status)
        return status

    def _calc_mean_rms_noise(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_CalcMeanRmsNoise(self.instrument_handle,
                                              ctypes.byref(self.intensity_mean),
                                              ctypes.byref(self.intensity_rms))
        log_wfs.debug('Calc Mean RMS Noise: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Intensity Mean: {0}'.format(self.intensity_mean.value))
        log_wfs.info('Intensity RMS: {0}'.format(self.intensity_rms.value))
        self._error_message(status)
        return status

    def _get_line(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetLine(self.instrument_handle,
                                     self.line,
                                     self.line_selected)
        log_wfs.debug('Get Line: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Line: {0}'.format(self.line.value))
        # TODO AttributeError: 'c_float_Array_1280' object has no attribute 'value'
        log_wfs.info('Line Selected: {0}'.format(self.line_selected.value))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.line_selected]))
        self._error_message(status)
        return status

    def _get_line_view(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetLineView(self.instrument_handle,
                                         self.line_min,
                                         self.line_max)
        log_wfs.debug('Get Line View: {0}'.format(self.instrument_handle.value))
        # TODO AttributeError: 'c_float_Array_1280' object has no attribute 'value'
        log_wfs.info('Line Minimum: {0}'.format(self.line_min.value))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.line_min]))
        log_wfs.info('Line Maximum: {0}'.format(self.line_max.value))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.line_max]))
        self._error_message(status)
        return status

    def _calc_beam_centroid_diameter(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_CalcBeamCentroidDia(self.instrument_handle,
                                                 ctypes.byref(self.beam_centroid_x_mm),
                                                 ctypes.byref(self.beam_centroid_y_mm),
                                                 ctypes.byref(self.beam_diameter_x_mm),
                                                 ctypes.byref(self.beam_diameter_y_mm))
        log_wfs.debug('Calc Beam Centroid Diameter: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Beam Centroid X (mm): {0}'.format(self.beam_centroid_x_mm.value))
        log_wfs.info('Beam Diameter X (mm): {0}'.format(self.beam_diameter_y_mm.value))
        log_wfs.info('Beam Centroid Y (mm): {0}'.format(self.beam_centroid_y_mm.value))
        log_wfs.info('Beam Diameter Y (mm): {0}'.format(self.beam_diameter_x_mm.value))
        self._error_message(status)
        return status

    def _calc_spots_centroid_diameter_intensity(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_CalcSpotsCentrDiaIntens(self.instrument_handle,
                                                     self.dynamic_noise_cut,
                                                     self.calculate_diameters)
        log_wfs.debug('Calc Spots Centroid Diameter Intensity: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Dynamic Noise Cut: {0}'.format(self.dynamic_noise_cut.value))
        log_wfs.info('Calculate diameters: {0}'.format(self.calculate_diameters.value))
        self._error_message(status)
        return status

    def _get_spot_centroids(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetSpotCentroids(self.instrument_handle,
                                              self.array_centroid_x,
                                              self.array_centroid_y)
        log_wfs.debug('Get Spot Centroids: {0}'.format(self.instrument_handle.value))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.array_centroid_x]))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.array_centroid_y]))
        self._error_message(status)
        return status

    def _get_spot_diameters(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetSpotDiameters(self.instrument_handle,
                                              self.array_diameter_x,
                                              self.array_diameter_y)
        log_wfs.debug('Get Spot Diameters: {0}'.format(self.instrument_handle.value))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.array_diameter_x]))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.array_diameter_y]))
        self._error_message(status)
        return status

    def _get_spot_diameters_statistics(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        # TODO
        status = lib_wfs.WFS_GetSpotDiameters(self.instrument_handle,
                                              ctypes.byref(self.diameter_min),
                                              ctypes.byref(self.diameter_max),
                                              ctypes.byref(self.diameter_mean))
        log_wfs.debug('Get Spot Diameter Statistics: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Diameter Minimum: {0}'.format(self.diameter_min.value))
        log_wfs.info('Diameter Maximum: {0}'.format(self.diameter_max.value))
        log_wfs.info('Diameter Mean: {0}'.format(self.diameter_mean.value))
        self._error_message(status)
        return status

    def _get_spot_intensities(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetSpotIntensities(self.instrument_handle,
                                                self.array_intensity)
        log_wfs.debug('Get Spot Intensities: {0}'.format(self.instrument_handle.value))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.array_intensity]))
        self._error_message(status)
        return status

    def _calc_spot_to_reference_deviations(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_CalcSpotToReferenceDeviations(self.instrument_handle,
                                                           self.cancel_wavefront_tilt)
        log_wfs.debug('Calc Spot to Reference Deviations: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Cancel Wavefront Tilt: {0}'.format(self.cancel_wavefront_tilt.value))
        self._error_message(status)
        return status

    def _get_spot_reference_positions(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetSpotReferencePositions(self.instrument_handle,
                                                       self.array_reference_x,
                                                       self.array_reference_y)
        log_wfs.debug('Get Spot Reference Positions: {0}'.format(self.instrument_handle.value))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.array_reference_x]))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.array_reference_y]))
        self._error_message(status)
        return status

    def _get_spot_deviations(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetSpotDeviations(self.instrument_handle,
                                               self.array_deviations_x,
                                               self.array_deviations_y)
        log_wfs.debug('Get Spot Deviations: {0}'.format(self.instrument_handle.value))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.array_deviations_x]))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.array_deviations_y]))
        self._error_message(status)
        return status

    def _zernike_lsf(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_ZernikeLsf(self.instrument_handle,
                                        ctypes.byref(self.zernike_orders),
                                        self.array_zernike_um,
                                        self.array_zernike_orders_um,
                                        ctypes.byref(self.roc_mm))
        log_wfs.debug('Zernike Least Square Fit: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Zernike (µm):' + ''.join(['{:18}'.format(item) for item in self.array_zernike_um]))
        log_wfs.info('Zernike Orders (µm)' + ''.join(['{:18}'.format(item) for item in self.array_zernike_orders_um]))
        log_wfs.info('Zernike Orders: {0}'.format(self.zernike_orders.value))
        log_wfs.info('RoC (mm): {0}'.format(self.roc_mm.value))
        self._error_message(status)
        return status

    def _calc_fourier_optometric(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_CalcFourierOptometric(self.instrument_handle,
                                                   self.zernike_orders,
                                                   self.fourier_orders,
                                                   ctypes.byref(self.fourier_m),
                                                   ctypes.byref(self.fourier_j0),
                                                   ctypes.byref(self.fourier_j45),
                                                   ctypes.byref(self.optometric_sphere),
                                                   ctypes.byref(self.optometric_cylinder),
                                                   ctypes.byref(self.optometric_axis))
        log_wfs.debug('Calc Fourier Optometric: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Zernike Orders: {0}'.format(self.zernike_orders.value))
        log_wfs.info('Fourier Orders: {0}'.format(self.fourier_orders.value))
        log_wfs.info('Fourier Coefficient M: {0}'.format(self.fourier_m.value))
        log_wfs.info('Fourier Coefficient J0: {0}'.format(self.fourier_j0.value))
        log_wfs.info('Fourier Coefficient J45: {0}'.format(self.fourier_j45.value))
        log_wfs.info('Optometric Parameter Sphere (diopters): {0}'.format(self.optometric_sphere.value))
        log_wfs.info('Optometric Parameter Cylinder (diopters): {0}'.format(self.optometric_cylinder.value))
        log_wfs.info('Optometric Parameter Axis (°): {0}'.format(self.optometric_axis.value))
        self._error_message(status)
        return status

    def _calc_reconstructed_deviations(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_CalcReconstrDeviations(self.instrument_handle,
                                                    self.zernike_orders,
                                                    self.array_zernike_reconstructed,
                                                    self.do_spherical_reference,
                                                    ctypes.byref(self.fit_error_mean),
                                                    ctypes.byref(self.fit_error_stdev))
        log_wfs.debug('Calc Reconstructed Deviations: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Zernike Orders: {0}'.format(self.zernike_orders.value))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row])
                                 for row in self.array_zernike_reconstructed]))
        log_wfs.info('Do Spherical Reference: {0}'.format(self.do_spherical_reference.value))
        log_wfs.info('Fit Error Mean: {0}'.format(self.fit_error_mean.value))
        log_wfs.info('Fit Error Standard Deviation: {0}'.format(self.fit_error_stdev.value))
        self._error_message(status)
        return status

    def _calc_wavefront(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_CalcWavefront(self.instrument_handle,
                                           self.wavefront_type,
                                           self.limit_to_pupil,
                                           self.array_wavefront)
        log_wfs.debug('Calc Wavefront: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Wavefront Type: {0}'.format(self.wavefront_type.value))
        log_wfs.info('Limit to Pupil: {0}'.format(self.limit_to_pupil.value))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.array_wavefront]))
        self._error_message(status)
        return status

    def _calc_wavefront_statistics(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_CalcWavefrontStatistics(self.instrument_handle,
                                                     ctypes.byref(self.wavefront_min),
                                                     ctypes.byref(self.wavefront_max),
                                                     ctypes.byref(self.wavefront_diff),
                                                     ctypes.byref(self.wavefront_mean),
                                                     ctypes.byref(self.wavefront_rms),
                                                     ctypes.byref(self.wavefront_weighted_rms))
        log_wfs.debug('Calc Wavefront Statistics: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Min: {0}'.format(self.wavefront_min.value))
        log_wfs.info('Max: {0}'.format(self.wavefront_max.value))
        log_wfs.info('Diff: {0}'.format(self.wavefront_diff.value))
        log_wfs.info('Mean: {0}'.format(self.wavefront_mean.value))
        log_wfs.info('RMS: {0}'.format(self.wavefront_rms.value))
        log_wfs.info('Weighted RMS: {0}'.format(self.wavefront_weighted_rms.value))
        self._error_message(status)
        return status

    # Utility Functions
    def _self_test(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_self_test(self.instrument_handle,
                                       ctypes.byref(self.test_result),
                                       self.test_message)
        log_wfs.debug('Self Test: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Self Test Result: {0}'.format(self.test_result.value))
        log_wfs.info('Self Test Message: {0}'.format(self.test_message.value))
        self._error_message(status)
        return status

    def _reset(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_reset(self.instrument_handle)
        log_wfs.debug('Reset: {0}'.format(self.instrument_handle.value))
        self._error_message(status)
        return status

    def _revision_query(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_revision_query(self.instrument_handle,
                                            self.instrument_driver_revision,
                                            self.firmware_revision)
        log_wfs.debug('Revision Query: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Instrument Driver Version: {0}'.format(self.instrument_driver_revision.value))
        log_wfs.info('Instrument Firmware Version: {0}'.format(self.firmware_revision.value))
        self._error_message(status)
        return status

    def _error_query(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_error_query(self.instrument_handle,
                                         ctypes.byref(self.error_code),
                                         self.error_message)
        if status == self.WFS_WARN_NSUP_ERROR_QUERY:
            log_wfs.debug('Error query not supported')
            return 0
        log_wfs.debug('Error Query: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Error Code: {0}'.format(self.error_code.value))
        log_wfs.error('Error Message: {0}'.format(self.error_message.value))
        return status

    def _error_message(self, error_code=0, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        try:
            self.error_code = Vi.session(error_code)
        except TypeError:
            self.error_code = error_code
        if self.error_code.value == 0:
            # log_wfs.debug('Error Message: {0}'.format(self.instrument_handle.value))
            log_wfs.debug('No error: {0}'.format(self.error_code.value))
            return 0
        status = lib_wfs.WFS_error_message(self.instrument_handle,
                                           self.error_code,
                                           self.error_message)
        # log_wfs.debug('Error Message: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Error Code: {0}'.format(self.error_code.value))
        log_wfs.error('Error Message: {0}'.format(self.error_message.value))
        return status

    def _get_instrument_list_len(self,
                                 instrument_handle=Vi.null):
        if instrument_handle is not Vi.null:
            try:
                instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                instrument_handle = instrument_handle
        else:
            instrument_handle = Vi.session(instrument_handle)
        status = lib_wfs.WFS_GetInstrumentListLen(instrument_handle,
                                                  ctypes.byref(self.instrument_count))
        self.instrument_index = Vi.int32(self.instrument_count.value - 1)
        log_wfs.debug('Get Instrument List Length: {0}'.format(instrument_handle.value))
        log_wfs.debug('Instrument Count: {0}'.format(self.instrument_count.value))
        log_wfs.info('Instrument Index: {0}'.format(self.instrument_index.value))
        self._error_message(status)
        return status

    def _get_instrument_list_info(self,
                                  instrument_handle=Vi.null,
                                  instrument_index=None):
        # TODO TODO
        if instrument_handle is not Vi.null:
            try:
                instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                instrument_handle = instrument_handle
        else:
            instrument_handle = Vi.session(instrument_handle)
        if instrument_index is not None:
            try:
                self.instrument_index = Vi.int32(instrument_index)
            except TypeError:
                self.instrument_index = instrument_index
        print(repr(self.instrument_name_wfs.value))
        print(repr(self.serial_number_wfs.value))
        print(repr(self.resource_name.value))
        print(type(self.instrument_name_wfs))
        print(type(self.serial_number_wfs))
        print(type(self.resource_name))
        lib_wfs.WFS_GetInstrumentListInfo.argtypes = [ctypes.c_ulong,
                                                      ctypes.c_long,
                                                      ctypes.POINTER(ctypes.c_long),
                                                      ctypes.POINTER(ctypes.c_long),
                                                      ctypes.c_char_p,
                                                      ctypes.c_char_p,
                                                      ctypes.c_char_p]
        lib_wfs.WFS_GetInstrumentListInfo.restypes = ctypes.c_long
        status = lib_wfs.WFS_GetInstrumentListInfo(instrument_handle,
                                                   self.instrument_index,
                                                   ctypes.byref(self.device_id),
                                                   ctypes.byref(self.in_use),
                                                   self.instrument_name_wfs,
                                                   self.serial_number_wfs,
                                                   self.resource_name)
        log_wfs.debug('Get Instrument List Info: {0}'.format(instrument_handle.value))
        log_wfs.info('Instrument Index: {0}'.format(self.instrument_index.value))
        log_wfs.info('Device ID: {0}'.format(self.device_id.value))
        log_wfs.info('In Use: {0}'.format(self.in_use.value))
        log_wfs.info('Instrument Name WFS: {0}'.format(self.instrument_name_wfs.value))
        log_wfs.info('Serial Number WFS: {0}'.format(self.serial_number_wfs.value))
        log_wfs.info('Resource Name: {0}'.format(self.resource_name.value))
        self._error_message(status)
        return status

    def _get_xy_scale(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_GetXYScale(self.instrument_handle,
                                        self.array_scale_x,
                                        self.array_scale_y)
        log_wfs.debug('Get XY Scale: {0}'.format(self.instrument_handle.value))
        log_wfs.debug('Array Scale X:' + ''.join(['{:18}'.format(item) for item in self.array_scale_x]))
        log_wfs.debug('Array Scale Y:' + ''.join(['{:18}'.format(item) for item in self.array_scale_y]))
        self._error_message(status)
        return status

    def _convert_wavefront_waves(self, instrument_handle=None, wavelength=None, array_wavefront=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        if wavelength is not None:
            try:
                self.wavelength = Vi.real64(wavelength)
            except TypeError:
                self.wavelength = wavelength
        if array_wavefront is not None:
            # try:
            #     self.array_wavefront = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
            # except TypeError:
            #     self.array_wavefront = array_wavefront
            self.array_wavefront = array_wavefront
        status = lib_wfs.WFS_ConvertWavefrontWaves(self.instrument_handle,
                                                   self.wavelength,
                                                   self.array_wavefront,
                                                   self.array_wavefront_waves)
        log_wfs.debug('Convert Wavefront to Waves: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Wavelength: {0}'.format(self.wavelength.value))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.array_wavefront]))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.array_wavefront_waves]))
        self._error_message(status)
        return status

    def _flip_2d_array(self, instrument_handle=None, array_wavefront_yx=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        if array_wavefront_yx is not None:
            # try:
            #     self.array_wavefront_yx = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
            # except TypeError:
            #     self.array_wavefront_yx = array_wavefront_yx
            self.array_wavefront_yx = array_wavefront_yx
        status = lib_wfs.WFS_Flip2DArray(self.instrument_handle,
                                         self.array_wavefront_yx,
                                         self.array_wavefront_xy)
        log_wfs.debug('Flip 2D Array: {0}'.format(self.instrument_handle.value))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.array_wavefront_yx]))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.array_wavefront_xy]))
        self._error_message(status)
        return status

    # Calibration Functions
    def _set_spots_to_user_reference(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_SetSpotsToUserReference(self.instrument_handle)
        log_wfs.debug('Set Spots To User Reference: {0}'.format(self.instrument_handle.value))
        self._error_message(status)
        return status

    def _set_calc_spots_to_user_reference(self, instrument_handle=None, spot_ref_type=None,
                                          array_reference_x=None, array_reference_y=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        if spot_ref_type is not None:
            try:
                self.spot_ref_type = Vi.int32(spot_ref_type)
            except TypeError:
                self.spot_ref_type = spot_ref_type
        if array_reference_x is not None:
            # try:
            #     self.array_reference_x = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
            # except TypeError:
            #     self.array_reference_x = array_reference_x
            self.array_reference_x = array_reference_x
        if array_reference_y is not None:
            # try:
            #     self.array_reference_y = ((ctypes.c_float * self.MAX_SPOTS_X) * self.MAX_SPOTS_Y)()
            # except TypeError:
            #     self.array_reference_y = array_reference_y
            self.array_reference_y = array_reference_y
        status = lib_wfs.WFS_SetCalcSpotsToUserReference(self.instrument_handle,
                                                         self.spot_ref_type,
                                                         self.array_reference_x,
                                                         self.array_reference_y)
        log_wfs.debug('Set Calc Spots to User Reference: {0}'.format(self.instrument_handle.value))
        log_wfs.info('Spot Reference Type: {0}'.format(self.spot_ref_type.value))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.array_reference_x]))
        log_wfs.debug('\n'.join([''.join(['{:16}'.format(item) for item in row]) for row in self.array_reference_y]))
        self._error_message(status)
        return status

    def _create_default_user_reference(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_CreateDefaultUserReference(self.instrument_handle)
        log_wfs.debug('Create Default User Reference: {0}'.format(self.instrument_handle.value))
        self._error_message(status)
        return status

    def _save_user_reference_file(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_SaveUserRefFile(self.instrument_handle)
        log_wfs.debug('Save User Reference: {0}'.format(self.instrument_handle.value))
        self._error_message(status)
        return status

    def _load_user_reference_file(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_LoadUserRefFile(self.instrument_handle)
        log_wfs.debug('Load User Reference: {0}'.format(self.instrument_handle.value))
        self._error_message(status)
        return status

    def _do_spherical_reference(self, instrument_handle=None):
        if instrument_handle is not None:
            try:
                self.instrument_handle = Vi.session(instrument_handle)
            except TypeError:
                self.instrument_handle = instrument_handle
        status = lib_wfs.WFS_DoSphericalRef(self.instrument_handle)
        log_wfs.debug('Do Spherical Reference: {0}'.format(self.instrument_handle.value))
        self._error_message(status)
        return status

    def connect(self):
        self._get_instrument_list_len()
        self._get_instrument_list_info()
        self._init(id_query=1, reset_device=1)
        self._revision_query()
        self._get_instrument_info()
        self._get_mla_count()
        self._get_mla_data()
        self._select_mla()
        self._configure_cam()
        self._set_reference_plane(0)
        self._set_pupil()
        self._get_status()

    def update(self):
        if self.allow_auto_exposure.value == 1:
            self._take_spotfield_image_auto_exposure()
        else:
            self._take_spotfield_image()
        self._get_spotfield_image()
        self._calc_spots_centroid_diameter_intensity()
        self._get_spot_centroids()
        self._calc_beam_centroid_diameter()
        self._calc_spot_to_reference_deviations()
        self._get_spot_deviations()
        self._calc_wavefront()
        self._calc_wavefront_statistics()
        self._zernike_lsf()

    def testing(self, var):
        print(var)


if __name__ == '__main__':
    wfs = WFS()
