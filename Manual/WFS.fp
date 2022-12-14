s??        ??   M c?  3   ?   ????                               WFS                             Wavefront Sensor                            _WFS_FUNC                                                    
   	ViReal32[]     	? 	??ViAReal32     ? ??ViAUInt8     ? ??float[MAX_SPOTS_X][MAX_SPOTS_Y]     ? ??float[MAX_SPOTS_Y][MAX_SPOTS_X]     ? ??ViUInt8     	?  ViUInt8[]  ? ? ??ViInt16     	?  ViInt16[]  ? ? ??ViUInt16     
?  	ViUInt16[]  ?  ? ??ViInt32     	?  ViInt32[]     ? ??ViUInt32  ? ? ??ViReal64     
?  	ViReal64[]     ? ??ViRsrc     	? 	??ViBoolean     ? ??ViChar     ?  ViChar[]     ? ??ViString     ? 	 
ViBoolean[]  ? 	? 	??ViSession  ?  ? ??ViStatus     ? ??ViConstString   p    This instrument driver module provides programming support for the Thorlabs WFS Wavefront Sensor instruments.
     p    This class of functions configures the instrument by setting acquisition and system configuration parameters.
     o    This class of functions allow the user to perform actions and determine the current state of the instrument.
     [    This class of functions transfer data from the instrument and perform data calculations.
     i    This class of functions provides utility and lower level functions to communicate with the instrument.
     m    This class of functions handle calibration data of the instrument. These functions are allowed to the user.    E    This function initializes the instrument driver session and performs the following initialization actions:

(1) Opens a session to the Default Resource Manager resource and a session to the selected device using the Resource Name.
(2) Performs an identification query on the Instrument.
(3) Resets the instrument to a known state.
(4) Sends initialization commands to the instrument.
(5) Returns an instrument handle which is used to differentiate between different sessions of this instrument driver.

Notes:
(1) Each time this function is invoked an unique session is opened.          This parameter specifies the interface of the device that is to be initialized.The resource name has to follow the syntax:

"USB::0x1313::0x0000::" followed by the Device ID.

The Device ID can be get with the function "WFS_GetInstrumentListInfo". E.g. "USB::0x1313::0x0000::1"

     _    Performs an In-System Verification.
Checks if the resource matches the vendor and product id.     R    Performs Reset operation and places the instrument in a pre-defined reset state.     ?    This parameter returns an instrument handle that is used in all subsequent calls to distinguish between different sessions of this instrument driver.    ?    Operational return status. Contains either a completion code or an error code. Instrument driver specific codes that may be returned in addition to the VISA error codes defined in VPP-4.3 and vendor specific codes, are as follows.

Completition Codes
----------------------------------------------------------------
VI_SUCCESS              Initialization successful
VI_WARN_NSUP_ID_QUERY   Identification query not supported
VI_WARN_NSUP_RESET      Reset not supported


Error Codes
----------------------------------------------------------------
VI_ERROR_FAIL_ID_QUERY  Instrument identification query failed


Vendor Specific Codes
----------------------------------------------------------------
For error codes and descriptions see <Error Message>.    ? %   ? ^    Resource Name                     	 %? ?       ID Query                          	? %? ?       Reset Device                      	? i  ?  ?    Instrument Handle                 
y????  ?    Status                          ????/ ??                                         ????  ??                                         ???? ??                                               Yes VI_TRUE No VI_FALSE   Yes VI_TRUE No VI_FALSE    	           	           Copyright? 2018 Thorlabs GmbH    FWavefront Sensor Instrument Driver for WFS/WFS10/20/30/40 instruments    Thorlabs - WFS    ?    This function returns the following information about the opened instrument:
- Driver Manufacturer Name
- Instrument Name
- Instrument Serial Number
- Camera Serial Number
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
     ?    This parameter returns the Instrument Name of the WFS.

Note: The string must contain at least WFS_BUFFER_SIZE (256) elements (char[WFS_BUFFER_SIZE]).      ?    This parameter returns the Serial Number of the WFS.

Note: The string must contain at least WFS_BUFFER_SIZE (256) elements (char[WFS_BUFFER_SIZE]).     ?    This parameter returns the Serial Number of the camera body the WFS is based on.

Note: The string must contain at least WFS_BUFFER_SIZE (256) elements (char[WFS_BUFFER_SIZE]).     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     ?    This parameter returns the Manufacturer Name of this instrument driver.

Note: The string must contain at least WFS_BUFFER_SIZE (256) elements (char[WFS_BUFFER_SIZE]).     ?????  d    Status                             2 ? ?  d    Instrument Name WFS               ? 2" ?  d    Serial Number WFS                 V 2? ?  d    Serial Number Cam                    ?  d    Instrument Handle                 ? 2  ?  d    Manufacturer Name                  	           	            	            	                	               This function configures the WFS instrument's camera resolution and returns the max. number of detectable spots in X and Y direction.

The result depends on the selected microlens array in function WFS_SelectMla().

Note: This function is not available in Highspeed Mode!     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     ?    This parameter selects the bit width per pixel of the returned camera image. Thorlabs WFS instruments currently support only 8 bit format.    ?    This parameter selects the camera resolution in pixels. Only the following pre-defined settings are supported:

For WFS instruments:
 Index  Resolution
   0    1280x1024         
   1    1024x1024         
   2     768x768           
   3     512x512           
   4     320x320

For WFS10 instruments:
 Index  Resolution
   0     640x480         
   1     480x480         
   2     360x360           
   3     260x260           
   4     180x180

For WFS20 instruments:
 Index  Resolution
   0    1440x1080            
   1    1080x1080            
   2     768x768              
   3     512x512              
   4     360x360              
   5     720x540, bin2 
   6     540x540, bin2 
   7     384x384, bin2 
   8     256x256, bin2 
   9     180x180, bin2 

For WFS30 instruments:
 Index  Resolution
   0    1936x1216            
   1    1216x1216            
   2    1024x1024              
   3     768x768              
   4     512x512              
   5     360x360
   6     968x608, sub2 
   7     608x608, sub2 
   8     512x512, sub2 
   9     384x384, sub2 
  10     256x256, sub2 
  11     180x180, sub2 

For WFS40 instruments:
 Index  Resolution
   0    2048x2048            
   1    1536x1536
   2    1024x1024              
   3     768x768              
   4     512x512              
   5     360x360
   6    1024x1024, sub2 
   7     768x768, sub2 
   8     512x512, sub2 
   9     384x384, sub2 
  10     256x256, sub2 
  11     180x180, sub2 
     ?    This parameter retuns the number of spots which can be detected in X direction, based on the selected camera resolution and Microlens Array in function SetMlaIdx.     ?    This parameter retuns the number of spots which can be detected in Y direction, based on the selected camera resolution and Microlens Array in function SetMlaIdx.    ?????  d    Status                            V   ?  d    Instrument Handle                 ? 0 ? ?       Pixel Format                      p -? ?       Cam Resol. Index                  6 ?  ?  d    Spots X                           ? ? ? ?  d    Spots Y                         ???? 
 y??                                            	                         16 bit 1 8 bit 0              ?1280x1024     640x480       1440x1080         1936x1216          2048x2048 0 1024x1024     480x480       1080x1080         1216x1216          1536x1536 1 768x768         360x360       768x768             1024x1024          1024x1024 2 512x512         260x260       512x512             768x768              768x768     3 320x320         180x180       360x360             512x512              512x512     4 bin2 720x540         360x360              360x360     5 bin2 540x540    sub2 968x608  sub2 1024x1024 6 bin2 384x384    sub2 608x608      sub2 768x768 7 bin2 256x256    sub2 512x512      sub2 512x512 8 bin2 180x180    sub2 384x384      sub2 384x384 9 sub2 256x256      sub2 256x256 10 sub2 180x180      sub2 180x180 11    	            	            JWFS150/300     WFS10          WFS20              WFS30              WFS40   ?    This function activates/deactivates the camera's Highspeed Mode for WFS10/WFS20 instruments.

When activated, the camera calculates the spot centroid positions internally and sends the result to the WFS driver instead of sending raw spotfield images.

Note:
There is no camera image available when Highspeed Mode is activated!
Highspeed Mode is not available for WFS150/WFS300/WFS30/WFS40 instruments!     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     Q    This parameter determines if the camera's Highspeed Mode is switched on or off.    I    This parameter defines an offset level for Highspeed Mode only. All camera pixels will be subtracted by this level before the centroids are being calculated, which increases accuracy.

Valid range: 0 ... 255

Note: The offset is only valid in Highspeed Mode and must not set too high to clear the spots within the camera image!        When Highspeed Mode is selected, this parameter determines if the centroid positions measured in Normal Mode should be used to adapt the spot search windows for Highspeed Mode.
Otherwise, a rigid grid based on reference spot positions is used in Highspeed Mode.    =    When Highspeed Mode is selected, this parameter determines if the camera should also calculate the image saturation in order enable the auto exposure feature using function WFS_TakeSpotfieldImageAutoExpos() instead of WFS_TakeSpotfieldImage().
This option leads to a somewhat reduced measurement speed when enabled.    &????  d    Status                            &?   ?  d    Instrument Handle                 ' 0 I ?       Highspeed Mode                    'i 2 ?  d    Substract Offset                  (? 0 ? ?       Adapt Centroids                   )? 0? ?       Allow Auto Exposure                	                         On 1 Off 0                  On 1 Off 0              On 1 Off 0    ?    This function returns data of the spot detection windows valid in Highspeed Mode. Window size and positions depend on options passed to function WFS_SetHighspeedMode().

Note: This function is only available when Highspeed Mode is activated!     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     C    This parameter returns the number of spot windows in X direction.     C    This parameter returns the number of spot windows in Y direction.     K    This parameter returns the size in pixels of spot windows in X direction.     K    This parameter returns the size in pixels of spot windows in Y direction.     ?    This parameter returns a one-dimensional array containing the start positions in pixels for spot windows in X direction.

The required array size is MAX_SPOTS_X.

Note: Window Stoppos X = Windows Startpos X + Windows Size X     ?    This parameter returns a one-dimensional array containing the start positions in pixels for spot windows in Y direction.

The required array size is MAX_SPOTS_Y.

Note: Window Stoppos Y = Windows Startpos Y + Windows Size Y    -?????  d    Status                            .    ?  d    Instrument Handle                 .? 2  ?  d    Window Count X                    .? 2 ? ?  d    Window Count Y                    /< 2" ?  d    Window Size X                     /? 2? ?  d    Window Size Y                     /? x  ?  d    Window Startpos X                 0? x ? ?  d    Window Startpos Y                  	               	            	            	            	            	            	               This function checks if the actual measured spot centroid positions are within the calculation windows in Highspeed Mode.

Possible error: WFS_ERROR_HIGHSPEED_WINDOW_MISMATCH

If this error occures, measured centroids are not reliable for wavefront interrogation because the appropriated spots are truncated.

Note: This function is only available when Highspeed Mode is activated!     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
    5;????  d    Status                            5?   ?  d    Instrument Handle                  	               ?    This function returns the available exposure range of the WFS camera in ms. The range may depend on the camera resolution set by function ConfigureCam.
     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     K    This parameter returns the minimal exposure time of the WFS camera in ms.     K    This parameter returns the maximal exposure time of the WFS camera in ms.     T    This parameter returns the smallest possible increment of the exposure time in ms.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    7T   ?  d    Instrument Handle                 7? 2  ?  d    Exposure Time Min                 8- 2 ? ?  d    Exposure Time Max                 8? 2" ?  d    Exposure Time Incr                8?????  d    Status                                 	           	           	           	           b    This function sets the target exposure time for the WFS camera and returns the actual set value.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     J    This parameter returns the actual exposure time of the WFS camera in ms.     I    This parameter sets the target exposure time for the WFS camera in ms.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    :?   ?  d    Instrument Handle                 ;? 2 ? ?  d    Exposure Time Act                 ;? 2  ?  d    Exposure Time Set                 <#????  d    Status                                 	               	           I    This function returns the actual exposure time of the WFS camera in ms.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     J    This parameter returns the actual exposure time of the WFS camera in ms.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    =?   ?  d    Instrument Handle                 >e 2  ?  d    Exposure Time Act                 >?????  d    Status                                 	           	              This function returns the available linear master gain range of the WFS camera.

Note: Master gain increases image noise! Use higher exposure time to set the WFS camera more sensitive.
Lowest master gain of WFS10 camera is 1.5.
Master gain of WFS20 camera is fixed to 1.0.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     P    This parameter returns the minimal linear master gain value of the WFS camera.     P    This parameter returns the maximal linear master gain value of the WFS camera.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    A   ?  d    Instrument Handle                 A? 2  ?  d    Master Gain Min                   A? 2 ? ?  d    Master Gain Max                   B9????  d    Status                                 	           	           	           ?    This function sets the target linear master gain for the WFS camera and returns the actual set master gain.

Note: MasterGain of WFS20 is fixed to 1
     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     I    This parameter returns the actual linear master gain of the WFS camera.     p    This parameter sets the target linear master gain for the WFS camera.

Note: MasterGain of WFS20 is fixed to 1     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    DK   ?  d    Instrument Handle                 D? 2 ? ?  d    Master Gain Act                   E" 2  ?  d    Master Gain Set                   E?????  d    Status                                 	               	           :    This function returns the actual set linear master gain.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     I    This parameter returns the actual linear master gain of the WFS camera.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    GG   ?  d    Instrument Handle                 G? 2  ?  d    Master Gain Act                   H????  d    Status                                 	           	           ?    This function sets the black offset level of the WFS camera. A higher black level will increase the intensity level of a dark camera image.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     ?    This parameter sets the black offset value of the WFS camera. A higher black level will increase the intensity level of a dark camera image.

Valid range: 0 ... 255
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    I?   ?  d    Instrument Handle                 Jk 2  ?  d    Black Level Offset Set            K????  d    Status                                     	           A    This function returns the black offset level of the WFS camera.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     C    This parameter returns the black offset value of the WFS camera.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    L?   ?  d    Instrument Handle                 M 2  ?  d    Black Level Offset Act            M^????  d    Status                                 	            	          ?    This function sets the hardware/software trigger mode.
When the hardware trigger capability is activated, functions TakeSpotfieldImage() and TakeSpotfieldImageAutoExpos() will wait for a trigger event for a short period of time (WFS_TIMEOUT_CAPTURE_TRIGGER = 0.1 sec.) prior to start exposure and will return with error WFS_ERROR_AWAITING_TRIGGER if no trigger event occured.

Use function SetTriggerDelay() to define an extra trigger delay time.
     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
    ?    This parameter defines and activates the trigger mode.

Valid settings:
   WFS_HW_TRIGGER_OFF  No HW Trigger, continuous measurement
                       with highest speed
   WFS_HW_TRIGGER_HL   Trigger on high->low edge
   WFS_HW_TRIGGER_LH   Trigger on low->high edge
   WFS_SW_TRIGGER      Software trigger


Note: When WFS_SW_TRIGGER is used, a new measurement is started                      whenever WFS_TakeSpotfieldImage() or                      WFS_TakeSpotfieldImageAutoExpos() is called,
Compared to WFS_HW_TRIGGER_OFF lower measurememnt speed is achieved.

Note: For WFS150/WFS300, WFS30 and WFS40 modes WFS_HW_TRIGGER_OFF and WFS_SW_TRIGGER are identical.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    PY   ?  d    Instrument Handle                 P? 2  ?  d    Trigger Mode                      S?????  d    Status                                     	           C    This function returns the actual hardware/software trigger mode.
     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
    ?    This parameter returns the actual trigger mode.

Valid trigger modes:
   WFS_HW_TRIGGER_OFF  No HW Trigger, continuous measurement
                       with highest speed
   WFS_HW_TRIGGER_HL   Trigger on high->low edge
   WFS_HW_TRIGGER_LH   Trigger on low->high edge
   WFS_SW_TRIGGER      Software trigger


Note: When WFS_SW_TRIGGER is used, a new measurement is started                      whenever WFS_TakeSpotfieldImage() or                      WFS_TakeSpotfieldImageAutoExpos() is called,
Compared to WFS_HW_TRIGGER_OFF lower measurememnt speed is achieved.

Note: For WFS150/WFS300, WFS30 and WFS40 modes WFS_HW_TRIGGER_OFF and WFS_SW_TRIGGER are identical.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    T?   ?  d    Instrument Handle                 U? 2  ?  d    Trigger Mode                      X,????  d    Status                                 	            	           o    This function sets an additional trigger delay for a hardware trigger mode set by function SetTriggerMode().
     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     ~    This parameter accepts the target trigger delay in ?s. Use function GetTriggerDelayRange() to read out the accepted limits.
     `    This parameter returns the actual trigger delay in ?s which may differ from the target value.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    Y?   ?  d    Instrument Handle                 Z[ 2  ?  d    Trigger Delay Set                 Z? 2 ? ?  d    Trigger Delay Act                 [I????  d    Status                                     	            	           g    This function returns the allowed range for the trigger delay setting in function SetTriggerDelay().
     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     D    This parameter returns the minimum adjustable trigger delay in ?s.     E    This parameter returns the maximum adjustable trigger delay in ?s.
     T    This parameter returns the accepted minimum increment of the trigger delay in ?s.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ]#   ?  d    Instrument Handle                 ]? 2  ?  d    Trigger Delay Min                 ]? 2 ? ?  d    Trigger Delay Max                 ^B 2" ?  d    Trigger Delay Incr                ^?????  d    Status                                 	            	            	            	           B    This function returns the number of calibrated Microlens Arrays.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     C    This parameter returns the number of calibrated Microlens Arrays.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    `?   ?  d    Instrument Handle                 a" 2  ?  d    MLA Count                         am????  d    Status                                 	            	           ?    This function returns calibration data of the desired Microlens Array index. The number of calibrated lenslet arrays can be derived by function GetMlaCals.

Note: The calibration data are not automatically set active.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     b    This parameter defines the index of a removable microlens array.

Valid range: 0 ... MLACount-1
     ?    This parameter returns the name of the Microlens Array.

Note: The string must contain at least WFS_BUFFER_SIZE (256) elements (char[WFS_BUFFER_SIZE]).     7    This parameter returns the camera pixel pitch in ?m.
     :    This parameter returns the Microlens Array pitch in ?m.
     A    This parameter returns the X Offset of the central MLA lenslet.     B    This parameter returns the Y Offset of the central MLA lenslet.
     _    This parameter returns the calibrated distance (focal length) of  the Microlens Array in ?m.
     k    This parameter returns the calibrated correction value for astigmatism 0? of the Microlens Array in ppm.
     l    This parameter returns the calibrated correction value for astigmatism 45? of the Microlens Array in ppm.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    c?   ?  d    Instrument Handle                 d 2  ?  d    MLA Index                         dr 2 ? ?  d    MLA Name                          e 2" ?  d    Cam Pitch ?m                      eR 2? ?  d    Lenslet Pitch ?m                  e? x ? ?  d    Spot Offset X                     e? x" ?  d    Spot Offset Y                     f' x? ?  d    Lenslet f ?m                      f? ? ? ?  d    Grd Corr 0                        g ?" 	?  d    Grd Corr 45                       gu????  d    Status                                     	            	           	           	           	           	           	           	           	           ?    This function returns calibration data of the desired Microlens Array index. The number of calibrated lenslet arrays can be derived by function GetMlaCals.

Note: The calibration data are not automatically set active.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     b    This parameter defines the index of a removable microlens array.

Valid range: 0 ... MLACount-1
     ?    This parameter returns the name of the Microlens Array.

Note: The string must contain at least WFS_BUFFER_SIZE (256) elements (char[WFS_BUFFER_SIZE]).     7    This parameter returns the camera pixel pitch in ?m.
     :    This parameter returns the Microlens Array pitch in ?m.
     A    This parameter returns the X Offset of the central MLA lenslet.     B    This parameter returns the Y Offset of the central MLA lenslet.
     _    This parameter returns the calibrated distance (focal length) of  the Microlens Array in ?m.
     k    This parameter returns the calibrated correction value for astigmatism 0? of the Microlens Array in ppm.
     l    This parameter returns the calibrated correction value for astigmatism 45? of the Microlens Array in ppm.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
     k    This parameter returns the calibrated correction value for rotation of the Microlens Array in 10^-3 deg.
     c    This parameter returns the calibrated correction value for pitch  of the Microlens Array in ppm.
    k?   ?  d    Instrument Handle                 l 2  ?  d    MLA Index                         lz 2 ? ?  d    MLA Name                          m 2" ?  d    Cam Pitch ?m                      mZ 2? ?  d    Lenslet Pitch ?m                  m? x  ?  d    Spot Offset X                     m? x ? ?  d    Spot Offset Y                     n/ x" ?  d    Lenslet f ?m                      n? x? ?  d    Grd Corr 0                        o	 ?  	?  d    Grd Corr 45                       o}????  d    Status                            o? ? ? 
