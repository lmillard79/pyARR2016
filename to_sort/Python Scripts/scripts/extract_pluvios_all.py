import sys
import os
import datetime

# clear disply
os.system('cls')

#get the inputs 
parm = open('parameters.txt','r')
parm1 = parm.readlines()
for line in parm1:
    txt = line.split('=')
    if txt[0] == 'start_date':
        start_date = txt[1].rstrip('\n')
    if txt[0] == 'finish_date':
        finish_date = txt[1].rstrip('\n')
    if txt[0] == 'pluvio_path':
        pluvio_path = txt[1].rstrip('\n')
    if txt[0] == 'raw_path':
        raw_path = txt[1].rstrip('\n')
    if txt[0] == 'output_format':
        output_format = txt[1].rstrip('\n')

#split the dates up into months and years
s_date_split = start_date.split('/')
f_date_split = finish_date.split('/')
start_d = datetime.datetime(int(s_date_split[2]),int(s_date_split[1]),int(s_date_split[0]))
finish_d = datetime.datetime(int(f_date_split[2]),int(f_date_split[1]),int(f_date_split[0]))

#Initiate log file
mylog = {}
logfile = open('log.txt','wb')
logfile.write('Data was not found between \n')
logfile.write('Start : %s\n' %(start_d.strftime("%d/%m/%Y %H:%M:%S")))
logfile.write('Finish: %s\n' %(finish_d.strftime("%d/%m/%Y %H:%M:%S")))

# print to screen 
print 'Looking through all files for data between dates:'
print 'Start : %s' %(start_d.strftime("%d/%m/%Y %H:%M:%S"))
print 'Finish: %s' %(finish_d.strftime("%d/%m/%Y %H:%M:%S"))
print ''
print 'Data will be written to *.dp files in %s format' %(output_format)
print ''

#loop through the list of files in pluvio folder
for file in os.listdir(pluvio_path):
    if file.startswith('outputFor') and file.endswith('.txt'):
        station = file[9:14]
        #print '_%s' %station
        
        # Get all District 40 and 41 pluvios. Change below if you require different
        if station.startswith('40') or station.startswith('41'):
            p_file = open(pluvio_path + '\\' + file,'r')
            p_file2 = p_file.readlines()
            p_line_count = 0
            accum_rainfall = 0
            outfile = open(station+'.dp','wb')
            # Once each file is open, search through each line to get info and identify the time and date
            for idx,line in enumerate(p_file2):
                if idx == 1:
                    station_name = line[20:].strip()
                    if output_format == 'RAW':
                        outfile.write('Station: %s\n' %(station_name))
                        outfile.write('Source: BoM Climate Information Pack: Converted to RAW by Seqwater\n')
                    if output_format == 'FEWSCSV':
                        outfile.write('Station: %s\n' %(station_name))
                        outfile.write('Source: BoM Climate Information Pack: Converted to RAW by Seqwater\n')
                        outfile.write('LocationID,Date_Time,Value,Flag\n' )
                if idx >= 2:
                    year = int(line[12:16])
                    month = int(line[16:18])
                    day = int(line[18:20]) 
                    line_date = datetime.datetime(year,month,day)
                    # only look at lines that lay within the start and finish times provided
                    #if line_date >= start_d and line_date <= finish_d:
                    myarray = {}
                    myflag = {}
                    p_line_count += 1
                    for i in range(1,240):
                        line_start = (20+(i-1)*7)
                        time_of_day = datetime.timedelta(0,0,0,0,6*i)
                        date_out = line_date + time_of_day
                        line_finish = line_start + 7
                        myarray[i] = line[line_start:line_finish]
                        mm_rainfall = 0
                        myflag[i] = ''
                        # this section handles data flags
                        # this version converts all negatives and quality codes / error flags to zero
                        # If FEWSCSV format is being used, original data Qulity code is exported to last column
                        if myarray[i] == '-8888.0':
                            myflag[i] == myarray[i]
                            myarray[i] == '-9999'
                        if myarray[i] == '-9999.0':
                            myflag[i] == myarray[i]
                            myarray[i] == '-9999' 
                        if float(myarray[i]) < 0:
                            myflag[i] = myarray[i]
                            myarray[i] = '-9999'
                        if float(myarray[i]) >= 0:
                            mm_rainfall = float(myarray[i]) * 0.1
                            accum_rainfall = accum_rainfall + mm_rainfall # note: RAW format ONLY increments if its a valid number
                        if output_format == 'RAW':
                            outfile.write('%s \t %.2f\n' %(date_out.strftime("%d/%m/%Y\t%H:%M:%S"),accum_rainfall))
                            if accum_rainfall > 2000:
                                accum_rainfall = 0 # reset back to zero similar to alert stations
                        if output_format == 'FEWSCSV':
                            outfile.write('%s,%s,%.2f,%s\n' %(station,date_out.strftime("%d/%m/%Y %H:%M:%S"),mm_rainfall,myflag[i]))
            outfile.close()
            # Print status of file extraction
            if p_line_count > 1:
                print 'File %s written: Data found' %(outfile.name)
                mylog[station] = 'True'
            if p_line_count <= 1:
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
                    
print 'Finished!'
print 'Check log file for files that were not written.'                
                        

        

