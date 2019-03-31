import sys
import dbf
import os

file_loc = sys.argv[1] # location where all data files are kept
dbf_file = sys.argv[2] # the DBF file that will be modified

# Declare and define all objects and variables
table = dbf.Table(dbf_file)
table.open()
record_count = 0
stn_list = {}
file_count = 0
log_file = open('log.txt','w')

# Get a list of data files
for idx,filename in enumerate(os.listdir(file_loc)):
    if filename.endswith('.dp'):
        file_count += 1
        station = filename[8:-3]
        stn_list[station] = 'False'
        print 'Now processing %s of about %s' %(idx,len(os.listdir(file_loc)))
        print 'Searching for %s' %station
        for idx,record in enumerate(dbf.Process(table)):
            if str(station) == str(record.bom).strip():
                record.priority = '1'
                record_count += 1
                stn_list[station] = 'True'
    if stn_list[station] == 'True':
        print 'Searching for %s... FOUND!' %station
    if stn_list[station] == 'False':
        print 'Searching for %s... NOT FOUND!' %station
    os.system('cls')
table.close()
print 'Done. %s out of %s stations written to DBF file' %(record_count,file_count)

print 'Stations that failed to write to DBF are:'
for x in stn_list:
    if stn_list[x] == 'False':
        print 'Station: %s' %(x)
        log_file.write('failed to write %s to DBF file\n' %x)
print 'Done! Check log file for list of files not written'
log_file.close()