:: Use this if you use Franken+ to run tesseract
:: This batch should be used after Tesseract has examined the tiff images and created corresponding text files
:: Moves all text files in the chosen folder from 2 Output Image Magick to 3 Output OCR
:: For example, enter:  Vol1

set /p pathName=Enter the folder of tiffs from the Image Magick Output to the Output OCR folder:%=%
:: @echo %pathName%
MD "..\3_Output_OCR\%pathname%\"
MOVE /-y "..\2_Output_Image_Magick\%pathname%\*.txt" "..\3_Output_OCR\%pathname%\"

MOVE /-y "..\2_Output_Image_Magick\italic\%pathname%\*.txt" "..\3_Output_OCR\%pathname%\"
MOVE /-y "..\2_Output_Image_Magick\regular\%pathname%\*.txt" "..\3_Output_OCR\%pathname%\"

PAUSE