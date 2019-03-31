echo on
REM E:\Projects\Moogerah\Tuflow\results\2013
REM File Created at: 27/02/2015 2:35:31 PM
REM File Created by: Lindsay Millard
E:
c:\python27\python.exe plotdump.py moogerah_2011_00_PO.csv plotdump.csv
echo off
pause
ping 1.1.1.1 -n 1 -w 500 > nul
