import sys
import dbf
import os

# get parameters from file
parameter_file = open('parameters.txt','r')
prms = parameter_file.readlines()
for line in prms:
    txt = line.split('=')
    if txt[0] == 'pluvio_folder':
        pluvio_folder = txt[1].rstrip('\n')
    if txt[0] == 'daily_folder':
        daily_folder = txt[1].rstrip('\n')
    if txt[0] == 'dbf_file':
        dbf_file = txt[1].rstrip('\n')
parameter_file.close()

table = dbf.Table(dbf_file)
table.open()
record_count = 0
stn_list = {}
pluvio_list = {}
daily_list = {}

for file in os.listdir(pluvio_folder):
    if file.endswith('.dp'):
        station = file.lstrip('0').rstrip('.dp')
        pluvio_list[station] = 'ALERT'
print len(pluvio_list)
for file in os.listdir(daily_folder):
    if file.endswith('.dp'):
        station = file.lstrip('0').rstrip('.dp')
        daily_list[station] = 'Daily'

# merge both lists with priority on pluvio if clashes exist 
daily_list.update(pluvio_list)
log = {}
# loop through available rainfall files and update DBF as required
for idx,stat in enumerate(daily_list):
    log[stat] = 'False'
    print 'Now processing %s of %s' %(idx,len(daily_list))
    print 'Searching for %s' %stat
    for idx,record in enumerate(dbf.Process(table)):
        if stat == str(record.num):
            record.priority = '1'
            record.comms = daily_list[stat]
            record_count += 1
            log[stat] = 'True'
            print 'Searching for %s: Type = %s... FOUND!' %(stat,daily_list[stat])
    os.system('cls')
table.close()
print 'Done. %s out of %s stations written to DBF file' %(record_count,len(daily_list) )

print 'Stations that failed to write to DBF are:'
for x in log:
    if log[x] == 'False':
        print 'Station: %s' %(x)
print 'Done!'         