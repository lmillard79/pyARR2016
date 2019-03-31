import sys
import re
import locale
import pdb; 
from datetime import datetime

#pdb.set_trace()

eventlist = sys.argv[1] # "events_list.txt" --> 19310129, 19550325 etc
pqhparent_path = sys.argv[2]  # parent folder with all event folders "W:\Hydrology\pine\URBS\calibration"
PQHLocation = sys.argv[3]  # location folder "sideling"  "pqhparent_path" + \"eventlist"\"pqhlocation"\pqhlocation.ini/ .pqh etc
outputfile = sys.argv[4]  # "sideling.csv"
IWL = 'scd_cal.o' # sys.argv[5] # scd_cal.o
outfile = 'test.csv' # <><><>fix this later

f1 = open(eventlist,'r') # ini path file name
f2 = f1.readlines()
qout = open(outfile,'w')
qout.write('Event, IWL, Baseflow, \n')
qout.write(' , mAHD, m3/s \n')

catcherror = 5

for idx,f_lines in enumerate(f2):
    inipath = pqhparent_path + '\\' + f_lines[0:-1] + '\\' + PQHLocation + '\\' + IWL   # <<< FIX THIS later
    print(inipath)
    i1 = open(inipath,'r') 
    count = 0
    i2 = i1.readlines()
    print(('processing event %s ini file') %f_lines[0:-1])
    for idx,i_lines in enumerate(i2):
        if idx == 5:
            print(i_lines)
            IWL_var = i_lines[0:-1]
        if idx > 5:
            break 
            

#fout = open(outputfile,'w')