?  d    Grd Corr Rot                      pg ? ?  d    Grd Corr Pitch                             	            	           	           	           	           	           	           	           	           	           	           ?    This function selects one of the removable microlens arrays by its index. Appropriate calibration values are read out of the instrument and set active.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     ?    This parameter defines the index of a removable microlens array to be selected.

Valid range: 0 ... Number of calibrated MLAs-1
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    t?   ?  d    Instrument Handle                 u6 2  ?  d    MLA Index                         u?????  d    Status                                     	           ?    This function defines the area of interest (AOI) within the camera image in position and size. All spots outside this area are ignored for Zernike and wavefront calculations.

In order to set the max. available area set all 4 input values to 0.0.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     ?    This parameter defines the AOI center X position in mm. It needs to be within the active camera area defined by function ConfigureCam. Origin is the image center.

Note: The parameter must fit to the selected camera area.     ?    This parameter defines the AOI center Y position in mm. It needs to be within the active camera area defined by function ConfigureCam. Origin is the image center.

Note: The parameter must fit to the selected camera area.
     ?    This parameter defines the AOI width in mm. The area needs to be within the active camera area defined by function ConfigureCam.


Note: The parameter must fit to the selected camera area.     ?    This parameter defines the AOI height in mm. The area needs to be within the active camera area defined by function ConfigureCam.


