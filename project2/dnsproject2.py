import re
import urllib
import string
import httplib
import requests
import httplib2
from datetime import datetime
from dateutil.relativedelta import relativedelta

count1=0
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
                count1=count1+1
n1=[]
n=[]
a=""
l=0
t=[]
s1=""
s2=""
f=open("dnslog1.txt","r")
g=open("dnslog2.txt","w")
s=f.readlines()
for i in range(len(s)):
    t.append(s[i].split(" "))
i=0
k=0
for i in range(0,count1):  
    if i==0:
        a=s[i].split(" ") # store first line of file
        i=i+1
        t1=s[i].strip().split(" ")
        if "www." in s[i] or len(t1[2][:-1].split("."))==2: #get websites having length 2 or website starting with www.
            n1.append(t1[2][:-1])
        continue

    t1=s[i].strip().split(" ")
    if "www." in s[i] or len(t1[2][:-1].split("."))==2: #get websites having length 2 or website starting with www.
        n1.append(t1[2][:-1])
    if i>len(s):
        break
    FMT = '%H:%M:%S.%f'
    s1=t[i-1][1]
    s2=t[i][1]
    tdiff = relativedelta(datetime.strptime(s1+'', FMT),datetime.strptime(s2+'', FMT))
    if tdiff.hours<0:
        tdiff.hours=tdiff.hours*-1
    if tdiff.minutes<0:
        tdiff.minutes=tdiff.minutes*-1
    if tdiff.seconds<0:
        tdiff.seconds=tdiff.seconds*-1
    if tdiff.microseconds<0:
        tdiff.microseconds=tdiff.microseconds*-1
    if tdiff.hours<=1:
#         g.write(s[l])
        if tdiff.minutes<2:
#             g.write(s[l])
            if tdiff.seconds<5:
                g.write(s[i-1])
                k=k+1
                if i==len(s):
                    g.write(s[i])
                    g.write("\n")
            elif k>=10:
                g.write(s[i-1])
#                 g.write("\n")
#                 g.write(s[i])
                if i==count1:
                    g.write(s[i])
                    print i
                k=0
            elif k<10:
                g.write(s[i-1])
                g.write("\n")
                if i==count1:
                    g.write(s[i])
                    print i
#                 g.write(s[i])
                k=0
        else:
            g.write(s[i-1])
            g.write("\n")
            if i==count1:
                g.write(s[i])
                print i
#             g.write(s[i])
    else:
        g.write(s[i-1])
        g.write("\n")
#         g.write(s[i])
f.close()
g.close()
n1=list(dict.fromkeys(n1)) #remove duplicates of websites in n1 list
# for i in range(len(n1)):
#     if '-' in n1[i]:#[2][:-1]: #remove website names that contain '-' 
#         continue   
#     url='http://'+n1[i]#[2][:-1]
#     try:
#         resp=requests.get(url)
#     except requests.exceptions.RequestException as e:  # This is the correct syntax
#         print e
#     if resp.status_code< 400:  #check whether a particular website exist or not. If exist store in a list.
# #         print n[i]
# #         print r.status_code
#         n.append(n1[i])#[2][:-1])
# print n
f=open("dnslog2.txt","r")
g=open("report.txt","w")
r1=f.readlines()
count=[]
count2=[]
cnt=0
tr=[]
j=0
for i in range(len(r1)):
    tr.append(r1[i].split(" "))
    if r1[i]=="\n":
        count.append(cnt)
        cnt=0
    else:
        cnt=cnt+1
tempcnt=0
for i in range(len(count)):
    if count[i]>10:
        count2.append(count[i])
        tempcnt=count[i]
    else:
        count2.pop(-1)
        count2.append(tempcnt+count[i])
        tempcnt=tempcnt+count[i]

print count
print count2
j=0
cnt1=0
l=0
k=0
for i in range(0,len(tr)):
    if i==len(tr):
        break
    if j>=len(count2):
        break
    if cnt1==0:
        cnt1=count2[j]
    if cnt1==count2[j] and cnt1>0:
        g.write(str(t[i][2][:-1]))
        g.write("  "+str(count2[j]))
        g.write(" Time:")
        g.write(t[i][0]+" ")
        g.write(t[i][1])
        g.write("\n")
        g.write(t[i][2][:-1])
        g.write("\n")
        cnt1=cnt1-1
    elif cnt1<count2[j] and cnt1>0:
        g.write(str(t[i][2][:-1]))
        g.write("\n")
        cnt1=cnt1-1
        if cnt1==0:
            j=j+1
            g.write("\n")
    
f.close()
g.close()