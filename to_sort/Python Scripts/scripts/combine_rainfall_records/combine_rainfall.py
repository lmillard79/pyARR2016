# a script to combine pre-2011 and post-2011 daily and
# pluvio files into one file
import sys
import os
import datetime

# get the parameters
prm_file = open('parameters.in','r')
p_file = prm_file.readlines()
for prm in p_file:
    txt = prm.split('=')
    if txt[0] == 'rainfall_type':
        rainfall_type = txt[1].rstrip('\n')
    if txt[0] == 'old_folder':
        old_folder = txt[1].rstrip('\n')
    if txt[0] == 'new_folder':
        new_folder =  txt[1].rstrip('\n')

log = {}
log_file = open('log.txt','w')   
log_file.write('The following stations were not found in the old folder\n')    

if rainfall_type == 'aws':
    # get a list of new files
    for file in os.listdir(new_folder):
        if 'Data' in file:
            station_long = file[11:17]
            station = file[11:17].lstrip('0')
#            if station.startswith('40') or station.startswith('41'):
            # Open files - assumes if new file exists then old file will exist
            new_file = open(new_folder + '\\' + file,'r')
            n_file = new_file.readlines()
            old_filename = file[0:26] + '6879360' + '.txt'
            try:
                old_file = open(old_folder + '\\' + old_filename,'r')
            except IOError:
                log[station] = 'False'
                continue
            out_file = open(old_filename,'w')
            o_file = old_file.readlines()
            print 'Now writing file: %s... old file' %(out_file.name)
            # write to files from the old file first up to 31 21 2010
            for idx,line in enumerate(o_file):
                txt = line.split(',')
                try:
                    year = int(txt[2])
                    month = int(txt[3])
                    day = int(txt[4])
                    hour = int(txt[5])
                    min  = int(txt[6])
                    line_date = datetime.datetime(year,month,day,hour,min)
                except:
                    line_date = datetime.datetime(1900,1,1)
                if line_date < datetime.datetime(2011,1,1):
                    out_file.write(line)
            out_file.close()
            # Open file for appending and write to file from 1 1 201
            out_file = open(old_filename,'a')
            print 'Now writing file: %s... new file' %(out_file.name)
            for ix,n in enumerate(n_file):
                if ix > 1:
                  out_file.write(n)
# get old copies that werent repeated in the new versions                        
    for file in os.listdir(new_folder):
        if 'Data' in file:
            station_long = file[11:17]
            station = file[11:17].lstrip('0')    
                


if rainfall_type == 'pluvio':
    # get a list of new files
    for file in os.listdir(new_folder):
        if file.startswith('output'):
            station = file[9:14]
#            if station.startswith('40') or station.startswith('41'):
            # Open files - assumes if new file exists then old file will exist
            new_file = open(new_folder + '\\' + file,'r')
            n_file = new_file.readlines()
            old_filename = file[0:23] + '6840853' + '.txt'
            try:
                old_file = open(old_folder + '\\' + old_filename,'r')
            except IOError:
                log[station] = 'False'
                log_file.write('%s,%s\n' %(station,log[station]))
                continue
            out_file = open(old_filename,'w')
            o_file = old_file.readlines()
            print 'Now writing file: %s... old file' %(out_file.name)
            # write to files from the old file first up to 31 21 2010
            for idx,line in enumerate(o_file):
                try:
                    year = int(line[12:16])
                    month = int(line[16:18])
                    day = int(line[18:20])
                    line_date = datetime.datetime(year,month,day)
                except:
                    line_date = datetime.datetime(1900,1,1)
                if line_date < datetime.datetime(2011,1,1):
                    out_file.write(line)
                    last = line_date
            out_file.close()
            
            # Open file for appending and write to file from 1 1 201
            out_file = open(old_filename,'a')
            print 'Now writing file: %s... new file' %(out_file.name)
            for ix,n in enumerate(n_file):
                if ix > 1:
                    out_file.write(n)
            #os.system('cls')    
    


if rainfall_type.lower() == 'daily':
    # get a list of new files
    for file in os.listdir(new_folder):
        if 'Data' in file:
            station_long = file[11:17]
            station = file[11:17].lstrip('0')
#            if station.startswith('40') or station.startswith('41'):
            # Open files - assumes if new file exists then old file will exist
            new_file = open(new_folder + '\\' + file,'r')
            n_file = new_file.readlines()
            old_filename = 'dr_' + station_long + '.txt'
            try:
                old_file = open(old_folder + '\\' + old_filename,'r')
            except IOError:
                log[station] = 'False'
                log_file.write('%s,%s\n' %(station,log[station]))
                continue
            o_file = old_file.readlines()
            out_file = open(old_filename,'w')
            print 'Now writing file: %s... old file' %(out_file.name)
            # write to files from the old file first up to 31 21 2010
            for idx,line in enumerate(o_file):
                txt = line.split(',')
                try:
                    line_date = datetime.datetime(int(txt[2]),int(txt[3]),int(txt[4]))
                except:
                    line_date = datetime.datetime(1900,1,1)
                if line_date < datetime.datetime(2011,1,1):
                    out_file.write(line)
            out_file.close()
            
            # Open file for appending and write to file from 1 1 201
            out_file = open(old_filename,'a')
            print 'Now writing file: %s... new file' %(out_file.name)
            for ix,n in enumerate(n_file):
                if ix > 0:
                    out_file.write('%sx,%s'%(n[0:-2],n[len(n)-2:]))
            #os.system('cls')

print 'The following stations were not found in the old folder:'

for i in log:
    if log[i] == 'False':
        print i                
            
                    
                
    