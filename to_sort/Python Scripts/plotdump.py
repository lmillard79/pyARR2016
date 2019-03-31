import sys, os

input = sys.argv[1] 
output = sys.argv[2] 

f1 = open(input,"r")
f2 = f1.readlines()
f1.close

out = open(output,"w")

for i,x in enumerate(f2):
	if i != 1 or i != 2: 
		out.write(x)

out.close

	
