import os
import sys
import datetime

#get the inputs 
parm = open('parameters.txt','r')
parm1 = parm.readlines()
for line in parm1:
    txt = line.split('=')
    if txt[0] == 'start_date':
        start_date = txt[1].rstrip('\n')
    if txt[0] == 'finish_date':
        finish_date = txt[1].rstrip('\n')
    if txt[0] == 'daily_path':
        daily_path = txt[1].rstrip('\n')
    if txt[0] == 'raw_path':
        raw_path = txt[1].rstrip('\n')
    if txt[0] == 'output_format':
        output_format = txt[1].rstrip('\n')

#split the dates up into months and years
s_date_split = start_date.split('/')
f_date_split = finish_date.split('/')
start_d = datetime.datetime(int(s_date_split[2]),int(s_date_split[1]),int(s_date_split[0]))
finish_d = datetime.datetime(int(f_date_split[2]),int(f_date_split[1]),int(f_date_split[0]),9)

#Initiate log file
mylog = {}
logfile = open('log.txt','wb')
logfile.write('Data was not found between \n')
logfile.write('Start : %s\n' %(start_d.strftime("%d/%m/%Y %H:%M:%S")))
logfile.write('Finish: %s\n' %(finish_d.strftime("%d/%m/%Y %H:%M:%S")))

# write output file header


# print to screen 
print 'Looking through all files for data between dates:'
print 'Start : %s' %(start_d.strftime("%d/%m/%Y %H:%M:%S"))
print 'Finish: %s' %(finish_d.strftime("%d/%m/%Y %H:%M:%S"))
print ''
print 'Data will be written to *.dp files in %s format' %(output_format)
print ''


for file in os.listdir(daily_path):
    if file.endswith(".txt"):
        infile = open(daily_path + '\\' + file,'rb')
        ifile = infile.readlines()
        station = file[3:9].lstrip('0')
        if output_format == 'RAW':
            outfile = open(station + '.raw','wb')
            outfile.write('Station: %s\n' %(station))
            outfile.write('Source: BoM Climate Information Pack: Converted to RAW by Seqwater\n')
        if output_format == 'FEWSCSV':
            outfile = open(station + '.dp','wb')
            outfile.write('Station # ' + file[0:6] + ' Rain Gauge millimetres\n')
            outfile.write('Source: BoM Climate Information Pack: Converted to FEWSCSV by Seqwater\n')
            outfile.write('LocationID,Date_time,rainfall,quality,accum_rain_day,accum_duration,type\n')
        
        accum_rainfall = 0.0
        count = 0
        rainfall = 0.0
        for idx,line in enumerate(ifile):
            if idx > 0 and idx < len(ifile)-1:
                txt = line.split(',')
                line_date = datetime.datetime(int(txt[2]),int(txt[3]),int(txt[4]),9)
                
                if line_date >= start_d and line_date <= finish_d:
                    try:
                        rainfall = float(txt[5])
                        accum_rainfall += rainfall
                    except ValueError:
                        rainfall = -999
                    quality = txt[6] 
                    accum_rain_day = txt[7]
                    accum_duration = txt[8]
                    type = txt[9]
                    if output_format == 'FEWSCSV':
                        outfile.write('%s,%s,%.2f,%s,%s,%s,%s\n' %(station,line_date.strftime("%d/%m/%Y %H:%M:%S"),rainfall,quality,accum_rain_day,accum_duration,type))
                        count = count + 1
                    if output_format == 'RAW':
                        outfile.write('%s  %.2f,  %s,%s,%s,%s\n' %(line_date.strftime("%d/%m/%Y %H:%M:%S"),accum_rainfall,quality,accum_rain_day,accum_duration,type))
                        #outfile.write('%s  %.2f\n' %(line_date.strftime("%d/%m/%Y %H:%M:%S"),accum_rainfall))
                        count = count + 1
        outfile.close()
        # Print status of file extraction
        if count > 1:
            print 'File %s written: Data found' %(outfile.name)
            mylog[station] = 'True'
        if count <= 1:
            print 'File %s not written: No data found start and finish dates' %(outfile.name)
            os.remove(outfile.name)
            mylog[station] = 'False'
            logfile.write('%s\n' %(station))

print ''
print 'The following files were not written:'
for x in mylog:
    if mylog[x] == 'False':
        print x

logfile.close()
                
                
            
        
        