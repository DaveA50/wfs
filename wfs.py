# -*- coding: utf-8 -*-
"""Wrapper for interfacing with the Thorlabs Wavefront Sensor (WFS)."""
import ctypes
from ctypes.util import find_library
import logging.config
import os

import yaml

from vi import Vi

__version__ = '0.5.0'
__author__ = 'David Amrhein'
__email__ = 'davea50@gmail.com'


def setup_logging(path='logging.yaml', level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration.

    Uses logging.yaml for the default configuration.

    Args:
        path:
        level:
        env_key:
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


class WFS(object):
    """Thorlabs Shack-Hartmann Wavefront Sensor Interface."""
    # Constants declared in WFS.h header file
    # Buffers
    WFS_BUFFER_SIZE = 256  # General buffer size
    WFS_ERR_DESCR_BUFFER_SIZE = 512  # Buffer size for error messages

    # Error/Warning Codes
    # max errors from camera driver
    MAX_CAM_DRIVER_ERRORS = 2000  # camera driver errors in range 1 ... MAX_CAM_DRIVER_ERRORS
    MAX_WFS_DEVICES = 5  # max 5 cams at the same time connected
    MAX_MLA_CALS = 7  # max. 7 MLA cals per device

    # Offsets
    WFS_ERROR = (-2147483647 - 1)  # 0x80000000, -2147483648
    WFS_INSTR_WARNING_OFFSET = 0x3FFC0900  # 1073481984
    WFS_INSTR_ERROR_OFFSET = WFS_ERROR + 0x3FFC0900  # 0xBFFC0900, -1074001664

    # WFS Driver Error Codes; error texts defined in WFS_ErrorMessage()
    WFS_SUCCESS = 0

    WFS_ERROR_PARAMETER1 = WFS_ERROR + 0x3FFC0001  # -1074003967
    WFS_ERROR_PARAMETER2 = WFS_ERROR + 0x3FFC0002  # -1074003966
    WFS_ERROR_PARAMETER3 = WFS_ERROR + 0x3FFC0003  # -1074003965
    WFS_ERROR_PARAMETER4 = WFS_ERROR + 0x3FFC0004  # -1074003964
    WFS_ERROR_PARAMETER5 = WFS_ERROR + 0x3FFC0005  # -1074003963
    WFS_ERROR_PARAMETER6 = WFS_ERROR + 0x3FFC0006  # -1074003962
    WFS_ERROR_PARAMETER7 = WFS_ERROR + 0x3FFC0007  # -1074003961
    WFS_ERROR_PARAMETER8 = WFS_ERROR + 0x3FFC0008  # -1074003960
    WFS_ERROR_PARAMETER9 = WFS_ERROR + 0x3FFC0009  # -1074003959
    WFS_ERROR_API_ID_NOT_SUPPORTED = 0x00000504

    WFS_ERROR_NO_SENSOR_CONNECTED = WFS_INSTR_ERROR_OFFSET + 0x00  # -1074001664
    WFS_ERROR_OUT_OF_MEMORY = WFS_INSTR_ERROR_OFFSET + 0x01  # -1074001663
    WFS_ERROR_INVALID_HANDLE = WFS_INSTR_ERROR_OFFSET + 0x02  # -1074001662
    WFS_ERROR_CAM_NOT_CONFIGURED = WFS_INSTR_ERROR_OFFSET + 0x03  # -1074001661
    WFS_ERROR_PIXEL_FORMAT = WFS_INSTR_ERROR_OFFSET + 0x04  # -1074001660
    WFS_ERROR_EEPROM_CHECKSUM = WFS_INSTR_ERROR_OFFSET + 0x05  # -1074001659
    WFS_ERROR_EEPROM_CAL_DATA = WFS_INSTR_ERROR_OFFSET + 0x06  # -1074001658
    WFS_ERROR_OLD_REF_FILE = WFS_INSTR_ERROR_OFFSET + 0x07  # -1074001657
    WFS_ERROR_NO_REF_FILE = WFS_INSTR_ERROR_OFFSET + 0x08  # -1074001656
    WFS_ERROR_CORRUPT_REF_FILE = WFS_INSTR_ERROR_OFFSET + 0x09  # -1074001655
    WFS_ERROR_WRITE_FILE = WFS_INSTR_ERROR_OFFSET + 0x0a  # -1074001654
    WFS_ERROR_INSUFF_SPOTS_FOR_ZERNFIT = WFS_INSTR_ERROR_OFFSET + 0x0b  # -1074001653
    WFS_ERROR_TOO_MANY_SPOTS_FOR_ZERNFIT = WFS_INSTR_ERROR_OFFSET + 0x0c  # -1074001652
    WFS_ERROR_FOURIER_ORDER = WFS_INSTR_ERROR_OFFSET + 0x0d  # -1074001651
    WFS_ERROR_NO_RECON_DEVIATIONS = WFS_INSTR_ERROR_OFFSET + 0x0e  # -1074001650
    WFS_ERROR_NO_PUPIL_DEFINED = WFS_INSTR_ERROR_OFFSET + 0x0f  # -1074001649
    WFS_ERROR_WRONG_PUPIL_DIA = WFS_INSTR_ERROR_OFFSET + 0x10  # -1074001648
    WFS_ERROR_WRONG_PUPIL_CTR = WFS_INSTR_ERROR_OFFSET + 0x11  # -1074001647
    WFS_ERROR_INVALID_CAL_DATA = WFS_INSTR_ERROR_OFFSET + 0x12  # -1074001646
    WFS_ERROR_INTERNAL_REQUIRED = WFS_INSTR_ERROR_OFFSET + 0x13  # -1074001645
    WFS_ERROR_ROC_RANGE = WFS_INSTR_ERROR_OFFSET + 0x14  # -1074001644
    WFS_ERROR_NO_USER_REFERENCE = WFS_INSTR_ERROR_OFFSET + 0x15  # -1074001643
    WFS_ERROR_AWAITING_TRIGGER = WFS_INSTR_ERROR_OFFSET + 0x16  # -1074001642
    WFS_ERROR_NO_HIGHSPEED = WFS_INSTR_ERROR_OFFSET + 0x17  # -1074001641
    WFS_ERROR_HIGHSPEED_ACTIVE = WFS_INSTR_ERROR_OFFSET + 0x18  # -1074001640
    WFS_ERROR_HIGHSPEED_NOT_ACTIVE = WFS_INSTR_ERROR_OFFSET + 0x19  # -1074001639
    WFS_ERROR_HIGHSPEED_WINDOW_MISMATCH = WFS_INSTR_ERROR_OFFSET + 0x1a  # -1074001638
    WFS_ERROR_NOT_SUPPORTED = WFS_INSTR_ERROR_OFFSET + 0x1b  # -1074001637

    # returned from non-exported functions
    WFS_ERROR_SPOT_TRUNCATED = WFS_INSTR_ERROR_OFFSET + 0x1b  # -1074001637
    WFS_ERROR_NO_SPOT_DETECTED = WFS_INSTR_ERROR_OFFSET + 0x1c  # -1074001636
    WFS_ERROR_TILT_CALCULATION = WFS_INSTR_ERROR_OFFSET + 0x1d  # -1074001635

    # WFS Driver Warning Codes
    WFS_WARNING = WFS_INSTR_WARNING_OFFSET + 0x00  # 1073481984
    WFS_WARN_NSUP_ID_QUERY = 0x3FFC0101  # 1073479937
    WFS_WARN_NSUP_RESET = 0x3FFC0102  # 1073479938
    WFS_WARN_NSUP_SELF_TEST = 0x3FFC0103  # 1073479939
    WFS_WARN_NSUP_ERROR_QUERY = 0x3FFC0104  # 1073479940
    WFS_WARN_NSUP_REV_QUERY = 0x3FFC0105  # 1073479941
    WFS_WARNING_CODES = {WFS_WARN_NSUP_ID_QUERY: b'Identification query not supported!',
                         WFS_WARN_NSUP_RESET: b'Reset not supported!',
                         WFS_WARN_NSUP_SELF_TEST: b'Self-test not supported!',
                         WFS_WARN_NSUP_ERROR_QUERY: b'Error query not supported!',
                         WFS_WARN_NSUP_REV_QUERY: b'Instrument revision query not supported!'}

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
    WFS_STATBIT_SPC = 0x00000400  # Number of spots or pupil or aoi has been changed
    WFS_STATBIT_RDA = 0x00000800  # Reconstructed spot deviations available
    WFS_STATBIT_URF = 0x00001000  # User reference data available
    WFS_STATBIT_HSP = 0x00002000  # Camera is in Highspeed Mode
    WFS_STATBIT_MIS = 0x00004000  # Mismatched centroids in Highspeed Mode
    WFS_STATBIT_LOS = 0x00008000  # Low number of detected spots, warning: reduced Zernike accuracy
    WFS_STATBIT_FIL = 0x00010000  # Pupil is badly filled with spots, warning: reduced Zernike accuracy
    WFS_DRIVER_STATUS = {WFS_STATBIT_CON: b'USB connection lost, set by driver',
                         WFS_STATBIT_PTH: b'Power too high (cam saturated)',
                         WFS_STATBIT_PTL: b'Power too low (low cam digits)',
                         WFS_STATBIT_HAL: b'High ambient light',
                         WFS_STATBIT_SCL: b'Spot contrast too low',
                         WFS_STATBIT_ZFL: b'Zernike fit failed because of not enough detected spots',
                         WFS_STATBIT_ZFH: b'Zernike fit failed because of too many detected spots',
                         WFS_STATBIT_ATR: b'Camera is still awaiting a trigger',
                         WFS_STATBIT_CFG: b'Camera is configured, ready to use',
                         WFS_STATBIT_PUD: b'Pupil is defined',
                         WFS_STATBIT_SPC: b'Number of spots or pupil or aoi has been changed',
                         WFS_STATBIT_RDA: b'Reconstructed spot deviations available',
                         WFS_STATBIT_URF: b'User reference data available',
                         WFS_STATBIT_HSP: b'Camera is in Highspeed Mode',
                         WFS_STATBIT_MIS: b'Mismatched centroids in Highspeed Mode',
                         WFS_STATBIT_LOS: b'Low number of detected spots, warning: reduced Zernike accuracy',
                         WFS_STATBIT_FIL: b'Pupil is badly filled with spots, warning: reduced Zernike accuracy'}

    # Timeout
    # * 10 ms = 24 hours, given to is_SetTimeout, after that time is_IsVideoFinish returns 'finish' without error
    WFS_TRIG_TIMEOUT = 100 * 60 * 60 * 24  # 8640000
    WFS_TIMEOUT_CAPTURE_NORMAL = 5.0  # in seconds
    WFS_TIMEOUT_CAPTURE_TRIGGER = 0.1  # in seconds, allow fast return of functions WFS_TakeSpotfieldImage...
    WFS10_TIMEOUT_CAPTURE_NORMAL = 4000  # in ms, allow 500 ms exposure time + reserve
    WFS10_TIMEOUT_CAPTURE_TRIGGER = 100  # in ms, allow fast return of functions WFS_TakeSpotfieldImage...
    WFS20_TIMEOUT_CAPTURE_NORMAL = 4000  # in ms, allow 84 ms exposure time + reserve
    WFS20_TIMEOUT_CAPTURE_TRIGGER = 100  # in ms, allow fast return of functions WFS_TakeSpotfieldImage...

    # Exported constants
    WFS_TRUE = 1
    WFS_FALSE = 0

    # Defines for WFS camera
    EXPOSURE_MANUAL = 0
    EXPOSURE_AUTO = 1

    MASTER_GAIN_MIN_WFS = 1.0  # real gain factor, not 0 ... 100% percent
    MASTER_GAIN_MIN_WFS10 = 1.5  # 1.0 prevents ADC from saturation on overexposure
    MASTER_GAIN_MIN_WFS20 = 1.0
    MASTER_GAIN_MAX_WFS20 = 1.0
    MASTER_GAIN_MAX_WFS30 = 24.0
    MASTER_GAIN_MAX_WFS40 = 4.0
    MASTER_GAIN_MAX = 13.66
    MASTER_GAIN_MAX_DISPLAY = 5.0  # dark signal is too noisy for higher amplification
    MASTER_GAIN_EXPONENT = 38.26  # based on natural logarithm
    MASTER_GAIN_EXPONENT_WFS30 = 31.465
    MASTER_GAIN_FACTOR_WFS40 = 33.333

    NOISE_LEVEL_MIN = 0  # level for cutting spotfield
    NOISE_LEVEL_MAX = 256

    BLACK_LEVEL_MIN = 0
    BLACK_LEVEL_MAX = 255
    BLACK_LEVEL_WFS_DEF = 100  # lower values causes problems with auto-exposure and trigger (WFS)
    BLACK_LEVEL_WFS10_DEF = 100  # for cam shifted to 0 ... +15
    BLACK_LEVEL_WFS20_DEF = 0
    BLACK_LEVEL_WFS30_DEF = 0
    BLACK_LEVEL_WFS40_DEF = 0

    # Pixel format defines
    PIXEL_FORMAT_MONO8 = 0
    PIXEL_FORMAT_MONO16 = 1

    # pre-defined image sizes for WFS150/300 instruments
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
    CAM_MAX_PIX_X = 1440
    CAM_MAX_PIX_Y = 1080

    # pre-defined image sizes for WFS30 instruments
    CAM_RES_WFS30_1936 = 0  # 1936x1216
    CAM_RES_WFS30_1216 = 1  # 1216x1216
    CAM_RES_WFS30_1024 = 2  # 1024x1024
    CAM_RES_WFS30_768 = 3  # 768x768
    CAM_RES_WFS30_512 = 4  # 512x512
    CAM_RES_WFS30_360 = 5  # 360x360 smallest!
    CAM_RES_WFS30_968_SUB2 = 6  # 968x608, subsampling 2x2
    CAM_RES_WFS30_608_SUB2 = 7  # 608x608, subsampling 2x2
    CAM_RES_WFS30_512_SUB2 = 8  # 512x512, subsampling 2x2
    CAM_RES_WFS30_384_SUB2 = 9  # 384x384, subsampling 2x2
    CAM_RES_WFS30_256_SUB2 = 10  # 256x256, subsampling 2x2
    CAM_RES_WFS30_180_SUB2 = 11  # 180x180, subsampling 2x2
    CAM_RES_WFS30_MAX_IDX = 11

    # pre-defined image sizes for WFS40 instruments
    CAM_RES_WFS40_2048 = 0  # 2048x2048
    CAM_RES_WFS40_1536 = 1  # 1536x1536
    CAM_RES_WFS40_1024 = 2  # 1024x1024
    CAM_RES_WFS40_768 = 3  # 768x768
    CAM_RES_WFS40_512 = 4  # 512x512
    CAM_RES_WFS40_360 = 5  # 360x360 smallest!
    CAM_RES_WFS40_1024_SUB2 = 6  # 1024x1024, subsampling 2x2
    CAM_RES_WFS40_768_SUB2 = 7  # 608x608, subsampling 2x2
    CAM_RES_WFS40_512_SUB2 = 8  # 512x512, subsampling 2x2
    CAM_RES_WFS40_384_SUB2 = 9  # 384x384, subsampling 2x2
    CAM_RES_WFS40_256_SUB2 = 10  # 256x256, subsampling 2x2
    CAM_RES_WFS40_180_SUB2 = 11  # 180x180, subsampling 2x2
    CAM_RES_WFS40_MAX_IDX = 11

    # Hardware trigger modes
    WFS_HW_TRIGGER_OFF = 0
    WFS_HW_TRIGGER_HL = 1
    WFS_HW_TRIGGER_LH = 2
    WFS_SW_TRIGGER = 3
    WFS_TRIGGER_MODE_MIN = WFS_HW_TRIGGER_OFF
    WFS_TRIGGER_MODE_MAX = WFS_SW_TRIGGER

    # Averaging
    AVERAGE_COUNT_MAX = 256

    # Pupil
    PUPIL_DIA_MIN_MM = 0.5  # for coarse check only
    PUPIL_DIA_MAX_MM = 12.0
    PUPIL_CTR_MIN_MM = -8.0
    PUPIL_CTR_MAX_MM = 8.0

    # Wavefront types
    WAVEFRONT_MEAS = 0
    WAVEFRONT_REC = 1
    WAVEFRONT_DIFF = 2

    # Max number of detectable spots
    MAX_SPOTS_X = 80  # WFS30: 1936 * 5.86 / 150 = 75.6; WFS40: 2048 * 5.5 / 150 = 75.1
    MAX_SPOTS_Y = 80  # WFS40: 2048 * 5.5 / 150 = 75.1
    # MAX_SPOTS_X = 47  # WFS20: 1440*5/150 - 1 = 47
    # MAX_SPOTS_Y = 35  # WFS20: 1080*5/150 - 1 = 35

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
        setup_logging()
        self.log_wfs = logging.getLogger('WFS')
        self.lib = self.find_wfs_library()
        self.adapt_centroids = Vi.int32(0)
        self.allow_auto_exposure = Vi.int32(1)
        self.array_centroid_x = Vi.array_float(self.MAX_SPOTS_X, self.MAX_SPOTS_Y)
        self.array_centroid_y = Vi.array_float(self.MAX_SPOTS_X, self.MAX_SPOTS_Y)
        self.array_deviations_x = Vi.array_float(self.MAX_SPOTS_X, self.MAX_SPOTS_Y)
        self.array_deviations_y = Vi.array_float(self.MAX_SPOTS_X, self.MAX_SPOTS_Y)
        self.array_diameter_x = Vi.array_float(self.MAX_SPOTS_X, self.MAX_SPOTS_Y)
        self.array_diameter_y = Vi.array_float(self.MAX_SPOTS_X, self.MAX_SPOTS_Y)
        self.array_image_buffer = Vi.array_uint8(self.CAM_MAX_PIX_X, self.CAM_MAX_PIX_Y)
        self.array_image_buffer_ref = Vi.array_uint8(self.WFS_BUFFER_SIZE)
        self.array_intensity = Vi.array_float(self.MAX_SPOTS_X, self.MAX_SPOTS_Y)
        self.array_line_max = Vi.array_float(self.CAM_MAX_PIX_X)
        self.array_line_min = Vi.array_float(self.CAM_MAX_PIX_X)
        self.array_line_selected = Vi.array_float(self.CAM_MAX_PIX_X)
        self.array_reference_x = Vi.array_float(self.MAX_SPOTS_X, self.MAX_SPOTS_Y)
        self.array_reference_y = Vi.array_float(self.MAX_SPOTS_X, self.MAX_SPOTS_Y)
        self.array_scale_x = Vi.array_float(self.MAX_SPOTS_X)
        self.array_scale_y = Vi.array_float(self.MAX_SPOTS_Y)
        self.array_wavefront = Vi.array_float(self.MAX_SPOTS_X, self.MAX_SPOTS_Y)
        self.array_wavefront_wave = Vi.array_float(self.MAX_SPOTS_X, self.MAX_SPOTS_Y)
        self.array_wavefront_xy = Vi.array_float(self.MAX_SPOTS_Y, self.MAX_SPOTS_X)
        self.array_wavefront_yx = Vi.array_float(self.MAX_SPOTS_X, self.MAX_SPOTS_Y)
        self.array_zernike_orders_um = Vi.array_float((self.MAX_ZERNIKE_ORDERS + 1))
        self.array_zernike_reconstructed = Vi.array_uint8(self.MAX_ZERNIKE_MODES + 1)
        self.array_zernike_um = Vi.array_float(self.MAX_ZERNIKE_MODES + 1)
        self.average_count = Vi.int32(1)
        self.average_data_ready = Vi.int32(0)
        self.aoi_center_x_mm = Vi.real64(0)
        self.aoi_center_y_mm = Vi.real64(0)
        self.aoi_size_x_mm = Vi.real64(0)  # 0 is full sensor size
        self.aoi_size_y_mm = Vi.real64(0)  # 0 is full sensor size
        self.beam_centroid_x_mm = Vi.real64(0)
        self.beam_centroid_y_mm = Vi.real64(0)
        self.beam_diameter_x_mm = Vi.real64(0)
        self.beam_diameter_y_mm = Vi.real64(0)
        self.black_level_offset_actual = Vi.int32(0)
        self.black_level_offset_set = Vi.int32(100)
        self.calculate_diameters = Vi.int32(1)
        self.cam_pitch_um = Vi.real64(0)
        self.cam_resolution_index = Vi.int32(0)
        self.cam_resolution_factor = Vi.int32(1)
        self.cam_resolution_x = Vi.int32(0)
        self.cam_resolution_y = Vi.int32(0)
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
        self.exposure_time_increment = Vi.real64(0.005)
        self.exposure_time_max = Vi.real64(83.3479995727539)
        self.exposure_time_min = Vi.real64(0.01)
        self.exposure_time_set = Vi.real64(0.0793666666667)
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
        self.intensity_limit = Vi.int32(1)
        self.intensity_max = Vi.int32(0)
        self.intensity_min = Vi.int32(0)
        self.intensity_mean = Vi.real64(0)
        self.intensity_rms = Vi.real64(0)
        self.in_use = Vi.int32(0)
        self.instrument_count = Vi.int32(0)
        self.instrument_driver_revision = Vi.char(self.WFS_BUFFER_SIZE)
        self.instrument_handle = Vi.session(Vi.NULL)
        self.instrument_index = Vi.int32(0)
        self.instrument_name_wfs = Vi.char(self.WFS_BUFFER_SIZE)
        self.lenslet_focal_length_um = Vi.real64(0)
        self.lenslet_pitch_um = Vi.real64(0)
        self.limit_to_pupil = Vi.int32(0)
        self.line = Vi.int32(0)
        self.manufacturer_name = Vi.char(self.WFS_BUFFER_SIZE)
        self.master_gain_actual = Vi.real64(0)
        self.master_gain_max = Vi.real64(1)
        self.master_gain_min = Vi.real64(1)
        self.master_gain_set = Vi.real64(1)
        self.mla_count = Vi.int32(1)
        self.mla_index = Vi.int32(0)
        self.mla_name = Vi.char(self.WFS_BUFFER_SIZE)
        self.optometric_axis = Vi.real64(0)
        self.optometric_cylinder = Vi.real64(0)
        self.optometric_sphere = Vi.real64(0)
        self.pixel_format = Vi.int32(self.PIXEL_FORMAT_MONO8)
        self.pupil_center_x_mm = Vi.real64(0)
        self.pupil_center_y_mm = Vi.real64(0)
        self.pupil_diameter_x_mm = Vi.real64(5.4)  # Max diameter without clipping edges
        self.pupil_diameter_y_mm = Vi.real64(5.4)  # Max diameter without clipping edges
        self.reference_index = Vi.int32(0)
        self.reset_device = Vi.boolean(0)
        self.resource_name = Vi.rsrc(self.WFS_BUFFER_SIZE, b'USB::0x1313::0x0000::1')
        self.roc_mm = Vi.real64(0)
        self.rolling_reset = Vi.int32(0)
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
        self.test_result = Vi.int16(0)
        self.test_message = Vi.char(self.WFS_BUFFER_SIZE)
        self.trigger_delay_actual = Vi.int32(0)
        self.trigger_delay_increment = Vi.int32(1)
        self.trigger_delay_max = Vi.int32(699000)
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
        self.zernike_orders = Vi.int32(4)  # 0=Auto, 2, 3, 4, 5, 6, 7, 8, 9, 10
        self.zernike_modes = Vi.int32(15)
        self.window_count_x = Vi.int32(0)
        self.window_count_y = Vi.int32(0)
        self.window_size_x = Vi.int32(0)
        self.window_size_y = Vi.int32(0)
        # self.window_start_position_x = Vi.int32(0)
        # self.window_start_position_y = Vi.int32(0)
        self.window_start_position_x = Vi.array_float(self.MAX_SPOTS_X)
        self.window_start_position_y = Vi.array_float(self.MAX_SPOTS_Y)

        # NAME = {Index: (x_res, y_res, sub_factor)}
        self.cam_res_WFS150 = {0: (1280, 1024, 1),
                               1: (1024, 1024, 1),
                               2: (768, 768, 1),
                               3: (512, 512, 1),
                               4: (320, 320, 1)}
        self.cam_res_WFS10 = {0: (640, 480, 1),
                              1: (480, 480, 1),
                              2: (360, 360, 1),
                              3: (260, 260, 1),
                              4: (180, 180, 1)}
        self.cam_res_WFS20 = {0: (1440, 1080, 1),
                              1: (1080, 1080, 1),
                              2: (768, 768, 1),
                              3: (512, 512, 1),
                              4: (360, 360, 1),
                              5: (720, 540, 2),
                              6: (540, 540, 2),
                              7: (384, 384, 2),
                              8: (256, 256, 2),
                              9: (180, 180, 2)}
        self.cam_res_WFS30 = {0: (1936, 1216, 1),
                              1: (1216, 1216, 1),
                              2: (1024, 1024, 1),
                              3: (768, 768, 1),
                              4: (512, 512, 1),
                              5: (360, 360, 1),
                              6: (968, 968, 2),
                              7: (608, 608, 2),
                              8: (512, 512, 2),
                              9: (384, 384, 2),
                              10: (256, 256, 2),
                              11: (180, 180, 2)}
        self.cam_res_WFS40 = {0: (2048, 2048, 1),
                              1: (1536, 1536, 1),
                              2: (1024, 1024, 1),
                              3: (768, 768, 1),
                              4: (512, 512, 1),
                              5: (360, 360, 1),
                              6: (1024, 1024, 2),
                              7: (768, 768, 2),
                              8: (512, 512, 2),
                              9: (384, 384, 2),
                              10: (256, 256, 2),
                              11: (180, 180, 2)}
        self.cam_res_id = {'WFS150': self.cam_res_WFS150,
                           'WFS10': self.cam_res_WFS10,
                           'WFS20': self.cam_res_WFS20,
                           'WFS30': self.cam_res_WFS30,
                           'WFS40': self.cam_res_WFS40}
        # Zernike Order: Zernike Modes
        self.zernike_modes_per_order = {2: 6,
                                        3: 10,
                                        4: 15,
                                        5: 21,
                                        6: 28,
                                        7: 36,
                                        8: 45,
                                        9: 55,
                                        10: 66}

    def find_wfs_library(self):
        """Find and load the WFS .dll in the system.
    
        Returns:
            ctypes.windll.LoadLibrary(WFS_32/64.dll)
        """
        bitness = ctypes.sizeof(ctypes.c_void_p) * 8  # =32 on x86, =64 on x64
        if bitness is 64:
            self.log_wfs.critical('64 bit Windows has OSError Access Violations')
            raise ImportError('64 bit Windows has OSError Access Violations')
        lib = find_library(f'WFS_{bitness}')
        if lib is None:
            self.log_wfs.critical(f'WFS_{bitness}.dll not found')
            raise ImportError(f'WFS_{bitness}.dll not found')
        _lib_wfs = ctypes.windll.LoadLibrary(lib)
        self.log_wfs.debug(f'{lib} loaded')
        return _lib_wfs

    # WFS Functions
    def _init(self, resource_name=None, id_query=None, reset_device=None):
        """Initializes the instrument driver session.

        Each time this function is invoked an unique session is opened.
        It Performs the following initialization actions:
        (1) Opens a session to the Default Resource Manager resource
            and a session to the selected device using the Resource
            Name.
        (2) Performs an identification query on the Instrument.
        (3) Resets the instrument to a known state.
        (4) Sends initialization commands to the instrument.
        (5) Returns an instrument handle which is used to differentiate
            between different sessions of this instrument driver.

        Args:
            resource_name (Vi.rsrc(int, str)): This parameter specifies the
                interface of the device that is to be initialized. The
                resource name has to follow the syntax:
                "USB::0x1313::0x0000::" followed by the Device ID.
                The Device ID can be gotten with the function
                _get_instrument_list_info E.g. "USB::0x1313::0x0000::1"
            id_query (Vi.boolean(int)): Performs an In-System
                Verification. Checks if the resource matches the vendor
                and product id.
            reset_device (Vi.boolean(int)): Performs Reset operation
                and places the instrument in a pre-defined reset state.

        Returns:
            status (Vi.status(int)): Operational return status.
                Contains either a completion code or an error code.
                Instrument driver specific codes that may be returned
                in addition to the VISA error codes defined in VPP-4.3
                and vendor specific codes, are as follows.
                Completion Codes:
                    WFS_SUCCESS: Initialization successful
                    WFS_WARN_NSUP_ID_QUERY: Identification query not
                                            supported
                    WFS_WARN_NSUP_RESET: Reset not supported
                Error Codes:
                    VI_ERROR_FAIL_ID_QUERY: Instrument identification
                                            query failed
            instrument_handle (Vi.session(int)): This parameter returns
                an instrument handle that is used in all subsequent
                calls to distinguish between different sessions of this
                instrument driver.
        """
        if resource_name is not None:
            try:
                self.resource_name = Vi.rsrc(self.WFS_BUFFER_SIZE, resource_name)
            except (TypeError, ValueError):
                self.resource_name = resource_name
        if id_query is not None:
            try:
                self.id_query = Vi.boolean(id_query)
            except ValueError:
                self.id_query = id_query
        if reset_device is not None:
            try:
                self.reset_device = Vi.boolean(reset_device)
            except ValueError:
                self.reset_device = reset_device
        status = self.lib.WFS_init(self.resource_name,
                                   self.id_query,
                                   self.reset_device,
                                   ctypes.byref(self.instrument_handle))
        self.log_wfs.info(f'Init: {self.instrument_handle.value}')
        self.log_wfs.info(f'Resource Name: {self.resource_name.value.decode()}')
        self.log_wfs.info(f'ID Query: {self.id_query.value}')
        self.log_wfs.info(f'Reset Device: {self.reset_device.value}')
        self._error_message(status)
        return status, self.instrument_handle.value

    def _get_status(self):
        """Get the device status of the Wavefront Sensor instrument.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            device_status (Vi.int32(int)): This parameter returns the
                device status of the Wavefront Sensor instrument.
                Lower 24 bits are used.
        """
        self.device_status = ctypes.c_ubyte(0)
        status = self.lib.WFS_GetStatus(self.instrument_handle,
                                        ctypes.byref(self.device_status))
        self.log_wfs.debug(f'Get Status: {self.instrument_handle.value}')
        self.log_wfs.info(f'Device Status: {self.device_status.value}')
        if self.device_status.value in self.WFS_DRIVER_STATUS:
            self.log_wfs.info(f'Device Status: {self.WFS_DRIVER_STATUS[self.device_status.value].decode()}')
        else:
            self.log_wfs.info('Device Status: OK/Unknown')
        self._error_message(status)
        return status, self.device_status.value

    def _close(self):
        """Closes the instrument driver session.

        Note: The instrument must be reinitialized to use it again.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        status = self.lib.WFS_close(self.instrument_handle)
        self.log_wfs.info(f'Close: {self.instrument_handle.value}')
        self.instrument_handle.value = Vi.NULL
        self._error_message(status)
        return status

    # Configuration Functions
    def _get_instrument_info(self):
        """Get information about the instrument names and serials.

        This function returns the following information about the
        opened instrument:
        - Driver Manufacturer Name
        - Instrument Name
        - Instrument Serial Number
        - Camera Serial Number

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            manufacturer_name (Vi.char(int)): This parameter returns
                the Manufacturer Name of this instrument driver.
                Note: The string must contain at least WFS_BUFFER_SIZE
                (256) elements (char(WFS_BUFFER_SIZE)).
            instrument_name_wfs (Vi.char(int)): This parameter returns
                the Instrument Name of the WFS.
                Note: The string must contain at least WFS_BUFFER_SIZE
                (256) elements (char(WFS_BUFFER_SIZE)).
            serial_number_wfs (Vi.char(int)): This parameter returns
                the Serial Number of the WFS.
                Note: The string must contain at least WFS_BUFFER_SIZE
                (256) elements (char(WFS_BUFFER_SIZE)).
            serial_number_camera (Vi.char(int)): This parameter returns
                the Serial Number of the camera body the WFS is based
                on.
                Note: The string must contain at least WFS_BUFFER_SIZE
                (256) elements (char(WFS_BUFFER_SIZE)).
        """
        status = self.lib.WFS_GetInstrumentInfo(self.instrument_handle,
                                                self.manufacturer_name,
                                                self.instrument_name_wfs,
                                                self.serial_number_wfs,
                                                self.serial_number_camera)
        self.log_wfs.debug(f'Get Instrument Info: {self.instrument_handle.value}')
        self.log_wfs.info(f'Manufacturer Name: {self.manufacturer_name.value.decode()}')
        self.log_wfs.info(f'Instrument Name WFS: {self.instrument_name_wfs.value.decode()}')
        self.log_wfs.info(f'Serial Number WFS: {self.serial_number_wfs.value.decode()}')
        self.log_wfs.info(f'Serial Number Camera: {self.serial_number_camera.value.decode()}')
        self._error_message(status)
        return (status, self.manufacturer_name.value, self.instrument_name_wfs.value,
                self.serial_number_wfs.value, self.serial_number_camera.value)

    def _configure_cam(self, cam_resolution_index=None, pixel_format=None):
        """Configure the WFS camera resolution and max spots in X and Y.

        This function configures the WFS instrument's camera resolution
        and returns the maximum number of detectable spots in X and Y
        direction. The result depends on the selected microlens array
        in function _select_mla()
        Note: This function is not available in Highspeed Mode!

        Args:
            cam_resolution_index (Vi.int32(int)): This parameter
                selects the camera resolution in pixels. Only the
                following pre-defined settings are supported:
                For WFS150/300 instruments:
                Index  Resolution
                0      1280x1024
                1      1024x1024
                2      768x768
                3      512x512
                4      320x320
                For WFS10 instruments:
                Index  Resolution
                0      640x480
                1      480x480
                2      360x360
                3      260x260
                4      180x180
                For WFS20 instruments:
                Index  Resolution
                0      1440x1080
                1      1080x1080
                2      768x768
                3      512x512
                4      360x360
                5      720x540, bin2
                6      540x540, bin2
                7      384x384, bin2
                8      256x256, bin2
                9      180x180, bin2
                For WFS30 instruments:
                Index  Resolution
                0      1936x1216
                1      1216x1216
                2      1024x1024
                3      768x768
                4      512x512
                5      360x360
                6      968x608, sub2
                7      608x608, sub2
                8      512x512, sub2
                9      384x384, sub2
                10     256x256, sub2
                11     180x180, sub2
                For WFS40 instruments:
                Index  Resolution
                0      2048x2048
                1      1536x1536
                2      1024x1024
                3      768x768
                4      512x512
                5      360x360
                6      1024x1024, sub2
                7      768x768, sub2
                8      512x512, sub2
                9      384x384, sub2
                10     256x256, sub2
                11     180x180, sub2

            pixel_format (Vi.int32(int)): This parameter selects the
                bit width per pixel of the returned camera image.
                Thorlabs WFS instruments currently support only 8 bit
                format.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            spots_x (Vi.int32(int)): This parameter returns the number
                of spots which can be detected in X direction, based
                on the selected camera resolution and Microlens Array
                in function _select_mla.
            spots_y (Vi.int32(int)): This parameter returns the number
                of spots which can be detected in Y direction, based
                on the selected camera resolution and Microlens Array
                in function _select_mla.
        """
        if cam_resolution_index is not None:
            try:
                self.cam_resolution_index = Vi.int32(cam_resolution_index)
            except ValueError:
                self.cam_resolution_index = cam_resolution_index
        if pixel_format is not None:
            try:
                self.pixel_format = Vi.int32(pixel_format)
            except ValueError:
                self.pixel_format = pixel_format
        status = self.lib.WFS_ConfigureCam(self.instrument_handle,
                                           self.pixel_format,
                                           self.cam_resolution_index,
                                           ctypes.byref(self.spots_x),
                                           ctypes.byref(self.spots_y))
        cam_id = self.instrument_name_wfs.value.decode().split('-', 1)[0]  # Remove text after '-'
        self.cam_resolution_x.value = self.cam_res_id[cam_id][self.cam_resolution_index.value][0]
        self.cam_resolution_y.value = self.cam_res_id[cam_id][self.cam_resolution_index.value][1]
        self.cam_resolution_factor.value = self.cam_res_id[cam_id][self.cam_resolution_index.value][2]
        self.log_wfs.debug(f'Configure Cam: {self.instrument_handle.value}')
        self.log_wfs.info(f'Pixel Format: {self.pixel_format.value}')
        self.log_wfs.info(f'Camera Resolution Index: {self.cam_resolution_index.value}')
        self.log_wfs.info(f'Camera Resolution X: {self.cam_resolution_x.value}')
        self.log_wfs.info(f'Camera Resolution Y: {self.cam_resolution_y.value}')
        self.log_wfs.info(f'Camera Resolution Factor: {self.cam_resolution_factor.value}')
        self.log_wfs.info(f'Spots X: {self.spots_x.value}')
        self.log_wfs.info(f'Spots Y: {self.spots_y.value}')
        self._error_message(status)
        return status, self.spots_x.value, self.spots_y.value

    def _set_highspeed_mode(self, highspeed_mode=None, adapt_centroids=None, subtract_offset=None,
                            allow_auto_exposure=None):
        """Set the WFS to use Highspeed mode.

        This function activates/deactivates the camera's Highspeed Mode
        for WFS10/WFS20 instruments. When activated, the camera
        calculates the spot centroid positions internally and sends the
        result to the WFS driver instead of sending raw spotfield
        images.
        Note: There is no camera image available when Highspeed Mode is
        activated! Highspeed Mode is not available for
        WFS150/WFS300/WFS30/WFS40 instruments!

        Args:
            highspeed_mode (Vi.int32(int)): This parameter determines
                if the camera's Highspeed Mode is switched on or off.
            adapt_centroids (Vi.int32(int)): When Highspeed Mode is
                selected, this parameter determines if the centroid
                positions measured in Normal Mode should be used to
                adapt the spot search windows for Highspeed Mode.
                Otherwise, a rigid grid based on reference spot
                positions is used in Highspeed Mode.
            subtract_offset (Vi.int32(int)): This parameter defines an
                offset level for Highspeed Mode only. All camera pixels
                will be subtracted by this level before the centroids
                are being calculated, which increases accuracy.
                Valid range: 0 ... 255
                Note: The offset is only valid in Highspeed Mode and
                must not set too high to clear the spots within the
                camera image!
            allow_auto_exposure (Vi.int32(int)): When Highspeed Mode is
                selected, this parameter determines if the camera
                should also calculate the image saturation in order
                enable the auto exposure feature using function
                _take_spotfield_image_auto_exposure() instead of
                _take_spotfield_image(). This option leads to a
                somewhat reduced measurement speed when enabled.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        if highspeed_mode is not None:
            try:
                self.highspeed_mode = Vi.int32(highspeed_mode)
            except ValueError:
                self.highspeed_mode = highspeed_mode
        if adapt_centroids is not None:
            try:
                self.adapt_centroids = Vi.int32(adapt_centroids)
            except ValueError:
                self.adapt_centroids = adapt_centroids
        if subtract_offset is not None:
            try:
                self.subtract_offset = Vi.int32(subtract_offset)
            except ValueError:
                self.subtract_offset = subtract_offset
        if allow_auto_exposure is not None:
            try:
                self.allow_auto_exposure = Vi.int32(allow_auto_exposure)
            except ValueError:
                self.allow_auto_exposure = allow_auto_exposure
        status = self.lib.WFS_SetHighspeedMode(self.instrument_handle,
                                               self.highspeed_mode,
                                               self.adapt_centroids,
                                               self.subtract_offset,
                                               self.allow_auto_exposure)
        self.log_wfs.debug(f'Set Highspeed Mode: {self.instrument_handle.value}')
        self.log_wfs.info(f'Highspeed Mode: {self.highspeed_mode.value}')
        self.log_wfs.info(f'Adapt Centroids: {self.adapt_centroids.value}')
        self.log_wfs.info(f'Subtract Offset: {self.subtract_offset.value}')
        self.log_wfs.info(f'Allow Auto Exposure: {self.allow_auto_exposure.value}')
        self._error_message(status)
        return status

    def _get_highspeed_windows(self):
        """Get the data from spot detection in Highspeed Mode.

        This function returns data of the spot detection windows valid
        in Highspeed Mode. Window size and positions depend on options
        passed to function _set_highspeed_mode().
        Note: This function is only available when Highspeed Mode is
        activated!

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            window_count_x (Vi.int32(int)): This parameter returns the
                number of spot windows in X direction.
            window_count_y (Vi.int32(int)): This parameter returns the
                number of spot windows in Y direction.
            window_size_x (Vi.int32(int)): This parameter returns the
                size in pixels of spot windows in X direction.
            window_size_y (Vi.int32(int)): This parameter returns the
                size in pixels of spot windows in Y direction.
            window_start_position_x (Vi.int32(int)): This parameter
                returns a one-dimensional array containing the start
                positions in pixels for spot windows in X direction.
                The required array size is MAX_SPOTS_X.
                Note: Window Stop X = Windows Start X + Windows Size X
            window_start_position_y (Vi.int32(int)):This parameter
                returns a one-dimensional array containing the start
                positions in pixels for spot windows in Y direction.
                The required array size is MAX_SPOTS_Y.
                Note: Window Stop Y = Windows Start Y + Windows Size Y
        """
        status = self.lib.WFS_GetHighspeedWindows(self.instrument_handle,
                                                  ctypes.byref(self.window_count_x),
                                                  ctypes.byref(self.window_count_y),
                                                  ctypes.byref(self.window_size_x),
                                                  ctypes.byref(self.window_size_y),
                                                  self.window_start_position_x,
                                                  self.window_start_position_y)
        columns = self.spots_x.value
        rows = self.spots_y.value
        self.log_wfs.debug(f'Get Highspeed Windows: {self.instrument_handle.value}')
        self.log_wfs.info(f'Window Count X: {self.window_count_x.value}')
        self.log_wfs.info(f'Window Count Y: {self.window_count_y.value}')
        self.log_wfs.info(f'Window Size X: {self.window_size_x.value}')
        self.log_wfs.info(f'Window Size Y: {self.window_size_y.value}')
        self.log_wfs.debug('Window Start Position X:\n' +
                           ' '.join([f'{item:12.8}' for item in self.window_start_position_x[:columns]]))
        self.log_wfs.debug('Window Start Position Y:\n' +
                           ' '.join([f'{item:12.8}' for item in self.window_start_position_y[:rows]]))
        self._error_message(status)
        return (status, self.window_count_x.value, self.window_count_y.value, self.window_size_x.value,
                self.window_size_y.value, self.window_start_position_x, self.window_start_position_y)

    def _check_highspeed_centroids(self):
        """Check if measured spots are in calculation in Highspeed Mode.

        This function checks if the actual measured spot centroid
        positions are within the calculation windows in Highspeed Mode.
        Possible error: WFS_ERROR_HIGHSPEED_WINDOW_MISMATCH
        If this error occurs, measured centroids are not reliable for
        wavefront interrogation because the appropriated spots are
        truncated.
        Note: This function is only available when Highspeed Mode is
        activated!

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        status = self.lib.WFS_CheckHighspeedCentroids(self.instrument_handle)
        self.log_wfs.debug(f'Check Highspeed Centroids: {self.instrument_handle.value}')
        self._error_message(status)
        return status

    def _get_exposure_time_range(self):
        """Get the exposure time range in ms based on camera resolution.

        This function returns the available exposure range of the WFS
        camera in ms. The range may depend on the camera resolution
        set by function _configure_cam.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            exposure_time_min (Vi.real64(float)): This parameter
                returns the minimal exposure time of the WFS camera in
                ms.
            exposure_time_min (Vi.real64(float)): This parameter
                returns the maximal exposure time of the WFS camera in
                ms.
            exposure_time_min (Vi.real64(float)): This parameter
                returns the smallest possible increment of the
                exposure time in ms.
        """
        status = self.lib.WFS_GetExposureTimeRange(self.instrument_handle,
                                                   ctypes.byref(self.exposure_time_min),
                                                   ctypes.byref(self.exposure_time_max),
                                                   ctypes.byref(self.exposure_time_increment))
        self.log_wfs.debug(f'Get Exposure Time Range: {self.instrument_handle.value}')
        self.log_wfs.info(f'Exposure Time Minimum (ms): {self.exposure_time_min.value}')
        self.log_wfs.info(f'Exposure Time Maximum (ms): {self.exposure_time_max.value}')
        self.log_wfs.info(f'Exposure Time Increment (ms): {self.exposure_time_increment.value}')
        self._error_message(status)
        return (status, self.exposure_time_min.value, self.exposure_time_max.value,
                self.exposure_time_increment.value)

    def _set_exposure_time(self, exposure_time_set=None):
        """Set the target exposure time in ms and get actual value.

        This function sets the target exposure time for the WFS camera
        and returns the actual set value.

        Args:
            exposure_time_set (Vi.real64(float)): This parameter sets
                the target exposure time for the WFS camera in ms.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            exposure_time_actual (Vi.real64(float)): This parameter
                returns the actual exposure time of the WFS camera in
                ms.
        """
        if exposure_time_set is not None:
            try:
                self.exposure_time_set = Vi.real64(exposure_time_set)
            except ValueError:
                self.exposure_time_set = exposure_time_set
        status = self.lib.WFS_SetExposureTime(self.instrument_handle,
                                              self.exposure_time_set,
                                              ctypes.byref(self.exposure_time_actual))
        self.log_wfs.debug(f'Set Exposure Time: {self.instrument_handle.value}')
        self.log_wfs.info(f'Exposure Time Set (ms): {self.exposure_time_set.value}')
        self.log_wfs.info(f'Exposure Time Actual (ms): {self.exposure_time_actual.value}')
        self._error_message(status)
        return status, self.exposure_time_actual.value

    def _get_exposure_time(self):
        """Get the actual exposure time in ms.

        This function returns the actual exposure time of the WFS
        camera in ms.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            exposure_time_actual (Vi.real64(float)): This parameter
                returns the actual exposure time of the WFS camera in
                ms.
        """
        status = self.lib.WFS_GetExposureTime(self.instrument_handle,
                                              ctypes.byref(self.exposure_time_actual))
        self.log_wfs.debug(f'Get Exposure Time (ms): {self.instrument_handle.value}')
        self.log_wfs.info(f'Exposure Time Actual (ms): {self.exposure_time_actual.value}')
        self._error_message(status)
        return status, self.exposure_time_actual.value

    def _get_master_gain_range(self):
        """Get the available linear master gain range.

        This function returns the available linear master gain range
        of the WFS camera. Note: Master gain increases image noise!
        Use higher exposure time to set the WFS camera more sensitive.
        Lowest master gain of WFS10 camera is 1.5.
        Master gain of WFS20 camera is fixed to 1.0.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            master_gain_min (Vi.real64(float)): This parameter returns
                the minimal linear master gain value of the WFS camera.
            master_gain_max (Vi.real64(float)): This parameter returns
                the maximal linear master gain value of the WFS camera.
        """
        status = self.lib.WFS_GetMasterGainRange(self.instrument_handle,
                                                 ctypes.byref(self.master_gain_min),
                                                 ctypes.byref(self.master_gain_max))
        self.log_wfs.debug(f'Get Master Gain Range: {self.instrument_handle.value}')
        self.log_wfs.info(f'Master Gain Minimum: {self.master_gain_min.value}')
        self.log_wfs.info(f'Master Gain Maximum: {self.master_gain_max.value}')
        self._error_message(status)
        return status, self.master_gain_min.value, self.master_gain_max.value

    def _set_master_gain(self, master_gain_set=None):
        """Set the target linear master gain.

        This function sets the target linear master gain for the WFS
        camera and returns the actual set master gain.
        Note: MasterGain of WFS20 is fixed to 1

        Args:
            master_gain_set (Vi.real64(float)): This parameter accepts
                the Instrument Handle returned by the _init() function
                to select the desired instrument driver session.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            master_gain_actual (Vi.real64(float)): This parameter
                returns the actual linear master gain of the WFS
                camera.
        """
        if master_gain_set is not None:
            try:
                self.master_gain_set = Vi.real64(master_gain_set)
            except ValueError:
                self.master_gain_set = master_gain_set
        status = self.lib.WFS_SetMasterGain(self.instrument_handle,
                                            self.master_gain_set,
                                            ctypes.byref(self.master_gain_actual))
        self.log_wfs.debug(f'Get Exposure Time: {self.instrument_handle.value}')
        self.log_wfs.info(f'Master Gain Set: {self.master_gain_set.value}')
        self.log_wfs.info(f'Master Gain Actual: {self.master_gain_actual.value}')
        self._error_message(status)
        return status, self.master_gain_actual.value

    def _get_master_gain(self):
        """Get the actual linear master gain.

        This function returns the actual set linear master gain.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            master_gain_actual (Vi.real64(float)): This parameter
                returns the actual linear master gain of the WFS
                camera.
        """
        status = self.lib.WFS_GetMasterGain(self.instrument_handle,
                                            ctypes.byref(self.master_gain_actual))
        self.log_wfs.debug(f'Get Exposure Time: {self.instrument_handle.value}')
        self.log_wfs.info(f'Master Gain Actual: {self.master_gain_actual.value}')
        self._error_message(status)
        return status, self.master_gain_actual.value

    def _set_black_level_offset(self, black_level_offset_set=None):
        """Set the black level offset.

        This function sets the black offset level of the WFS camera. A
        higher black level will increase the intensity level of a dark
        camera image.

        Args:
            black_level_offset_set (Vi.int32(int)): This parameter
                sets the black offset value of the WFS camera. A
                higher black level will increase the intensity level
                of a dark camera image. Valid range: 0 ... 255

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        if black_level_offset_set is not None:
            try:
                self.black_level_offset_set = Vi.int32(black_level_offset_set)
            except ValueError:
                self.black_level_offset_set = black_level_offset_set
        status = self.lib.WFS_SetBlackLevelOffset(self.instrument_handle,
                                                  self.black_level_offset_set)
        self.log_wfs.debug(f'Set Black Level Offset: {self.instrument_handle.value}')
        self.log_wfs.info(f'Black Level Offset Set: {self.black_level_offset_set.value}')
        self._error_message(status)
        return status

    def _get_black_level_offset(self):
        """Get the black level offset.

        This function returns the black offset level of the WFS camera.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.:
            black_level_offset_set (Vi.int32(int)): This parameter
                returns the black offset value of the WFS camera.
        """
        status = self.lib.WFS_GetBlackLevelOffset(self.instrument_handle,
                                                  ctypes.byref(self.black_level_offset_actual))
        self.log_wfs.debug(f'Get Black Level Offset: {self.instrument_handle.value}')
        self.log_wfs.info(f'Black Level Offset Actual: {self.black_level_offset_actual.value}')
        self._error_message(status)
        return status, self.black_level_offset_actual.value

    def _set_trigger_mode(self, trigger_mode=None):
        """Set the hardware trigger mode.

        This function sets the hardware trigger mode. When the trigger
        capability is activated, functions _take_spotfield_image() and
        _take_spotfield_image_auto_exposure() will wait for a trigger
        event for a short period of time (WFS_TIMEOUT_CAPTURE_TRIGGER
        = 0.1 sec.) prior to start exposure and will return with error
        WFS_ERROR_AWAITING_TRIGGER if no trigger event occurred. Use
        function _set_trigger_delay() to define an extra trigger delay
        time.

        Args:
            trigger_mode (Vi.int32(int)): This parameter defines and
                activates the trigger mode. Valid settings:
                WFS_HW_TRIGGER_OFF - Trigger input disabled
                WFS_HW_TRIGGER_HL - Trigger on high->low edge
                WFS_HW_TRIGGER_LH - Trigger on low->high edge

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        if trigger_mode is not None:
            try:
                self.trigger_mode = Vi.int32(trigger_mode)
            except ValueError:
                self.trigger_mode = trigger_mode
        status = self.lib.WFS_SetTriggerMode(self.instrument_handle,
                                             self.trigger_mode)
        self.log_wfs.debug(f'Set Trigger Mode: {self.instrument_handle.value}')
        self.log_wfs.info(f'Trigger Mode: {self.trigger_mode.value}')
        self._error_message(status)
        return status

    def _get_trigger_mode(self):
        """Get the hardware trigger mode.

        This function returns the actual hardware trigger mode.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            trigger_mode (Vi.int32(int)): This parameter returns the
                actual trigger mode. Valid trigger modes:
                WFS_HW_TRIGGER_OFF - Trigger input disabled
                WFS_HW_TRIGGER_HL - Trigger on high->low edge
                WFS_HW_TRIGGER_LH - Trigger on low->high edge
        """
        status = self.lib.WFS_GetTriggerMode(self.instrument_handle,
                                             ctypes.byref(self.trigger_mode))
        self.log_wfs.debug(f'Get Trigger Mode: {self.instrument_handle.value}')
        self.log_wfs.info(f'Trigger Mode: {self.trigger_mode.value}')
        self._error_message(status)
        return status, self.trigger_mode.value

    def _set_trigger_delay(self, trigger_delay_set=None):
        """Set a target trigger delay for a hardware trigger mode.

        This function sets an additional trigger delay for a hardware
        trigger mode set by function _set_trigger_mode().

        Args:
            trigger_delay_set (Vi.int32(int)): This parameter accepts
                the target trigger delay in µs. Use function
                _get_trigger_delay_range() to read out the accepted
                limits.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            trigger_delay_actual (Vi.int32(int)): This parameter
                returns the actual trigger delay in µs which may
                differ from the target value.
        """
        if trigger_delay_set is not None:
            try:
                self.trigger_delay_set = Vi.int32(trigger_delay_set)
            except ValueError:
                self.trigger_delay_set = trigger_delay_set
        status = self.lib.WFS_SetTriggerDelay(self.instrument_handle,
                                              self.trigger_delay_set,
                                              ctypes.byref(self.trigger_delay_actual))
        self.log_wfs.debug(f'Set Trigger Delay: {self.instrument_handle.value}')
        self.log_wfs.info(f'Trigger Delay Set (µs): {self.trigger_delay_set.value}')
        self.log_wfs.info(f'Trigger Delay Actual (µs): {self.trigger_delay_actual.value}')
        self._error_message(status)
        return status, self.trigger_delay_actual.value

    def _get_trigger_delay_range(self):
        """Get the allowed time range in µs for hardware trigger delays.

        This function returns the allowed range for the trigger delay
        setting in function _set_trigger_delay().

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            trigger_delay_min (Vi.int32(int)): This parameter
                returns the minimum adjustable trigger delay in µs.
            trigger_delay_max (Vi.int32(int)): This parameter
                returns the maximum adjustable trigger delay in µs.
            trigger_delay_increment (Vi.int32(int)): This parameter
                returns the accepted minimum increment of the trigger
                delay in µs.
        """
        status = self.lib.WFS_GetTriggerDelayRange(self.instrument_handle,
                                                   ctypes.byref(self.trigger_delay_min),
                                                   ctypes.byref(self.trigger_delay_max),
                                                   ctypes.byref(self.trigger_delay_increment))
        self.log_wfs.debug(f'Get Trigger Delay Range: {self.instrument_handle.value}')
        self.log_wfs.info(f'Trigger Delay Minimum (µs): {self.trigger_delay_min.value}')
        self.log_wfs.info(f'Trigger Delay Maximum (µs): {self.trigger_delay_max.value}')
        self.log_wfs.info(f'Trigger Delay Increment (µs): {self.trigger_delay_increment.value}')
        self._error_message(status)
        return status, self.trigger_delay_min.value, self.trigger_delay_max.value, self.trigger_delay_increment.value

    def _get_mla_count(self):
        """Get the index of calibrated Microlens Arrays.

        This function returns the number of calibrated Microlens Arrays.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            mla_index (Vi.int32(int)): This parameter returns the
                index of calibrated Microlens Arrays.
        """
        status = self.lib.WFS_GetMlaCount(self.instrument_handle,
                                          ctypes.byref(self.mla_count))
        self.mla_index = Vi.int32(self.mla_count.value - 1)
        self.log_wfs.debug(f'Get MLA Count: {self.instrument_handle.value}')
        self.log_wfs.debug(f'Micro Lens Array Count: {self.mla_count.value}')
        self.log_wfs.info(f'Micro Lens Array Index: {self.mla_index.value}')
        self._error_message(status)
        return status, self.mla_index.value

    def _get_mla_data(self, mla_index=None):
        """Get the calibration data of the Microlens Array index.

        This function returns calibration data of the desired
        Microlens Array index. The number of calibrated lenslet arrays
        can be derived by function _get_mla_count().
        Note: The calibration data are not automatically set active.

        Args:
            mla_index (Vi.int32(int)): This parameter defines the
                index of a removable microlens array.
                Valid range: 0 ... mla_count-1

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            mla_name (Vi.char(int)): This parameter returns the name
                of the Microlens Array. Note: The string must contain
                at least WFS_BUFFER_SIZE (256) elements
                (Vi.char(WFS_BUFFER_SIZE)).
            cam_pitch_um (Vi.real64(float)): This parameter returns
                the camera pixel pitch in µm.
            lenslet_pitch_um (Vi.real64(float)): This parameter
                returns the Microlens Array pitch in µm.
            spot_offset_x (Vi.real64(float)): This parameter returns
                the X Offset of the central MLA lenslet.
            spot_offset_y (Vi.real64(float)): This parameter returns
                the Y Offset of the central MLA lenslet.
            lenslet_focal_length_um (Vi.real64(float)): This parameter
                returns the calibrated distance (focal length) of  the
                Microlens Array in µm.
            grid_correction_0 (Vi.real64(float)): This parameter
                returns the calibrated correction value for
                astigmatism 0° of the Microlens Array in ppm.
            grid_correction_45 (Vi.real64(float)): This parameter
                returns the calibrated correction value for
                astigmatism 45° of the Microlens Array in ppm.
        """
        if mla_index is not None:
            try:
                self.mla_index = Vi.int32(mla_index)
            except ValueError:
                self.mla_index = mla_index
        status = self.lib.WFS_GetMlaData(self.instrument_handle,
                                         self.mla_index,
                                         self.mla_name,
                                         ctypes.byref(self.cam_pitch_um),
                                         ctypes.byref(self.lenslet_pitch_um),
                                         ctypes.byref(self.spot_offset_x),
                                         ctypes.byref(self.spot_offset_y),
                                         ctypes.byref(self.lenslet_focal_length_um),
                                         ctypes.byref(self.grid_correction_0),
                                         ctypes.byref(self.grid_correction_45))
        self.log_wfs.debug(f'Get MLA Data: {self.instrument_handle.value}')
        self.log_wfs.info(f'MLA Index: {self.mla_index.value}')
        self.log_wfs.info(f'MLA Name: {self.mla_name.value.decode()}')
        self.log_wfs.info(f'MLA Camera Pitch (µm): {self.cam_pitch_um.value}')
        self.log_wfs.info(f'MLA Lenslet Pitch (µm): {self.lenslet_pitch_um.value}')
        self.log_wfs.info(f'MLA Spot Offset X: {self.spot_offset_x.value}')
        self.log_wfs.info(f'MLA Spot Offset Y: {self.spot_offset_y.value}')
        self.log_wfs.info(f'MLA Lenslet Focal length (µm): {self.lenslet_focal_length_um.value}')
        self.log_wfs.info(f'MLA Grid Correction 0°')
        self.log_wfs.info(f'MLA Grid Correction 45°')
        self._error_message(status)
        return (status, self.mla_name.value, self.cam_pitch_um.value, self.lenslet_pitch_um.value,
                self.spot_offset_x.value, self.spot_offset_y.value, self.lenslet_focal_length_um.value,
                self.grid_correction_0.value, self.grid_correction_45.value)

    def _get_mla_data2(self, mla_index=None):
        """Get the calibration data of the Microlens Array index.

        This function returns more calibration data of the desired
        Microlens Array index. The number of calibrated lenslet arrays
        can be derived by function _get_mla_count().
        Note: The calibration data are not automatically set active.

        Args:
            mla_index (Vi.int32(int)): This parameter defines the
                index of a removable microlens array.
                Valid range: 0 ... mla_count-1

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            mla_name (Vi.char(int)): This parameter returns the name
                of the Microlens Array. Note: The string must contain
                at least WFS_BUFFER_SIZE (256) elements
                (Vi.char(WFS_BUFFER_SIZE)).
            cam_pitch_um (Vi.real64(float)): This parameter returns
                the camera pixel pitch in µm.
            lenslet_pitch_um (Vi.real64(float)): This parameter
                returns the Microlens Array pitch in µm.
            spot_offset_x (Vi.real64(float)): This parameter returns
                the X Offset of the central MLA lenslet.
            spot_offset_y (Vi.real64(float)): This parameter returns
                the Y Offset of the central MLA lenslet.
            lenslet_focal_length_um (Vi.real64(float)): This parameter
                returns the calibrated distance (focal length) of  the
                Microlens Array in µm.
            grid_correction_0 (Vi.real64(float)): This parameter
                returns the calibrated correction value for
                astigmatism 0° of the Microlens Array in ppm.
            grid_correction_45 (Vi.real64(float)): This parameter
                returns the calibrated correction value for
                astigmatism 45° of the Microlens Array in ppm.
            grid_correction_rotation (Vi.real64(float)): This
                parameter returns the calibrated correction value for
                rotation of the Microlens Array in 10^-3 deg.
            grid_correction_pitch (Vi.real64(float)): This parameter
                returns the calibrated correction value for pitch of
                the Microlens Array in ppm.
        """
        if mla_index is not None:
            try:
                self.mla_index = Vi.int32(mla_index)
            except ValueError:
                self.mla_index = mla_index
        status = self.lib.WFS_GetMlaData2(self.instrument_handle,
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
        self.log_wfs.debug(f'Get MLA Data2: {self.instrument_handle.value}')
        self.log_wfs.info(f'MLA Index: {self.mla_index.value}')
        self.log_wfs.info(f'MLA Name: {self.mla_name.value.decode()}')
        self.log_wfs.info(f'MLA Camera Pitch (µm): {self.cam_pitch_um.value}')
        self.log_wfs.info(f'MLA Lenslet Pitch (µm): {self.lenslet_pitch_um.value}')
        self.log_wfs.info(f'MLA Spot Offset X: {self.spot_offset_x.value}')
        self.log_wfs.info(f'MLA Spot Offset Y: {self.spot_offset_y.value}')
        self.log_wfs.info(f'MLA Lenslet Focal length (µm): {self.lenslet_focal_length_um.value}')
        self.log_wfs.info(f'MLA Grid Correction 0°')
        self.log_wfs.info(f'MLA Grid Correction 45°')
        self.log_wfs.info(f'MLA Grid Correction Rotation: {self.grid_correction_rotation.value}')
        self.log_wfs.info(f'MLA Grid Correction Pitch: {self.grid_correction_pitch.value}')
        self._error_message(status)
        return (status, self.mla_name.value, self.cam_pitch_um.value, self.lenslet_pitch_um.value,
                self.spot_offset_x.value, self.spot_offset_y.value, self.lenslet_focal_length_um.value,
                self.grid_correction_0.value, self.grid_correction_45.value, self.grid_correction_rotation.value,
                self.grid_correction_pitch.value)

    def _select_mla(self, mla_index=None):
        """Select the microlens array by index.

        This function selects one of the removable microlens arrays by
        its index. Appropriate calibration values are read out of the
        instrument and set active.

        Args:
            mla_index (Vi.int32(int)): This parameter defines the
                index of a removable microlens array to be selected.
                Valid range: 0 ... Number of calibrated MLAs-1

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        if mla_index is not None:
            try:
                self.mla_index = Vi.int32(mla_index)
            except ValueError:
                self.mla_index = mla_index
        status = self.lib.WFS_SelectMla(self.instrument_handle,
                                        self.mla_index)
        self.log_wfs.debug(f'Select MLA: {self.instrument_handle.value}')
        self.log_wfs.info(f'MLA selection: {self.mla_index.value}')
        self._error_message(status)
        return status

    def _set_aoi(self, aoi_center_x_mm=None, aoi_center_y_mm=None,
                 aoi_size_x_mm=None, aoi_size_y_mm=None):
        """Set the area of interest position and size.

        This function defines the area of interest (AOI) within the
        camera image in position and size. All spots outside this area
        are ignored for Zernike and wavefront calculations.

        In order to set the maximum available area set all 4 input
        values to 0.0.

        Args:
            aoi_center_x_mm (Vi.real64(int)): This parameter defines
                the AOI center X position in mm. It needs to be within
                the active camera area defined by function
                _configure_cam. Origin is the image center. Note:
                The parameter must fit to the selected camera area.
            aoi_center_y_mm (Vi.real64(int)): This parameter defines
                the AOI center Y position in mm. It needs to be within
                the active camera area defined by function
                _configure_cam. Origin is the image center. Note:
                The parameter must fit to the selected camera area.
            aoi_size_x_mm (Vi.real64(int)): This parameter defines the
                AOI width in mm. The area needs to be within the active
                camera area defined by function _configure_cam. Note:
                The parameter must fit to the selected camera area.
            aoi_size_y_mm (Vi.real64(int)): This parameter defines the
                AOI height in mm. The area needs to be within the
                active camera area defined by function _configure_cam.
                Note: The parameter must fit to the selected camera
                area.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        if aoi_center_x_mm is not None:
            try:
                self.aoi_center_x_mm = Vi.real64(aoi_center_x_mm)
            except ValueError:
                self.aoi_center_x_mm = aoi_center_x_mm
        if aoi_center_y_mm is not None:
            try:
                self.aoi_center_y_mm = Vi.real64(aoi_center_y_mm)
            except ValueError:
                self.aoi_center_y_mm = aoi_center_y_mm
        if aoi_size_x_mm is not None:
            try:
                self.aoi_size_x_mm = Vi.real64(aoi_size_x_mm)
            except ValueError:
                self.aoi_size_x_mm = aoi_size_x_mm
        if aoi_size_y_mm is not None:
            try:
                self.aoi_size_y_mm = Vi.real64(aoi_size_y_mm)
            except ValueError:
                self.aoi_size_y_mm = aoi_size_y_mm
        if 0 < self.aoi_size_x_mm.value < self.PUPIL_DIA_MIN_MM:
            self.log_wfs.debug(f'Set AoI: {self.instrument_handle.value}')
            status = self.WFS_ERROR_PARAMETER4
            self._error_message(status)
            return status
        if 0 < self.aoi_size_y_mm.value < self.PUPIL_DIA_MIN_MM:
            self.log_wfs.debug(f'Set AoI: {self.instrument_handle.value}')
            status = self.WFS_ERROR_PARAMETER5
            self._error_message(status)
            return status
        status = self.lib.WFS_SetAoi(self.instrument_handle,
                                     self.aoi_center_x_mm,
                                     self.aoi_center_y_mm,
                                     self.aoi_size_x_mm,
                                     self.aoi_size_y_mm)
        self.log_wfs.debug(f'Set AoI: {self.instrument_handle.value}')
        self.log_wfs.info(f'AoI Center X (mm): {self.aoi_center_x_mm.value}')
        self.log_wfs.info(f'AoI Center y (mm): {self.aoi_center_y_mm.value}')
        self.log_wfs.info(f'AoI Size X (mm): {self.aoi_size_x_mm.value}')
        self.log_wfs.info(f'AoI Size Y (mm): {self.aoi_size_y_mm.value}')
        self._error_message(status)
        return status

    def _get_aoi(self):
        """Get the area of interest position and size.

        This function returns the actual the area of interest (AOI)
        position and size. All spots outside this area are ignored for
        Beam View display as well as for Zernike and wavefront
        calculations.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            aoi_center_x_mm (Vi.real64(int)): This parameter returns
                the AOI center X position in mm.
            aoi_center_y_mm (Vi.real64(int)): This parameter returns
                the AOI center Y position in mm.
            aoi_size_x_mm (Vi.real64(int)): This parameter returns the
                AOI X size in mm.
            aoi_size_y_mm (Vi.real64(int)): This parameter returns the
                AOI Y size in mm.
        """
        status = self.lib.WFS_GetAoi(self.instrument_handle,
                                     ctypes.byref(self.aoi_center_x_mm),
                                     ctypes.byref(self.aoi_center_y_mm),
                                     ctypes.byref(self.aoi_size_x_mm),
                                     ctypes.byref(self.aoi_size_y_mm))
        self.log_wfs.debug(f'Set AoI: {self.instrument_handle.value}')
        self.log_wfs.info(f'AoI Center X (mm): {self.aoi_center_x_mm.value}')
        self.log_wfs.info(f'AoI Center y (mm): {self.aoi_center_y_mm.value}')
        self.log_wfs.info(f'AoI Size X (mm): {self.aoi_size_x_mm.value}')
        self.log_wfs.info(f'AoI Size Y (mm): {self.aoi_size_y_mm.value}')
        self._error_message(status)
        return (status, self.aoi_center_x_mm.value, self.aoi_center_y_mm.value,
                self.aoi_size_x_mm.value, self.aoi_size_y_mm.value)

    def _set_pupil(self, pupil_center_x_mm=None, pupil_center_y_mm=None,
                   pupil_diameter_x_mm=None, pupil_diameter_y_mm=None):
        """Set the pupil position and size in mm.

        This function defines the pupil in position and size.

        Args:
            pupil_center_x_mm (Vi.real64(int)): This parameter defines
                the pupil center X position in mm. It needs to be
                within the active camera area defined by function
                _configure_cam. Origin is the image center.
                Valid range: -5.0 ... +5.0 mm
            pupil_center_y_mm (Vi.real64(int)): This parameter defines
                the pupil center Y position in mm. It needs to be
                within the active camera area defined by function
                _configure_cam. Origin is the image center.
                Valid range: -5.0 ... +5.0 mm
            pupil_diameter_x_mm (Vi.real64(int)): This parameter
                defines the pupil X diameter in mm. The pupil area
                needs to be within the active camera area defined by
                function _configure_cam.
                Valid range: 0.1 ... +10.0 mm
            pupil_diameter_y_mm (Vi.real64(int)): This parameter
                defines the pupil Y diameter in mm. The pupil area
                needs to be within the active camera area defined by
                function _configure_cam.
                Valid range: 0.1 ... +10.0 mm

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        if pupil_center_x_mm is not None:
            try:
                self.pupil_center_x_mm = Vi.real64(pupil_center_x_mm)
            except ValueError:
                self.pupil_center_x_mm = pupil_center_x_mm
        if pupil_center_y_mm is not None:
            try:
                self.pupil_center_y_mm = Vi.real64(pupil_center_y_mm)
            except ValueError:
                self.pupil_center_y_mm = pupil_center_y_mm
        if pupil_diameter_x_mm is not None:
            try:
                self.pupil_diameter_x_mm = Vi.real64(pupil_diameter_x_mm)
            except ValueError:
                self.pupil_diameter_x_mm = pupil_diameter_x_mm
        if pupil_diameter_y_mm is not None:
            try:
                self.pupil_diameter_y_mm = Vi.real64(pupil_diameter_y_mm)
            except ValueError:
                self.pupil_diameter_y_mm = pupil_diameter_y_mm
        status = self.lib.WFS_SetPupil(self.instrument_handle,
                                       self.pupil_center_x_mm,
                                       self.pupil_center_y_mm,
                                       self.pupil_diameter_x_mm,
                                       self.pupil_diameter_y_mm)
        self.log_wfs.debug(f'Set Pupil: {self.instrument_handle.value}')
        self.log_wfs.info(f'Set Pupil Centroid X (mm): {self.pupil_center_x_mm.value}')
        self.log_wfs.info(f'Set Pupil Centroid Y (mm): {self.pupil_center_y_mm.value}')
        self.log_wfs.info(f'Set Pupil Diameter X (mm): {self.pupil_diameter_x_mm.value}')
        self.log_wfs.info(f'Set Pupil Diameter Y (mm): {self.pupil_diameter_y_mm.value}')
        self._error_message(status)
        return status

    def _get_pupil(self):
        """Get the actual pupil position and size.

        This function returns the actual the pupil position and size.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            pupil_center_x_mm (Vi.real64(int)): This parameter returns
                the pupil center X position in mm.
            pupil_center_y_mm (Vi.real64(int)): This parameter returns
                the pupil center Y position in mm.
            pupil_diameter_x_mm (Vi.real64(int)): This parameter
                returns the pupil X diameter in mm.
            pupil_diameter_y_mm (Vi.real64(int)): This parameter
                returns the pupil Y diameter in mm.
        """
        status = self.lib.WFS_GetPupil(self.instrument_handle,
                                       ctypes.byref(self.pupil_center_x_mm),
                                       ctypes.byref(self.pupil_center_y_mm),
                                       ctypes.byref(self.pupil_diameter_x_mm),
                                       ctypes.byref(self.pupil_diameter_y_mm))
        self.log_wfs.debug(f'Get Pupil: {self.instrument_handle.value}')
        self.log_wfs.info(f'Get Pupil Centroid X (mm): {self.pupil_center_x_mm.value}')
        self.log_wfs.info(f'Get Pupil Centroid Y (mm): {self.pupil_center_y_mm.value}')
        self.log_wfs.info(f'Get Pupil Diameter X (mm): {self.pupil_diameter_x_mm.value}')
        self.log_wfs.info(f'Get Pupil Diameter Y (mm): {self.pupil_diameter_y_mm.value}')
        self._error_message(status)
        return (status, self.pupil_center_x_mm.value, self.pupil_center_y_mm.value,
                self.pupil_diameter_x_mm.value, self.pupil_diameter_y_mm.value)

    def _set_reference_plane(self, reference_index=None):
        """Set the reference plane to either Internal or User Defined.

        This function defines the WFS Reference Plane to either
        Internal or User (external).

        Args:
            reference_index (Vi.int32(int)): This parameter sets the
                Reference Plane to either Internal or User (external).
                Valid values:
                0 - WFS_REF_INTERNAL
                1 - WFS_REF_USER
                User reference is based on a file .ref containing spot
                reference positions which can be loaded and saved by
                functions _load_user_reference_file and
                _save_user_reference_file. It's name is specific to
                the WFS serial number, MLA name and actual camera
                resolution. A default User Reference file containing a
                copy of internal reference data can be created by
                function _create_default_user_reference.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        if reference_index is not None:
            try:
                self.reference_index = Vi.int32(reference_index)
            except ValueError:
                self.reference_index = reference_index
        status = self.lib.WFS_SetReferencePlane(self.instrument_handle,
                                                self.reference_index)
        self.log_wfs.debug(f'Set Reference Plane: {self.instrument_handle.value}')
        self.log_wfs.info(f'Set Reference Index: {self.reference_index.value}')
        self._error_message(status)
        return status

    def _get_reference_plane(self):
        """Get the reference plane of the WFS Instrument.

        This function returns the Reference Plane setting of the WFS
        instrument.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            reference_index (Vi.int32(int)): This parameter returns
                the actual Reference Plane of the WFS instrument.
                Valid return values:
                0 - WFS_REF_INTERNAL
                1 - WFS_REF_USER
        """
        status = self.lib.WFS_GetReferencePlane(self.instrument_handle,
                                                ctypes.byref(self.reference_index))
        self.log_wfs.debug(f'Get Reference Plane: {self.instrument_handle.value}')
        self.log_wfs.info(f'Get Reference Index: {self.reference_index.value}')
        self._error_message(status)
        return status, self.reference_index.value

    # Data Functions
    def _take_spotfield_image(self):
        """Take a spotfield image from the WFS and load into buffer.

        This function receives a spotfield image from the WFS camera
        into a driver buffer. The reference to this buffer is provided
        by function _get_spotfield_image() and an image copy is
        returned by function _get_spotfield_image_copy(). In case of
        unsuited image exposure the function sets the appropriate
        status bits. Use function _get_status() to check the reason.
        Bit          Name              Meaning if bit is set
        0x00000002 - WFS_STATBIT_PTH - Power Too High (cam saturated)
        0x00000004 - WFS_STATBIT_PTL - Power Too Low (low cam digits)
        0x00000008 - WFS_STATBIT_HAL - High Ambient Light
        You need to set optimized exposure and gain settings by
        functions _set_exposure_time() and _set_master_gain() and
        repeat calling the function until these status bits are
        cleared. Alternatively, you may use function
        _take_spotfield_image_auto_exposure(). When the trigger
        capability is activated by function _set_trigger_mode() this
        function will wait for a trigger event for a short period of
        time (WFS_TIMEOUT_CAPTURE_TRIGGER = 0.1 sec.) prior to start
        exposure and will return with error WFS_ERROR_AWAITING_TRIGGER
        if no trigger event occurred. You need to repeat calling this
        function until this error and status bit WFS_STATBIT_ATR
        disappear.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        status = self.lib.WFS_TakeSpotfieldImage(self.instrument_handle)
        self.log_wfs.debug(f'Take Spotfield Image: {self.instrument_handle.value}')
        self._error_message(status)
        return status

    def _take_spotfield_image_auto_exposure(self):
        """Take a spotfield image with auto-exposure and load to buffer.

        This function tries to find optimal exposure and gain settings
        and then it receives a spotfield image from the WFS camera
        into a driver buffer. The reference to this buffer is provided
        by function _get_spotfield_image() and an image copy is
        returned by function _get_spotfield_image_copy(). The exposure
        and gain settings used for this image are returned. In case of
        still unsuited image exposure the function sets the
        appropriate status bits. Use function _get_status() to check
        the reason.
        Bit          Name              Meaning if bit is set
        0x00000002 - WFS_STATBIT_PTH - Power Too High (cam saturated)
        0x00000004 - WFS_STATBIT_PTL - Power Too Low (low cam digits)
        0x00000008 - WFS_STATBIT_HAL - High Ambient Light
        You may repeat calling the function until these status bits
        are cleared. When the trigger capability is activated by
        function _set_trigger_mode() this function will wait for a
        trigger event for a short period of time
        (WFS_TIMEOUT_CAPTURE_TRIGGER = 0.1 sec.) prior to start
        exposure and will return with error
        WFS_ERROR_AWAITING_TRIGGER if no trigger event occurred. You
        need to repeat calling this function until this error and
        status bit WFS_STATBIT_ATR disappear.
        Note: This function is not available in Highspeed Mode!

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            exposure_time_actual (Vi.real64(float)): This parameter
                returns the automatically selected actual exposure
                time the camera image was taken with.
            master_gain_actual (Vi.real64(float)): This parameter
                returns the automatically selected actual master gain
                the camera image was taken with.
        """
        status = self.lib.WFS_TakeSpotfieldImageAutoExpos(self.instrument_handle,
                                                          ctypes.byref(self.exposure_time_actual),
                                                          ctypes.byref(self.master_gain_actual))
        self.log_wfs.debug(f'Take Spotfield Image Auto Exposure: {self.instrument_handle.value}')
        self.log_wfs.info(f'Exposure Time Actual: {self.exposure_time_actual.value}')
        self.log_wfs.info(f'Master Gain Actual: {self.master_gain_actual.value}')
        self._error_message(status)
        return status, self.exposure_time_actual.value, self.master_gain_actual.value

    def _get_spotfield_image(self):
        """Get the reference to a spotfield image.

        This function returns the reference to a spotfield image taken
        by functions _take_spotfield_image() or
        _take_spotfield_image_auto_exposure(). It returns also the
        image size.
        Note: This function is not available in Highspeed Mode!

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            array_image_buffer_ref (Vi.array_uint8(int)): This
                parameter returns a reference to the image buffer.
                Note: This buffer is allocated by the camera driver
                and the actual image size is Rows * Columns. Do not
                modify this buffer!
            spotfield_rows (Vi.int32(int)): This parameter returns the
                image height (rows) in pixels.
            spotfield_columns (Vi.int32(int)): This parameter returns
                the image width (columns) in pixels.
        """
        status = self.lib.WFS_GetSpotfieldImage(self.instrument_handle,
                                                ctypes.byref(self.array_image_buffer_ref),
                                                ctypes.byref(self.spotfield_rows),
                                                ctypes.byref(self.spotfield_columns))
        self.log_wfs.debug(f'Get Spotfield Image: {self.instrument_handle.value}')
        self.log_wfs.debug('Image Buffer: ' + ' '.join([f'{item:3}' for item in self.array_image_buffer_ref[:8]]))
        self.log_wfs.info(f'Rows: {self.spotfield_rows.value}')
        self.log_wfs.info(f'Columns: {self.spotfield_columns.value}')
        self._error_message(status)
        return status, self.array_image_buffer_ref, self.spotfield_rows.value, self.spotfield_columns.value

    def _get_spotfield_image_copy(self):
        """Get a copy of the spotfield image as an array.

        This function returns a copy of the spotfield image taken by
        functions _take_spotfield_image() or
        _take_spotfield_image_auto_exposure() into the user provided
        buffer array_image_buffer. It returns also the image size.
        Note: This function is not available in Highspeed Mode!

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            array_image_buffer (Vi.array_uint8(int, int)): This
                parameter accepts an user provided image buffer. Note:
                This buffer needs to be allocated by the user. The
                required size is CAM_MAX_PIX_X * CAM_MAX_PIX_Y bytes.
            spotfield_rows (Vi.int32(int)): This parameter returns the
                image height (rows) in pixels.
            spotfield_columns (Vi.int32(int)): This parameter returns
                the image width (columns) in pixels.
        """
        status = self.lib.WFS_GetSpotfieldImageCopy(self.instrument_handle,
                                                    self.array_image_buffer,
                                                    ctypes.byref(self.spotfield_rows),
                                                    ctypes.byref(self.spotfield_columns))
        self.log_wfs.debug(f'Get Spotfield Image Copy: {self.instrument_handle.value}')
        self.log_wfs.info(f'Rows: {self.spotfield_rows.value}')
        self.log_wfs.info(f'Columns: {self.spotfield_columns.value}')
        self.log_wfs.debug('Image Buffer Copy:\n' +
                           '\n'.join([' '.join([f'{item:3}' for item in row]) for row in self.array_image_buffer]))
        self._error_message(status)
        return status, self.array_image_buffer, self.spotfield_rows.value, self.spotfield_columns.value

    def _average_image(self, average_count=None):
        """Generate an averaged image from a number of images in buffer.

        This function generates an averaged image from a number of
        input camera images in image_buffer. The function returns
        after each call and the summarized image is stored in
        ImageBufAveraged. As soon as the desired number of averages in
        average_count is reached image_buffer and ImageBufAveraged
        return both the averaged image data and AverageDataReady
        returns 1 instead of 0. Note: As soon as the image size is
        changed by function _configure_cam the averaging process is
        re-started. This function is not available in Highspeed Mode!

        Args:
            average_count (Vi.int32(int)): This parameter defines the
                number of averages. Valid range: 1 ... 256

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            average_data_ready (Vi.int32(int)): This parameter returns
                0 if the averaging process is going on and 1 when the
                target average count is reached.
        """
        if average_count is not None:
            try:
                self.average_count = Vi.int32(average_count)
            except ValueError:
                self.average_count = average_count
        status = self.lib.WFS_AverageImage(self.instrument_handle,
                                           self.average_count,
                                           ctypes.byref(self.average_data_ready))
        self.log_wfs.debug(f'Average Image: {self.instrument_handle.value}')
        self.log_wfs.info(f'Average Count: {self.average_count.value}')
        self.log_wfs.info(f'Average Data Ready: {self.average_data_ready.value}')
        self._error_message(status)
        return status, self.average_data_ready.value

    def _average_image_rolling(self, average_count=None, rolling_reset=None):
        """Generate a rolling averaged image from a number of images.

        This function generates a rolling averaged image based on all
        previously entered camera images in image_buffer. The function
        returns after each call and the averaged image is returned in
        image_buffer and also stored in ImageBufAveraged. The new
        rolling averaged image is calculated pixel by pixel according
        to the formula: ((average_count - 1) * ImageBufAveraged +
                         image_buffer) / average_count
        Note: As soon as the image size is changed by function
        _configure_cam the averaging process is re-started. This
        function is not available in Highspeed Mode!

        Args:
            average_count (Vi.int32(int)): This parameter defines the
                number of averages. Valid range: 1 ... 256
            rolling_reset (Vi.int32(int)): This parameter resets the
                rolling averaging process for Reset != 0.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        if average_count is not None:
            try:
                self.average_count = Vi.int32(average_count)
            except ValueError:
                self.average_count = average_count
        if rolling_reset is not None:
            try:
                self.rolling_reset = Vi.int32(rolling_reset)
            except ValueError:
                self.rolling_reset = rolling_reset
        status = self.lib.WFS_AverageImageRolling(self.instrument_handle,
                                                  self.average_count,
                                                  self.rolling_reset)
        self.log_wfs.debug(f'Average Image Rolling: {self.instrument_handle.value}')
        self.log_wfs.info(f'Average Count: {self.average_count.value}')
        self.log_wfs.info(f'Rolling Reset: {self.rolling_reset.value}')
        self._error_message(status)
        return status

    def _cut_image_noise_floor(self, intensity_limit=None):
        """Set all pixels under an intensity limit to zero.

        This function sets all pixels with intensities < Limit to zero
        which cuts the noise floor of the camera.
        Note: This function is not available in Highspeed Mode!

        Args:
            intensity_limit (Vi.int32(int)): This parameter defines
                the intensity limit. All image pixels with intensities
                < Limit are set to zero. Valid range: 1 ... 256
                Note: The limit must not be set too high to clear the
                spots within the WFS camera image.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        if intensity_limit is not None:
            try:
                self.intensity_limit = Vi.int32(intensity_limit)
            except ValueError:
                self.intensity_limit = intensity_limit
        status = self.lib.WFS_CutImageNoiseFloor(self.instrument_handle,
                                                 self.intensity_limit)
        self.log_wfs.debug(f'Cut Image Noise Floor: {self.instrument_handle.value}')
        self.log_wfs.info(f'Intensity Limit: {self.intensity_limit.value}')
        self._error_message(status)
        return status

    def _calc_image_min_max(self):
        """Calculate the min and max pixel intensity and saturation.

        This function returns minimum and maximum pixel intensities in
        image_buffer as well as the number of saturated pixels in
        percent.
        Note: This function is not available in Highspeed Mode!

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            intensity_min (Vi.int32(int)): This parameter returns the
                minimum pixel intensity within image_buffer.
            intensity_max (Vi.int32(int)): This parameter returns the
                maximum pixel intensity within image_buffer.
            saturated_pixels_percent (Vi.real64(float)): This
                parameter returns the percentage of saturated pixels
                within image_buffer.
        """
        status = self.lib.WFS_CalcImageMinMax(self.instrument_handle,
                                              ctypes.byref(self.intensity_min),
                                              ctypes.byref(self.intensity_max),
                                              ctypes.byref(self.saturated_pixels_percent))
        self.log_wfs.debug(f'Calc Image Min Max: {self.instrument_handle.value}')
        self.log_wfs.info(f'Intensity Minimum: {self.intensity_min.value}')
        self.log_wfs.info(f'Intensity Maximum: {self.intensity_max.value}')
        self.log_wfs.info(f'Saturated Pixels Percent: {self.saturated_pixels_percent.value:.2f}')
        self._error_message(status)
        return status, self.intensity_min.value, self.intensity_max.value, self.saturated_pixels_percent.value

    def _calc_mean_rms_noise(self):
        """Calculate the mean average and rms of pixel intensities.

        This function returns the mean average and rms variations of
        the pixel intensities in image_buffer.
        Note: This function is not available in Highspeed Mode!

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            intensity_mean (Vi.real64(float)): This parameter returns
                the mean average of the pixel intensities in
                image_buffer.
            intensity_rms (Vi.real64(float)): This parameter returns
                the rms variations of the pixel intensities in
                image_buffer.
        """
        status = self.lib.WFS_CalcMeanRmsNoise(self.instrument_handle,
                                               ctypes.byref(self.intensity_mean),
                                               ctypes.byref(self.intensity_rms))
        self.log_wfs.debug(f'Calc Mean RMS Noise: {self.instrument_handle.value}')
        self.log_wfs.info(f'Intensity Mean: {self.intensity_mean.value:.4f}')
        self.log_wfs.info(f'Intensity RMS: {self.intensity_rms.value:.4f}')
        self._error_message(status)
        return status, self.intensity_mean.value, self.intensity_rms.value

    def _get_line(self, line=None):
        """Get a single horizontal line of the image in a linear array.

        This function returns a single horizontal line of the image in
        a linear array.
        Note: This function is not available in Highspeed Mode!

        Args:
            line (Vi.int32(int)): This parameter defines the
                horizontal line to be selected within image_buffer.
                Valid range: 0 .. columns-1

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            array_line_selected (Vi.array_float(int)): This
                parameter returns a linear array of floats containing
                the pixel intensities along the selected line in
                image_buffer. The required array size corresponds to
                the selected image width in function _configure_cam():
                max. 1024 for WFS150/WFS300
                max.  480 for WFS10
                max. 1080 for WFS20
                max. 1216 for WFS30
                max. 2048 for WFS40
        """
        if line is not None:
            try:
                self.line = Vi.int32(line)
            except ValueError:
                self.line = line
        status = self.lib.WFS_GetLine(self.instrument_handle,
                                      self.line,
                                      self.array_line_selected)
        self.log_wfs.debug(f'Get Line: {self.instrument_handle.value}')
        self.log_wfs.info(f'Line: {self.line.value}')
        self.log_wfs.debug('Line Selected:\n' +
                           ' '.join([f'{int(item):3}' for item in self.array_line_selected]))
        self._error_message(status)
        return status, self.array_line_selected

    def _get_line_view(self):
        """Get the linear arrays with the min and max intensities.

        This function returns two linear arrays containing the minimum
        and maximum intensities within the image columns, respectively.
        Note: This function is not available in Highspeed Mode!

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            array_line_min (Vi.array_float(int)): This parameter
                returns a linear array of floats containing the
                minimum pixel intensities within all columns of
                image_buffer. The required array size corresponds to
                the selected image width in function _configure_cam():
                max. 1280 for WFS150/WFS300
                max.  640 for WFS10
                max. 1440 for WFS20
            array_line_max (Vi.array_float(int)): This parameter
                returns a linear array of floats containing the
                maximum pixel intensities within all columns of
                image_buffer. The required array size corresponds to
                the selected image width in function _configure_cam():
                max. 1280 for WFS150/WFS300
                max.  640 for WFS10
                max. 1440 for WFS20
        """
        status = self.lib.WFS_GetLineView(self.instrument_handle,
                                          self.array_line_min,
                                          self.array_line_max)
        self.log_wfs.debug(f'Get Line View: {self.instrument_handle.value}')
        self.log_wfs.debug('Line Minimum:\n' +
                           ' '.join([f'{int(item):3}' for item in self.array_line_min]))
        self.log_wfs.debug('Line Maximum:\n' +
                           ' '.join([f'{int(item):3}' for item in self.array_line_max]))
        self._error_message(status)
        return status, self.array_line_min, self.array_line_max

    def _calc_beam_centroid_diameter(self):
        """Calculate the beam centroid and diameter in mm.

        This function calculates and returns the beam centroid and
        diameter data based on the intensity distribution of the WFS
        camera image in mm.
        Note: The beam centroid is highly sensitive to an increased
        black level of the camera image. For good accuracy it is
        recommended to set it as low as needed using function
        _set_black_level_offset. The beam diameter is calculated by
        the second moment formula. The initial beam is split into many
        spots by the lenslets which reduces accuracy also.
        This function is not available in Highspeed Mode!

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            beam_centroid_x_mm (Vi.real64(float)): This parameter
                returns the beam centroid X in mm.
            beam_centroid_y_mm (Vi.real64(float)): This parameter
                returns the beam centroid Y in mm.
            beam_diameter_x_mm (Vi.real64(float)): This parameter
                returns the beam diameter X in mm.
            beam_diameter_y_mm (Vi.real64(float)): This parameter
                returns the beam diameter Y in mm.
        """
        status = self.lib.WFS_CalcBeamCentroidDia(self.instrument_handle,
                                                  ctypes.byref(self.beam_centroid_x_mm),
                                                  ctypes.byref(self.beam_centroid_y_mm),
                                                  ctypes.byref(self.beam_diameter_x_mm),
                                                  ctypes.byref(self.beam_diameter_y_mm))
        self.log_wfs.debug(f'Calc Beam Centroid Diameter: {self.instrument_handle.value}')
        self.log_wfs.info(f'Beam Centroid X (mm): {self.beam_centroid_x_mm.value:.4f}')
        self.log_wfs.info(f'Beam Centroid Y (mm): {self.beam_centroid_y_mm.value:.4f}')
        self.log_wfs.info(f'Beam Diameter X (mm): {self.beam_diameter_y_mm.value:.4f}')
        self.log_wfs.info(f'Beam Diameter Y (mm): {self.beam_diameter_x_mm.value:.4f}')
        self._error_message(status)
        return (status, self.beam_centroid_x_mm.value, self.beam_centroid_y_mm.value,
                self.beam_diameter_y_mm.value, self.beam_diameter_x_mm.value)

    def _calc_spots_centroid_diameter_intensity(self, dynamic_noise_cut=None, calculate_diameters=None):
        """Calculate the spot centroids, diameters, and intensities.

        This function calculates the centroids, diameters (optional)
        and intensities of all spots generated by the lenslets.
        Data arrays are returned by separate functions:
        _get_spot_centroids()
        _get_spot_diameters()
        _get_spot_intensities()
        Note: This function is not available in Highspeed Mode!

        Args:
            dynamic_noise_cut (Vi.int32(int)): This parameter
                activates the dynamic noise cut function if (=1). In
                this case each detected spot is analyzed using an
                individual optimized minimum intensity limit. If it is
                not used (=0) it is recommended to use function
                _cut_image_noise_floor() prior to this function in
                order to clear lower intensity pixels at a fixed level.
            calculate_diameters (Vi.int32(int)): This parameter
                activates (=1) or deactivates (=0) the calculation of
                the spot diameters. Only when activated the function
                _get_spot_diameters can subsequently return valid spot
                diameters.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        if dynamic_noise_cut is not None:
            try:
                self.dynamic_noise_cut = Vi.int32(dynamic_noise_cut)
            except ValueError:
                self.dynamic_noise_cut = dynamic_noise_cut
        if calculate_diameters is not None:
            try:
                self.calculate_diameters = Vi.int32(calculate_diameters)
            except ValueError:
                self.calculate_diameters = calculate_diameters
        status = self.lib.WFS_CalcSpotsCentrDiaIntens(self.instrument_handle,
                                                      self.dynamic_noise_cut,
                                                      self.calculate_diameters)
        self.log_wfs.debug(f'Calc Spots Centroid Diameter Intensity: {self.instrument_handle.value}')
        self.log_wfs.info(f'Dynamic Noise Cut: {self.dynamic_noise_cut.value}')
        self.log_wfs.info(f'Calculate diameters: {self.calculate_diameters.value}')
        self._error_message(status)
        return status

    def _get_spot_centroids(self):
        """Get the spot centroids in X and Y in pixels.

        This function returns two two-dimensional arrays containing the
        centroid X and Y positions in pixels calculated by function
        _calc_spots_centroid_diameter_intensity. Note: Function
        _calc_spots_centroid_diameter_intensity is required to run
        successfully before calculated data can be retrieved.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            array_centroid_x (Vi.array_float(int, int)): This
                parameter returns a two-dimensional array of floats
                containing the centroid X spot positions in pixels.
                The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].
                Note: First array index is the spot number in Y,
                second index the spot number in X direction.
            array_centroid_y (Vi.array_float(int, int)): This
                parameter returns a two-dimensional array of floats
                containing the centroid Y spot positions in pixels.
                The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].
                Note: First array index is the spot number in Y,
                second index the spot number in X direction.
        """
        status = self.lib.WFS_GetSpotCentroids(self.instrument_handle,
                                               self.array_centroid_x,
                                               self.array_centroid_y)
        columns = self.spots_x.value
        rows = self.spots_y.value
        self.log_wfs.debug(f'Get Spot Centroids: {self.instrument_handle.value}')
        self.log_wfs.debug('Centroid X:\n' + '\n'.join(
            [' '.join([f'{item:12.8}' for item in row[:columns]]) for row in self.array_centroid_x[:rows]]))
        self.log_wfs.debug('Centroid Y:\n' + '\n'.join(
            [' '.join([f'{item:12.8}' for item in row[:columns]]) for row in self.array_centroid_y[:rows]]))
        self._error_message(status)
        return status, self.array_centroid_x, self.array_centroid_y

    def _get_spot_diameters(self):
        """Get the spot diameters in X and Y in pixels.

        This function returns two two-dimensional arrays containing the
        spot diameters in X and Y direction in pixels calculated by
        function _calc_spots_centroid_diameter_intensity(). Note:
        Function _calc_spots_centroid_diameter_intensity() is required
        to run successfully with option calculate_diameters = 1 before
        calculated data can be retrieved.
        This function is not available in Highspeed Mode!

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            array_diameter_x (Vi.array_float(int, int)): This
                parameter returns a two-dimensional array of floats
                containing the spot diameters X positions in pixels.
                The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].
                Note: First array index is the spot number in Y,
                second index the spot number in X direction.
            array_diameter_y (Vi.array_float(int, int)): This
                parameter returns a two-dimensional array of floats
                containing the spot diameters Y positions in pixels.
                The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].
                Note: First array index is the spot number in Y,
                second index the spot number in X direction.
        """
        status = self.lib.WFS_GetSpotDiameters(self.instrument_handle,
                                               self.array_diameter_x,
                                               self.array_diameter_y)
        columns = self.spots_x.value
        rows = self.spots_y.value
        self.log_wfs.debug(f'Get Spot Diameters: {self.instrument_handle.value}')
        self.log_wfs.debug('Diameter X:\n' + '\n'.join(
            [' '.join([f'{item:12.8}' for item in row[:columns]]) for row in self.array_diameter_x[:rows]]))
        self.log_wfs.debug('Diameter Y:\n' + '\n'.join(
            [' '.join([f'{item:12.8}' for item in row[:columns]]) for row in self.array_diameter_y[:rows]]))
        self._error_message(status)
        return status, self.array_diameter_x, self.array_diameter_y

    def _get_spot_diameters_statistics(self):
        """Get the calculated statistic parameters of the wavefront.

        This function calculates statistic parameters of the wavefront
        calculated in function _calc_wavefront().
        Note: Function _calc_wavefront() is required to run prior to
        this function.
        This function is not available in Highspeed Mode!

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            diameter_min (Vi.real64(float)): This parameter returns
                the Minimum spot diameter.
            diameter_max (Vi.real64(float)): This parameter returns
                the Maximum spot diameter.
            diameter_mean (Vi.real64(float)): This parameter returns
                the Mean average of spot diameters.
        """
        status = self.lib.WFS_GetSpotDiaStatistics(self.instrument_handle,
                                                   ctypes.byref(self.diameter_min),
                                                   ctypes.byref(self.diameter_max),
                                                   ctypes.byref(self.diameter_mean))
        self.log_wfs.debug(f'Get Spot Diameter Statistics: {self.instrument_handle.value}')
        self.log_wfs.info(f'Diameter Minimum: {self.diameter_min.value:.4f}')
        self.log_wfs.info(f'Diameter Maximum: {self.diameter_max.value:.4f}')
        self.log_wfs.info(f'Diameter Mean: {self.diameter_mean.value:.4f}')
        self._error_message(status)
        return status, self.diameter_min.value, self.diameter_max.value, self.diameter_mean.value

    def _get_spot_intensities(self):
        """Get the spot intensities in X and Y in arbitrary units.

        This function returns a two-dimensional array containing the
        spot intensities in arbitrary unit calculated by function
        _calc_spots_centroid_diameter_intensity(). Note: Function
        _calc_spots_centroid_diameter_intensity() is required to run
        successfully before calculated data can be retrieved.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            array_intensity (Vi.array_float(int, int)): This
                parameter returns a two-dimensional array of floats
                containing the spot intensities in arbitrary units.
                The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].
                Note: First array index is the spot number in Y,
                second index the spot number in X direction.
        """
        status = self.lib.WFS_GetSpotIntensities(self.instrument_handle,
                                                 self.array_intensity)
        columns = self.spots_x.value
        rows = self.spots_y.value
        self.log_wfs.debug(f'Get Spot Intensities: {self.instrument_handle.value}')
        self.log_wfs.debug('Intensity:\n' + '\n'.join(
            [' '.join([f'{int(item):6}' for item in row[:columns]]) for row in self.array_intensity[:rows]]))
        self._error_message(status)
        return status, self.array_intensity

    def _calc_spot_to_reference_deviations(self, cancel_wavefront_tilt=None):
        """Calculate reference positions and deviations for all spots.

        This function calculates reference positions and deviations
        for all spots depending on the setting reference_index
        (internal/user) set by function _set_reference_plane().
        When option cancel_wavefront_tilt is enabled the mean
        deviation in X and Y direction is subtracted from the
        deviation data arrays. Reference positions can be retrieved
        using function _get_spot_reference_positions() and calculated
        deviations by function _get_spot_deviations().

        Args:
            cancel_wavefront_tilt (Vi.int32(int)): This parameter
                forces the mean spot deviations to be canceled so that
                the average wavefront tilt will disappear when
                calculated with function _calc_wavefront().
                Valid values:
                0 - calculate deviations normal
                1 - subtract mean deviation from all spot deviations

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        if cancel_wavefront_tilt is not None:
            try:
                self.cancel_wavefront_tilt = Vi.int32(cancel_wavefront_tilt)
            except ValueError:
                self.cancel_wavefront_tilt = cancel_wavefront_tilt
        status = self.lib.WFS_CalcSpotToReferenceDeviations(self.instrument_handle,
                                                            self.cancel_wavefront_tilt)
        self.log_wfs.debug(f'Calc Spot to Reference Deviations: {self.instrument_handle.value}')
        self.log_wfs.info(f'Cancel Wavefront Tilt: {self.cancel_wavefront_tilt.value}')
        self._error_message(status)
        return status

    def _get_spot_reference_positions(self):
        """Get the arrays with actual X and Y spot positions in pixels.

        This function returns two two-dimensional arrays containing
        the actual X and Y reference spot positions in pixels. A prior
        call to function _set_reference_plane() determines whether the
        internal or user defined reference positions are returned.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            array_reference_x (Vi.array_float(int, int)): This
                parameter returns a two-dimensional array of floats
                containing the reference X spot positions in pixels.
                The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].
                Note: First array index is the spot number in Y,
                second index the spot number in X direction.
            array_reference_y (Vi.array_float(int, int)): This
                parameter returns a two-dimensional array of floats
                containing the reference Y spot positions in pixels.
                The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].
                Note: First array index is the spot number in Y,
                second index the spot number in X direction.
        """
        status = self.lib.WFS_GetSpotReferencePositions(self.instrument_handle,
                                                        self.array_reference_x,
                                                        self.array_reference_y)
        self.log_wfs.debug(f'Get Spot Reference Positions: {self.instrument_handle.value}')
        columns = self.spots_x.value
        rows = self.spots_y.value
        self.log_wfs.debug('Reference X:\n' + '\n'.join(
            [' '.join([f'{item:12.8}' for item in row[:columns]]) for row in self.array_reference_x[:rows]]))
        self.log_wfs.debug('Reference Y:\n' + '\n'.join(
            [' '.join([f'{item:12.8}' for item in row[:columns]]) for row in self.array_reference_y[:rows]]))
        self._error_message(status)
        return status, self.array_reference_x, self.array_reference_y

    def _get_spot_deviations(self):
        """Get the arrays with actual X and Y spot deviations in pixels.

        This function returns two two-dimensional arrays containing
        the actual X and Y spot deviations between centroid and
        reference spot positions in pixels calculated by function
        _calc_spot_to_reference_deviations(). Note: Function
        _calc_spot_to_reference_deviations() needs to run prior to
        this function.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            array_deviations_x (Vi.array_float(int, int)): This
                parameter returns a two-dimensional array of floats
                containing the reference X spot positions in pixels.
                The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].
                Note: First array index is the spot number in Y,
                second index the spot number in X direction.
            array_deviations_y (Vi.array_float(int, int)): This
                parameter returns a two-dimensional array of floats
                containing the reference Y spot positions in pixels.
                The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].
                Note: First array index is the spot number in Y,
                second index the spot number in X direction.
        """
        status = self.lib.WFS_GetSpotDeviations(self.instrument_handle,
                                                self.array_deviations_x,
                                                self.array_deviations_y)
        columns = self.spots_x.value
        rows = self.spots_y.value
        self.log_wfs.debug(f'Get Spot Deviations: {self.instrument_handle.value}')
        self.log_wfs.debug('Deviations X:\n' + '\n'.join(
            [' '.join([f'{item:12.8}' for item in row[:columns]]) for row in self.array_deviations_x[:rows]]))
        self.log_wfs.debug('Deviations Y:\n' + '\n'.join(
            [' '.join([f'{item:12.8}' for item in row[:columns]]) for row in self.array_deviations_y[:rows]]))
        self._error_message(status)
        return status, self.array_deviations_x, self.array_deviations_y

    def _zernike_lsf(self, zernike_orders=None):
        """Calculate Zernike coefficients and Radius of Curvature in mm.

        This function calculates the spot deviations (centroid with
        respect to its reference) and performs a least square fit to
        the desired number of Zernike functions. Output results are
        the Zernike coefficients up to the desired number of Zernike
        modes and an array summarizing these coefficients to rms
        amplitudes for each Zernike order.

        Args:
            zernike_orders (Vi.int32(int)): This parameter sets and
                returns the number of desired Zernike modes to fit.
                An input value 0 sets the number of calculated modes
                automatically, depending on the number of available
                spot deviations, and returns it. Input values in the
                range 2 ... 10 define the number of calculated Zernike
                modes according to this table:
                Input Zernike Order  Calculated Zernike Modes
                0 = auto             auto
                2                      6
                3                     10
                4                     15
                5                     21
                6                     28
                7                     36
                8                     45
                9                     55
                10                    66

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            roc_mm (Vi.real64(float)): This parameter returns the
                Radius of Curvature RoC for a spherical wavefront
                in mm, derived from Zernike coefficient Z[5].
            zernike_modes (Vi.int32(int)): This parameter returns the
                number of desired Zernike modes to fit based on order.
            array_zernike_um (Vi.array_float(int)): This
                parameter returns a one-dimensional array of float
                containing the calculated Zernike coefficients. The
                required array size is [MAX_ZERNIKE_MODES+1] because
                indices [1..66] are used instead of [0 .. 65].
            array_zernike_orders_um (Vi.array_float(int)): This
                parameter returns a one-dimensional array of float
                containing the calculated Zernike coefficients
                summarizing these coefficients to rms amplitudes for
                each Zernike order. The required array size is
                [MAX_ZERNIKE_ORDERS+1] because indices [1..10] are
                used instead of [0 .. 9].
        """
        if zernike_orders is not None:
            try:
                self.zernike_orders = Vi.int32(zernike_orders)
            except ValueError:
                self.zernike_orders = zernike_orders
        status = self.lib.WFS_ZernikeLsf(self.instrument_handle,
                                         ctypes.byref(self.zernike_orders),
                                         self.array_zernike_um,
                                         self.array_zernike_orders_um,
                                         ctypes.byref(self.roc_mm))
        self.log_wfs.debug(f'Zernike Least Square Fit: {self.instrument_handle.value}')
        try:
            self.zernike_modes.value = self.zernike_modes_per_order[self.zernike_orders.value]
        except KeyError:
            self.zernike_modes.value = self.MAX_ZERNIKE_MODES
            self.log_wfs.error('Invalid Zernike Order')
            self._error_message(status)
            return (status, self.roc_mm.value, self.zernike_orders.value,
                    self.array_zernike_um, self.array_zernike_orders_um)
        self.log_wfs.info(f'RoC (mm): {self.roc_mm.value:.4f}')
        self.log_wfs.info(f'Zernike Modes: {self.zernike_modes.value}')
        self.log_wfs.info(f'Zernike Orders: {self.zernike_orders.value}')
        self.log_wfs.info('Zernike (µm): ' + ' '.join(
            [f'{item:.8f}' for item in self.array_zernike_um[1:self.zernike_modes.value+1]]))
        self.log_wfs.info('Zernike Orders (µm): ' + ' '.join(
            [f'{item:.8f}' for item in self.array_zernike_orders_um[1:self.zernike_orders.value+1]]))
        self._error_message(status)
        return (status, self.roc_mm.value, self.zernike_orders.value,
                self.array_zernike_um, self.array_zernike_orders_um)

    def _calc_fourier_optometric(self, zernike_orders=None, fourier_orders=None):
        """Calculate the Fourier and Optometric notations from Zernikes.

        This function calculates the Fourier and Optometric notations
        from the Zernike coefficients calculated in function
        _zernike_lsf(). Note: Function _zernike_lsf() is required to
        run prior to this function.

        Args:
            zernike_orders (Vi.int32(int)): This parameter is the
                calculated number of Zernike orders in function
                _zernike_lsf(). Use the value returned from this
                function.
            fourier_orders (Vi.int32(int)): This parameter defines the
                highest Zernike order considered for calculating
                Fourier coefficients M, J0 and J45 as well as the
                Optometric parameters Sphere, Cylinder and Axis.
                Valid settings: 2, 4 or 6

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            fourier_m (Vi.real64(float)): This parameter returns
                Fourier coefficient M.
            fourier_j0 (Vi.real64(float)): This parameter returns
                Fourier coefficient J0.
            fourier_j45 (Vi.real64(float)): This parameter returns
                Fourier coefficient J45.
            optometric_sphere (Vi.real64(float)): This parameter
                returnsOptometric parameter Sphere in diopters.
            optometric_cylinder (Vi.real64(float)): This parameter
                returns Optometric parameter Cylinder in diopters.
            optometric_axis (Vi.real64(float)): This parameter returns
                Optometric parameter Axis in deg.
        """
        if zernike_orders is not None:
            try:
                self.zernike_orders = Vi.int32(zernike_orders)
            except ValueError:
                self.zernike_orders = zernike_orders
        if fourier_orders is not None:
            try:
                self.fourier_orders = Vi.int32(fourier_orders)
            except ValueError:
                self.fourier_orders = fourier_orders
        status = self.lib.WFS_CalcFourierOptometric(self.instrument_handle,
                                                    self.zernike_orders,
                                                    self.fourier_orders,
                                                    ctypes.byref(self.fourier_m),
                                                    ctypes.byref(self.fourier_j0),
                                                    ctypes.byref(self.fourier_j45),
                                                    ctypes.byref(self.optometric_sphere),
                                                    ctypes.byref(self.optometric_cylinder),
                                                    ctypes.byref(self.optometric_axis))
        self.log_wfs.debug(f'Calc Fourier Optometric: {self.instrument_handle.value}')
        self.log_wfs.info(f'Zernike Orders: {self.zernike_orders.value}')
        self.log_wfs.info(f'Fourier Orders: {self.fourier_orders.value}')
        self.log_wfs.info(f'Fourier Coefficient M: {self.fourier_m.value:.8f}')
        self.log_wfs.info(f'Fourier Coefficient J0: {self.fourier_j0.value:.8f}')
        self.log_wfs.info(f'Fourier Coefficient J45: {self.fourier_j45.value:.8f}')
        self.log_wfs.info(f'Optometric Parameter Sphere (diopters): {self.optometric_sphere.value:.8f}')
        self.log_wfs.info(f'Optometric Parameter Cylinder (diopters): {self.optometric_cylinder.value:.8f}')
        self.log_wfs.info(f'Optometric Parameter Axis (°): {self.optometric_axis.value:.8f}')
        self._error_message(status)
        return (status, self.fourier_m.value, self.fourier_j0.value, self.fourier_j45.value,
                self.optometric_sphere.value, self.optometric_cylinder.value, self.optometric_axis.value)

    def _calc_reconstructed_deviations(self, zernike_orders=None, array_zernike_reconstructed=None,
                                       do_spherical_reference=None):
        """Calculate the reconstructed spot deviations from Zernikes.

        This function calculates the reconstructed spot deviations
        based on the calculated Zernike coefficients. Note: This
        function needs to run prior to function _calc_wavefront() when
        the reconstructed or difference Wavefront should be calculated.

        Args:
            zernike_orders (Vi.int32(int)): This parameter is the
                calculated number of Zernike orders in function
                _zernike_lsf(). Use the value returned from this
                function.
            array_zernike_reconstructed (Vi.array_uint8(int)):
                This parameter accepts a one-dimensional array of
                content 0 or 1 indicating if the appropriate Zernike
                mode is checked for reconstruction or not. Note:
                Required array dimension is [MAX_ZERNIKE_MODES+1]
                because valid indices are [1 ... 66] instead of
                [0 ... 65]. Valid array values:
                0 - ignore this Zernike mode in reconstruction
                1 - reconstruct this Zernike mode
            do_spherical_reference (Vi.int32(int)): This parameter
                forces only Zernike mode Z[5] to be reconstructed in
                order to get deviations based on a pure spherical
                wavefront. Set parameter to 1 to perform a Spherical
                Reference calibration. Valid values:
                0 - use all Zernike Modes checked in
                    array_zernike_reconstructed
                1 - use only Z[5] for pure spherical reconstruction

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            fit_error_mean (Vi.real64(float)): This parameter returns
                the Mean Fit error in arcmin.
            fit_error_stdev (Vi.real64(float)): This parameter returns
                the Standard Deviation Fit error in arcmin.
        """
        if zernike_orders is not None:
            try:
                self.zernike_orders = Vi.int32(zernike_orders)
            except ValueError:
                self.zernike_orders = zernike_orders
        if array_zernike_reconstructed is not None:
            if isinstance(array_zernike_reconstructed, list):
                self.array_zernike_reconstructed = Vi.array_uint8(self.MAX_ZERNIKE_MODES+1)
                for i in range(len(array_zernike_reconstructed)):
                    # Offset one because of we ignore the 0th index
                    self.array_zernike_reconstructed[i+1] = array_zernike_reconstructed[i]
            else:
                self.array_zernike_reconstructed = array_zernike_reconstructed
        if do_spherical_reference is not None:
            try:
                self.do_spherical_reference = Vi.int32(do_spherical_reference)
            except ValueError:
                self.do_spherical_reference = do_spherical_reference
        status = self.lib.WFS_CalcReconstrDeviations(self.instrument_handle,
                                                     self.zernike_orders,
                                                     self.array_zernike_reconstructed,
                                                     self.do_spherical_reference,
                                                     ctypes.byref(self.fit_error_mean),
                                                     ctypes.byref(self.fit_error_stdev))
        self.zernike_modes.value = self.zernike_modes_per_order[self.zernike_orders.value]
        self.log_wfs.debug(f'Calc Reconstructed Deviations: {self.instrument_handle.value}')
        self.log_wfs.info(f'Zernike Modes: {self.zernike_modes.value}')
        self.log_wfs.info(f'Zernike Orders: {self.zernike_orders.value}')
        self.log_wfs.debug('Zernike Reconstruction: ' + ' '.join(
            [f'{item}' for item in self.array_zernike_reconstructed[1:self.zernike_modes.value+1]]))
        self.log_wfs.info(f'Do Spherical Reference: {self.do_spherical_reference.value}')
        self.log_wfs.info(f'Fit Error Mean: {self.fit_error_mean.value:.8f}')
        self.log_wfs.info(f'Fit Error Standard Deviation: {self.fit_error_stdev.value:.8f}')
        self._error_message(status)
        return status, self.fit_error_mean.value, self.fit_error_stdev.value

    def _calc_wavefront(self, wavefront_type=None, limit_to_pupil=None):
        """Calculate the wavefront based on the spot deviations.

        This function calculates the wavefront based on the spot deviations.

        Args:
            wavefront_type (Vi.int32(int)): This parameter defines the
                type of wavefront to calculate. Valid settings:
                0 - Measured Wavefront
                1 - Reconstructed Wavefront based on Zernike
                    coefficients
                2 - Difference between measured and reconstructed
                    Wavefront
                Note: Function _calc_reconstructed_deviations() needs
                to be called prior to this function in case of
                Wavefront type 1 and 2.
            limit_to_pupil (Vi.int32(int)): This parameter defines if
                the Wavefront should be calculated based on all
                detected spots or only within the defined pupil.
                Valid settings:
                0 - Calculate Wavefront for all spots
                1 - Limit Wavefront to pupil interior

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            array_wavefront (Vi.array_float(int, int)): This
                parameter returns a two-dimensional array of floats
                containing wavefront data in µm.
                The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].
                Note: First array index is the spot number in Y,
                second index the spot number in X direction.
                You may used function _flip_2d_array() to flip the
                index order prior to display by a graphical tool.

        """
        if wavefront_type is not None:
            try:
                self.wavefront_type = Vi.int32(wavefront_type)
            except ValueError:
                self.wavefront_type = wavefront_type
        if limit_to_pupil is not None:
            try:
                self.limit_to_pupil = Vi.int32(limit_to_pupil)
            except ValueError:
                self.limit_to_pupil = limit_to_pupil
        status = self.lib.WFS_CalcWavefront(self.instrument_handle,
                                            self.wavefront_type,
                                            self.limit_to_pupil,
                                            self.array_wavefront)
        columns = self.spots_x.value
        rows = self.spots_y.value
        self.log_wfs.debug(f'Calc Wavefront: {self.instrument_handle.value}')
        self.log_wfs.info(f'Wavefront Type: {self.wavefront_type.value}')
        self.log_wfs.info(f'Limit to Pupil: {self.limit_to_pupil.value}')
        self.log_wfs.debug('Wavefront:\n' + '\n'.join(
            [' '.join([f'{item:12.8}' for item in row[:columns]]) for row in self.array_wavefront[:rows]]))
        self._error_message(status)
        return status, self.array_wavefront

    def _calc_wavefront_statistics(self):
        """Calculate statistic parameters of the wavefront in µm.

        This function returns statistic parameters of the wavefront
        in µm calculated by function _calc_wavefront().
        Note: Function _calc_wavefront() is required to run prior
        to this function.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            wavefront_min (Vi.real64(float)): This parameter returns
                the minimum value of the wavefront.
            wavefront_max (Vi.real64(float)): This parameter returns
                the maximum value of the wavefront.
            wavefront_diff (Vi.real64(float)): This parameter returns
                the difference between maximum and minimum of the
                wavefront.
            wavefront_mean (Vi.real64(float)): This parameter returns
                the mean value of the wavefront.
            wavefront_rms (Vi.real64(float)): This parameter returns
                the RMS value of the wavefront.
            wavefront_weighted_rms (Vi.real64(float)): This parameter
                returns the weighted RMS value of the wavefront. The
                weighting is based on the individual spot intensity.
        """
        status = self.lib.WFS_CalcWavefrontStatistics(self.instrument_handle,
                                                      ctypes.byref(self.wavefront_min),
                                                      ctypes.byref(self.wavefront_max),
                                                      ctypes.byref(self.wavefront_diff),
                                                      ctypes.byref(self.wavefront_mean),
                                                      ctypes.byref(self.wavefront_rms),
                                                      ctypes.byref(self.wavefront_weighted_rms))
        self.log_wfs.debug(f'Calc Wavefront Statistics: {self.instrument_handle.value}')
        self.log_wfs.info(f'Min: {self.wavefront_min.value:.4f}')
        self.log_wfs.info(f'Max: {self.wavefront_max.value:.4f}')
        self.log_wfs.info(f'Diff: {self.wavefront_diff.value:.4f}')
        self.log_wfs.info(f'Mean: {self.wavefront_mean.value:.4f}')
        self.log_wfs.info(f'RMS: {self.wavefront_rms.value:.4f}')
        self.log_wfs.info(f'Weighted RMS: {self.wavefront_weighted_rms.value:.4f}')
        self._error_message(status)
        return (status, self.wavefront_min.value, self.wavefront_max.value, self.wavefront_diff.value,
                self.wavefront_mean.value, self.wavefront_rms.value, self.wavefront_weighted_rms.value)

    # Utility Functions
    def _self_test(self):
        """Perform a self-test of the instrument.

        This function causes the instrument to perform a self-test and
        returns the result of that self-test.

        Returns:
            status (Vi.status(int)): Operational return status.
                Contains either a completion code or an error code.
                Instrument driver specific codes that may be returned
                in addition to the VISA error codes defined in VPP-4.3
                and vendor specific codes, are as follows:
                WFS_SUCCESS - Self-test operation successful
                WFS_WARN_NSUP_SELF_TEST - Self-test  not supported
                For Status Codes see function _error_message.
            test_result (Vi.int16(int)): Numeric result from self-test
                operation, 0 = no error (test passed).
            test_message (Vi.char(int)): Self-test status message.
        """
        status = self.lib.WFS_self_test(self.instrument_handle,
                                        ctypes.byref(self.test_result),
                                        self.test_message)
        self.log_wfs.debug(f'Self Test: {self.instrument_handle.value}')
        self.log_wfs.info(f'Self Test Result: {self.test_result.value}')
        self.log_wfs.info(f'Self Test Message: {self.test_message.value.decode()}')
        self._error_message(status)
        return status, self.test_result.value, self.test_message.value

    def _reset(self):
        """Places the instrument in a default state.

        Returns:
            status (Vi.status(int)): Operational return status.
                Contains either a completion code or an error code.
                Instrument driver specific codes that may be returned
                in addition to the VISA error codes defined in VPP-4.3
                and vendor specific codes, are as follows:
                WFS_SUCCESS - Reset operation successful
                WFS_WARN_NSUP_RESET - Reset operation not supported
                For Status Codes see function _error_message.
        """
        status = self.lib.WFS_reset(self.instrument_handle)
        self.log_wfs.debug(f'Reset: {self.instrument_handle.value}')
        self._error_message(status)
        return status

    def _revision_query(self):
        """Queries the instrument for driver and firmware revisions.

        This function returns the revision of the instrument driver
        and the firmware revision of the instrument being used.

        Returns:
            status (Vi.status(int)): Operational return status.
                Contains either a completion code or an error code.
                Instrument driver specific codes that may be returned
                in addition to the VISA error codes defined in VPP-4.3
                and vendor specific codes, are as follows:
                WFS_SUCCESS - Revision query operation successful
                WFS_WARN_NSUP_REV_QUERY - Revision query not supported
                For Status Codes see function _error_message.
            instrument_driver_revision (Vi.char(int)): Instrument
                driver revision. The message buffer has to be
                initialized with 256 bytes.
            firmware_revision (Vi.char(int)): Instrument firmware
                revision. The message buffer has to be initialized
                with 256 bytes.
        """
        status = self.lib.WFS_revision_query(self.instrument_handle,
                                             self.instrument_driver_revision,
                                             self.firmware_revision)
        self.log_wfs.debug(f'Revision Query: {self.instrument_handle.value}')
        self.log_wfs.info(f'Instrument Driver Version: {self.instrument_driver_revision.value.decode()}')
        self.log_wfs.info(f'Instrument Firmware Version: {self.firmware_revision.value.decode()}')
        self._error_message(status)
        return status, self.instrument_driver_revision.value, self.firmware_revision.value

    def _error_query(self):
        """Queries the instrument for specific error information.

        This function queries the instrument and returns instrument-
        specific error information.

        Returns:
            status (Vi.status(int)): Operational return status.
                Contains either a completion code or an error code.
                Instrument driver specific codes that may be returned
                in addition to the VISA error codes defined in VPP-4.3
                and vendor specific codes, are as follows:
                WFS_SUCCESS - Error query operation successful
                WFS_WARN_NSUP_ERROR_QUERY - Error query not supported
                For Status Codes see function _error_message.
            error_code (Vi.status(int)): Instrument error code
                returned by driver functions.
            error_message (Vi.char(int)): Error message. The message
                buffer has to be initialized with 256 bytes.
        """
        status = self.lib.WFS_error_query(self.instrument_handle,
                                          ctypes.byref(self.error_code),
                                          self.error_message)
        self.log_wfs.debug(f'Error Query: {self.instrument_handle.value}')
        self.log_wfs.info(f'Error Code: {self.error_code.value}')
        self.log_wfs.error(f'Error Message: {self.error_message.value.decode()}')
        self._error_message(status)
        return status, self.error_code.value, self.error_message.value

    def _error_message(self, error_code=None):
        """Translates an error code into its user-readable message.

        This function translates the error return value from a
        VXI plug&play instrument driver function to a user-readable
        string.

        Args:
            error_code (Vi.status(int)): Instrument driver error code.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            error_message (Vi.char(int)): VISA or instrument driver
                error message. The message buffer has to be initialized
                with 256 bytes.
        """
        if error_code is not None:
            try:
                self.error_code = Vi.status(error_code)
            except ValueError:
                self.error_code = error_code
        if self.error_code.value == 0:
            self.log_wfs.debug(f'No error: {self.error_code.value}')
            self.error_message.value = b'No errors'
            status = 0
            return status, self.error_message.value
        elif self.error_code.value in self.WFS_WARNING_CODES:
            self.log_wfs.warning(self.WFS_WARNING_CODES[self.error_code.value].decode())
            self.error_message.value = self.WFS_WARNING_CODES[self.error_code.value]
            status = 0
            return status, self.error_message.value
        status = self.lib.WFS_error_message(self.instrument_handle,
                                            self.error_code,
                                            self.error_message)
        if self.error_code.value == self.WFS_ERROR_CORRUPT_REF_FILE:
            # Typo in reference is expected in normal return message
            self.error_message.value = b'Corrupt reference file!'
        # self.log_wfs.debug(f'Error Message: {self.instrument_handle.value}')
        self.log_wfs.info(f'Error Code: {self.error_code.value}')
        self.log_wfs.error(f'Error Message: {self.error_message.value.decode()}')
        return status, self.error_message.value

    def _get_instrument_list_len(self):
        """Get the information about all WFS Instrument indexes.

        This function reads all Wavefront Sensor devices connected to
        the PC and returns the number of it. Use function
        _get_instrument_list_info to retrieve information about each
        WFS instrument.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            instrument_index (Vi.int32(int)): This parameter returns
                the index of WFS instruments connected to the PC.
            instrument_count (Vi.int32(int)): This parameter returns
                the number of WFS instruments connected to the PC.
        """
        status = self.lib.WFS_GetInstrumentListLen(Vi.NULL,
                                                   ctypes.byref(self.instrument_count))
        self.instrument_index = Vi.int32(self.instrument_count.value - 1)
        self.log_wfs.debug(f'Get Instrument List Length: {Vi.NULL}')
        self.log_wfs.debug(f'Instrument Count: {self.instrument_count.value}')
        self.log_wfs.info(f'Instrument Index: {self.instrument_index.value}')
        self._error_message(status)
        return status, self.instrument_index.value, self.instrument_count.value

    def _get_instrument_list_info(self):
        """Get the information about a WFS Instrument based on index.

        This function returns information about one connected WFS
        instrument selected by Instrument Index.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            device_id (Vi.int32(int)): This parameter returns the
                Device ID required to open the WFS instrument in
                function _init.
            in_use (Vi.int32(int)): This parameter returns the
                information if the instrument is already used by
                another application or driver session.
                0 - Not in use, free to open
                1 - Already in use
                Note: An instrument already in use will fail to open
                in function _init.
            instrument_name_wfs (Vi.char(int)): This parameter returns
                the Instrument Name of the selected instrument.
                Note: The string must contain at least WFS_BUFFER_SIZE
                (256) elements (Vi.char(WFS_BUFFER_SIZE)).
            serial_number_wfs (Vi.char(int)): This parameter returns
                the Serial Number of the selected instrument.
                Note: The string must contain at least WFS_BUFFER_SIZE
                (256) elements (Vi.char(WFS_BUFFER_SIZE)).
            resource_name (Vi.rsrc(int, str)): 	This resource name can
                be used for the _int function. The string has the
                format: "USB::0x1313::0x0000::" followed by the device
                ID.
        """
        status = self.lib.WFS_GetInstrumentListInfo(Vi.NULL,
                                                    self.instrument_index,
                                                    ctypes.byref(self.device_id),
                                                    ctypes.byref(self.in_use),
                                                    self.instrument_name_wfs,
                                                    self.serial_number_wfs,
                                                    self.resource_name)
        self.log_wfs.debug(f'Get Instrument List Info: {Vi.NULL}')
        self.log_wfs.info(f'Instrument Index: {self.instrument_index.value}')
        self.log_wfs.info(f'Device ID: {self.device_id.value}')
        self.log_wfs.info(f'In Use: {self.in_use.value}')
        self.log_wfs.info(f'Instrument Name WFS: {self.instrument_name_wfs.value.decode()}')
        self.log_wfs.info(f'Serial Number WFS: {self.serial_number_wfs.value.decode()}')
        self.log_wfs.info(f'Resource Name: {self.resource_name.value.decode()}')
        self._error_message(status)
        return (status, self.instrument_index.value, self.device_id.value, self.instrument_name_wfs.value,
                self.serial_number_wfs.value, self.resource_name.value)

    def _get_xy_scale(self):
        """Get X and Y scales for spot intensity and wavefront in mm.

        This function returns two one-dimensional arrays containing the
        X and Y axis scales in mm for spot intensity and wavefront
        arrays. The center spot in the image center is denoted
        (0.0, 0.0) mm.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            array_scale_x ((ctypes.float*X)()): This parameter returns
                a one-dimensional array containing the X scale in mm.
                The required array size is MAX_SPOTS_X.
            array_scale_x ((ctypes.float*X)()): This parameter returns
                a one-dimensional array containing the Y scale in mm.
                The required array size is MAX_SPOTS_Y.
        """
        status = self.lib.WFS_GetXYScale(self.instrument_handle,
                                         self.array_scale_x,
                                         self.array_scale_y)
        columns = self.spots_x.value
        rows = self.spots_y.value
        self.log_wfs.debug(f'Get XY Scale: {self.instrument_handle.value}')
        self.log_wfs.debug('Array Scale X:\n' + ' '.join([f'{item:8.3f}' for item in self.array_scale_x[:columns]]))
        self.log_wfs.debug('Array Scale Y:\n' + ' '.join([f'{item:8.3f}' for item in self.array_scale_y[:rows]]))
        self._error_message(status)
        return status, self.array_scale_x, self.array_scale_y

    def _convert_wavefront_waves(self, wavelength=None, array_wavefront=None):
        """Convert wavefront from µm into waves based on wavelength.

        This function converts the wavefront data array calculated by
        function CalcWavefront() from µm into waves unit depending on
        the actual wavelength.

        Args:
            wavelength (Vi.real64(float)): This parameter accepts the
                actual wavelength in nm. Valid range: 300 ... 1100 nm.
            array_wavefront (((ctypes.float*X)*Y)()): This parameter
                accepts a two-dimensional array of float containing the
                wavefront data in µm.
                The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            array_wavefront_wave (((ctypes.float*X)*Y)()): This
                parameter returns a two-dimensional array of float
                containing the wavefront data in waves. The required
                array size is [MAX_SPOTS_Y][MAX_SPOTS_X].
        """
        if wavelength is not None:
            try:
                self.wavelength = Vi.real64(wavelength)
            except ValueError:
                self.wavelength = wavelength
        if array_wavefront is not None:
            self.array_wavefront = array_wavefront
        status = self.lib.WFS_ConvertWavefrontWaves(self.instrument_handle,
                                                    self.wavelength,
                                                    self.array_wavefront,
                                                    self.array_wavefront_wave)
        columns = self.spots_x.value
        rows = self.spots_y.value
        self.log_wfs.debug(f'Convert Wavefront to Waves: {self.instrument_handle.value}')
        self.log_wfs.info(f'Wavelength: {self.wavelength.value}')
        self.log_wfs.debug('Wavefront (µm):\n' + '\n'.join(
            [' '.join([f'{item:12.8}' for item in row[:columns]]) for row in self.array_wavefront[:rows]]))
        self.log_wfs.debug('Wavefront (waves):\n' + '\n'.join(
            [' '.join([f'{item:12.8}' for item in row[:columns]]) for row in self.array_wavefront_wave[:rows]]))
        self._error_message(status)
        return status, self.array_wavefront_wave

    def _flip_2d_array(self, array_wavefront_yx=None):
        """Flip a 2D array YX into another array XY.

        This function flips a 2-dimensional array of size
        array_wavefront_yx[MAX_SPOTS_Y][MAX_SPOTS_X] into another array
        array_wavefront_xy[MAX_SPOTS_X][MAX_SPOTS_Y] with flipped x, y
        index order.
        This function is helpful to convert data arrays calculated by
        this WFS driver into a format accepted by graphic tools for
        display.

        Args:
            array_wavefront_yx (((ctypes.float*X)*Y)()): This parameter
                accepts a two-dimensional array of float and array size
                [MAX_SPOTS_Y][MAX_SPOTS_X].

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
            array_reference_xy (((ctypes.float*Y)*X)()): This parameter
                returns a two-dimensional array of float and array size
                [MAX_SPOTS_X][MAX_SPOTS_Y]. All array indices are
                flipped compared to input ArrayYX
                Note: Array XY must not be the same as Array YX!
        """
        if array_wavefront_yx is not None:
            self.array_wavefront_yx = array_wavefront_yx
        status = self.lib.WFS_Flip2DArray(self.instrument_handle,
                                          self.array_wavefront_yx,
                                          self.array_wavefront_xy)
        self.log_wfs.debug(f'Flip 2D Array: {self.instrument_handle.value}')
        self.log_wfs.debug(f'Wavefront YX: {len(self.array_wavefront_yx[0])} x {len(self.array_wavefront_yx)}\n' +
                           '\n'.join([' '.join([f'{item:12.8}' for item in row]) for row in self.array_wavefront_yx]))
        self.log_wfs.debug(f'Wavefront XY: {len(self.array_wavefront_xy[0])} x {len(self.array_wavefront_xy)}\n' +
                           '\n'.join([' '.join([f'{item:12.8}' for item in row]) for row in self.array_wavefront_xy]))
        self._error_message(status)
        return status, self.array_wavefront_xy

    # Calibration Functions
    def _set_spots_to_user_reference(self):
        """Set the measured spot centroid positions to the User Ref.

        This function copies the measured spot centroid positions to
        the User Reference spot positions. Consequently spot
        deviations become zero resulting in a plane wavefront.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        status = self.lib.WFS_SetSpotsToUserReference(self.instrument_handle)
        self.log_wfs.debug(f'Set Spots To User Reference: {self.instrument_handle.value}')
        self._error_message(status)
        return status

    def _set_calc_spots_to_user_reference(self, spot_ref_type=None, array_reference_x=None,
                                          array_reference_y=None):
        """Set the X and Y user ref spots to calculated spot positions.

        This function sets the X and Y user reference spot positions in
        pixels to calculated spot positions given by two
        two-dimensional arrays.

        Args:
            spot_ref_type (Vi.int32(int)): This parameter defines the
                reference type to either relative or or absolute.
                Valid values:
                0   WFS_REF_TYPE_REL
                1   WFS_REF_TYPE_ABS
                Relative reference type means that the given spot
                positions are relative (+/- pixels) to the internal
                factory calibration data whereas absolute reference
                type denotes absolute spot position data
                (0 ... max. camera pixels).
            array_reference_x (((ctypes.float*X)*Y)()): This parameter
                accepts a two-dimensional array of float containing
                user calculated reference X spot positions in pixels.
                The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].
                Note: First array index is the spot number in Y, second
                index the spot number in X direction.
            array_reference_y (((ctypes.float*X)*Y)()): This parameter
                accepts a two-dimensional array of float containing
                user calculated reference Y spot positions in pixels.
                The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].
                Note: First array index is the spot number in Y, second
                index the spot number in X direction.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        if spot_ref_type is not None:
            try:
                self.spot_ref_type = Vi.int32(spot_ref_type)
            except ValueError:
                self.spot_ref_type = spot_ref_type
        if array_reference_x is not None:
            self.array_reference_x = array_reference_x
        if array_reference_y is not None:
            self.array_reference_y = array_reference_y
        columns = self.spots_x.value
        rows = self.spots_y.value
        status = self.lib.WFS_SetCalcSpotsToUserReference(self.instrument_handle,
                                                          self.spot_ref_type,
                                                          self.array_reference_x,
                                                          self.array_reference_y)
        self.log_wfs.debug(f'Set Calc Spots to User Reference: {self.instrument_handle.value}')
        self.log_wfs.info(f'Spot Reference Type: {self.spot_ref_type.value}')
        self.log_wfs.debug('Reference X:\n' + '\n'.join([' '.join(
            [f'{item:12.8}' for item in row[:columns]]) for row in self.array_reference_x[:rows]]))
        self.log_wfs.debug('Reference Y:\n' + '\n'.join([' '.join(
            [f'{item:12.8}' for item in row[:columns]]) for row in self.array_reference_y[:rows]]))
        self._error_message(status)
        return status

    def _create_default_user_reference(self):
        """Create a default User Reference identical to Internal Ref.

        Generates a default User Reference which is identical to the
        Internal Reference. Use function _get_spot_reference_positions
        to get the data arrays.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        status = self.lib.WFS_CreateDefaultUserReference(self.instrument_handle)
        self.log_wfs.debug(f'Create Default User Reference: {self.instrument_handle.value}')
        self._error_message(status)
        return status

    def _save_user_reference_file(self):
        """Save a User Reference spotfield file for the selected MLA.

        This function saves a User Reference spotfield file for the
        actual selected Microlens Array and image resolution to folder
        C:\\Users\\<user>\\Documents\\Thorlabs\\Wavefront Sensor\\Reference
        The file name is automatically set to:
        WFS_<serial_number_wfs>_<mla_name>_<cam_resolution_index>.ref
        or
        WFS10_<serial_number_wfs>_<mla_name>_<cam_resolution_index>.ref
        or
        WFS20_<serial_number_wfs>_<mla_name>_<cam_resolution_index>.ref
        Example: 'WFS_M00224955_MLA150M-5C_0.ref'

        Note: Centroid positions stored as 0.0 are converted to NaN in
        the reference spotfield array because they denote undetected
        spots.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        status = self.lib.WFS_SaveUserRefFile(self.instrument_handle)
        self.log_wfs.debug(f'Save User Reference: {self.instrument_handle.value}')
        self._error_message(status)
        return status

    def _load_user_reference_file(self):
        """Load a User Reference spotfield file for the selected MLA.

        This function loads a User Reference spotfield file for the
        actual selected Microlens Array and image resolution from folder
        C:\\Users\\<user>\\Documents\\Thorlabs\\Wavefront Sensor\\Reference
        The file name is automatically set to:
        WFS_<serial_number_wfs>_<mla_name>_<cam_resolution_index>.ref
        or
        WFS10_<serial_number_wfs>_<mla_name>_<cam_resolution_index>.ref
        or
        WFS20_<serial_number_wfs>_<mla_name>_<cam_resolution_index>.ref
        Example: 'WFS_M00224955_MLA150M-5C_0.ref'

        Note: Centroid positions stored as 0.0 are converted to NaN in
        the reference spotfield array because they denote undetected
        spots.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        status = self.lib.WFS_LoadUserRefFile(self.instrument_handle)
        self.log_wfs.debug(f'Load User Reference: {self.instrument_handle.value}')
        self._error_message(status)
        return status

    def _do_spherical_reference(self):
        """Calculate spot positions based on a pure spherical wavefront.

        This function calculates User Reference spot positions based on
        an already performed measurement of a pure spherical wavefront.
        It supposes an already performed measurement including
        - calculation of Zernike coefficients with function ZernikeLsf
        - already calculated reconstructed deviations using function
        _calc_reconstructed_deviations with option
        do_spherical_reference set to 1.

        Use function _set_reference_plane to activate the performed
        spherical User Reference calibration.

        Returns:
            status (Vi.status(int)): This value shows the status code
                returned by the function call. For Status Codes see
                function _error_message.
        """
        status = self.lib.WFS_DoSphericalRef(self.instrument_handle)
        self.log_wfs.debug(f'Do Spherical Reference: {self.instrument_handle.value}')
        self._error_message(status)
        return status

    def connect(self):
        """Connect to the WFS automatically."""
        self._get_instrument_list_len()
        self._get_instrument_list_info()
        self._init(id_query=1, reset_device=1)
        if self.in_use.value == 1:
            self.log_wfs.error('Instrument is being used!')
            raise ConnectionError
        if self.instrument_handle.value == Vi.NULL:
            self.log_wfs.error('Instrument not found!')
            raise ConnectionError
        self._revision_query()
        self._get_instrument_info()
        self._get_mla_count()
        self._get_mla_data()
        self._get_status()
        return self.device_status.value

    def config(self):
        """Configure default WFS settings."""
        self._select_mla(0)
        self._configure_cam(0)
        self.intensity_limit.value = 10
        self.allow_auto_exposure.value = 1
        self._get_aoi()
        self._get_black_level_offset()
        self._get_exposure_time_range()
        self._get_exposure_time()
        self._get_master_gain_range()
        self._get_master_gain()
        self._get_trigger_delay_range()
        self._set_trigger_delay(self.trigger_delay_min.value)
        self._get_trigger_mode()
        self._set_pupil(0, 0, 5.4, 5.4)
        self._get_pupil()
        self._set_aoi(0, 0, 0, 0)
        self._get_aoi()
        self._set_master_gain(1)
        self._set_black_level_offset(0)
        self._set_reference_plane(0)
        self._get_status()
        return self.device_status.value

    def update(self):
        """Update the WFS and calculate values and RoC."""
        if self.allow_auto_exposure.value == 1:
            self._take_spotfield_image_auto_exposure()
        else:
            self._take_spotfield_image()
        self._get_status()
        self._cut_image_noise_floor()
        self._get_spotfield_image()
        # self._get_spotfield_image_copy()  # Takes a significant amount of time to run
        self._calc_spots_centroid_diameter_intensity()
        self._get_spot_centroids()
        self._calc_beam_centroid_diameter()
        self._calc_spot_to_reference_deviations()
        self._get_spot_deviations()
        self._calc_wavefront()
        self._calc_wavefront_statistics()
        self._get_line_view()
        self._zernike_lsf()
        return self.roc_mm.value

    def disconnect(self):
        """Disconnect from the WFS."""
        return self._close()


if __name__ == '__main__':
    wfs = WFS()
