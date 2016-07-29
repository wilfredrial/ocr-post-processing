::This file replaces move-it.bat if you do not use Franken+ to run tesseract
setlocal
:Start
   ::@Echo off
   set /p pathName=Enter the folder of tiffs from the Image Magick Output to the Output OCR folder:%=%
	:: @echo %pathName%
   Set _SourcePathReg=""C:\Users\William\Dropbox\OCR_2015\deliverables_OCR_2015\2_Output_Image_Magick\%pathName%\regular\*.tif""
   Set _SourcePathIta=""C:\Users\William\Dropbox\OCR_2015\deliverables_OCR_2015\2_Output_Image_Magick\%pathName%\italic\*.tif""
   Set _OutputPath=C:\Users\William\Dropbox\OCR_2015\deliverables_OCR_2015\3_Output_OCR\%pathName%\
   Set _Tesseract="C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
:Convert
   MD "..\3_Output_OCR\%pathname%\"
   For %%A in (%_SourcePathReg%) Do Echo Converting %%A...&%_Tesseract% %%A %_OutputPath%%%~nA -l scudery_lang_regular_only
   For %%A in (%_SourcePathIta%) Do Echo Converting %%A...&%_Tesseract% %%A %_OutputPath%%%~nA -l scuderyFrench001

:End   
   Set "_SourcePathReg="
   Set "_SourcePathIta="
   Set "_OutputPath="
   Set "_Tesseract="
endlocal
PAUSE