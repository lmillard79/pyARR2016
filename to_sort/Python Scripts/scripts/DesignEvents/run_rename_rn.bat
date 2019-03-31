
move *.* ss\ /-y 


copy ..\..\..\rainfall\IFD\output\ari1e7.6h      ARI_PMP06h.06h 
copy ..\..\..\rainfall\IFD\output\ari1e7.9h      ARI_PMP09h.09h
copy ..\..\..\rainfall\IFD\output\ari1e7.12h     ARI_PMP12h.12h
copy ..\..\..\rainfall\IFD\output\ari1e7.18h     ARI_PMP18h.18h
copy ..\..\..\rainfall\IFD\output\ari1e7.24h     ARI_PMP24h.24h

c:\python34\python.exe PMP01.py ARI_PMP06h.06h AVM24hDistbn.txt OUT_PMP06h.06h
c:\python34\python.exe PMP01.py ARI_PMP09h.09h AVM24hDistbn.txt OUT_PMP09h.09h
c:\python34\python.exe PMP01.py ARI_PMP12h.12h AVM24hDistbn.txt OUT_PMP12h.12h
c:\python34\python.exe PMP01.py ARI_PMP18h.18h AVM24hDistbn.txt OUT_PMP18h.18h
c:\python34\python.exe PMP01.py ARI_PMP24h.24h AVM24hDistbn.txt OUT_PMP24h.24h