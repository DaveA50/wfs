/*===============================================================================================================================

	Thorlabs Wavefront Sensor sample application

	This sample program for WFS Wavefront Sensor instruments connects to a selected instrument,
	configures it, takes some measurment and displays the results.
	Finally it closes the connection.

	Source file 'sample.c'

	Date:          Sep-08-2014
	Software-Nr:   N/A
	Version:       1.3
	Copyright:     Copyright(c) 2014, Thorlabs GmbH (www.thorlabs.com)
	Author:        Egbert Krause (ekrause@thorlabs.com)

	Changelog:     Dec-04-2009 -> V1.0
						Nov-30-2010 -> V1.1 extended to WFS10 series instruments, highspeed mode enabled
						Dec-19-2013 -> V1.2 added loop with data output to file
						Sep-08-2014 -> V1.3 added WFS20 support
						
	Disclaimer:

	This program is free software; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; either version 2 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program; if not, write to the Free Software
	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

===============================================================================================================================*/


/*===============================================================================================================================
  Include Files

  Note: You may need to set your compilers include search path to the VXIPNP include directory.
		  This is typically 'C:\Program Files (x86)\IVI Foundation\VISA\WinNT\WFS'.

===============================================================================================================================*/

#include "wfs.h" // Wavefront Sensor driver's header file
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <utility.h>
#include <userint.h>


/*===============================================================================================================================
  Defines
===============================================================================================================================*/

#define  DEVICE_OFFSET_WFS10           (0x00100) // device IDs of WFS10 instruments start at 256 decimal
#define  DEVICE_OFFSET_WFS20           (0x00200) // device IDs of WFS20 instruments start at 512 decimal

// settings for this sample program, you may adapt settings to your preferences
#define  OPTION_OFF                    (0)
#define  OPTION_ON                     (1)

#define  SAMPLE_PIXEL_FORMAT           PIXEL_FORMAT_MONO8   // only 8 bit format is supported
#define  SAMPLE_CAMERA_RESOL_WFS       CAM_RES_768          // 768x768 pixels, see wfs.h for alternative cam resolutions
#define  SAMPLE_CAMERA_RESOL_WFS10     CAM_RES_WFS10_360    // 360x360 pixels
#define  SAMPLE_CAMERA_RESOL_WFS20     CAM_RES_WFS20_512    // 512x512 pixels
#define  SAMPLE_REF_PLANE              WFS_REF_INTERNAL

#define  SAMPLE_PUPIL_CENTROID_X       (0.0) // in mm
#define  SAMPLE_PUPIL_CENTROID_Y       (0.0)
#define  SAMPLE_PUPIL_DIAMETER_X       (2.0) // in mm, needs to fit to selected camera resolution
#define  SAMPLE_PUPIL_DIAMETER_Y       (2.0)

#define  SAMPLE_IMAGE_READINGS         (10) // trials to read a exposed spotfield image

#define  SAMPLE_OPTION_DYN_NOISE_CUT   OPTION_ON   // use dynamic noise cut features  
#define  SAMPLE_OPTION_CALC_SPOT_DIAS  OPTION_OFF  // don't calculate spot diameters
#define  SAMPLE_OPTION_CANCEL_TILT     OPTION_ON   // cancel average wavefront tip and tilt
#define  SAMPLE_OPTION_LIMIT_TO_PUPIL  OPTION_OFF  // don't limit wavefront calculation to pupil interior

#define  SAMPLE_OPTION_HIGHSPEED       OPTION_ON   // use highspeed mode (only for WFS10 and WFS20 instruments)
#define  SAMPLE_OPTION_HS_ADAPT_CENTR  OPTION_ON   // adapt centroids in highspeed mode to previously measured centroids
#define  SAMPLE_HS_NOISE_LEVEL         (30)        // cut lower 30 digits in highspeed mode
#define  SAMPLE_HS_ALLOW_AUTOEXPOS     (1)         // allow autoexposure in highspeed mode (runs somewhat slower)

#define  SAMPLE_WAVEFRONT_TYPE         WAVEFRONT_MEAS // calculate measured wavefront

