import re
import urllib
import string
import httplib
import requests
import httplib2
from datetime import datetime
from dateutil.relativedelta import relativedelta

with open("dnslog.txt", "r") as f:
    with open("dnslog1.txt","w") as g: 
        for x in f.readlines():
            if "AAAA" not in x:     #remove IPv6 address
#                 g.write(x[0:27])
#                 g.write(x[65:-5])
#                 g.write("\n")
                g.write(x[0:24])
                g.write(x[62:-5])
                g.write("\n")
n1=[]
n=[]
a=""
with open("dnslog1.txt","r") as f:
    s=f.readlines()
    i=0
    for x in s:
        if i==0:
            a=x.split(" ") # store first line of file
            i=i+1
        t=x.strip().split(" ")
        if "www." in x or len(t[2][:-1].split("."))==2: #get websites having length 2 or website starting with www.
            n1.append(t)
            
for i in range(len(n1)):
    n.append(n1[i][2][:-1])
n=list(dict.fromkeys(n)) #remove duplicates of websites in n1 list
print n
n2=[]
for i in range(0,len(n)):
    if '-' in n[i]: #remove website names that contain '-' 
        continue   
    url='http://'+n[i]
    try:
        resp=requests.get(url)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print e
    if resp.status_code< 400:  #check whether a particular website exist or not. If exist store in a list.
#         print n[i]
#         print r.status_code
        n2.append(n[i])
print n2
count=[] #count number of times a domain name queries
f=open("dnslog1.txt","r")
g=open("dnslog2.txt","w")
r1=f.readlines()
temp=""
temp1=""
y=0
cnt1=0
index=0
for i in range(0,len(r1)):
    if i==0:
        x1=r1[i]
        t1=x1.split(" ")
        temp=t1[2][:-1]
        temp1=t1[1]
        cnt1=cnt1+1
#         t1=t[2][:-1].split(".")
#         if len(t1)==3:
#             temp=t1[1]
#         elif len(t1)==2:
#             temp=t1[0]
        continue
    if index>len(r1):
        break
    if i>len(r1):
        break
    x=r1[i]
    t=x.split(" ")
    FMT = '%H:%M:%S.%f'
    tdiff = relativedelta(datetime.strptime(t[1], FMT),datetime.strptime(temp1, FMT))
    if tdiff.hours<0:
        tdiff.hours=tdiff.hours*-1
    if tdiff.minutes<0:
        tdiff.minutes=tdiff.minutes*-1
    if tdiff.seconds<0:
        tdiff.seconds=tdiff.seconds*-1
    if tdiff.microseconds<0:
        tdiff.microseconds=tdiff.microseconds*-1
    if t[2][:-1] in n2 and temp not in t[2][:-1] and (tdiff.minutes>=2 and tdiff.seconds<5) or (tdiff.minutes<=1 and tdiff.seconds>=5): #if a website exist in the list and not in previous line then write it in another log file with new line in between
        count.insert(y,cnt1)
        if count[y]<=7:
            cnt1=cnt1+1
            g.write(temp)
            g.write("\n")
            continue
        y=y+1
        g.write("\n")
        g.write(x[:])
        cnt1=0
        cnt1=cnt1+1
    else: #if website name matches, just write the line
        cnt1=cnt1+1
        g.write(t[2][:-1])
        g.write("\n")
    if index==len(r1)-1:
        count.insert(y,cnt1)
    t1=t[2][:-1].split(".")
    if len(t1)==3:
        temp=t1[1]
        temp1=t[1]
    elif len(t1)==2:
        temp=t1[0]
        temp1=t[1]
#     print temp
    index=index+1
    if i+1>=len(r1):
        break

f.close()
g.close()
print count
tx1=[]
f=open("dnslog2.txt","r")
r2=f.readlines()
for i in range(len(r2)):
    x=r2[i]
    tx=x.split(" ")
    if len(tx)==3:
        tx1.append(tx)
