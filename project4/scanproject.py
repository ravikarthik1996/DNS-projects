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
diff={}
for i in range(0,5):
    diff[i+1]=0 # 1 is F, 2 is O, 3 is sn, 4 is sS, 5 is sV
for j in range(len(x)): #log files
    tcnt=0
    l1=0
    l2=0
    cnt={} #saving IP with port
    cnt1={}#saving port with count
    final={} #count
    q=[] #saving IP that has count more than 60
    q2=[]
    k=0
    k1=0
    tempcnt=0
    temp=0
    count=0
    f=open(x[j],'r')
    print x[j]
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
        
    print final
    for i in final: 
        for j in cnt:
            if i==j:
                if cnt[i] not in q:
                    q.append(cnt[i])  
    for u, v in final.iteritems():
        if v<1000:
            count=count+1
        if count==len(final):# F mode
            print count
            diff[1]=1
            count=0
    l=len(r1)
    for p in range(l/2,l):
        p1=r1[p].split(" ")
        if '[wscale' in p1: # O mode
            diff[2]=1
        if '[F.],' in p1: # sV mode
            diff[5]=1
        l1=0
        l2=0
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
                if len(y)==5:
                    if bool(ord(y[4][0])>=48 and ord(y[4][0])<=57)==0:
                        continue

                if int(q1[3])==1 or int(q1[3])==254 or int(q1[3])==255:
                    continue
#                 if (ord(int(q1[3]))>=0 and ord(int(q1[3])<48)) or ord(int(q1[3]))>57:
#                     continue
                if q[j]==k:
                    if diff[1]==1:# F mode
                        g.write("\t")
                        g.write("nmap -F from "+str(q[j])+ " at "+ t[0])
                        g.write("\n")
                        print diff
                        diff[1]=0
                    elif diff[2]==1: # O mode
                        g.write("\t")
                        g.write("nmap -O from "+str(q[j])+ " at "+ t[0])
                        g.write("\n")
                        print diff
                        diff[2]=0
                    elif diff[3]==1:# sn mode
                        g.write("\t")
                        g.write("nmap -sn from "+str(q[j])+ " at "+ t[0])
                        g.write("\n")
                        print diff
                        diff[3]=0
                    elif diff[4]==1:# sS mode
                        g.write("\t")
                        g.write("nmap -ss from "+str(q[j])+ " at "+ t[0])
                        g.write("\n")
                        print diff
                        diff[4]=0
                    elif diff[5]==1:# sV mode
                        g.write("\t")
                        g.write("nmap -sV from "+str(q[j])+ " at "+ t[0])
                        g.write("\n")
                        print diff
                        diff[5]=0
                    else:
                        g.write("\t")
                        g.write("scanned from "+str(q[j])+ " at "+ t[0])
                        g.write("\n")
                    break
    
    f.close()
g.close()