#define  SAMPLE_ZERNIKE_ORDERS         (3)  // calculate up to 3rd Zernike order

#define  SAMPLE_PRINTOUT_SPOTS         (5)  // printout results for first 5 x 5 spots only

#define  SAMPLE_OUTPUT_FILE_NAME       "WFS_sample_output.txt"


/*===============================================================================================================================
  Data type definitions
===============================================================================================================================*/
typedef struct
{
	int               selected_id;
	int               handle;
	int               status;
	
	char              version_wfs_driver[WFS_BUFFER_SIZE];
	char              version_cam_driver[WFS_BUFFER_SIZE];
	char              manufacturer_name[WFS_BUFFER_SIZE];
	char              instrument_name[WFS_BUFFER_SIZE];
	char              serial_number_wfs[WFS_BUFFER_SIZE];
	char              serial_number_cam[WFS_BUFFER_SIZE];
	
	int               mla_cnt;
	int               selected_mla;
	int               selected_mla_idx;
	char              mla_name[WFS_BUFFER_SIZE];
	double            cam_pitch_um;
	double            lenslet_pitch_um;
	double            center_spot_offset_x;
	double            center_spot_offset_y;
	double            lenslet_f_um;
	double            grd_corr_0;
	double            grd_corr_45;
	
	int               spots_x;
	int               spots_y;

}  instr_t;


/*===============================================================================================================================
  Function Prototypes
===============================================================================================================================*/
void handle_errors (int);
int select_instrument (int *selection, ViChar resourceName[]);
int select_mla (int *selection);


/*===============================================================================================================================
  Global Variables
===============================================================================================================================*/
const int   cam_wfs_xpixel[] = { 1280, 1024, 768, 512, 320 };
const int   cam_wfs_ypixel[] = { 1024, 1024, 768, 512, 320 };
const int   cam_wfs10_xpixel[] = {  640,  480, 360, 260, 180 };
const int   cam_wfs10_ypixel[] = {  480,  480, 360, 260, 180 };
const int   cam_wfs20_xpixel[] = {  1440, 1080, 768, 512, 360,  720, 540, 384, 256, 180 };
const int   cam_wfs20_ypixel[] = {  1080, 1080, 768, 512, 360,  540, 540, 384, 256, 180 };

const int   zernike_modes[] = { 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66 }; // converts Zernike order to Zernike modes

instr_t     instr = { 0 };    // all instrument related data are stored in this structure

int         hs_win_count_x,hs_win_count_y,hs_win_size_x,hs_win_size_y; // highspeed windows data
int         hs_win_start_x[MAX_SPOTS_X],hs_win_start_y[MAX_SPOTS_Y];