Note: The parameter must fit to the selected camera area.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    w?   ?  d    Instrument Handle                 xp 2  ?  d    AOI Center X mm                   yW 2 ? ?  d    AOI Center Y mm                   z? 2" ?  d    AOI Size X mm                     { 2? ?  d    AOI Size Y mm                     {?????  d    Status                                                 	           ?    This function returns the actual the area of interest (AOI) position and size. All spots outside this area are ignored for BeamView display as well as for Zernike and wavefront calculations.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     :    This parameter returns the AOI center X position in mm.
     <    This parameter returns the pupil center Y position in mm.
     /    This parameter returns the AOI X size in mm.
     /    This parameter returns the AOI Y size in mm.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ~i   ?  d    Instrument Handle                 ~? 2  ?  d    AOI Center X mm                   1 2 ? ?  d    AOI Center Y mm                   u 2" ?  d    AOI Size X mm                     ? 2? ?  d    AOI Size Y mm                     ?????  d    Status                                 	           	           	           	           	           7    This function defines the pupil in position and size.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     ?    This parameter defines the pupil center X position in mm. It needs to be within the active camera area defined by function ConfigureCam. Origin is the image center.

Valid range: -5.0 ... +5.0 mm     ?    This parameter defines the pupil center Y position in mm. It needs to be within the active camera area defined by function ConfigureCam. Origin is the image center.

Valid range: -5.0 ... +5.0 mm     ?    This parameter defines the pupil X diameter in mm. The pupil area needs to be within the active camera area defined by function ConfigureCam.

Valid range: 0.1 ... +10.0 mm     ?    This parameter defines the pupil Y diameter in mm. The pupil area needs to be within the active camera area defined by function ConfigureCam.

Valid range: 0.1 ... +10.0 mm     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ?   ?  d    Instrument Handle                 ?? 2  ?  d    Pupil Center X mm                 ?j 2 ? ?  d    Pupil Center Y mm                 ?7 2" ?  d    Pupil Diameter X mm               ?? 2? ?  d    Pupil Diameter Y mm               ??????  d    Status                                                 	           ?    This function returns the actual the pupil position and size.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     <    This parameter returns the pupil center X position in mm.
     ;    This parameter returns the pupil center Y position in mm.     4    This parameter returns the pupil X diameter in mm.     4    This parameter returns the pupil Y diameter in mm.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ??   ?  d    Instrument Handle                 ?E 2  ?  d    Pupil Center X mm                 ?? 2 ? ?  d    Pupil Center Y mm                 ?? 2" ?  d    Pupil Diameter X mm               ? 2? ?  d    Pupil Diameter Y mm               ?D????  d    Status                                 	           	           	           	           	           V    This function defines the WFS Reference Plane to either Internal or User (external).     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
    ?    This parameter sets the Reference Plane to either Internal or User (external).

Valid values:
  0   WFS_REF_INTERNAL
  1   WFS_REF_USER

User reference is based on a file .ref containing spot reference positions which can be loaded and saved by functions LoadUserRefFile and SaveUserRefFile. It's name is specific to the WFS serial number, MLA name and actual camera resolution.

A default User Refrence file containing a copy of internal reference data can be created by function CreateDefaultUserReference.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ??   ?  d    Instrument Handle                 ? 2 P ?       Reference Index                   ?#????  d    Status                                            Internal 0 User 1    	           J    This function returns the Reference Plane setting of the WFS instrument.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     ?    This parameter returns the actual Reference Plane of the WFS instrument.

Valid return values:
  0   WFS_REF_INTERNAL
  1   WFS_REF_USER
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ??   ?  d    Instrument Handle                 ?B 2  ?  d    Reference Index                   ??????  d    Status                                 	            	           M    This function returns the device status of the Wavefront Sensor instrument.     ?    This parameter accepts the Instrument Handle returned by the Initialize function to select the desired instrument driver session.
        This parameter returns the device status of the Wavefront Sensor
instrument. Lower 24 bits are used.

Bit         Name             Meaning if bit is set

0x00000001  WFS_STATBIT_CON  USB CONnection to device lost
0x00000002  WFS_STATBIT_PTH  Power Too High (cam saturated)
0x00000004  WFS_STATBIT_PTL  Power Too Low (low cam digits)
0x00000008  WFS_STATBIT_HAL  High Ambient Light
0x00000010  WFS_STATBIT_SCL  Spot Contrast too Low
0x00000020  WFS_STATBIT_ZFL  Zernike fit Failed, Low spots no.
0x00000040  WFS_STATBIT_ZFH  Zernike fit Failed, High spots no.
0x00000080  WFS_STATBIT_ATR  Camera is still Awaiting a TRigger
                             
