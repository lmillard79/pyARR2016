import os
import sys
# H:\\Python\\plotting\\20110102\\upper\\upper.csv

def separate(csv_file_location):
    out1 = open('rainfall.csv','w')
    out2 = open('eff_rainfall.csv','w')
    out3 = open('water_level.csv','w')
    out4 = open('flow_rates.csv','w')
    out5 = open('param.csv','w')
    print 'Now extracting %s' %(csv_file_location)
    p = open(csv_file_location,'r')
    
    for n, line in enumerate(p):
        if "Effect. Rain    " in line:
            effrain_start = int(n)
        if "River Levels" in line:
            WL_start = int(n)
        if "Flow Rates  " in line:
            Q_start = int(n)
        if "PARAMETER data" in line:
            param_start = int(n)
        
    count  = 0 
    p = open(csv_file_location,'r')
    p2 = p.readlines()

    try:
        test = WL_start
    except UnboundLocalError:
        WL_start = 100000

    if WL_start < 100000:
        for rows in p2:
            count = count + 1
            textlist = rows.split(',')
            if count == 1:
                loc_count = len(textlist[1:-1])
                out1.write('%s' %(rows))
            if count > 1 and count <= effrain_start:
                out1.write('%s' %(rows))
            if count > effrain_start and count <= WL_start:
                out1.close
                out2.write('%s' %(rows))
            if count > WL_start and count <= Q_start:
                out2.close
                out3.write('%s' %(rows))
            if count > Q_start and count <= param_start:
                out3.close
                out4.write('%s' %(rows))
            if count > param_start:
                out4.close
                out5.write('%s' %(rows))
    elif WL_start >= 100000:
        for rows in p2:
            count = count + 1
            textlist = rows.split(',')
            if count == 1:
                loc_count = len(textlist[1:-1])
                out1.write('%s' %(rows))
            if count > 1 and count <= effrain_start:
                out1.write('%s' %(rows))
            if count > effrain_start and count <= Q_start:
                out1.close
                out2.write('%s' %(rows))
            if count > Q_start and count <= param_start:
                out2.close
                out3.close
                out4.write('%s' %(rows))
            if count > param_start:
                out4.close
                out5.write('%s' %(rows))                
  
    out5.close
    p.close
    
    if WL_start < 100000:
        WL_status = 1
    elif WL_start >= 100000:
        WL_status = 0
    
    return WL_status
    
if __name__ == "__main__":
    import sys
