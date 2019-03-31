import sys
import re
import locale
import pdb; 

a_ARI = sys.argv[1] #durations
a1=open(list,'r')

#pqhparent_path = sys.argv[2]  # parent folder with all event folders  
#PQHLocation = sys.argv[3]  # location folder 
b_PMPAVM = sys.argv[2]
b1=open(b_PMPAVM, 'r')

z_outputfile = sys.argv[3]

a2 = a1.readlines()
zout = open(outputfile,'w')

count = 0
for idx, a_lines in a2:  
    if idx <= 6:
        zout.write(a_lines)
    if idx == 6: 
        
        b2 = b1.readlines()
        for b_lines in b2:
            zout.write(b_lines)
    if  idx >= 12:
        zout.write(a_lines)
a1.close
b1.close 
zout.close
        
    
    
             
            
