@echo off
set /p directory=Provide executable directory (with forward slashes) : 
(
echo Windows Registry Editor Version 5.00
echo.
echo [HKEY_CLASSES_ROOT\.frctl]
echo [HKEY_CLASSES_ROOT\.frctl\shell]
echo [HKEY_CLASSES_ROOT\.frctl\shell\open]
echo [HKEY_CLASSES_ROOT\.frctl\shell\open\command]
echo @="\"%directory%/browser.exe/" \"%1\""
) > frctl.reg

set __COMPAT_LAYER=RunAsInvoker
REGEDIT.EXE /S "%~dp0\frctl.reg"