/*===============================================================================================================================
  Code
===============================================================================================================================*/
void main (void)
{
	int               err;
	int               i,j,cnt;
	int               rows, cols;   // image height and width, depending on camera resolution
	int               selection;
	unsigned char     *ImageBuffer; // pointer to the camera image buffer
	
	double            expos_act, master_gain_act;
	double            beam_centroid_x, beam_centroid_y;
	double            beam_diameter_x, beam_diameter_y;
	
	float             centroid_x[MAX_SPOTS_Y][MAX_SPOTS_X];
	float             centroid_y[MAX_SPOTS_Y][MAX_SPOTS_X];

	float             deviation_x[MAX_SPOTS_Y][MAX_SPOTS_X];
	float             deviation_y[MAX_SPOTS_Y][MAX_SPOTS_X];

	float             wavefront[MAX_SPOTS_Y][MAX_SPOTS_X];
	
	float             zernike_um[MAX_ZERNIKE_MODES+1];             // index runs from 1 - MAX_ZERNIKE_MODES
	float             zernike_orders_rms_um[MAX_ZERNIKE_ORDERS+1]; // index runs from 1 - MAX_ZERNIKE_MODES
	double            roc_mm;
	
	int               zernike_order;
	
	double            wavefront_min, wavefront_max, wavefront_diff, wavefront_mean, wavefront_rms, wavefront_weighted_rms;
	ViChar            resourceName[256];
	FILE              *fp;
	int               key;


	printf("This is a Thorlabs Wavefront Sensor sample application.\n\n");
	
	// Get the driver revision
	if(err = WFS_revision_query (NULL, instr.version_wfs_driver, instr.version_cam_driver)) // pass NULL because handle is not yet initialized
		handle_errors(err);
	
	//printf("Camera USB driver version     : %s\n", instr.version_cam_driver);
	printf("WFS instrument driver version : %s\n\n", instr.version_wfs_driver);
	
	
	// Show all and select one WFS instrument
	if(select_instrument(&instr.selected_id, resourceName) == 0)
	{
		printf("\nNo instrument selected. Press <ENTER> to exit.\n");
		fflush(stdin);
		getchar();
		return; // program ends here if no instrument selected
	}
	
	// Get the resource name for this instrument
	//if(err = WFS_GetInstrumentListInfo (VI_NULL, instr.selected_id, VI_NULL, VI_NULL, VI_NULL, VI_NULL, resourceName))
	// handle_errors(err);
	
	
	// print out the resource name
	printf("\nResource name of selected WFS: %s\n", resourceName);
	
	
	// Open the Wavefront Sensor instrument
	//if(err = WFS_init (instr.selected_id, &instr.handle))
	if(err = WFS_init (resourceName, VI_FALSE, VI_FALSE, &instr.handle)) 
		handle_errors(err);

	// Get instrument information
	if(err = WFS_GetInstrumentInfo (instr.handle, instr.manufacturer_name, instr.instrument_name, instr.serial_number_wfs, instr.serial_number_cam))
		handle_errors(err);
	
	printf("\n");
	printf("Opened Instrument:\n");
	printf("Manufacturer           : %s\n", instr.manufacturer_name);
	printf("Instrument Name        : %s\n", instr.instrument_name);
	printf("Serial Number WFS      : %s\n", instr.serial_number_wfs);
	
	
	// Select a microlens array (MLA)
	if(select_mla(&instr.selected_mla) < 0)
	{
		printf("\nNo MLA selected. Press <ENTER> to exit.\n");
		fflush(stdin);
		getchar();
		return;
	}
	
	// Activate desired MLA
	if(err = WFS_SelectMla (instr.handle, instr.selected_mla))
		handle_errors(err);

	
	
	// Configure WFS camera, use a pre-defined camera resolution
	if((instr.selected_id & DEVICE_OFFSET_WFS10) == 0 && (instr.selected_id & DEVICE_OFFSET_WFS20) == 0) // WFS150/300 instrument
	{   
		printf("\n\nConfigure WFS camera with resolution index %d (%d x %d pixels).\n", SAMPLE_CAMERA_RESOL_WFS, cam_wfs_xpixel[SAMPLE_CAMERA_RESOL_WFS], cam_wfs_ypixel[SAMPLE_CAMERA_RESOL_WFS]);
		
		if(err = WFS_ConfigureCam (instr.handle, SAMPLE_PIXEL_FORMAT, SAMPLE_CAMERA_RESOL_WFS, &instr.spots_x, &instr.spots_y))
			handle_errors(err);
	}
	
	if(instr.selected_id & DEVICE_OFFSET_WFS10) // WFS10 instrument
	{
		printf("\n\nConfigure WFS10 camera with resolution index %d (%d x %d pixels).\n", SAMPLE_CAMERA_RESOL_WFS10, cam_wfs10_xpixel[SAMPLE_CAMERA_RESOL_WFS10], cam_wfs10_ypixel[SAMPLE_CAMERA_RESOL_WFS10]);
	
		if(err = WFS_ConfigureCam (instr.handle, SAMPLE_PIXEL_FORMAT, SAMPLE_CAMERA_RESOL_WFS10, &instr.spots_x, &instr.spots_y))
			handle_errors(err);
	}
	
	if(instr.selected_id & DEVICE_OFFSET_WFS20) // WFS20 instrument
	{
		printf("\n\nConfigure WFS20 camera with resolution index %d (%d x %d pixels).\n", SAMPLE_CAMERA_RESOL_WFS20, cam_wfs20_xpixel[SAMPLE_CAMERA_RESOL_WFS20], cam_wfs20_ypixel[SAMPLE_CAMERA_RESOL_WFS20]);
	
		if(err = WFS_ConfigureCam (instr.handle, SAMPLE_PIXEL_FORMAT, SAMPLE_CAMERA_RESOL_WFS20, &instr.spots_x, &instr.spots_y))
			handle_errors(err);
	}
	

	printf("Camera is configured to detect %d x %d lenslet spots.\n\n", instr.spots_x, instr.spots_y);
	
	
	// set camera exposure time and gain if you don't want to use auto exposure
	// use functions WFS_GetExposureTimeRange, WFS_SetExposureTime, WFS_GetMasterGainRange, WFS_SetMasterGain
	
	// set WFS internal reference plane
	printf("\nSet WFS to internal reference plane.\n");
	if(err = WFS_SetReferencePlane (instr.handle, SAMPLE_REF_PLANE))
		handle_errors(err);
	
	
	// define pupil
	printf("\nDefine pupil to:\n");
	printf("Centroid_x = %6.3f\n", SAMPLE_PUPIL_CENTROID_X);
	printf("Centroid_y = %6.3f\n", SAMPLE_PUPIL_CENTROID_Y);
	printf("Diameter_x = %6.3f\n", SAMPLE_PUPIL_DIAMETER_X);
	printf("Diameter_y = %6.3f\n", SAMPLE_PUPIL_DIAMETER_Y);

	if(err = WFS_SetPupil (instr.handle, SAMPLE_PUPIL_CENTROID_X, SAMPLE_PUPIL_CENTROID_Y, SAMPLE_PUPIL_DIAMETER_X, SAMPLE_PUPIL_DIAMETER_Y))
		handle_errors(err);
	
	printf("\nRead camera images:\n");
	
	printf("Image No.     Status     ->   newExposure[ms]   newGainFactor\n");
	
	// do some trials to read a well exposed image
	for(cnt = 0; cnt < SAMPLE_IMAGE_READINGS; cnt++)
	{
		// take a camera image with auto exposure, note that there may several function calls required to get an optimal exposed image
		if(err = WFS_TakeSpotfieldImageAutoExpos (instr.handle, &expos_act, &master_gain_act))
			handle_errors(err);
	
		printf("    %d     ", cnt);
	
		// check instrument status for non-optimal image exposure
		if(err = WFS_GetStatus (instr.handle, &instr.status))
			handle_errors(err);   
	
		if(instr.status & WFS_STATBIT_PTH) printf("Power too high!    ");
		 else
		if(instr.status & WFS_STATBIT_PTL) printf("Power too low!     ");
		 else
		if(instr.status & WFS_STATBIT_HAL) printf("High ambient light!");
		 else
			printf(                                "OK                 ");
		
		printf("     %6.3f          %6.3f\n", expos_act, master_gain_act);
		
		if( !(instr.status & WFS_STATBIT_PTH) && !(instr.status & WFS_STATBIT_PTL) && !(instr.status & WFS_STATBIT_HAL) )
			break; // image well exposed and is usable
	}
	

	// close program if no well exposed image is feasible
	if( (instr.status & WFS_STATBIT_PTH) || (instr.status & WFS_STATBIT_PTL) ||(instr.status & WFS_STATBIT_HAL) )
	{
		printf("\nSample program will be closed because of unusable image quality, press <ENTER>.");
		WFS_close(instr.handle); // required to release allocated driver data
		fflush(stdin);
		getchar();
		exit(1);
	}
	
	
	// get last image (only required to display the image)
	if(err = WFS_GetSpotfieldImage (instr.handle, &ImageBuffer, &rows, &cols))
		handle_errors(err);

	
	// calculate all spot centroid positions using dynamic noise cut option
	if(err = WFS_CalcSpotsCentrDiaIntens (instr.handle, SAMPLE_OPTION_DYN_NOISE_CUT, SAMPLE_OPTION_CALC_SPOT_DIAS))
		handle_errors(err);

	// get centroid result arrays
	if(err = WFS_GetSpotCentroids (instr.handle, *centroid_x, *centroid_y))
		handle_errors(err);
	
	
	// print out some centroid positions
	printf("\nCentroid X Positions in pixels (first 5x5 elements)\n");
	for(i=0;i<SAMPLE_PRINTOUT_SPOTS;i++)
	{   
		for(j=0;j<SAMPLE_PRINTOUT_SPOTS;j++)
			printf(" %8.3f", centroid_x[i][j]);
		printf("\n");  
	}      

	printf("\nCentroid Y Positions in pixels (first 5x5 elements)\n");
	for(i=0;i<SAMPLE_PRINTOUT_SPOTS;i++)
	{   
		for(j=0;j<SAMPLE_PRINTOUT_SPOTS;j++)
			printf(" %8.3f", centroid_y[i][j]);
		printf("\n");  
	}      

	printf("\nPress <ENTER> to proceed...");
	getchar();
	

	// get centroid and diameter of the optical beam, you may use this beam data to define a pupil variable in position and size
	// for WFS20: this is based on centroid intensties calculated by WFS_CalcSpotsCentrDiaIntens()
	if(err = WFS_CalcBeamCentroidDia (instr.handle, &beam_centroid_x, &beam_centroid_y, &beam_diameter_x, &beam_diameter_y))
		handle_errors(err);
	
	printf("\nInput beam is measured to:\n");
	printf("Centroid_x = %6.3f mm\n", beam_centroid_x);
	printf("Centroid_y = %6.3f mm\n", beam_centroid_y);
	printf("Diameter_x = %6.3f mm\n", beam_diameter_x);
	printf("Diameter_y = %6.3f mm\n", beam_diameter_y);

	fflush(stdin);
	printf("\nPress <ENTER> to proceed...");
	getchar();

	

	// calculate spot deviations to internal reference
	if(err = WFS_CalcSpotToReferenceDeviations (instr.handle, SAMPLE_OPTION_CANCEL_TILT))
		handle_errors(err);
	
	// get spot deviations
	if(WFS_GetSpotDeviations (instr.handle, *deviation_x, *deviation_y))
		handle_errors(err);
	
	// print out some spot deviations
	printf("\nSpot Deviation X in pixels (first 5x5 elements)\n");
	for(i=0;i<SAMPLE_PRINTOUT_SPOTS;i++)
	{   
		for(j=0;j<SAMPLE_PRINTOUT_SPOTS;j++)
			printf(" %8.3f", deviation_x[i][j]);
		printf("\n");  
	}      

	printf("\nSpot Deviation Y in pixels (first 5x5 elements)\n");
	for(i=0;i<SAMPLE_PRINTOUT_SPOTS;i++)
	{   
		for(j=0;j<SAMPLE_PRINTOUT_SPOTS;j++)
			printf(" %8.3f", deviation_y[i][j]);
		printf("\n");  
	}      

	printf("\nPress <ENTER> to proceed...");
	getchar();
	
	
	
	// calculate and printout measured wavefront
	if(err = WFS_CalcWavefront (instr.handle, SAMPLE_WAVEFRONT_TYPE, SAMPLE_OPTION_LIMIT_TO_PUPIL, *wavefront))
		handle_errors(err);
	
	// print out some wavefront points
	printf("\nWavefront in microns (first 5x5 elements)\n");
	for(i=0;i<SAMPLE_PRINTOUT_SPOTS;i++)
	{   
		for(j=0;j<SAMPLE_PRINTOUT_SPOTS;j++)
			printf(" %8.3f", wavefront[i][j]);
		printf("\n");  
	}      
	
	printf("\nPress <ENTER> to proceed...");
	getchar();
	
	
	// calculate wavefront statistics within defined pupil
	if(err = WFS_CalcWavefrontStatistics (instr.handle, &wavefront_min, &wavefront_max, &wavefront_diff, &wavefront_mean, &wavefront_rms, &wavefront_weighted_rms))
		handle_errors(err);
	
	printf("\nWavefront Statistics in microns:\n");
	printf("Min          : %8.3f\n", wavefront_min);
	printf("Max          : %8.3f\n", wavefront_max);
	printf("Diff         : %8.3f\n", wavefront_diff);
	printf("Mean         : %8.3f\n", wavefront_mean);
	printf("RMS          : %8.3f\n", wavefront_rms);
	printf("Weigthed RMS : %8.3f\n", wavefront_weighted_rms);
	
	printf("\nPress <ENTER> to proceed...");
	getchar();

	
	// calculate Zernike coefficients
	printf("\nZernike fit up to order %d:\n",SAMPLE_ZERNIKE_ORDERS);
	zernike_order = SAMPLE_ZERNIKE_ORDERS; // pass 0 to function for auto Zernike order, choosen order is returned
	if(err = WFS_ZernikeLsf (instr.handle, &zernike_order, zernike_um, zernike_orders_rms_um, &roc_mm)) // calculates also deviation from centroid data for wavefront integration
		handle_errors(err);
		
	printf("\nZernike Mode    Coefficient\n");
	for(i=0; i < zernike_modes[SAMPLE_ZERNIKE_ORDERS]; i++)
	{
		printf("  %2d         %9.3f\n",i, zernike_um[i]);
	}

	
	
	printf("\nEnter measurement loop with output to file 0/1?");
	fflush(stdin);
	selection = getchar() - '0';

	if(selection == 1)
	{
		printf("\nMeasurement data is continuously written into file %s.\n", SAMPLE_OUTPUT_FILE_NAME);
		
		printf("\nPress <ESC> to exit loop...\n");
	  
		do
		{   
			// take a camera image with auto exposure
			if(err = WFS_TakeSpotfieldImageAutoExpos (instr.handle, &expos_act, &master_gain_act))
				handle_errors(err);
	
			// calculate all spot centroid positions using dynamic noise cut option
			if(err = WFS_CalcSpotsCentrDiaIntens (instr.handle, SAMPLE_OPTION_DYN_NOISE_CUT, SAMPLE_OPTION_CALC_SPOT_DIAS))
				handle_errors(err);

			// calculate spot deviations to internal reference
			if(err = WFS_CalcSpotToReferenceDeviations (instr.handle, SAMPLE_OPTION_CANCEL_TILT))
				handle_errors(err);
	

			// calculate measured wavefront
			if(err = WFS_CalcWavefront (instr.handle, SAMPLE_WAVEFRONT_TYPE, SAMPLE_OPTION_LIMIT_TO_PUPIL, *wavefront))
				handle_errors(err);
	
			// calculate wavefront statistics within defined pupil
			if(err = WFS_CalcWavefrontStatistics (instr.handle, &wavefront_min, &wavefront_max, &wavefront_diff, &wavefront_mean, &wavefront_rms, &wavefront_weighted_rms))
				handle_errors(err);
	
			// calculate Zernike coefficients
			zernike_order = SAMPLE_ZERNIKE_ORDERS; // pass 0 to function for auto Zernike order, choosen order is returned
			if(err = WFS_ZernikeLsf (instr.handle, &zernike_order, zernike_um, zernike_orders_rms_um, &roc_mm)) // calculates also deviation from centroid data for wavefront integration
				handle_errors(err);
		
	
			// copy some values into a text file, overwrite old file content
			if((fp = fopen (SAMPLE_OUTPUT_FILE_NAME, "w")) != NULL)
			{   
				fprintf(fp, "Wavefront results in um:\n");
				fprintf(fp, "%s %8.3f\n", "PV   ", wavefront_diff);
				fprintf(fp, "%s %8.3f\n", "RMS  ", wavefront_rms);
		
				fprintf(fp, "\nZernike amplitudes in um:\n");
				for(i=0;i < zernike_modes[SAMPLE_ZERNIKE_ORDERS]; i++)
					fprintf(fp, "%2d    %8.3f\n", i, zernike_um[i]);

				fclose(fp);
			}
		
			// exit loop?
			key = 0;
			if(KeyHit())
				key = GetKey();

		} while(key != VAL_ESC_VKEY);

	}
	
	
	
	// enter highspeed mode for WFS10 and WFS20 instruments only
	if((instr.selected_id & DEVICE_OFFSET_WFS10) || (instr.selected_id & DEVICE_OFFSET_WFS20)) // WFS10 or WFS20 instrument
	{
		printf("\nEnter Highspeed Mode 0/1?");
		fflush(stdin);
		selection = getchar() - '0';
	
		if(selection == 1)
		{   
			if(err = WFS_SetHighspeedMode (instr.handle, SAMPLE_OPTION_HIGHSPEED, SAMPLE_OPTION_HS_ADAPT_CENTR, SAMPLE_HS_NOISE_LEVEL, SAMPLE_HS_ALLOW_AUTOEXPOS))
				handle_errors(err);
						  
			if(err = WFS_GetHighspeedWindows (instr.handle, &hs_win_count_x, &hs_win_count_y, &hs_win_size_x, &hs_win_size_y, hs_win_start_x, hs_win_start_y))handle_errors(err);
	
			printf("\nCentroid detection windows are defined as follows:\n"); // refere to WFS_GetHighspeedWindows function help
			printf("Count_x = %3d, Count_y = %3d\n", hs_win_count_x, hs_win_count_y);
			printf("Size_x  = %3d, Size_y  = %3d\n", hs_win_size_x, hs_win_size_y);
			printf("Start coordinates x: ");
			for(i=0;i<hs_win_count_x;i++)
				printf("%3d ", hs_win_start_x[i]);
			printf("\n");
			printf("Start coordinates y: ");
			for(i=0;i<hs_win_count_y;i++)
				printf("%3d ", hs_win_start_y[i]);
			printf("\n");
			
			
			fflush(stdin);
			printf("\nPress <ENTER> to proceed...");
			getchar();
			
		
		   // take a camera image with auto exposure, this is also supported in highspeed-mode
		   if(err = WFS_TakeSpotfieldImageAutoExpos (instr.handle, &expos_act, &master_gain_act))
			   handle_errors(err);

		   printf("\nexposure = %6.3f ms, gain =  %6.3f\n", expos_act, master_gain_act);
			

			// get centroid and diameter of the optical beam, these data are based on the detected centroids
			if(err = WFS_CalcBeamCentroidDia (instr.handle, &beam_centroid_x, &beam_centroid_y, &beam_diameter_x, &beam_diameter_y))
				handle_errors(err);
	
			printf("\nInput beam is measured to:\n");
			printf("Centroid_x = %6.3f mm\n", beam_centroid_x);
			printf("Centroid_y = %6.3f mm\n", beam_centroid_y);
			printf("Diameter_x = %6.3f mm\n", beam_diameter_x);
			printf("Diameter_y = %6.3f mm\n", beam_diameter_y);

			fflush(stdin);
			printf("\nPress <ENTER> to proceed...");
			getchar();
			
			// Info: calling WFS_CalcSpotsCentrDiaIntens() is not required because the WFS10/WFS20 camera itself already did the calculation
			
			// get centroid result arrays
			if(err = WFS_GetSpotCentroids (instr.handle, *centroid_x, *centroid_y))
				handle_errors(err);
			
			// print out some centroid positions
			printf("\nCentroid X Positions in pixels (first 5x5 elements)\n");
			for(i=0;i<SAMPLE_PRINTOUT_SPOTS;i++)
			{   
				for(j=0;j<SAMPLE_PRINTOUT_SPOTS;j++)
					printf(" %8.3f", centroid_x[i][j]);
				printf("\n");  
			}      

			printf("\nCentroid Y Positions in pixels (first 5x5 elements)\n");
			for(i=0;i<SAMPLE_PRINTOUT_SPOTS;i++)
			{   
				for(j=0;j<SAMPLE_PRINTOUT_SPOTS;j++)
					printf(" %8.3f", centroid_y[i][j]);
				printf("\n");  
			}      

			
			printf("\nThe following wavefront and Zernike calculations can be done identical to normal mode.\n");
		}
	}


	printf("\nEnd of Sample Program, press <ENTER> to exit.");
	fflush(stdin);
	getchar();

	// Close instrument, important to release allocated driver data!
	WFS_close(instr.handle);
}



