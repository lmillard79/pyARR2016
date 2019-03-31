path="c:\python27"
rem Batch file to generate images of calibration plots

rem Remove old plots
del *.png

rem Input files

rem events_list.txt
rem 1st line path of model calibration
rem subsequent lines event labels

rem catchments.txt
rem list of models one per line
rem last line must be blank

python.exe plot_all_events.py events.txt catchments.txt

pause