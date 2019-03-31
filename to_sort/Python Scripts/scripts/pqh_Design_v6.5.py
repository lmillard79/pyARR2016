##  File v6.0 edited by Lindsay Millard SEQWater 22 August 2014
# modification to reflect latest release of URBS and Python34 and general tidy up of file structure
# v6.5 adds extraction of starting water level 

import sys
import os
import re
import locale
import pdb; 
from datetime import datetime

#eventlist = sys.argv[1] # "events_list.txt" --> 19310129, 19550325 etc
pqhparent_path = sys.argv[1]  # Where the results are saved "W:\Hydrology\pine\URBS\calibration\test\"
PQHLocation = sys.argv[2]  # Design_Event m53h.pqh 
outputfile = sys.argv[3]  # "sideling_DesignURBS.csv"
##IWL = 'scd_cal.o' # sys.argv[5] # scd_cal.o

#f1 = open(eventlist,'r') # ini path file name
#f2 = f1.readlines()

#file output location and formatting
fout = open(outputfile,'w')  #sideling.csv
fout.write('Location,IL,CL,Alpha,Beta,m,Cal_QP,Rated_QP,Peak Ratio,Cal_Vol,Rated_Vol,Volume Ratio,Cal_HP,Rec_HP,delta H,Nash-Sutcliffe, Calibn Date,\n')
fout.write(', ,mm,mm/h,,,,m3/s,m3/s,,ML,ML,,m,m,m,,,,,\n')

header = 9

#for idxf,f_lines in enumerate(f2):   #eventlist dates (f_lines)
        
#for idxi,i_lines in enumerate(i2):
    # if idxi == 5:
        # IWL_var = i_lines[0:-1]
        # break
    
pqhpath = pqhparent_path + '\\' + PQHLocation + '.pqh'
p1 = open(pqhpath,'r')  #p path file name 
count = 0
p2 = p1.readlines()
 
print(('Processing %s event     ') %(pqhpath))
for p_lines in p2:
    count = count + 1
    textlist = p_lines.split()
    if "DATED " in p_lines:
        try:
            mydate = p_lines[10:-1]
            calibn_date = datetime.strptime(mydate, '%a %b %d %H:%M:%S %Y')
        except IndexError:
            month = ' '
            day = ' '
            year = ' ' 
    if "alpha=" in p_lines:
        try:
            alpha = textlist[3]
            m = textlist[5]
            beta = textlist[7]
            IL = textlist[9]
            CL = textlist[11]
        except IndexError:
            alpha = ''
            m = ''
            beta = ''
            IL = ''
            CL = ''
    if "Location" in textlist[0]:
        header = count
        continue 
    if count > header:
        location = textlist[0]
        cal_Q = textlist[1]
        cal_V = textlist[2]
        cal_H = textlist[3]
        # cal_P_text = "".join(textlist[4]) + ' ' + "".join(textlist[5]) + ' ' + "".join(textlist[6]) + ' ' + "".join(textlist[7]) + ' ' + "".join(textlist[8])
        # cal_P = datetime.strptime(cal_P_text,'%a %b %d %Y %H:%M')
        fout.write('%s,%s,%s,%s,%s,%s,' %(location,IL,CL,alpha,beta,m))
        try:
            rec_Q = textlist[10]
            rec_V = textlist[11]
            rec_H = textlist[12]
            rec_P_text = "".join(textlist[13]) + ' ' + "".join(textlist[14]) + ' ' + "".join(textlist[15]) + ' ' + "".join(textlist[16]) + ' ' + "".join(textlist[17])
            rec_P = datetime.strptime(rec_P_text,'%a %b %d %Y %H:%M')
            NS = textlist[18]
            VR = textlist[19]
            PR = textlist[20]
            if cal_H != 'N/A' and rec_H != 'N/A':
                deltaH = float(rec_H) - float(cal_H)
                dH = str(deltaH)
            elif cal_H == 'N/A' or rec_H == 'N/A':
                dH = ''
        except IndexError:
            rec_Q = ''
            rec_V = ''
            rec_H = ''
            rec_P = ''
            NS = ''
            VR = ''
            PR = ''
            dH = ''
        myformatdate = calibn_date.strftime('%d/%b/%Y %H:%M')
        fout.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\n' %(cal_Q,rec_Q,PR,cal_V,rec_V,VR,cal_H,rec_H,dH,NS,myformatdate,))
    
p1.close