/*===============================================================================================================================
  Handle Errors
  This function retrieves the appropriate text to the given error number and closes the connection in case of an error
===============================================================================================================================*/
void handle_errors (int err)
{
	char buf[WFS_ERR_DESCR_BUFFER_SIZE];

	if(!err) return;

	// Get error string
	WFS_error_message (instr.handle, err, buf);

	if(err < 0) // errors
	{
		printf("\nWavefront Sensor Error: %s\n", buf);

		// close instrument after an error has occured
		printf("\nSample program will be closed because of the occured error, press <ENTER>.");
		WFS_close(instr.handle); // required to release allocated driver data
		fflush(stdin);
		getchar();
		exit(1);
	}
}



/*===============================================================================================================================
	Select Instrument
===============================================================================================================================*/
int select_instrument (int *selection, ViChar resourceName[])
{
	int            i,err,instr_cnt;
	ViInt32        device_id;
	int            in_use;
	char           instr_name[WFS_BUFFER_SIZE];
	char           serNr[WFS_BUFFER_SIZE];
	char           strg[WFS_BUFFER_SIZE];

	// Find available instruments
	if(err = WFS_GetInstrumentListLen (VI_NULL, &instr_cnt))
		handle_errors(err);
		
	if(instr_cnt == 0)
	{
		printf("No Wavefront Sensor instrument found!\n");
		return 0;
	}

	// List available instruments
	printf("Available Wavefront Sensor instruments:\n\n");
	
	for(i=0;i<instr_cnt;i++)
	{
		if(err = WFS_GetInstrumentListInfo (VI_NULL, i, &device_id, &in_use, instr_name, serNr, resourceName))
			handle_errors(err);
		
		printf("%3d   %s    %s    %s\n", device_id, instr_name, serNr, (!in_use) ? "" : "(inUse)");
	}

	// Select instrument
	printf("\nSelect a Wavefront Sensor instrument: ");
	fflush(stdin);
	
	fgets (strg, WFS_BUFFER_SIZE, stdin);
	*selection = atoi(strg);

	// get selected resource name
	for(i=0;i<instr_cnt;i++)
	{   
		if(err = WFS_GetInstrumentListInfo (VI_NULL, i, &device_id, &in_use, instr_name, serNr, resourceName))
		   handle_errors(err);
		
		if(device_id == *selection)
			break; // resourceName fits to device_id
	}
	
	return *selection;
}


