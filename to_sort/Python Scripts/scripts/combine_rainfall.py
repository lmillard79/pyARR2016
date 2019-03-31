# a script to combine pre-2011 and post-2011 daily and
# pluvio files into one file
import sys
import os

prm_file = open('parameters.txt','r')
p_file = prm_file.readlines()
for prm in p_file:
    txt = prm.split('=')