0x00000100  WFS_STATBIT_CFG  Camera is ConFiGured
0x00000200  WFS_STATBIT_PUD  PUpil is Defined
0x00000400  WFS_STATBIT_SPC  No. of Spots or Pupil Changed
0x00000800  WFS_STATBIT_RDA  Reconstr. spot Deviation Available
0x00001000  WFS_STATBIT_URF  No User ReFerence available

0x00002000  WFS_STATBIT_HSP  Camera is in HighSPeed Mode
0x00004000  WFS_STATBIT_MIS  MISmatched centroids in Highspeed
                             Mode
0x00008000  WFS_STATBIT_LOS  LOw Spot count within pupil,
                             reduces Zernike accuracy
0x00010000  WFS_STATBIT_FIL, Pupil badly FILled with spots,
                             reduces Zernike accuracy     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ?\   ?  d    Instrument Handle                 ?? 2  ?  d    Device Status                     ?????  d    Status                                 	           	          ?    This function receives a spotfield image from the WFS camera into a driver buffer. The reference to this buffer is provided by function GetSpotfieldImage() and an image copy is returned by function GetSpotfieldImageCopy().

In case of unsuited image exposure the function sets the appropriate status bits. Use function GetStatus() to check the reason.

Bit         Name             Meaning if bit is set

0x00000002  WFS_STATBIT_PTH  Power Too High (cam saturated)
0x00000004  WFS_STATBIT_PTL  Power Too Low (low cam digits)
0x00000008  WFS_STATBIT_HAL  High Ambient Light

You need to set optimized exposure and gain settings by functions SetExposureTime() and SetMasterGain() and repeate calling the function until these status bits are cleared.

Alternatively, you may use function GetImageAutoExpos().


When the trigger capability is activated by function SetTriggerMode() this function will wait for a trigger event for a short period of time (WFS_TIMEOUT_CAPTURE_TRIGGER = 0.1 sec.) prior to start exposure and will return with error WFS_ERROR_AWAITING_TRIGGER if no trigger event occured.
You need to repeate calling this function until this error and status bit WFS_STATBIT_ATR disappear.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ??   ?  d    Instrument Handle                 ?~????  d    Status                                 	          ?    This function tries to find optimal exposure and gain settings and then it receives a spotfield image from the WFS camera into a driver buffer. The reference to this buffer is provided by function GetSpotfieldImage() and an image copy is returned by function GetSpotfieldImageCopy().

The exposure and gain settings used for this image are returned.

In case of still unsuited image exposure the function sets the appropriate status bits. Use function GetStatus() to check the reason.

Bit         Name             Meaning if bit is set

0x00000002  WFS_STATBIT_PTH  Power Too High (cam saturated)
0x00000004  WFS_STATBIT_PTL  Power Too Low (low cam digits)
0x00000008  WFS_STATBIT_HAL  High Ambient Light

You may repeate calling the function until these status bits are cleared.


When the trigger capability is activated by function SetTriggerMode() this function will wait for a trigger event for a short period of time (WFS_TIMEOUT_CAPTURE_TRIGGER = 0.1 sec.) prior to start exposure and will return with error WFS_ERROR_AWAITING_TRIGGER if no trigger event occured.
You need to repeate calling this function until this error and status bit WFS_STATBIT_ATR disappear.

Note: This function is not available in Highspeed Mode!     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     i    This parameter returns the automatically selected actual exposure time the camera image was taken with.     g    This parameter returns the automatically selected actual master gain the camera image was taken with.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ?F   ?  d    Instrument Handle                 ?? 2  ?  d    Exposure Time Act                 ?= 2 ? ?  d    Master Gain Act                   ??????  d    Status                                 	           	           	           ?    This function returns the reference to a spotfield image taken by functions TakeSpotfieldImage() or TakeSpotfieldImageAutoExpos().
It returns also the image size.

Note: This function is not available in Highspeed Mode!      ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     ?    This parameter returns a reference to the image buffer.

Note: This buffer is allocated by the camera driver and the actual image size is Rows * Columns.
Do not modify this buffer!
     ;    This parameter returns the image height (rows) in pixels.     =    This parameter returns the image width (columns) in pixels.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ?   ?  d    Instrument Handle                 ?? 2  ?  d    ImageBuf                          ?J 2 ? ?  d    Rows                              ?? 2" ?  d    Columns                           ??????  d    Status                                 	            	            	            	               This function returns a copy of the spotfield image taken by functions TakeSpotfieldImage() or TakeSpotfieldImageAutoExpos() into the user provided buffer ImageBuf.
It returns also the image size.

Note: This function is not available in Highspeed Mode!      ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     ?    This parameter accepts an user provided image buffer.

Note: This buffer needs to be allocated by the user. The required size is CAM_MAXPIX_X * CAM_MAXPIX_Y bytes.
     ;    This parameter returns the image height (rows) in pixels.     =    This parameter returns the image width (columns) in pixels.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ??   ?  d    Instrument Handle                 ? 2  ?  d    ImageBuf                          ?? 2 ? ?  d    Rows                              ? 2" ?  d    Columns                           ?J????  d    Status                                 	            	            	            	              This function generates an averaged image from a number of input camera images in ImageBuf. The function returns after each call and the summarized image is stored in ImageBufAveraged.

As soon as the desired number of averages in AverageCount is reached ImageBuf and ImageBufAveraged return both the averaged image data and AverageDataReady returns 1 instead of 0.

Note:
As soon as the image size is changed by function ConfigureCam the averaging process is re-started.
This function is not available in Highspeed Mode!      ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     H    This parameter defines the number of averages.

Valid range: 1 ... 256     o    This parameter returns 0 if the averaging process is going on and 1 when the target average count is reached.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ?   ?  d    Instrument Handle                 ?? 2  ?  d    Average Count                     ?? 2 ? ?  d    Averaged Data Ready               ?_????  d    Status                                     	            	              This function generates a rolling averaged image based on all previously entered camera images in ImageBuf. The function returns after each call and the averaged image is returned in ImageBuf and also stored in ImageBufAveraged.

The new rolling averaged image is calculated pixel by pixel according to the formula:
(AverageCount - 1) * ImageBufAvg + ImageBuf) / AverageCount

Note:
As soon as the image size is changed by function ConfigureCam the averaging process is re-started.
This function is not available in Highspeed Mode!      ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     P    This parameter defines the number of rolling averages.

Valid range: 1 ... 256     F    This parameter resets the rolling averaging process for Reset != 0.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ??   ?  d    Instrument Handle                 ?n 2  ?  d    Average Count                     ?? 2 ? ?  d    Reset                             ?????  d    Status                                         	           ?    This function sets all pixels with intensities < Limit to zero which cuts the noise floor of the camera.

Note: This function is not available in Highspeed Mode!      ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     ?    This parameter defines the intensity limit. All image pixels with intensities < Limit are set to zero.

Valid range: 1 ... 256

Note: The Limit must not set too high to clear the spots within the WFS camera image.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ?#   ?  d    Instrument Handle                 ?? 2  ?  d    Limit                             ??????  d    Status                                     	           ?    This function returns minimum and maximum pixel intensities in ImageBuf as well as the number of saturated pixels in percent.

Note: This function is not available in Highspeed Mode!      ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     F    This parameter returns the minimum pixel intensity within ImageBuf.
     F    This parameter returns the maximum pixel intensity within ImageBuf.
     M    This parameter returns the percentage of saturated pixels within ImageBuf.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ?s   ?  d    Instrument Handle                 ?? 2  ?  d    Image Min                         ?G 2 ? ?  d    Image Max                         ?? 2" ?  d    Saturated Pixels Percent          ??????  d    Status                                 	            	            	           	           ?    This function returns the mean average and rms variations of the pixel intensities in ImageBuf.

Note: This function is not available in Highspeed Mode!      ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     P    This parameter returns the mean average of the pixel intensities in ImageBuf.
     R    This parameter returns the rms variations of the pixel intensities in ImageBuf.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ?A   ?  d    Instrument Handle                 ?? 2  ?  d    Mean                              ? 2 ? ?  d    Rms                               ?y????  d    Status                                 	           	           	           ?    This function returns a single horizontal line of the image in a linear array.

Note: This function is not available in Highspeed Mode!      ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     f    This parameter defines the horizontal line to be selected within ImageBuf.