/*===============================================================================================================================
	Select MLA
===============================================================================================================================*/
int select_mla (int *selection)
{
	int            i,err,mla_cnt;

	// Read out number of available Microlens Arrays 
	if(err = WFS_GetMlaCount (instr.handle, &instr.mla_cnt))
		handle_errors(err);

	// List available Microlens Arrays
	printf("\nAvailable Microlens Arrays:\n\n");
	for(i=0;i<instr.mla_cnt;i++)
	{   
		if(WFS_GetMlaData (instr.handle, i, instr.mla_name, &instr.cam_pitch_um, &instr.lenslet_pitch_um, &instr.center_spot_offset_x, &instr.center_spot_offset_y, &instr.lenslet_f_um, &instr.grd_corr_0, &instr.grd_corr_45))
			handle_errors(err);   
	
		printf("%2d  %s   CamPitch=%6.3f LensletPitch=%8.3f\n", i, instr.mla_name, instr.cam_pitch_um, instr.lenslet_pitch_um);
	}
	
	// Select MLA
	printf("\nSelect a Microlens Array: ");
	fflush(stdin);
	*selection = getchar() - '0';
	if(*selection < -1)
		*selection = -1; // nothing selected

	return *selection;
}


/*===============================================================================================================================
	End of source file
===============================================================================================================================*/
