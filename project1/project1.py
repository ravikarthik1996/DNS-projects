from collections import Counter
from collections import OrderedDict
from itertools import combinations
import csv
import string
import math

f=open("text.txt","r")
g=open("sample.txt","w+")
f1=f.readlines()
for x in f1:
    x= x.rstrip(" ")
    x=x.replace("-"," ")
    z=x.translate(None,string.punctuation) #Remove punctuations
    z=z.lower()  #Lower the letters
    g.write(z)  #Save it in the file sample.txt 
f.close()
g.close()

nwords=0
s=0.000
t=[]
q={}
with open("sample.txt") as h:
    q = Counter(h.read().split()).most_common() #counting frequency of each word
for i in range(len(q)):
    s=s+q[i][1]     #calculating total number of words
q=dict((x, y) for x,y in q ) #converting tuples to dictionary
d = OrderedDict(sorted(q.items(), key=lambda x: x[1],reverse=True))#sorting the dictionary
    
with open("result.csv","wb") as j: #creating a csv file
    fnames=['Word','Occurrence','Percentage']
    w = csv.DictWriter(j, fieldnames=fnames)
    w.writeheader()
    
    for i in d:
        w.writerow({'Word':i, 'Occurrence':d[i], 'Percentage':(d[i]/s)}) # writing the words,occurences and percentage

f= open('text.txt', 'r')
lines=list (f)
file=f.read()
cnt=0
cnt1=0
for i in lines:
    cnt=cnt+len(i.split('.'))-1 #count number of sentences that end with '.'
    cnt=cnt+len(i.split("!"))-1 #count number of sentences that end with '!'
    cnt=cnt+len(i.split("?"))-1 #count number of sentences that end with '?'
    cnt1=cnt1+len(i.split(". The"))-1 #count number of sentences that end with '. The'
    cnt1=cnt1+len(i.split("! The"))-1 #count number of sentences that end with '! The'
    cnt1=cnt1+len(i.split("? The"))-1 #count number of sentences that end with '? The'
f.close()

a=[]
with open("text.txt") as f:
    line=f.readlines()
    i=0
    for x in line:        
        x= x.rstrip(" ")
        x=x.replace("-"," ")
        z=x.translate(None,"!@#$%^&*()_+={}[]|\:;'<?/,") #Remove punctuations
        a.insert(i,z.split(" ")) # storing a list of strings of a sentence to another list
        i=i+1    
d1  = Counter()
for i in a:
    if len(a) < 2:
        continue
    i.sort()
    for c in combinations(i,2):
        d1[c] += 1

print "Number of words: ", s
print "Number of sentences: ",cnt
print "Number of sentences that start with 'The': ",cnt1 
print "Most frequent two word combination: ",d1.most_common(1)
