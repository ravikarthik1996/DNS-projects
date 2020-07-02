import glob

x1=[]
x2=[]
x = glob.glob("*.log")
for i in range(0,len(x)): #getting log files
    if 'network' in x[i]:
        x1.append(x[i])
    else:
        x2.append(x[i])
x=x1+x2
g=open('result.txt','w')

for j in range(len(x)): #log files
    tcnt=0
    cnt={} #saving IP with port
    cnt1={}#saving port with count
    final={} #count
    q=[] #saving IP that has count more than 60
    q2=[]
    k=0
    k1=0
    tempcnt=0
    temp=0
    f=open(x[j],'r')
#     print x[j]
    r1=f.readlines()
    g.write("\n")
    g.write(x[j])
    g.write("\n")
    for i in range(len(r1)): 
        t=r1[i].split(" ")
        if 'IP' in t and ('NXDomain' not in t or 'ack' not in t): #checking only IP packets
            ip=t.index('IP')
            ip1=t.index('>')
            y=t[ip+1].split(".")
            y1=t[ip1+1].split(".")
            k=y[0]+"."+y[1]+"."+y[2]+"."+y[3]
            k1=y1[0]+"."+y1[1]+"."+y1[2]+"."+y1[3]
            if y[3]==1 or y[3]==254 or y[3]==255:
                continue
            if len(y)==5:
                if k not in cnt and (ord(y[4][0])>=48 and ord(y[4][0])<=57):
                    cnt[y[4]]=k
                    cnt1[y[4]]=tempcnt
                
    for i in range(len(r1)):
        t=r1[i].split(" ")
        if 'IP' in t and ('NXDomain' not in t or 'ack' not in t):
            ip=t.index('IP')
            ip1=t.index('>')
            y=t[ip+1].split(".")
            y1=t[ip1+1].split(".")
            k=y[0]+"."+y[1]+"."+y[2]+"."+y[3]
            k1=y1[0]+"."+y1[1]+"."+y1[2]+"."+y1[3]
            if y[3]==1 or y[3]==254 or y[3]==255:
                continue
            if len(y)==5:
                if y[4] in cnt and (ord(y[4][0])>=48 and ord(y[4][0])<=57):
                    tcnt=tcnt+1
                    tempcnt=cnt1[y[4]]
                    cnt1[y[4]]=tcnt+tempcnt
                    tcnt=0
#     print cnt
    for i in cnt1: 
        if cnt1[i]>60: #save count more than 60
            final[i]=cnt1[i]
        
#     print final
    for i in final: 
        for j in cnt:
            if i==j:
                if cnt[i] not in q:
                    q.append(cnt[i])  
    
    for j in range(len(q)):  
        for i in range(len(r1)):
            t=r1[i].split(" ")
            if 'IP' in t and ('NXDomain' not in t or 'ack' not in t):
                ip=t.index('IP')
                ip1=t.index('>')
                y=t[ip+1].split(".")
                y1=t[ip1+1].split(".")
                k=y[0]+"."+y[1]+"."+y[2]+"."+y[3]
                q1=q[j].split(".")
                if int(q1[3])==1 or int(q1[3])==254 or int(q1[3])==255:
                    continue
                if q[j]==k:
                    g.write("\t")
                    g.write("scanned from "+str(q[j])+ " at "+ t[0])
                    g.write("\n")
                    break
    
    f.close()
g.close()

