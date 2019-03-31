import sys
import re
import locale
import pdb
import os
import getpass

a_ARI = sys.argv[1]
b_PMP = sys.argv[2]
data_path= sys.argv[3]


#read files
ari_file = open( data_path + '\\Input\\' + a_ARI, 'r')
pat_file = open(b_PMP, 'r')

#find import ARI duration
fileName, fileExtension = os.path.splitext(a_ARI)
file_ext = fileExtension.strip('.')


ari_1 = ari_file.readlines()
for idx, a_line in enumerate(ari_1):
    txt = a_line.split()
    if 'Rain on Subareas' in a_line: 
        secondhalf = idx
    if 'Storm Duration' in a_line:
        duration = txt[2]

duration_line = -1
#find duration row number and number of event(10 events)
##ignore empty lines
pat_1 = [line.strip() for line in pat_file if line.strip()]
for idx, b_line in enumerate(pat_1):
    txt = b_line.split()
    if txt[0] == file_ext:
        duration_line = idx
    if (duration_line != -1 and idx == float(duration_line) + 1):
        num_event = len(txt)

print 
        
#number of timesteps for each duration
if file_ext == '24h':
    steps = 8 
elif file_ext == '36h':
    steps = 12
elif file_ext == '48h':
    steps = 16
elif file_ext == '72h':
    steps = 24
elif file_ext =='96h':
    steps = 32
elif file_ext == '120':
    steps = 40

#calculate duration
dataInt = float(duration) / float(steps)

#get user name
user = getpass.getuser()

#export file
event_count = 0
while event_count != num_event:
    #make the output directory if does not exist
    if not os.path.exists (data_path + '\\Output\\' + file_ext):
        os.makedirs(data_path + '\\Output\\' + file_ext)
        
    zout = open(data_path + '\\Output\\' + '%s\\%d_PMP_%s' %(file_ext, event_count+1, a_ARI), 'wb') 
    for idx, a_lines in enumerate(ari_1):
        if idx == 0:
            zout.write('%s Converted to PMP by %s \n' %(a_lines.rstrip('\n'), user))
        elif idx < 6 and idx > 0:
            zout.write(a_lines)
        elif idx == 6:
            zout.write('Data Interval: %s \n' %dataInt)
        elif idx == 7:
            for idx, b_lines in enumerate(pat_1):
                if (duration_line != -1 and idx > float(duration_line) + 1 and idx <= float(duration_line) + float(steps)+1) :
                    txt = b_lines.split()
                    zout.write(txt[event_count] + '\n')
        elif idx >= secondhalf:
            zout.write(a_lines)    
            
    event_count += 1
    print event_count
    