Valid range: 0 .. rows-1    `    This parameter returns a linear array of floats containing the pixel intensities along the selected line in ImageBuf.

The required array size corresponds to the selected image width in function ConfigureCam and is
   max. 1280 for WFS150/WFS300
   max   640 for WFS10
   max. 1440 for WFS20
   max. 1936 for WFS30
   max. 2048 for WFS40
instruments.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ?~   ?  d    Instrument Handle                 ? 2  ?  d    Line                              ?r 2 ?    d    Line Selected                     ??????  d    Status                                     	            	           ?    This function returns two linear arrays containing the minimum and maximum intensities within the image columns, respectively.

Note: This function is not available in Highspeed Mode!      ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
    c    This parameter returns a linear array of floats containing the minimum pixel intensities within all columns of ImageBuf.

The required array size corresponds to the selected image width in function ConfigureCam and is
   max. 1280 for WFS150/WFS300
   max   640 for WFS10
   max. 1440 for WFS20
   max. 1936 for WFS30
   max. 2048 for WFS40
instruments.    c    This parameter returns a linear array of floats containing the maximum pixel intensities within all columns of ImageBuf.

The required array size corresponds to the selected image width in function ConfigureCam and is
   max. 1280 for WFS150/WFS300
   max   640 for WFS10
   max. 1440 for WFS20
   max. 1936 for WFS30
   max. 2048 for WFS40
instruments.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ?   ?  d    Instrument Handle                 ɍ 2     d    Line Min                          ?? 2 ?    d    Line Max                          ?c????  d    Status                                 	            	            	              This function calculates and returns the beam centroid and diameter data based on the intensity distribution of the WFS camera image in mm.

Note:
The beam centroid is highly sensitive to an increased black level of the camera image. For good accuracy it is recommended to set it as low as needed using function SetBlackLevelOffset.

The beam diameter is calculated by the second moment formula. 

The initial beam is split into many spots by the lenslets which reduces accuracy also.

This function is not available in Highspeed Mode!      ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     4    This parameter returns the beam centroid X in mm.
     4    This parameter returns the beam centroid Y in mm.
     4    This parameter returns the beam diameter X in mm.
     4    This parameter returns the beam diameter Y in mm.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ??   ?  d    Instrument Handle                 ?~ 2  ?  d    Beam Centroid X mm                к 2 ? ?  d    Beam Centroid Y mm                ?? 2" ?  d    Beam Diameter X mm                ?2 2? ?  d    Beam Diameter Y mm                ?n????  d    Status                                 	           	           	           	           	              This function calculates the centroids, diameters (optional) and intensities of all spots generated by the lenslets.

Data arrays are returned by separate functions:
GetSpotCentroids
GetSpotDiameters
GetSpotIntensities

Note: This function is not available in Highspeed Mode!      ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
    `    This parameter activates the dynamic noise cut function if DynamicNoiseCut = 1. In this case each detected spot is analyzed using an individual optimized minimum intensity limit.

If DynamicNoiseCut is not used (=0) it is recommended to use function CutImageNoiseFloor prior to this function in order to clear lower intensity pixels at a fixed level.     ?    This parameter activates (=1) or deactivates (=0) the calculation of the spot diameters. Only when activated the function GetSpotDiameters can susequently return valid spot diameters.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ԁ   ?  d    Instrument Handle                 ? 2 F ?       Dynamic Noise Cut                 ?o 2 ? ?       Calculate Diameters               ?1????  d    Status                                On 1 Off 0    On 1 Off 0    	              This function returns two two-dimensional arrays containing the centroid X and Y positions in pixels calculated by function WFS_CalcSpotsCentrDiaIntens.

Note: Function WFS_CalcSpotsCentrDiaIntens is required to run successfully before calculated data can be retrieved.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
        This parameter returns a two-dimensional array of float containing the centroid X spot positions in pixels.

The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].

Note: First array index is the spot number in Y, second index the spot number in X direction.        This parameter returns a two-dimensional array of float containing the centroid Y spot positions in pixels.

The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].

Note: First array index is the spot number in Y, second index the spot number in X direction.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ٿ   ?  d    Instrument Handle                 ?E 2     d    Array Centroid X                  ?Q 2 ?    d    Array Centroid Y                  ?]????  d    Status                                 	            	            	          d    This function returns two two-dimensional arrays containing the spot diameters in X and Y direction in pixels calculated by function WFS_CalcSpotsCentrDiaIntens.

Note: Function WFS_CalcSpotsCentrDiaIntens is required to run successfully with option CalcDias = 1 before calculated data can be retrieved.
This function is not available in Highspeed Mode!      ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
        This parameter returns a two-dimensional array of float containing the spot diameters in X direction in pixels.

The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].

Note: First array index is the spot number in Y, second index the spot number in X direction.        This parameter returns a two-dimensional array of float containing the spot diameters in Y direction in pixels.

The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].

Note: First array index is the spot number in Y, second index the spot number in X direction.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ?<   ?  d    Instrument Handle                 ?? 2     d    Array Diameter X                  ?? 2 ?    d    Array Diameter Y                  ??????  d    Status                                 	            	            	           ?    This function calculates statistic parameters of the wavefront calculated in function WFS_CalcWavefront.

Note: Function WFS_CalcWavefront is required to run prior to this function.
This function is not available in Highspeed Mode!      ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     3    This parameter returns the Minimum spot diameter.     3    This parameter returns the Maximum spot diameter.     <    This parameter returns the Mean average of spot diameters.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ?G   ?  d    Instrument Handle                 ?? 2  ?  d    Min                               ? 2 ? ?  d    Max                               ?C 2" ?  d    Mean                              ??????  d    Status                                 	           	           	           	          
    This function returns a two-dimensional array containing the spot intensities in arbitrary unit calculated by function WFS_CalcSpotsCentrDiaIntens.

Note: Function WFS_CalcSpotsCentrDiaIntens is required to run successfully before calculated data can be retrieved.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
        This parameter returns a two-dimensional array of float containing the spot intensities in arbitrary unit.

The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].

Note: First array index is the spot number in Y, second index the spot number in X direction.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ?M   ?  d    Instrument Handle                 ?? 2     d    Array Intensity                   ??????  d    Status                                 	            	          ?    This function calculates reference positions and deviations for all spots depending on the setting ref_idx(internal/user) set by function SetWavefrontReference.
When option CancelWavefrontTilt is enabled the mean deviation in X and Y direction, which is measured within the pupil, is subtracted from the deviation data arrays.

Reference positions can be retrieved using function GetSpotReferencePositions and calculated deviations by function GetSpotDeviations.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
    7    This parameter forces the mean spot deviations, which are measured within the pupil, to be canceled so that the average wavefront tilt will disappear when calculated with function CalcWavefront.

Valid values:
   0   calculate deviations normal
   1   subtract mean deviation in pupil from all spot deviations     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ??   ?  d    Instrument Handle                 ?n 2 P ?       Cancel Wavefront Tilt             ??????  d    Status                                            No 0 Yes 1    	           ?    This function returns two two-dimensional arrays containing the actual X and Y reference spot positions in pixels.

A prior call to function WFS_SetReferencePlane() determines whether the internal or user defined reference positions are returned.
     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
        This parameter returns a two-dimensional array of float containing the actual reference X spot positions in pixels.

The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].

Note: First array index is the spot number in Y, second index the spot number in X direction.        This parameter returns a two-dimensional array of float containing the actual reference Y spot positions in pixels.

The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].

Note: First array index is the spot number in Y, second index the spot number in X direction.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ??   ?  d    Instrument Handle                 ?t 2     d    Array Ref Pos X                   ?? 2 ?    d    Array Ref Pos Y                   ??????  d    Status                                 	            	            	          "    This function returns two two-dimensional arrays containing the actual X and Y spot deviations between centroid and reference spot positions in pixels calculated by function CalcSpotToReferenceDeviations.

Note: Function CalcSpotToReferenceDeviations needs to run prior to this function.
     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
    f    This parameter returns a two-dimensional array of float containing the deviation in X direction between centroid and reference spot positions in pixels calculated by function CalcSpotToReferenceDeviations.

The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].

Note: First array index is the spot number in Y, second index the spot number in X direction.    f    This parameter returns a two-dimensional array of float containing the deviation in Y direction between centroid and reference spot positions in pixels calculated by function CalcSpotToReferenceDeviations.

The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].

Note: First array index is the spot number in Y, second index the spot number in X direction.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ?9   ?  d    Instrument Handle                 ?? 2     d    Array Deviations X                ?- 2 ?    d    Array Deviations Y                ??????  d    Status                                 	            	            	          P    This function calculates the spot deviations (centroid with respect to its reference) and performs a least square fit to the desired number of Zernike functions.

Output results are the Zernike coefficients up to the desired number of Zernike modes and an array summarizing these coefficients to rms amplitudes for each Zernike order.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
    ?    This parameter sets and returns the number of desired Zernike modes to fit.
An input value 0 sets the number of calculated modes automatically, depending on the number of available spot deviations, and returns it.
Input values in the range 2 .. 10 define the number of calculated Zernike modes according to this table: 

Input Zernike Order   Calculated Zernike Modes
        0 = auto             auto
        2                      6
        3                     10
        4                     15
        5                     21
        6                     28
        7                     36
        8                     45
        9                     55
       10                     66
     ?    This parameter returns a one-dimensional array of float containing the calculated Zernike coefficients.

The required array size is [MAX_ZERNIKE_MODES+1] because indices [1..66] are used instead of [0 .. 65].        This parameter returns a one-dimensional array of float containing the calculated Zernike coefficients summarizing these coefficients to rms amplitudes for each Zernike order.

