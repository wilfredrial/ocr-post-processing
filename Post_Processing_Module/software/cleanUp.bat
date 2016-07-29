:: This batch file cleans up the tiff images of a folder in "1_Input_Tiff_Images"
:: The files are placed in a folder of the same name in "2_Output_Image_Magick"
:: For example, enter:  Volume1

set /p pathName=Enter the folder of tiffs from the Input Tiff Image folder to be cleaned : %=%
MD "..\2_Output_Image_Magick\%pathname%"
:: 2 f's
FOR %%a in ("..\1_Input_Tiff_Images\%pathname%\*.tiff") DO (
	convert "%%a" -write MPR:source ^
	-morphology close rectangle:6x5 ^
	-morphology erode square    MPR:source -compose Lighten -composite ^
	-morphology erode square    MPR:source -composite ^
	-morphology erode square    MPR:source -composite ^
	-morphology erode square    MPR:source -composite ^
	-morphology erode square    MPR:source -composite ^
	-morphology erode square    MPR:source -composite ^
	-morphology erode square    MPR:source -composite ^
	-morphology erode square    MPR:source -composite ^
	-morphology erode square    MPR:source -composite ^
	"..\2_Output_Image_Magick\%pathname%\%%~na.tif"
	)
	
:: 1 f
FOR %%a in ("..\1_Input_Tiff_Images\%pathname%\*.tif") DO (
	convert "%%a" -write MPR:source ^
	-morphology close rectangle:6x5 ^
	-morphology erode square    MPR:source -compose Lighten -composite ^
	-morphology erode square    MPR:source -composite ^
	-morphology erode square    MPR:source -composite ^
	-morphology erode square    MPR:source -composite ^
	-morphology erode square    MPR:source -composite ^
	-morphology erode square    MPR:source -composite ^
	-morphology erode square    MPR:source -composite ^
	-morphology erode square    MPR:source -composite ^
	-morphology erode square    MPR:source -composite ^
	"..\2_Output_Image_Magick\%pathname%\%%~na.tif"
	)
