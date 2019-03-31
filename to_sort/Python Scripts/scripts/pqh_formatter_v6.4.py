##  File v6.0 edited by Lindsay Millard SEQWater 22 August 2014
# modification to reflect latest release of URBS and Python34 and general tidy up of file structure

import sys
import re
import locale
import pdb; 
from datetime import datetime

eventlist = sys.argv[1]
pqhparent_path = sys.argv[2]  # parent folder with all event folders  
PQHLocation = sys.argv[3]  # location folder 
outputfile = sys.argv[4]

#Call files "f1"  for concatenation "f2" is there contents
f1=open(eventlist,'r')
f2 = f1.readlines()
#file output location and formatting
fout = open(outputfile,'w')
fout.write('Event,IL,CL,Alpha,Beta,m,Location,Cal_QP,Rated_QP,Peak Ratio,Cal_Vol,Rated_Vol,Volume Ratio,Cal_HP,Rec_HP,delta H,Nash-Sutcliffe, Calibn Date,\n')
fout.write(',mm,mm/h,,,,,m3/s,m3/s,,ML,ML,,m,m,m,,,,,\n')

# For loop opening file information with header defined as larger than URBS header
# triggerline = 100000
header = 99
        
for idx,f_lines in enumerate(f2):
# test removal of intital entry file path folder in event list
    # --------------------------------------
    # removing header title from event list.
    # --------------------------------------    
    #if idx ==0:
        #pqhpath = pqhparent_path + '\\' + f_lines[0:-1] + '\\' + PQHLocation + '\\' + PQHLocation + '.pqh'
        #pqhpath_prefix = f_lines[0:-1]
    #if idx < -1:
    #pqhpath = pqhfolder + '\\' + PQHLocation + '.pqh'
    # --------------------------------------    
    pqhpath = pqhparent_path + '\\' + f_lines[0:-1] + '\\' + PQHLocation + '\\' + PQHLocation + '.pqh'
    #pdb.set_trace()
    p1 = open(pqhpath,'r')  #p path file name 
    count = 0
    p2 = p1.readlines()
    print(('Processing event %s') %f_lines)
    for p_lines in p2:
        count = count + 1
        textlist = p_lines.split()
        if "DATED " in p_lines:
            try:
               # month = textlist[3]
               # day = textlist[4]
               # time = textlist[5]
               # colon = time.split(':')
               # hour = colon[0]
               # minute = colon[1]
               # year = textlist[6]
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
            cal_P_text = "".join(textlist[4]) + ' ' + "".join(textlist[5]) + ' ' + "".join(textlist[6]) + ' ' + "".join(textlist[7]) + ' ' + "".join(textlist[8])
            cal_P = datetime.strptime(cal_P_text,'%a %b %d %Y %H:%M')
            fout.write('%s,%s,%s,%s,%s,%s,%s,' %(f_lines[0:-1],location,IL,CL,alpha,beta,m))
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
       
    
f1.close
p1.close

