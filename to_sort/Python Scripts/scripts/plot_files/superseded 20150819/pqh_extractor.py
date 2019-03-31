def get_PQH_stats(pqhpath,event,catchment,location):
    
    p = open(pqhpath,'rb')
    count  = 0
    p2 = p.readlines()
    p.seek(0)
    
    # assign parameter values here in the
    # rare case when location is in header file
    # but not in PQH locations - eg L_Manchester in the
    # lower catchment
    NS_line = 1000
    NS = 0
    VR = 0
    PR = 0
    
    for n, line in enumerate(p):
        if location in line[0:16]:
            NS_line = int(n)

    p.seek(0)
    for rows in p2:
        count = count + 1
        textlist = rows.split()
        if 'MODEL PARAMETERS' in rows:
            for idx, items in enumerate(textlist):
                #print enumerate(items)
                if textlist[idx] == 'alpha=':
                    alpha = float(textlist[idx + 1])
                if textlist[idx] == 'm=':
                    m = float(textlist[idx + 1])
                if textlist[idx] == 'beta=':
                    beta = float(textlist[idx + 1])
                if textlist[idx] == 'IL=':
                    IL = float(textlist[idx + 1])
                if textlist[idx] == 'CL=':
                    CL = float(textlist[idx + 1])
            
                        
            #try:
            #    alpha = float(textlist[3])
            #    m = float(textlist[5])
            #    beta = float(textlist[7])
            #    IL = float(textlist[9])
            #    CL = float(textlist[11])
            #except IndexError:
            #    alpha = 'failed'
            #    m = 'failed'
            #    beta = 'failed'
            #    IL = 'failed'
            #    CL = 'failed'
        #if 'Location' in rows:
        #    #print textlist
        #    for inx, headings in enumerate(textlist):
        #        if textlist[inx] == 'NS':
        #            ns_index = inx + 4
        #        if textlist[inx] == 'VR':
        #            vr_index = inx + 4
        #        if textlist[inx] == 'PR':
        #            pr_index = inx + 4
        
        
        if textlist[0] == location.upper():
			#print 'something'
            #for ix, ps in enumerate(textlist):
            #    print '%s %s' %(str(ix),ps)
            try:
                NS = float(textlist[18])
            except IndexError:
                #print 'No NS value found'
                NS = 0
            try:
                VR = float(textlist[19])
            except IndexError:
                #print 'No VR value found'
                VR = 0
            try:
                PR = float(textlist[20])
            except IndexError:
                PR = 0
                #print 'No PR value found'
                    
    return alpha, beta, m, IL, CL, NS, VR, PR
    p.close