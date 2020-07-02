import re
import urllib
import string
import httplib
import requests
import httplib2

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
y=0
cnt1=0
index=0
for i in range(0,len(r1)):
    x=r1[i]
    if index>len(r1):
        break
    t=x.split(" ")
    if t[2][:-1] in n2 and temp not in t[2][:-1]: #if a website exist in the list and not in previous line then write it in another log file with new line in between
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
    elif len(t1)==2:
        temp=t1[0]
#     print temp
    index=index+1
f.close()
g.close()
print count
tempcnt=0
count2=[]
for i in range(len(count)):
    if count[i]>10:
        count2.append(count[i])
        tempcnt=count[i]
    else:
#         if count[i]<50 or len(count2)<=2:
#             tempcnt=tempcnt+count[i]
#             continue
#         else:
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
cnt1=count2[j]
for i in range(0,len(r1)):
    if j>len(count2):
        break
    x=r1[i]
    tcnt=tcnt+1
    if tcnt==1:
        t=x.split(" ")
        g.write(t[2][:-1])
        g.write("  "+str(count2[j]))
        g.write(" Time:")
        g.write(t[0]+" ")
        g.write(t[1])
        g.write("\n")
        g.write(t[2][:-1])
        g.write("\n")
        print t
    elif tcnt<=cnt1:
        t=x.split(" ")
        g.write(t[2][:-1])
        g.write("\n")
    if tcnt==cnt1:
        j=j+1
        cnt1=count2[j]
        tcnt=0

h.close()
g.close()
