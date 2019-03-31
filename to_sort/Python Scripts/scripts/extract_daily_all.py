import os
import sys
import datetime

#get the inputs 
start_date = sys.argv[1]
finish_date = sys.argv[2] 
path = 'W:\Hydrology\hydrometricdata\Climate Data Pack\Complete_Daily'

#split the dates up into months and years
s_date_split = start_date.split('/')
f_date_split = finish_date.split('/')
s_date = datetime.datetime(int(s_date_split[2]),int(s_date_split[1]),int(s_date_split[0]))
f_date = datetime.datetime(int(f_date_split[2]),int(f_date_split[1]),int(f_date_split[0]))

logfile = open('log.txt','w')

for file in os.listdir(path):
    
    if file.endswith(".txt"):
    #if file == "040000.txt":
        infile = open(path + '\\' + file,'rb')
        ifile = infile.readlines()
        outfile = open(file[3:9].lstrip('0')+'.dp','wb')
        outfile.write('Station # ' + file[0:6] + ' Rain Gauge millimetres\n')
        outfile.write('Source: BoM Climate Information Pack: Converted to RAW by Seqwater\n')
        outfile.write('LocationID,Date_time,rainfall,quality,accum_rain_day,accum_duration,type')
        accum_rainfall = 0.0
        count = 0
        for idx,line in enumerate(ifile):
            if idx > 0 and idx < len(ifile)-1:
                txt = line.split(',')
                line_date = datetime.datetime(int(txt[2]),int(txt[3]),int(txt[4]),9)
                #print idx,len(ifile) , line
                try:
                    rainfall = float(txt[5])
                except ValueError:
                    rainfall = -999
                quality = txt[6] 
                accum_rain_day = txt[7]
                accum_duration = txt[8]
                type = txt[9]
                #if line_date >= s_date and line_date <= f_date:
                if line_date > datetime.datetime(1900,1,1):
                    outfile.write('%s,%s,%.2f,%s,%s,%s,%s\n' %(file[3:9].lstrip('0'),line_date.strftime("%d/%m/%Y %H:%M:%S"),rainfall,quality,accum_rain_day,accum_duration,type))
                    count = count + 1
        outfile.close()
        if count > 0:
            print '%s: data found' %(file)
            logfile.write('%s: data found\n' %(file))            
        if count == 0:
            print '%s: no valid data found' %(file)
            logfile.write('%s: no valid data found\n' %(file))
            os.remove(outfile.name)   
                
                
            
        
        