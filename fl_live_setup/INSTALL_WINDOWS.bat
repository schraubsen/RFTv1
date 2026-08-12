@echo off
setlocal
set "TARGET=%USERPROFILE%\Documents\Image-Line\FL Studio\Settings\Hardware\SCHRAUBI RFT Lab Setup"
echo.
echo Installing SCHRAUBI RFT Lab Setup to:
echo %TARGET%
echo.
if not exist "%TARGET%" mkdir "%TARGET%"
copy /Y "%~dp0device_SCHRAUBI_RFT_LAB.py" "%TARGET%\device_SCHRAUBI_RFT_LAB.py" >nul
if errorlevel 1 (
  echo ERROR: Could not copy the script.
  pause
  exit /b 1
)
echo Installed successfully.
echo.
echo NEXT:
echo 1. Restart FL Studio or reload MIDI scripts.
echo 2. Options ^> MIDI Settings.
echo 3. Select "SCHRAUBI RFT Lab Setup (user)" as Controller type on your MIDI input.
echo 4. Open SCHRAUBI_RFT_SAMPLE_LAB_V3.flp.
echo.
echo The script changes ONLY a matching V3 project. It auto-names Mixer 1-32
 echo and links channels 00-23 to Mixer 1-24. Optional bus functions are manual.
echo.
pause
