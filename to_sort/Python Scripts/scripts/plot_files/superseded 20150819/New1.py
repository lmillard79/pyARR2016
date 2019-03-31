#script to extract a flow from a location in an URBS CSV given the file name
import sys

input_file = sys.argv[1]

ifile = open(input_file,'r')
if2 = ifile.readlines()

for idx,x in enumerate(if2):
    if idx >= 1:
            