@echo off
:: Store the current  execution dir 
set CURRENT_DIR=%cd%
::echo %CURRENT_DIR%

:: Move to the location of the script dir
::echo %~dp0
cd %~dp0

:: Delete all the pyc files recursively
del /S *.pyc

:: Now execute the main.py
py .\src\main.py

:: Now restore the stored current dir
cd %CURRENT_DIR%
@echo on