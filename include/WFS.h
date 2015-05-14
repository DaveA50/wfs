/****************************************************************************

	Thorlabs WFS - WavefrontSensor Instrument Driver

	Copyright:  Copyright(c) 2015, Thorlabs GmbH (www.thorlabs.com)
	Author:     Egbert Krause (ekrause@thorlabs.com)

	Disclaimer: This software is protected by the Thorlabs End-user License Agreement in License.rtf.


	Header file

	Date:          Feb-04-2015
	Software-Nr:   09.76.440
	Version:       4.4.0

	Changelog:     see 'Readme.rtf'

****************************************************************************/

#ifndef __WFS_HEADER
#define __WFS_HEADER

#include <vpptype.h>

#if defined(__cplusplus) || defined(__cplusplus__)
extern "C"
{
#endif

/*---------------------------------------------------------------------------
 Buffers
---------------------------------------------------------------------------*/
#define WFS_BUFFER_SIZE                      (256)   // General buffer size
#define WFS_ERR_DESCR_BUFFER_SIZE            (512)   // Buffer size for error messages


/*---------------------------------------------------------------------------
 Error/Warning Codes
---------------------------------------------------------------------------*/
// max errors from camera driver
#define MAX_CAM_DRIVER_ERRORS                (2000) // camera driver errors in range 1 .. MAX_CAM_DRIVER_ERRORS
#define MAX_WFS_DEVICES                      (5) // max 5 cams at the same time connected
#define MAX_MLA_CALS                         (7) // max. 7 MLA cals per device

// Offsets
#define _WFS_ERROR                           (-2147483647L-1)  /* 0x80000000 */
#define WFS_INSTR_WARNING_OFFSET                          (0x3FFC0900L)
#define WFS_INSTR_ERROR_OFFSET               (_WFS_ERROR + 0x3FFC0900L)  //0xBFFC0900

// WFS Driver Error Codes; error texts defined in WFS_ErrorMessage()
/*#define WFS_SUCCESS                          (0)

#define WFS_ERROR_PARAMETER1                 (_WFS_ERROR+0x3FFC0001L)
#define WFS_ERROR_PARAMETER2                 (_WFS_ERROR+0x3FFC0002L)
#define WFS_ERROR_PARAMETER3                 (_WFS_ERROR+0x3FFC0003L)
#define WFS_ERROR_PARAMETER4                 (_WFS_ERROR+0x3FFC0004L)
#define WFS_ERROR_PARAMETER5                 (_WFS_ERROR+0x3FFC0005L)
#define WFS_ERROR_PARAMETER6                 (_WFS_ERROR+0x3FFC0006L)
#define WFS_ERROR_PARAMETER7                 (_WFS_ERROR+0x3FFC0007L)
#define WFS_ERROR_PARAMETER8                 (_WFS_ERROR+0x3FFC0008L)
#define WFS_ERROR_PARAMETER9                 (_WFS_ERROR+0x3FFC0009L)  */

#define WFS_ERROR_NO_SENSOR_CONNECTED        (WFS_INSTR_ERROR_OFFSET + 0x00)
#define WFS_ERROR_OUT_OF_MEMORY              (WFS_INSTR_ERROR_OFFSET + 0x01)
#define WFS_ERROR_INVALID_HANDLE             (WFS_INSTR_ERROR_OFFSET + 0x02)
#define WFS_ERROR_CAM_NOT_CONFIGURED         (WFS_INSTR_ERROR_OFFSET + 0x13)
#define WFS_ERROR_PIXEL_FORMAT               (WFS_INSTR_ERROR_OFFSET + 0x04)
#define WFS_ERROR_EEPROM_CHECKSUM            (WFS_INSTR_ERROR_OFFSET + 0x05)
#define WFS_ERROR_EEPROM_CAL_DATA            (WFS_INSTR_ERROR_OFFSET + 0x06)
#define WFS_ERROR_OLD_REF_FILE               (WFS_INSTR_ERROR_OFFSET + 0x07)
#define WFS_ERROR_NO_REF_FILE                (WFS_INSTR_ERROR_OFFSET + 0x08)
#define WFS_ERROR_CORRUPT_REF_FILE           (WFS_INSTR_ERROR_OFFSET + 0x09)
#define WFS_ERROR_WRITE_FILE                 (WFS_INSTR_ERROR_OFFSET + 0x0a)
#define WFS_ERROR_INSUFF_SPOTS_FOR_ZERNFIT   (WFS_INSTR_ERROR_OFFSET + 0x0b)
#define WFS_ERROR_TOO_MANY_SPOTS_FOR_ZERNFIT (WFS_INSTR_ERROR_OFFSET + 0x0c)
#define WFS_ERROR_FOURIER_ORDER              (WFS_INSTR_ERROR_OFFSET + 0x0d)
#define WFS_ERROR_NO_RECON_DEVIATIONS        (WFS_INSTR_ERROR_OFFSET + 0x0e)
#define WFS_ERROR_NO_PUPIL_DEFINED           (WFS_INSTR_ERROR_OFFSET + 0x0f)
#define WFS_ERROR_WRONG_PUPIL_DIA            (WFS_INSTR_ERROR_OFFSET + 0x10)
#define WFS_ERROR_WRONG_PUPIL_CTR            (WFS_INSTR_ERROR_OFFSET + 0x11)
#define WFS_ERROR_INVALID_CAL_DATA           (WFS_INSTR_ERROR_OFFSET + 0x12)
#define WFS_ERROR_INTERNAL_REQUIRED          (WFS_INSTR_ERROR_OFFSET + 0x13)
#define WFS_ERROR_ROC_RANGE                  (WFS_INSTR_ERROR_OFFSET + 0x14)
#define WFS_ERROR_NO_USER_REFERENCE          (WFS_INSTR_ERROR_OFFSET + 0x15)
#define WFS_ERROR_AWAITING_TRIGGER           (WFS_INSTR_ERROR_OFFSET + 0x16)
#define WFS_ERROR_NO_HIGHSPEED               (WFS_INSTR_ERROR_OFFSET + 0x17)
#define WFS_ERROR_HIGHSPEED_ACTIVE           (WFS_INSTR_ERROR_OFFSET + 0x18)
#define WFS_ERROR_HIGHSPEED_NOT_ACTIVE       (WFS_INSTR_ERROR_OFFSET + 0x19)
#define WFS_ERROR_HIGHSPEED_WINDOW_MISMATCH  (WFS_INSTR_ERROR_OFFSET + 0x1a)
#define WFS_ERROR_NOT_SUPPORTED              (WFS_INSTR_ERROR_OFFSET + 0x1b)

// returned from non-exported functions
#define WFS_ERROR_SPOT_TRUNCATED             (WFS_INSTR_ERROR_OFFSET + 0x1b)
#define WFS_ERROR_NO_SPOT_DETECTED           (WFS_INSTR_ERROR_OFFSET + 0x1c)
#define WFS_ERROR_TILT_CALCULATION           (WFS_INSTR_ERROR_OFFSET + 0x1d)


// WFS Driver Warning Codes
#define WFS_WARNING                          (WFS_INSTR_WARNING_OFFSET + 0x00)

#define WFS_WARN_NSUP_ID_QUERY     (          0x3FFC0101L)
#define WFS_WARN_NSUP_RESET        (          0x3FFC0102L)
#define WFS_WARN_NSUP_SELF_TEST    (          0x3FFC0103L)
#define WFS_WARN_NSUP_ERROR_QUERY  (          0x3FFC0104L)
#define WFS_WARN_NSUP_REV_QUERY    (          0x3FFC0105L)
/*---------------------------------------------------------------------------
 Driver Status reporting (lower 24 bits)
---------------------------------------------------------------------------*/
#define  WFS_STATBIT_CON               0x00000001 // USB connection lost, set by driver
#define  WFS_STATBIT_PTH               0x00000002 // Power too high (cam saturated)
#define  WFS_STATBIT_PTL               0x00000004 // Power too low (low cam digits)
#define  WFS_STATBIT_HAL               0x00000008 // High ambient light
#define  WFS_STATBIT_SCL               0x00000010 // Spot contrast too low
#define  WFS_STATBIT_ZFL               0x00000020 // Zernike fit failed because of not enough detected spots
#define  WFS_STATBIT_ZFH               0x00000040 // Zernike fit failed because of too much detected spots
#define  WFS_STATBIT_ATR               0x00000080 // Camera is still awaiting a trigger
#define  WFS_STATBIT_CFG               0x00000100 // Camera is configured, ready to use
#define  WFS_STATBIT_PUD               0x00000200 // Pupil is defined
#define  WFS_STATBIT_SPC               0x00000400 // No. of spots or pupil or aoi has been changed
#define  WFS_STATBIT_RDA               0x00000800 // Reconstructed spot deviations available
#define  WFS_STATBIT_URF               0x00001000 // User reference data available
#define  WFS_STATBIT_HSP               0x00002000 // Camera is in Highspeed Mode
#define  WFS_STATBIT_MIS               0x00004000 // Mismatched centroids in Highspeed Mode
#define  WFS_STATBIT_LOS               0x00008000 // low number of detected spots, warning: reduced Zernike accuracy
#define  WFS_STATBIT_FIL               0x00010000 // pupil is badly filled with spots, warning: reduced Zernike accuracy

/*---------------------------------------------------------------------------
 Timeout
---------------------------------------------------------------------------*/
#define WFS_TRIG_TIMEOUT               (100*60*60*24) // * 10 ms = 24 hours, given to function is_SetTimeout
																		 // after that time is_IsVideoFinish returns 'finish' without error
#define WFS_TIMEOUT_CAPTURE_NORMAL     (1.0)  // in sec.
#define WFS_TIMEOUT_CAPTURE_TRIGGER    (0.1)  // in sec., allow fast return of functions WFS_TakeSpotfieldImage...
#define WFS10_TIMEOUT_CAPTURE_NORMAL   (4000) // in msec., allow 500 ms exposure time + reserve
#define WFS10_TIMEOUT_CAPTURE_TRIGGER  (100)  // in msec., allow fast return of functions WFS_TakeSpotfieldImage...
#define WFS20_TIMEOUT_CAPTURE_NORMAL   (4000) // in msec., allow 84 ms exposure time + reserve
#define WFS20_TIMEOUT_CAPTURE_TRIGGER  (100)  // in msec., allow fast return of functions WFS_TakeSpotfieldImage...

/*---------------------------------------------------------------------------
 Exported constants
---------------------------------------------------------------------------*/
#define  WFS_TRUE                      (1)
#define  WFS_FALSE                     (0)

//Defines for WFS camera
#define  MAX_FRAMERATE                 (15) // not higher for wider exposure range

#define  EXPOSURE_MANUAL               (0)
#define  EXPOSURE_AUTO                 (1)

#define  MASTER_GAIN_MIN_WFS           (1.0) // real gain factor, not 0..100% percent
#define  MASTER_GAIN_MIN_WFS10         (1.5) // 1.0 prevents ADC from saturation on overexposure
#define  MASTER_GAIN_MIN_WFS20         (1.0)
#define  MASTER_GAIN_MAX_WFS20         (1.0)
#define  MASTER_GAIN_MAX               (13.66)
#define  MASTER_GAIN_MAX_DISPLAY       (5.0)   // dark signal is too noisy for higher amplification
#define  MASTER_GAIN_EXPONENT          (38.26) // based on natural logarithm

#define  NOISE_LEVEL_MIN               (0)     // level for cutting spotfield
#define  NOISE_LEVEL_MAX               (255)

#define  BLACK_LEVEL_MIN               (0)
#define  BLACK_LEVEL_MAX               (255)
#define  BLACK_LEVEL_WFS_DEF           (100)  // lower values causes problems with autoexposure and trigger (WFS)
#define  BLACK_LEVEL_WFS10_DEF         (100)  // for cam shifted to 0 .. +15
#define  BLACK_LEVEL_WFS20_DEF         (0)

// Pixel format defines
#define  PIXEL_FORMAT_MONO8            (0)
#define  PIXEL_FORMAT_MONO16           (1)

// pre-defined image sizes for WFS instruments
#define  CAM_RES_1280                  (0) // 1280x1024
#define  CAM_RES_1024                  (1) // 1024x1024
#define  CAM_RES_768                   (2) // 768x768
#define  CAM_RES_512                   (3) // 512x512
#define  CAM_RES_320                   (4) // 320x320 smallest!
#define  CAM_RES_MAX_IDX               (4)

// pre-defined image sizes for WFS10 instruments
#define  CAM_RES_WFS10_640            (0) // 640x480
#define  CAM_RES_WFS10_480            (1) // 480x480
#define  CAM_RES_WFS10_360            (2) // 360x360
#define  CAM_RES_WFS10_260            (3) // 260x260
#define  CAM_RES_WFS10_180            (4) // 180x180 smallest!
#define  CAM_RES_WFS10_MAX_IDX        (4)

// pre-defined image sizes for WFS20 instruments
#define  CAM_RES_WFS20_1440           (0) // 1440x1080
#define  CAM_RES_WFS20_1080           (1) // 1080x1080
#define  CAM_RES_WFS20_768            (2) // 768x768
#define  CAM_RES_WFS20_512            (3) // 512x512
#define  CAM_RES_WFS20_360            (4) // 360x360 smallest!
#define  CAM_RES_WFS20_720_BIN2       (5) // 720x540, binning 2x2
#define  CAM_RES_WFS20_540_BIN2       (6) // 540x540, binning 2x2
#define  CAM_RES_WFS20_384_BIN2       (7) // 384x384, binning 2x2
#define  CAM_RES_WFS20_256_BIN2       (8) // 256x256, binning 2x2
#define  CAM_RES_WFS20_180_BIN2       (9) // 180x180, binning 2x2
#define  CAM_RES_WFS20_MAX_IDX        (9)


// Hardware trigger modes
#define  WFS_HW_TRIGGER_OFF            (0)
#define  WFS_HW_TRIGGER_HL             (1)
#define  WFS_HW_TRIGGER_LH             (2)
#define  WFS_TRIGGER_MODE_MIN          WFS_HW_TRIGGER_OFF
#define  WFS_TRIGGER_MODE_MAX          WFS_HW_TRIGGER_LH

	// Averaging
#define  AVERAGE_COUNT_MAX             (256)

// Pupil
#define  PUPIL_DIA_MIN_MM              (0.1)  // for coarse check only
#define  PUPIL_DIA_MAX_MM              (10.0)
#define  PUPIL_CTR_MIN_MM              (-5.0)
#define  PUPIL_CTR_MAX_MM              (5.0)

// Wavefront types
#define  WAVEFRONT_MEAS                (0)
#define  WAVEFRONT_REC                 (1)
#define  WAVEFRONT_DIFF                (2)

// Max number of detectable spots
#define  MAX_SPOTS_X                   (50) // WFS20: 1440*5/150 = 48
#define  MAX_SPOTS_Y                   (40) // WFS20: 1080*5/150 = 36
/*
#define  MAX_SPOTS_X                   (41) // max. for 1280x1024 with 4.65µm pixels and 150µm lenslet pitch (WFSx)
														  // also for 640x480 with 9.9µm pixels and 150µm lenslet pitch (WFS10x)
#define  MAX_SPOTS_Y                   (33) // determines also 3D display size
*/
// Reference
#define  WFS_REF_INTERNAL              (0)
#define  WFS_REF_USER                  (1)

// Spots ref types
#define  WFS_REF_TYPE_REL              (0)
#define  WFS_REF_TYPE_ABS              (1)

// Spherical reference
#define  ROC_CAL_MIN_MM                (100.0)
#define  ROC_CAL_MAX_MM                (5000.0)

// Zernike polynoms
#define  MIN_NUMDOTS_FIT               (5)
#define  MAX_NUMDOTS_FIT               (MAX_SPOTS_X * MAX_SPOTS_Y)      // max. number of spots used for Zernike fit
#define  MAX_NUM_ROWS_B                (2 * MAX_NUMDOTS_FIT + 1) // max. number of rows in Matrix B containing x and y deviations and a piston

#define  ZERNIKE_ORDERS_AUTO           (0)
#define  MIN_ZERNIKE_ORDERS            (2)
#define  MAX_ZERNIKE_ORDERS            (10)
#define  MIN_ZERNIKE_MODES             (6)  // min. number of modes in Zernike fit
#define  MAX_ZERNIKE_MODES             (66) // max. number of modes in Zernike fit
#define  ZERNIKE_WARNING_LEVEL         (1.3) // 30% more spots than desired Zernike modes should be detected for good accuracy


// for conversion pixel - mm
#define  NOT_CENTERED                  (0)
#define  CENTERED                      (1)


/*===========================================================================
 Structures
===========================================================================*/


/*===========================================================================
 Constants
===========================================================================*/
/*  Zernike constantes for information only
const static mode_t mode[] =
{
// number, order frequency name
	{  0,    0,    0,    "",                       }, // dummy to fill index 0
	{  1,    0,    0,    "Piston",                 },
	{  2,    1,   -1,    "Tip y",                  },
	{  3,    1,    1,    "Tilt x",                 },
	{  4,    2,   -2,    "Astigmatism +-45°",      },
	{  5,    2,    0,    "Defocus",                },
	{  6,    2,    2,    "Astigmatism 0/90°",      },
	{  7,    3,   -3,    "Trefoil y",              }, // corrected y
	{  8,    3,   -1,    "Coma x",                 },
	{  9,    3,    1,    "Coma y",                 },
	{ 10,    3,    3,    "Trefoil x",              }, // corrected x
	{ 11,    4,   -4,    "Tetrafoil y",            },
	{ 12,    4,   -2,    "Sec. Astigmatism y",     },
	{ 13,    4,    0,    "Spherical Aberration 3", },
	{ 14,    4,    2,    "Sec. Astigmatism x",     },
	{ 15,    4,    4,    "Tetrafoil x",            },
	{ 16,    5,   -5,    "Pentafoil y",            },
	{ 17,    5,   -3,    "Sec. Trefoil y",         },
	{ 18,    5,   -1,    "Sec. Coma y",            },
	{ 19,    5,    1,    "Sec. Coma x",            },
	{ 20,    5,    3,    "Sec. Trefoil x",         },
	{ 21,    5,    5,    "Pentafoil x",            },
	{ 22,    6,   -6,    "",                       },
	{ 23,    6,   -4,    "Sec.Tetrafoil y",        },
	{ 24,    6,   -2,    "Tert. Astigmatism y",    },
	{ 25,    6,    0,    "Spherical Aberration 4", },
	{ 26,    6,    2,    "Tert. Astigmatism x",    },
	{ 27,    6,    4,    "Sec.Tetrafoil x",        },
	{ 28,    6,    6,    "",                       },
	{ 29,    7,   -7,    "",                       },
	{ 30,    7,   -5,    "",                       },
	{ 31,    7,   -3,    "Tert. Trefoil y",        },
	{ 32,    7,   -1,    "Tert. Coma y",           },
	{ 33,    7,    1,    "Tert. Coma x",           },
	{ 34,    7,    3,    "Tert. Trefoil x",        },
	{ 35,    7,    5,    "",                       },
	{ 36,    7,    7,    "",                       },
	{ 37,    8,   -8,    "",                       },
	{ 38,    8,   -6,    "",                       },
	{ 39,    8,   -4,    "",                       },
	{ 40,    8,   -2,    "",                       },
	{ 41,    8,    0,    "Spherical Aberration 5", },
	{ 42,    8,    2,    "",                       },
	{ 43,    8,    4,    "",                       },
	{ 44,    8,    6,    "",                       },
	{ 45,    8,    8,    "",                       },
	{ 46,    9,   -9,    "",                       },
	{ 47,    9,   -7,    "",                       },
	{ 48,    9,   -5,    "",                       },
	{ 49,    9,   -3,    "",                       },
	{ 50,    9,   -1,    "",                       },
	{ 51,    9,    1,    "",                       },
	{ 52,    9,    3,    "",                       },
	{ 53,    9,    5,    "",                       },
	{ 54,    9,    7,    "",                       },
	{ 55,    9,    9,    "",                       },
	{ 56,   10,  -10,    "",                       },
	{ 57,   10,   -8,    "",                       },
	{ 58,   10,   -6,    "",                       },
	{ 59,   10,   -4,    "",                       },
	{ 60,   10,   -2,    "",                       },
	{ 61,   10,    0,    "Spherical Aberration 6", },
	{ 62,   10,    2,    "",                       },
	{ 63,   10,    4,    "",                       },
	{ 64,   10,    6,    "",                       },
	{ 65,   10,    8,    "",                       },
	{ 66,   10,   10,    "",                       },
};
*/

/*---------------------------------------------------------------------------
 GLOBAL USER-CALLABLE FUNCTION DECLARATIONS (Exportable Functions)
---------------------------------------------------------------------------*/

/*------------------------------------------------------------------------*//**
\brief	Initialize a communication session to a Thorlabs wavefront sensor
			that is very cool.
\details	Does something useful
\param[in] resourceName			InputParameter
\param[in] IDQuery				InputParameter
\param[in] resetDevice			InputParameter
\param[out] instrumentHandle	OutputParameter
\return			Error code. See \ref ERR_x.
*//*-------------------------------------------------------------------------*/
ViStatus _VI_FUNC WFS_init (ViRsrc resourceName, ViBoolean IDQuery,
									 ViBoolean resetDevice, ViSession *instrumentHandle);

ViStatus _VI_FUNC WFS_GetInstrumentInfo (ViSession instrumentHandle,
													  ViChar manufacturerName[],
													  ViChar instrumentNameWFS[],
													  ViChar serialNumberWFS[],
													  ViChar serialNumberCam[]);

ViStatus _VI_FUNC WFS_ConfigureCam (ViSession instrumentHandle,
												ViInt32 pixelFormat, ViInt32 camResolIndex,
												ViInt32 *spotsX, ViInt32 *spotsY);

ViStatus _VI_FUNC WFS_SetHighspeedMode (ViSession instrumentHandle,
													 ViInt32 highspeedMode,
													 ViInt32 adaptCentroids,
													 ViInt32 substractOffset,
													 ViInt32 allowAutoExposure);

ViStatus _VI_FUNC WFS_GetHighspeedWindows (ViSession instrumentHandle,
														 ViInt32 *windowCountX,
														 ViInt32 *windowCountY,
														 ViInt32 *windowSizeX,
														 ViInt32 *windowSizeY,
														 ViInt32 windowStartposX[],
														 ViInt32 windowStartposY[]);

ViStatus _VI_FUNC WFS_CheckHighspeedCentroids (ViSession instrumentHandle);

ViStatus _VI_FUNC WFS_GetExposureTimeRange (ViSession instrumentHandle,
														  ViReal64 *exposureTimeMin,
														  ViReal64 *exposureTimeMax,
														  ViReal64 *exposureTimeIncr);

ViStatus _VI_FUNC WFS_SetExposureTime (ViSession instrumentHandle,
													ViReal64 exposureTimeSet,
													ViReal64 *exposureTimeAct);

ViStatus _VI_FUNC WFS_GetExposureTime (ViSession instrumentHandle,
													ViReal64 *exposureTimeAct);

ViStatus _VI_FUNC WFS_GetMasterGainRange (ViSession instrumentHandle,
														ViReal64 *masterGainMin,
														ViReal64 *masterGainMax);

ViStatus _VI_FUNC WFS_SetMasterGain (ViSession instrumentHandle,
												 ViReal64 masterGainSet,
												 ViReal64 *masterGainAct);

ViStatus _VI_FUNC WFS_GetMasterGain (ViSession instrumentHandle,
												 ViReal64 *masterGainAct);

ViStatus _VI_FUNC WFS_SetBlackLevelOffset (ViSession instrumentHandle,
														 ViInt32 blackLevelOffsetSet);

ViStatus _VI_FUNC WFS_GetBlackLevelOffset (ViSession instrumentHandle,
														 ViInt32 *blackLevelOffsetAct);

ViStatus _VI_FUNC WFS_SetTriggerMode (ViSession instrumentHandle,
												  ViInt32 triggerMode);

ViStatus _VI_FUNC WFS_GetTriggerMode (ViSession instrumentHandle,
												  ViInt32 *triggerMode);

ViStatus _VI_FUNC WFS_GetTriggerDelayRange (ViSession instrumentHandle,
														  ViInt32 *triggerDelayMin,
														  ViInt32 *triggerDelayMax,
														  ViInt32 *triggerDelayIncr);

ViStatus _VI_FUNC WFS_SetTriggerDelay (ViSession instrumentHandle,
													ViInt32 triggerDelaySet,
													ViInt32 *triggerDelayAct);

ViStatus _VI_FUNC WFS_GetMlaCount (ViSession instrumentHandle, ViInt32 *MLACount);

ViStatus _VI_FUNC WFS_GetMlaData (ViSession instrumentHandle, ViInt32 MLAIndex,
											 ViChar MLAName[], ViReal64 *camPitchm,
											 ViReal64 *lensletPitchm, ViReal64 *spotOffsetX,
											 ViReal64 *spotOffsetY, ViReal64 *lensletFm,
											 ViReal64 *grdCorr0, ViReal64 *grdCorr45);

ViStatus _VI_FUNC WFS_GetMlaData2 (ViSession instrumentHandle, ViInt32 MLAIndex,
											  ViChar MLAName[], ViReal64 *camPitchm,
											  ViReal64 *lensletPitchm,
											  ViReal64 *spotOffsetX, ViReal64 *spotOffsetY,
											  ViReal64 *lensletFm, ViReal64 *grdCorr0,
											  ViReal64 *grdCorr45, ViReal64 *grdCorrRot,
											  ViReal64 *grdCorrPitch);

ViStatus _VI_FUNC WFS_SelectMla (ViSession instrumentHandle, ViInt32 MLAIndex);

ViStatus _VI_FUNC WFS_SetAoi (ViSession instrumentHandle,
										ViReal64 aoiCenterXMm,
										ViReal64 aoiCenterYMm,
										ViReal64 aoiSizeXMm,
										ViReal64 aoiSizeYMm);

ViStatus _VI_FUNC WFS_GetAoi (ViSession instrumentHandle,
										ViReal64 *aoiCenterXMm,
										ViReal64 *aoiCenterYMm,
										ViReal64 *aoiSizeXMm,
										ViReal64 *aoiSizeYMm);

ViStatus _VI_FUNC WFS_SetPupil (ViSession instrumentHandle,
										  ViReal64 pupilCenterXMm,
										  ViReal64 pupilCenterYMm,
										  ViReal64 pupilDiameterXMm,
										  ViReal64 pupilDiameterYMm);

ViStatus _VI_FUNC WFS_GetPupil (ViSession instrumentHandle,
										  ViReal64 *pupilCenterXMm,
										  ViReal64 *pupilCenterYMm,
										  ViReal64 *pupilDiameterXMm,
										  ViReal64 *pupilDiameterYMm);

ViStatus _VI_FUNC WFS_SetReferencePlane (ViSession instrumentHandle,
													  ViInt32 referenceIndex);

ViStatus _VI_FUNC WFS_GetReferencePlane (ViSession instrumentHandle,
													  ViInt32 *referenceIndex);

ViStatus _VI_FUNC WFS_GetStatus (ViSession instrumentHandle,
											ViInt32 *deviceStatus);

ViStatus _VI_FUNC WFS_TakeSpotfieldImage (ViSession instrumentHandle);

ViStatus _VI_FUNC WFS_TakeSpotfieldImageAutoExpos (ViSession instrumentHandle,
																	ViReal64 *exposureTimeAct,
																	ViReal64 *masterGainAct);

ViStatus _VI_FUNC WFS_GetSpotfieldImage (ViSession instrumentHandle,
													  ViAUInt8 *imageBuf, ViInt32 *rows,
													  ViInt32 *columns);

ViStatus _VI_FUNC WFS_GetSpotfieldImageCopy (ViSession instrumentHandle,
															ViUInt8 imageBuf[], ViInt32 *rows,
															ViInt32 *columns);

ViStatus _VI_FUNC WFS_AverageImage (ViSession instrumentHandle,
												ViInt32 averageCount,
												ViInt32 *averagedDataReady);

ViStatus _VI_FUNC WFS_AverageImageRolling (ViSession instrumentHandle,
														 ViInt32 averageCount, ViInt32 reset);

ViStatus _VI_FUNC WFS_CutImageNoiseFloor (ViSession instrumentHandle,
														ViInt32 limit);

ViStatus _VI_FUNC WFS_CalcImageMinMax (ViSession instrumentHandle,
													ViInt32 *imageMin, ViInt32 *imageMax,
													ViReal64 *saturatedPixelsPercent);

ViStatus _VI_FUNC WFS_CalcMeanRmsNoise (ViSession instrumentHandle,
													 ViReal64 *mean, ViReal64 *rms);

ViStatus _VI_FUNC WFS_GetLine (ViSession instrumentHandle, ViInt32 line,
										 float lineSelected[]);

ViStatus _VI_FUNC WFS_GetLineView (ViSession instrumentHandle, float lineMin[],
											  float lineMax[]);

ViStatus _VI_FUNC WFS_CalcBeamCentroidDia (ViSession instrumentHandle,
														 ViReal64 *beamCentroidXMm,
														 ViReal64 *beamCentroidYMm,
														 ViReal64 *beamDiameterXMm,
														 ViReal64 *beamDiameterYMm);

ViStatus _VI_FUNC WFS_CalcSpotsCentrDiaIntens (ViSession instrumentHandle,
															  ViInt32 dynamicNoiseCut,
															  ViInt32 calculateDiameters);

ViStatus _VI_FUNC WFS_GetSpotCentroids (ViSession instrumentHandle,
													 float arrayCentroidX[],
													 float arrayCentroidY[]);

ViStatus _VI_FUNC WFS_GetSpotDiameters (ViSession instrumentHandle,
													 float arrayDiameterX[],
													 float arrayDiameterY[]);

ViStatus _VI_FUNC WFS_GetSpotDiaStatistics (ViSession instrumentHandle,
														  ViReal64 *min, ViReal64 *max,
														  ViReal64 *mean);

ViStatus _VI_FUNC WFS_GetSpotIntensities (ViSession instrumentHandle,
														float arrayIntensity[]);

ViStatus _VI_FUNC WFS_CalcSpotToReferenceDeviations (ViSession instrumentHandle,
																	  ViInt32 cancelWavefrontTilt);

ViStatus _VI_FUNC WFS_GetSpotReferencePositions (ViSession instrumentHandle,
																 float arrayRefPosX[],
																 float arrayRefPosY[]);

ViStatus _VI_FUNC WFS_GetSpotDeviations (ViSession instrumentHandle,
													  float arrayDeviationsX[],
													  float arrayDeviationsY[]);

ViStatus _VI_FUNC WFS_ZernikeLsf (ViSession instrumentHandle,
											 ViInt32 *zernikeOrders, float arrayZernikeUm[],
											 float arrayZernikeOrdersUm[], ViReal64 *roCMm);

ViStatus _VI_FUNC WFS_CalcFourierOptometric (ViSession instrumentHandle,
															ViInt32 zernikeOrders,
															ViInt32 fourierOrder,
															ViReal64 *fourierM,
															ViReal64 *fourierJ0,
															ViReal64 *fourierJ45,
															ViReal64 *optoSphere,
															ViReal64 *optoCylinder,
															ViReal64 *optoAxisDeg);

ViStatus _VI_FUNC WFS_CalcReconstrDeviations (ViSession instrumentHandle,
															 ViInt32 zernikeOrders,
															 ViInt32 arrayZernikeReconstruct[],
															 ViInt32 doSphericalReference,
															 ViReal64 *fitErrMean,
															 ViReal64 *fitErrStdev);

ViStatus _VI_FUNC WFS_CalcWavefront (ViSession instrumentHandle,
												 ViInt32 wavefrontType, ViInt32 limitToPupil,
												 float arrayWavefront[]);

ViStatus _VI_FUNC WFS_CalcWavefrontStatistics (ViSession instrumentHandle,
															  ViReal64 *min, ViReal64 *max,
															  ViReal64 *diff, ViReal64 *mean,
															  ViReal64 *RMS,
															  ViReal64 *weightedRMS);

ViStatus _VI_FUNC WFS_self_test (ViSession instrumentHandle,
											ViInt16 *selfTestResult,
											ViChar selfTestMessage[]);

ViStatus _VI_FUNC WFS_reset (ViSession instrumentHandle);

ViStatus _VI_FUNC WFS_revision_query (ViSession instrumentHandle,
												  ViChar instrumentDriverRevision[],
												  ViChar firmwareRevision[]);

ViStatus _VI_FUNC WFS_error_query (ViSession instrumentHandle,
											  ViInt32 *errorCode, ViChar errorMessage[]);

ViStatus _VI_FUNC WFS_error_message (ViSession instrumentHandle,
												 ViStatus errorCode, ViChar errorMessage[]);

ViStatus _VI_FUNC WFS_GetInstrumentListLen (ViSession instrumentHandle,
														  ViInt32 *instrumentCount);

ViStatus _VI_FUNC WFS_GetInstrumentListInfo (ViSession handle,
															ViInt32 instrument_index,
															ViInt32 *device_id,
															ViInt32 *in_use,
															ViChar instrument_name[],
															ViChar serial_number_wfs[],
															ViChar resourceName[]);

ViStatus _VI_FUNC WFS_GetXYScale (ViSession instrumentHandle,
											 float arrayScaleX[], float arrayScaleY[]);

ViStatus _VI_FUNC WFS_ConvertWavefrontWaves (ViSession instrumentHandle, double wavelength,
															float arrayWavefrontIn[MAX_SPOTS_Y][MAX_SPOTS_X],
															float arrayWavefrontOut[MAX_SPOTS_Y][MAX_SPOTS_X]);

ViStatus _VI_FUNC WFS_close (ViSession instrumentHandle);

ViStatus _VI_FUNC WFS_Flip2DArray (ViSession handle, float arrayYX[MAX_SPOTS_Y][MAX_SPOTS_X], float arrayXY[MAX_SPOTS_X][MAX_SPOTS_Y]);


// Calibration functions for customers
ViStatus _VI_FUNC WFS_SetSpotsToUserReference (ViSession handle);
ViStatus _VI_FUNC WFS_SetCalcSpotsToUserReference (ViSession handle, ViInt32 spot_ref_type, float ArrayRefPosX[MAX_SPOTS_Y][MAX_SPOTS_X], float ArrayRefPosY[MAX_SPOTS_Y][MAX_SPOTS_X]);
ViStatus _VI_FUNC WFS_CreateDefaultUserReference (ViSession handle);
ViStatus _VI_FUNC WFS_SaveUserRefFile (ViSession handle);
ViStatus _VI_FUNC WFS_LoadUserRefFile (ViSession handle);
ViStatus _VI_FUNC WFS_DoSphericalRef (ViSession handle);

#if defined(__cplusplus) || defined(__cplusplus__)
}
#endif

#endif // __WFS_HEADER

/****************************************************************************
  End of Header file
****************************************************************************/