The required array size is [MAX_ZERNIKE_ORDERS+1] because indices [1..10] are used instead of [0 .. 9].     }    This parameter returns the Radius of Curvature RoC for a spherical wavefront in mm, derived from Zernike coefficient Z[5].
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    ?f   ?  d    Instrument Handle                 ?? 2  ?  d    Zernike Orders                    ?? 2 ?    d    Array Zernike um                  ? 2"    d    Array Zernike Orders um          ? 2? ?  d    RoC mm                           2????  d    Status                                 	            	            	            	           	           ?    This function calculates the Fourier and Optometric notations from the Zernike coefficients calculated in function WFS_ZernikeLsf.

Note: Function WFS_ZernikeLsf is required to run prior to this function.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     ?    This parameter is the calculated number of Zernike orders in function WFS_ZernikeLsf. Use the value returned from this function.     ?    This parameter defines the highest Zernike order considered for calculating Fourier coefficients M, J0 and J45 as well as the Optometric parameters Sphere, Cylinder and Axis.

Valid settings: 2, 4 or 6     /    This parameter returns Fourier coefficient M.     0    This parameter returns Fourier coefficient J0.     1    This parameter returns Fourier coefficient J45.     A    This parameter returns Optometric parameter Sphere in diopters.     C    This parameter returns Optometric parameter Cylinder in diopters.     :    This parameter returns Optometric parameter Axis in deg.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
   ?   ?  d    Instrument Handle                ? 2  ?  d    Zernike Orders                    ?  ?  d    Fourier Order                    ? 2 ? ?  d    Fourier M                         2" ?  d    Fourier J0                       O 2? ?  d    Fourier J45                      ? ? ? ?  d    Opto Sphere                      ? ?" ?  d    Opto Cylinder                     ?? ?  d    Opto Axis deg                    ^????  d    Status                                         	           	           	           	           	           	           	           ?    This function calculates the reconstructed spot deviations based on the calculated Zernike coefficients.

Note: This function needs to run prior to function WFS_CalcWavefront when the reconstructed or difference Wavefront should be calculated.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     ?    This parameter is the calculated number of Zernike orders in function WFS_ZernikeLsf. Use the value returned from this function.    q    This parameter accepts a one-dimensional array of content 0 or 1 indicating if the appropriate Zernike mode is checked for reconstruction or not.

Note: Required array dimension is [MAX_ZERNIKE_MODES+1] because valid indices are [1 .. 66] instead of [0 .. 65].

Valid array values:
  0   ignore this Zernike mode in reconstruction
  1   reconstruct this Zernike mode
     6    This parameter returns the Mean Fit error in arcmin.     D    This parameter returns the Standard Deviation Fit error in arcmin.    J    This parameter forces only Zernike mode Z[5] to be reconstructed in order to get deviations based on a pure spherical wavefront.

Set parameter to 1 to perform a Spherical Reference calibration.

Valid values:
   0   use all Zernike Modes checked in ArrayZernikeReconstruct
   1   use only Z[5] for pure spherical reconstruction     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
   D   ?  d    Instrument Handle                ? 2  ?  d    Zernike Orders                   T 2 ? ?  d    Array Zernike Reconstruct        ? ? ? ?  d    Fit Err Mean                      ?" ?  d    Fit Err Stdev                    W .T ?       Do Spherical Reference           ?????  d    Status                                         	           	                     Yes 1 No 0    	           F    This function calculates the wavefront based on the spot deviations.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
    W    This parameter returns a two-dimensional array of float containing the wavefront data in ?m.

The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].

Note: First array index is the spot number in Y, second index the spot number in X direction. You may used function Flip2DArray() to flip the index order prior to display by a graphical tool.    X    This parameter defines the type of wavefront to calculate.

Valid settings:
  0   Measured Wavefront
  1   Reconstructed Wavefront based on Zernike coefficients
  2   Difference between measured and reconstructed Wavefront

Note: Function WFS_CalcReconstrDeviations needs to be called prior to this function in case of Wavefront type 1 and 2.     ?    This parameter defines if the Wavefront should be calculated based on all detected spots or only within the defined pupil.

Valid settings:
   0   Calculate Wavefront for all spots
   1   Limit Wavefront to pupil interior     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
   +   ?  d    Instrument Handle                ? 2"    d    Array Wavefront                   2 n ?       Wavefront Type                   p 2 ? ?       Limit to Pupil                   W????  d    Status                                 	                       (Measured 0 Reconstructed 1 Difference 2              Yes 1 No 0    	           ?    This function returns statistic parameters of the wavefront in ?m calculated by function WFS_CalcWavefront.

Note: Function WFS_CalcWavefront is required to run prior to this function.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     <    This parameter returns the Minimum value of the wavefront.     <    This parameter returns the Maximum value of the wavefront.     U    This parameter returns the Difference between Maximum and Minimum of the wavefront.     9    This parameter returns the Mean value of the wavefront.     8    This parameter returns the RMS value of the wavefront.     z    This parameter returns the weighted RMS value of the wavefront. The weighting is based on the individual spot intensity.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
      ?  d    Instrument Handle                ? 2  ?  d    Min                              ? 2 ? ?  d    Max                               2" ?  d    Diff                             q ?  ?  d    Mean                             ? ? ? ?  d    RMS                              ? ?" ?  d    Weighted RMS                     t????  d    Status                                 	           	           	           	           	           	           	           f    This function causes the instrument to perform a self-test and returns the result of that self-test.     ?    This parameter accepts the Instrument Handle returned by the Initialize function to select the desired instrument driver session.    3    Operational return status. Contains either a completion code or an error code. Instrument driver specific codes that may be returned in addition to the VISA error codes defined in VPP-4.3 and vendor specific codes, are as follows.

Completition Codes
----------------------------------------------------------------
VI_SUCCESS              Self-test operation successful
VI_WARN_NSUP_SELF_TEST  Self-test not supported


Vendor Specific Codes
----------------------------------------------------------------
For error codes and descriptions see <Error Message>.     F    Numeric result from self-test operation 
0 = no error (test passed).         Self-test status message.   Y   ?  ?    Instrument Handle                ?|???  ?    Status                           " 2  ?  ?    Self Test Result                 "m 2 ? ?  ?    Self-Test Message                  0    	           	            	            +    Places the instrument in a default state.     ?    This parameter accepts the Instrument Handle returned by the Initialize function to select the desired instrument driver session.    ,    Operational return status. Contains either a completion code or an error code. Instrument driver specific codes that may be returned in addition to the VISA error codes defined in VPP-4.3 and vendor specific codes, are as follows.

Completition Codes
----------------------------------------------------------------
VI_SUCCESS              Reset operation successful.
VI_WARN_NSUP_RESET      Reset not supported.

Vendor Specific Codes
----------------------------------------------------------------
For error codes and descriptions see <Error Message>.   #?    ?  ?    Instrument Handle                $K????  ?    Status                             0    	           u    This function returns the revision of the instrument driver and the firmware revision of the instrument being used.     ?    This parameter accepts the Instrument Handle returned by the Initialize function to select the desired instrument driver session.    @    Operational return status. Contains either a completion code or an error code. Instrument driver specific codes that may be returned in addition to the VISA error codes defined in VPP-4.3 and vendor specific codes, are as follows.

Completition Codes
----------------------------------------------------------------
VI_SUCCESS               Revision query successful
VI_WARN_NSUP_REV_QUERY   Instrument revision query not supported


Vendor Specific Codes
----------------------------------------------------------------
For error codes and descriptions see <Error Message>.         Instrument driver revision.         Instrument firmware revision.   'w (  ?  ?    Instrument Handle                (????  ?    Status                           *J 2 ( ?  ?    Instrument Driver Revision       *o 2 ? ?  ?    Firmware Revision                  0    	           	            	            Y    This function queries the instrument and returns instrument-specific error information.     ?    This parameter accepts the Instrument Handle returned by the Initialize function to select the desired instrument driver session.    ;    Operational return status. Contains either a completion code or an error code. Instrument driver specific codes that may be returned in addition to the VISA error codes defined in VPP-4.3 and vendor specific codes, are as follows.

Completition Codes
----------------------------------------------------------------
VI_SUCCESS                Error query operation successful
VI_WARN_NSUP_ERROR_QUERY  Error query not supported


