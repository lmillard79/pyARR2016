cd %~dp0


c:\python27\python.exe WL_harvester.py WL_station_list.txt

@echo off

rem for /F %%i in (WL_station_list.txt) DO move %%i.csv .\bomriver\
rem pause