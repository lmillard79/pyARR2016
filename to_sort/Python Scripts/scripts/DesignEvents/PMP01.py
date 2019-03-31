import sys
import re
import locale
import pdb
import os
import getpass

a_ARI = sys.argv[1]
b_PMPAVM = sys.argv[2]
z_outputfile = sys.argv[3]

a1 = open(a_ARI,'r')
b1 = open(b_PMPAVM, 'r')

with open(b_PMPAVM) as bCount:
    avmCount = sum(1 for line in bCount if line.rstrip('\n'))

a2 = a1.readlines()
b2 = b1.readlines()

zout = open(z_outputfile,'w')

for idx, a_lines in enumerate(a2):  
    textlist = a_lines.split()
    if a_lines.startswith('Rain'):
        secondhalf = idx
        print (idx)
    if a_lines.startswith('Storm Duration:'):
        stormDurn = textlist[2]

dataIntl = float(stormDurn) / float(avmCount)

#print (dataIntl)


user = getpass.getuser()
print (user )


for idx, a_lines in enumerate(a2):      
    if idx == 0:
        zout.write('%s Converted to PMP by %s \n' %(a_lines.rstrip('\n'), user))
    elif idx < 6 and idx > 0:
        zout.write(a_lines)
    elif idx == 6:
        zout.write('Data Interval: %s \n' %dataIntl)
    elif idx == 7:
        for b_lines in b2:
            zout.write(b_lines)
    elif idx >= secondhalf:
        zout.write(a_lines)
 
a1.close
b1.close 
zout.close
