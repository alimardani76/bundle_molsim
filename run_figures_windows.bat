@echo off
setlocal
cd /d "%~dp0"
echo Rebuilding final results and figures from the reconciled scientific sources...
python scripts\make_figures.py
if errorlevel 1 (echo FIGURE REBUILD FAILED & exit /b 1)
python scripts\verify_package.py --prepare-checksums
if errorlevel 1 (echo PACKAGE VERIFICATION FAILED & exit /b 1)
python scripts\write_checksums.py
if errorlevel 1 (echo CHECKSUM WRITE FAILED & exit /b 1)
python scripts\check_checksums.py
if errorlevel 1 (echo CHECKSUM VERIFICATION FAILED & exit /b 1)
echo Complete. See figures\ and quality_control\.
exit /b 0