Vendor Specific Codes
----------------------------------------------------------------
For error codes and descriptions see <Error Message>.     5    Instrument error code returned by driver functions.     H    Error message.
The message buffer has to be intialized with 256 bytes.   +? (  ?  ?    Instrument Handle                ,????  ?    Status                           .?  ( ?  ?    Error Code                       .?  ? ?  ?    Error Message                      0    	           	            	            {    This function translates the error return value from a VXIplug&play instrument driver function to a user-readable string.     ?    This parameter accepts the Instrument Handle returned by the Initialize function to select the desired instrument driver session.    ?    Operational return status. Contains either a completion code or an error code. Instrument driver specific codes that may be returned in addition to the VISA error codes defined in VPP-4.3 and vendor specific codes, are as follows.

Completition Codes
----------------------------------------------------------------
VI_SUCCESS                Error query operation successful
VI_WARN_UNKNOWN_STATUS    The Error Code cannot be interpreted.         Instrument driver error code.     b    VISA or instrument driver Error message.
The message buffer has to be initalized with 256 bytes.   0? *  ?  ?    Instrument Handle                1Zv???  ?    Status                           3 / ( ?  ?    Error Code                       3A , ( ?  ?    Error Message                      0    	               	            ?    This function reads all Wavefront Sensor devices connected to the PC and returns the number of it.

Use function GetInstrumentListInfo to retrieve information about each WFS instrument.     K    This parameter returns the number of WFS instruments connected to the PC.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
     p    This parameter is necessary to be VXIpnp compliant.
Set the parameter to VI_NULL as this parameter is ignored.   5c 2  ?  d    Instrument Count                 5?????  d    Status                           6-    ?  d    Instrument Handle                  	            	           VI_NULL    d    This function returns information about one connected WFS instrument selected by Instrument Index.     ?    This parameter accepts the index of a WFS instrument of the instrument list generated by function GetInstrumentListLen.

Valid range: 0 .. InstrumentCount-1

Note: The first instrument has index 0.

     ]    This parameter returns the Device ID required to open the WFS instrument in function init.
     ?    This parameter returns the information if the instrument is already used by another application or driver session.

  0   not in use, free to open
  1   already in use

Note: An instrument already in use will fails to open in function init.     ?    This parameter returns the Instrument Name of the selected instrument.

Note: The string must contain at least WFS_BUFFER_SIZE (256) elements (char[WFS_BUFFER_SIZE]).      ?    This parameter returns the Serial Number of the selected instrument.

Note: The string must contain at least WFS_BUFFER_SIZE (256) elements (char[WFS_BUFFER_SIZE]).     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
     q    This parameter is necessary to be VXIpnp compliant.
Set the parameter to VI_NULL as this parameter is ignored.
     ?    This resoruce name can be used for the Initialize function.
The string has the format: "USB::0x1313::0x0000::" followed by the device ID.   7? 2  ?  d    Instrument List Index            8? 2 ? ?  d    Device ID                        9	 2" ?  d    In Use                           : ?  ?  d    Instrument Name                  :? ? ? ?  d    Instrument SN                    ;b????  d    Status                           ;?   ?  d    Instrument Handle                <R ?" ?  ?    Resource Name                          	            	            	            	            	           VI_NULL    	            ?    This function returns two one-dimensional arrays containing the X and Y axis scales in mm for spot intensity and wavefront arrays. The center spot in the image center is denoted (0.0, 0.0) mm.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     w    This parameter returns a one-dimensional array containing the X scale in mm.

The required array size is MAX_SPOTS_X.     w    This parameter returns a one-dimensional array containing the Y scale in mm.

The required array size is MAX_SPOTS_Y.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
   ??   ?  d    Instrument Handle                @4 2     d    Array Scale X                    @? 2 ?    d    Array Scale Y                    A2????  d    Status                                 	            	            	           ?    This function converts the wavefront data array calculated by function CalcWavefront() from ?m into waves unit depending on the actual wavelength.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     ?    This parameter accepts a two-dimensional array of float containing the wavefront data in ?m.

The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].
     ?    This parameter returns a two-dimensional array of float containing the wavefront data in waves.

The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].     T    This parameter accepts the actual wavelength in nm.

Valid range: 300 ... 1100 nm.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
   CA   ?  d    Instrument Handle                C? 2 ?    d    Array Wavefront In               Df 2"    d    Array Wavefront Out              E 2  ?  d    Wavelength                       Ec????  d    Status                                     	                	          ,    This function flips a 2-dimensional array of size ArrayYX[MAX_SPOTS_Y][MAX_SPOTS_X] into another array ArrayXY[MAX_SPOTS_X][MAX_SPOTS_Y] with fliped x,y index order.

This function is helpful to convert data arrays calculated by this WFS driver into a format accepted by graphic tools for display.
     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     ?    This parameter returns a two-dimensional array of float and array size [MAX_SPOTS_X][MAX_SPOTS_Y]. All array indices are flipped compared to input ArrayYX

Note: Array XY must not be the same than Array YX!
     e    This parameter accepts a two-dimensional array of float and array size [MAX_SPOTS_Y][MAX_SPOTS_X].
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
   H;   ?  d    Instrument Handle                H? 2 ?    d    Array XY                         I? 2     d    Array YX                         J????  d    Status                                 	                	           ?    This function copies the measured spot centroid positions to the User Reference spot positions. Consequently spot deviations become zero resulting in a plane wavefront.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
   L$   ?  d    Instrument Handle                L?????  d    Status                                 	           ?    This function sets the X and Y user reference spot positions in pixels to calculated spot positions given by two two-dimensional arrays.
     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
        This parameter accepts a two-dimensional array of float containing user calculated reference X spot positions in pixels.

The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].

Note: First array index is the spot number in Y, second index the spot number in X direction.        This parameter accepts a two-dimensional array of float containing user calculated reference Y spot positions in pixels.

The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].

Note: First array index is the spot number in Y, second index the spot number in X direction.     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
    l    This parameter defines the reference type to either relative or or absolute.

Valid values:
  0   WFS_REF_TYPE_REL
  1   WFS_REF_TYPE_ABS

Relative reference type means that the given spot positions are relative (+/- pixels) to the internal factory calibration data whereas absolute reference type denotes absolute spot position data (0 ... max. camera pixels).
   N.   ?  d    Instrument Handle                N? 2 ? ?  d    Array Ref Pos X                  O? 2" ?  d    Array Ref Pos Y                  P?????  d    Status                           Q] 2 P ?       Reference Type                                 	                      Relative 0 Absolute 1    ?    This function generates a default User Reference which is identical to the Internal Reference. Use function GetSpotReferencePositions to get the data arrays.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
   T?   ?  d    Instrument Handle                UD????  d    Status                                 	          ?    This function saves a User Reference spotfield file for the actual selected Microlens Array and image resolution into the folder
C:\Users\<user_name>\Documents\Thorlabs\Wavefront Sensor\Reference

The file name is automatically set to:
WFS_<serial_number_wfs>_<mla_name>_<cam_resol_idx>.ref
or
WFS10_<serial_number_wfs>_<mla_name>_<cam_resol_idx>.ref
or
WFS20_<serial_number_wfs>_<mla_name>_<cam_resol_idx>.ref
or
WFS30_<serial_number_wfs>_<mla_name>_<cam_resol_idx>.ref
or
WFS40_<serial_number_wfs>_<mla_name>_<cam_resol_idx>.ref

Example: "WFS_M00224955_MLA150M-5C_0.ref"

Note: Centroid positions of undetected spots are stored as 0.0 instead of NaN.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
   X?   ?  d    Instrument Handle                YR????  d    Status                                 	          ?    This function loads a User Reference spotfield file for the actual selected Microlens Array and image resolution from folder
C:\Users\<user_name>\Documents\Thorlabs\Wavefront Sensor\Reference

The file name is automatically set to:
WFS_<serial_number_wfs>_<mla_name>_<cam_resol_idx>.ref
or
WFS10_<serial_number_wfs>_<mla_name>_<cam_resol_idx>.ref
or
WFS20_<serial_number_wfs>_<mla_name>_<cam_resol_idx>.ref
or
WFS30_<serial_number_wfs>_<mla_name>_<cam_resol_idx>.ref
or
WFS40_<serial_number_wfs>_<mla_name>_<cam_resol_idx>.ref

Example: "WFS_M00224955_MLA150M-5C_0.ref"

Note: Centroid positions stored as 0.0 are converted to NaN in the reference spotfield array because they denote undetected spots.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
   ]
   ?  d    Instrument Handle                ]?????  d    Status                                 	          ?    This function calculates User Reference spot positions based on an already performed measurement of a pure sherical wavefront.

It supposes an already performed measurement including
- calculation of Zernike coefficients with function ZernikeLsf
- already calculated reconstructed deviations using function
  CalcReconstrDeviations with option do_spherical_reference
  set to 1.

Use function SetReferenceType to activate the performed spherical User Reference calibration.     ~    This parameter accepts the Instrument Handle returned by the Init function to select the desired instrument driver session.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
   `d   ?  d    Instrument Handle                `?????  d    Status                                 	           s    This function closes the instrument driver session.

Note: The instrument must be reinitialized to use it again.
     ?    This parameter accepts the Instrument Handle returned by the Initialize function to select the desired instrument driver session.
     o    This value shows the status code returned by the function call.