f.close()
print tx1
tempcnt=0
count2=[]
for i in range(len(count)):
    if count[i]>=10:
        count2.append(count[i])
        tempcnt=count[i]
    else:
        count2.pop(-1)
        count2.append(tempcnt+count[i])
        tempcnt=tempcnt+count[i]

print count2
h=open("dnslog1.txt","r")
g=open("report.txt","w")
r1=h.readlines()
j=0
cnt1=0
tcnt=0
tempcnt1=0
cnt1=count2[j]
for i in range(0,len(r1)):
    if j>len(count2):
        break
    x=r1[i]
    t=x.split(" ")
    if t[2][:-1] in n2 and tcnt==0:
        g.write("\n")
    tcnt=tcnt+1
    if tcnt==1 and t[2][:-1] in n2:
        g.write(t[2][:-1])
        g.write("  "+str(count2[j]+tempcnt1))
        g.write(" Time:")
        g.write(t[0]+" ")
        g.write(t[1])
        g.write("\n")
        g.write(t[2][:-1])
        g.write("\n")
        print t
#     elif tcnt==1 and t[2][:-1] not in n2:
#         g.write(t[2][:-1])
#         g.write("\n")
#         tempcnt1=count2[j]
    elif tcnt<=cnt1:
        g.write(t[2][:-1])
        g.write("\n")
    if tcnt==cnt1:
        j=j+1
        cnt1=count2[j]
#         g.write("\n")
        tcnt=0

h.close()
g.close()


# i=0
# h=open("dnslog2.txt","r")
# g=open("report.txt","w")
# r1=h.readlines()
# k=0
# j=0
# t1=[]
# for l in range(0,len(r1)):
#     x=r1[l]
#     if k>=len(r1): #to prevent index out of range
#         break
#     if x=="\n": #to check the line is empty
#         i=-1
#         continue
#     if i==0: #condition works at the start of line.write data into report.txt 
#         t=x.split("\n")
#         g.write(t[0])
#         g.write("  "+str(count[j]))
#         g.write(" Time:")
#         g.write(a[0]+" ")
#         g.write(a[1])
# #         g.write(t[0])
#         i=i+1
#         s1=a[0]
#         g.write("\n")
#         g.write(x[:])
#     elif i<0: #condition works when new line is present in before line ie when next domain name is found.writes data into report.txt
#         if j>=len(count):
#             break    
#         j=j+1
#         t=x.split(" ")
#         t1.append(t)
#         if k>=len(t1):
#             break
#         print t1[k]
#         if k==0:
#             print "k=0"
#             FMT = '%H:%M:%S.%f'
#             tdiff = relativedelta(datetime.strptime(a[0], FMT),datetime.strptime(t[1], FMT))
#             print tdiff
#             k=k+1
#         elif k!=0:
#             print "k"
#             FMT = '%H:%M:%S.%f'
#             tdiff = relativedelta(datetime.strptime(t1[k-1][1], FMT),datetime.strptime(t[1], FMT))
#             print tdiff
#             k=k+1
#         if tdiff.hours<0:
#             tdiff.hours=tdiff.hours*-1
#         if tdiff.minutes<0:
#             tdiff.minutes=tdiff.minutes*-1
#         if tdiff.seconds<0:
#             tdiff.seconds=tdiff.seconds*-1
#         if tdiff.microseconds<0:
#             tdiff.microseconds=tdiff.microseconds*-1
#         if tdiff.hours==0:
#             if tdiff.minutes>1:
#                 if tdiff.seconds>=5:
#                     g.write("\n")
#                     g.write(str(t[2])+"  "+str(count[j]))
#                     g.write(" Time:")
#                     g.write(x[:24])
#                     g.write("\n")
#                     g.write(str(t[2]))
#                     g.write("\n")
#                 print t
#         elif tdiff.seconds<5 | tdiff.minute>1:
#             g.write("\n")
#             g.write(str(t[2]))
#         i=1
#     else: #this happens when there is no new line or it is not the start of line
#         g.write(x[:])
        
#     k=k+1
# h.close()
# g.close()


