# Script to write from DNRM data to FEWSCSV or RAW file format
import datetime
import os
import re

# parameters
# start_date & finish_date=dd/mm/yyyy
# data_path= typical windows path where data is
# output_format: 'FEWSCSV' or 'RAW'
# file_ext: not used
# conversion_file: used to convert AWRC numbers to BOM numbers
# file_source: either 'internet' if files obtained form DNRM site or 'CD' if obtained from DNRM CD database


try:
    parm = open('parameters.txt','r')
except:
    print 'The PARMETER FILE does not exist! Please ensure parameter.txt file is in this directory'
    raise
parm1 = parm.readlines()
for line in parm1:
    txt = line.split('=')
    if txt[0] == 'start_date':
        start_date = txt[1].rstrip('\n')
    if txt[0] == 'finish_date':
        finish_date = txt[1].rstrip('\n')
    if txt[0] == 'data_path':
        data_path = txt[1].rstrip('\n')
    if txt[0] == 'output_format':
        output_format = txt[1].rstrip('\n')
    if txt[0] == 'file_ext':
        file_ext = txt[1].rstrip('\n')
    if txt[0] == 'conversion_file':
        conversion_file = txt[1].rstrip('\n') 
    if txt[0] == 'file_source':
        file_source = txt[1].rstrip('\n')             

#split the dates up into months and years
# this depends on where the file was sourced
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
if output_format == 'FEWSCSV':
    print 'Data will be written to *.dp files in %s format' %(output_format)
if output_format == 'RAW':
    print 'Data will be written to *.raw files in %s format' %(output_format)

print ''

# read in AWRC and bom equivalent numbers
convert = open(conversion_file,'r')
c_file = convert.readlines()
stn_array = {}
for x in c_file:
    txt = x.split(',')
    stn_array[txt[0]] = txt[1].rstrip('\n')
convert.close()

#loop through the list of files in data folder
for file in os.listdir(data_path):
    if file.endswith('.ps.txt') or file.endswith('.csv'):
        awrc_number_full = file[0:7]
        awrc_station = file[0:7]
        if output_format == 'FEWSCSV':
            try:
                bom_station = stn_array[awrc_station]
            except KeyError:
                
                try:
                    awrc_station = file[0:6]
                    bom_station = stn_array[awrc_station]
                except KeyError:
                    logfile.write('%s: Could not find BOM station number - not written\n' %(awrc_number_full))
                    mylog[awrc_station] = 'False'
                    print '%s --> XXXXXX: Not match found - not written' %(awrc_number_full)
                    continue
        
        infile = open(data_path + '\\' + file,'r')
        ifile = infile.readlines()
        if output_format == 'FEWSCSV':
            outfile = open(awrc_number_full + '_' + bom_station + '.dp','w')
            outfile.write('AWRC Station: %s\n'%awrc_number_full)
            outfile.write('BOM  Station: %s\n'%bom_station)
            outfile.write('Sourced from DNRM: March 2014\n')
            outfile.write('LocationID,Date_Time,Value,Q_code\n')
        if output_format == 'RAW':
            outfile = open(awrc_number_full + '.raw','w')
            outfile.write('AWRC Station: %s\n'%awrc_number_full)
            outfile.write('Sourced from DNRM: March 2014\n')
        line_count = 0
        for idx,i in enumerate(ifile):
            if idx > 3:
                # first strip by commas
                txt = i.split(',')
                if len(txt) < 3 and output_format == 'RAW': # this just skips the line if there arent the 3 parameters: date, value and qaulity code
                    continue
                messy_date = txt[0]
                clean_date = re.split(',|/| |:',messy_date)
                value = txt[1].strip() # remove all whitespaces and convert to float
                qual_code = txt[2] #remove any line breaks
                if file_source != 'internet':
                    day = int(clean_date[0])
                    month = int(clean_date[1])
                    year = int(clean_date[2])
                    hour = int(clean_date[3])
                    minute = int(clean_date[4])
                    second = int(clean_date[5])
                    #value = txt[1]
                    #qual_code = txt[2]
                if file_source == 'internet':
                # this is probably a more robust way to split date up than method above
                    hour = int(clean_date[0])
                    minute = int(clean_date[1])
                    second = int(clean_date[2])
                    day = int(clean_date[3])
                    month = int(clean_date[4])
                    year = int(clean_date[5])
                    #value = txt[1]
                    #qual_code =  txt[2:]
                linedate = datetime.datetime(year,month,day,hour,minute,second)
                if linedate >= start_d and linedate <= finish_d:
                    if output_format == 'FEWSCSV':
                        try:
                            outfile.write('%s,%s,%.3f,%s' %(bom_station,linedate.strftime('%d/%m/%Y %H:%M:%S'),float(value),qual_code))
                        except ValueError:
                            continue
                    if output_format == 'RAW':
                        try:
                            # if the water level is not a number then skip it
                            outfile.write('%s    %.2f    %s' %(linedate.strftime('%d/%m/%Y %H:%M:%S'),float(value),qual_code))
                        except ValueError:
                            continue
                    mylog[awrc_station] = 'True'
                    line_count += 1
        outfile.close()
        if line_count >= 1:
            if output_format == 'FEWSCSV':
                print '%s --> %s' %(awrc_number_full,bom_station)
                logfile.write('%s: Data OK\n' %(awrc_number_full))
            if output_format == 'RAW':
                print '%s --> ok' %(awrc_number_full)
                logfile.write('%s: Data OK\n' %(awrc_number_full))
        if line_count < 1:
            if output_format == 'FEWSCSV':
                print '%s --> %s: No data between dates' %(awrc_number_full,bom_station)
                logfile.write('%s: No data within dates\n' %(awrc_number_full))
            if output_format == 'RAW':
                print '%s --> No data between dates' %(awrc_number_full)
                logfile.write('%s: No data within dates\n' %(awrc_number_full))
            os.remove(outfile.name)
logfile.close()