For Status Codes see function ErrorMessage.
   bV 2   ?  d    Instrument Handle                b?????  d    Status                                 	        ????         ?  t             H.        init                                                                            _VI_FUNC                                                ????         ?  H             K.        GetInstrumentInfo                                                               _VI_FUNC                                                ????         ?  ?             K.        ConfigureCam                                                                    _VI_FUNC                                                ????         $x  +             K.        SetHighspeedMode                                                                _VI_FUNC                                                ????         ,?  1?             K.        GetHighspeedWindows                                                             _VI_FUNC                                                ????         3?  68             K.        CheckHighspeedCentroids                                                         _VI_FUNC                                                ????         6?  9S             K.        GetExposureTimeRange                                                            _VI_FUNC                                                ????         :?  <?             K.        SetExposureTime                                                                 _VI_FUNC                                                ????         =?  ?.             K.        GetExposureTime                                                                 _VI_FUNC                                                ????         ??  B?             K.        GetMasterGainRange                                                              _VI_FUNC                                                ????         C?  F             K.        SetMasterGain                                                                   _VI_FUNC                                                ????         G  H?             K.        GetMasterGain                                                                   _VI_FUNC                                                ????         IP  K?             K.        SetBlackLevelOffset                                                             _VI_FUNC                                                ????         LD  M?             K.        GetBlackLevelOffset                                                             _VI_FUNC                                                ????         N?  T              K.        SetTriggerMode                                                                  _VI_FUNC                                                ????         T?  X?             K.        GetTriggerMode                                                                  _VI_FUNC                                                ????         Y^  [?             K.        SetTriggerDelay                                                                 _VI_FUNC                                                ????         \?  _             K.        GetTriggerDelayRange                                                            _VI_FUNC                                                ????         `R  a?             K.        GetMlaCount                                                                     _VI_FUNC                                                ????         b?  g?             K.        GetMlaData                                                                      _VI_FUNC                                                ????         j?  p?             K.        GetMlaData2                                                                     _VI_FUNC                                                ????         t  v7             K.        SelectMla                                                                       _VI_FUNC                                                ????         v?  |C             K.        SetAoi                                                                          _VI_FUNC                                                ????         }?  ?Z             K.        GetAoi                                                                          _VI_FUNC                                                ????         ??  ?             K.        SetPupil                                                                        _VI_FUNC                                                ????         ?x  ??             K.        GetPupil                                                                        _VI_FUNC                                                ????         ?9  ??             K.        SetReferencePlane                                                               _VI_FUNC                                                ????         ?j  ?L             K.        GetReferencePlane                                                               _VI_FUNC                                                ????         ?  ??             K.        GetStatus                                                                       _VI_FUNC                                                ????         ?A  ??             K.        TakeSpotfieldImage                                                              _VI_FUNC                                                ????         ?o  ?#             K.        TakeSpotfieldImageAutoExpos                                                     _VI_FUNC                                                ????         ?  ?I             K.        GetSpotfieldImage                                                               _VI_FUNC                                                ????         ??  ??             K.        GetSpotfieldImageCopy                                                           _VI_FUNC                                                ????         ??  ??             K.        AverageImage                                                                    _VI_FUNC                                                ????         ??  ??             K.        AverageImageRolling                                                             _VI_FUNC                                                ????         ?w  ??             K.        CutImageNoiseFloor                                                              _VI_FUNC                                                ????         ??  ?a             K.        CalcImageMinMax                                                                 _VI_FUNC                                                ????         ??  ??             K.        CalcMeanRmsNoise                                                                _VI_FUNC                                                ????         ??  ?Q             K.        GetLine                                                                         _VI_FUNC                                                ????         ?E  ??             K.        GetLineView                                                                     _VI_FUNC                                                ????         ??  ??             K.        CalcBeamCentroidDia                                                             _VI_FUNC                                                ????         ?c  ר             K.        CalcSpotsCentrDiaIntens                                                         _VI_FUNC                                                ????         ب  ??             K.        GetSpotCentroids                                                                _VI_FUNC                                                ????         ??  ?Y             K.        GetSpotDiameters                                                                _VI_FUNC                                                ????         ?U  ??             K.        GetSpotDiaStatistics                                                            _VI_FUNC                                                ????         ?;  ?U             K.        GetSpotIntensities                                                              _VI_FUNC                                                ????         ?  ?$             K.        CalcSpotToReferenceDeviations                                                   _VI_FUNC                                                ????         ??  ?             K.        GetSpotReferencePositions                                                       _VI_FUNC                                                ????         ?  ?             K.        GetSpotDeviations                                                               _VI_FUNC                                                ????         ? ?             K.        ZernikeLsf                                                                      _VI_FUNC                                                ????        ' ?         
    K.        CalcFourierOptometric                                                           _VI_FUNC                                                ????        G               K.        CalcReconstrDeviations                                                          _VI_FUNC                                                ????        ? ?             K.        CalcWavefront                                                                   _VI_FUNC                                                ????        D ?             K.        CalcWavefrontStatistics                                                         _VI_FUNC                                                ????        ? "?             K.        self_test                                                                       _VI_FUNC                                                ????        #? &             K.        reset                                                                           _VI_FUNC                                                ????        &? *?             K.        revision_query                                                                  _VI_FUNC                                                ????        +? /O             K.        error_query                                                                     _VI_FUNC                                                ????        0L 3?             K.        error_message                                                                   _VI_FUNC                                                ????        4? 6?             K.        GetInstrumentListLen                                                            _VI_FUNC                                                ????        7g <?             K.        GetInstrumentListInfo                                                           _VI_FUNC                                                ????        >? A?             K.        GetXYScale                                                                      _VI_FUNC                                                ????        B? E?             K.        ConvertWavefrontWaves                                                           _VI_FUNC                                                ????        G J~             K.        Flip2DArray                                                                     _VI_FUNC                                                ????        Kr M!             K.        SetSpotsToUserReference                                                         _VI_FUNC                                                ????        M? R?             K.        SetCalcSpotsToUserReference                                                     _VI_FUNC                                                ????        T U?             K.        CreateDefaultUserReference                                                      _VI_FUNC                                                ????        V5 Y?             K.        SaveUserRefFile                                                                 _VI_FUNC                                                ????        ZC ^             K.        LoadUserRefFile                                                                 _VI_FUNC                                                ????        ^? aa             K.        DoSphericalRef                                                                  _VI_FUNC                                                ????        a? cY             K.        close                                                                           _VI_FUNC                                                      ?                                                                                     ?Initialize                                                                          sConfiguration Functions                                                              ?Get Instrument Info                                                                  ?Configure Cam                                                                        ?Set Highspeed Mode                                                                   ?Get Highspeed Windows                                                                ?Check Highspeed Centroids                                                            ?Get Exposure Time Range                                                              ?Set Exposure Time                                                                    ?Get Exposure Time                                                                    ?Get Master Gain Range                                                                ?Set Master Gain                                                                      ?Get Master Gain                                                                      ?Set Black Level Offset                                                               ?Get Black Level Offset                                                               ?Set Trigger Mode                                                                     ?Get Trigger Mode                                                                     ?Set Trigger Delay                                                                    ?Get Trigger Delay Range                                                              ?Get Mla Count                                                                        ?Get Mla Data                                                                         ?Get Mla Data 2                                                                       ?Select Mla                                                                           ?Set Aoi                                                                              ?Get Aoi                                                                              ?Set Pupil                                                                            ?Get Pupil                                                                            ?Set Reference Plane                                                                  ?Get Reference Plane                                                                 ?Action/Status Functions                                                              ?Get Status                                                                          bData Functions                                                                       ?Take Spotfield Image                                                                 ?Take Spotfield Image Auto Expos                                                      ?Get Spotfield Image                                                                  ?Get Spotfield Image Copy                                                             ?Average Image                                                                        ?Average Image Rolling                                                                ?Cut Image Noise Floor                                                                ?Calc Image Min Max                                                                   ?Calc Mean Rms Noise                                                                  ?Get Line                                                                             ?Get Line View                                                                        ?Calc Beam Centroid Dia                                                               ?Calc Spots Centr Dia Intens                                                          ?Get Spot Centroids                                                                   ?Get Spot Diameters                                                                   ?Get Spot Dia Statistics                                                              ?Get Spot Intensities                                                                 ?Calc Spot To Reference Deviations                                                    ?Get Spot Reference Positions                                                         ?Get Spot Deviations                                                                  ?Zernike Lsf                                                                          ?Calc Fourier Optometric                                                              ?Calc Reconstr Deviations                                                             ?Calc Wavefront                                                                       ?Calc Wavefront Statistics                                                           ?Utility Functions                                                                    ?Self-Test                                                                            ?Reset                                                                                ?Revision Query                                                                       ?Error Query                                                                          ?Error Message                                                                        ?Get Instrument List Len                                                              ?Get Instrument List Info                                                             ?Get XY Scale                                                                         ?Convert Wavefront Waves                                                              ?Flip 2D Array                                                                       6Calibration Functions                                                                ?Set Spots To User Reference                                                          ?Set Calc Spots To User Reference                                                     ?Create Default User Reference                                                        ?Save User Ref File                                                                   ?Load User Ref File                                                                   ?Do Spherical Ref                                                                     ?close                                                                           