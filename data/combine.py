from sortedcontainers import SortedDict
import glob

l={}
for f in glob.iglob("title-link*"):
	fo=open(f,"r")
	l[f[10:]]=fo
d=SortedDict()
for i in l:
	lin=l[i].readline()
	lin=lin.split(":[")
	d[lin[0]]=[]
	d[lin[0]].append("["+lin[1][0:-1])
	d[lin[0]].append(i)

fil=open("title-l","w")
c=0
while len(d):
	if c%300000==0:
		print c/300000
	c+=1
	x=d.popitem()
	fil.write(x[0]+":"+x[1][0]+"\n")
	lin=l[x[1][1]].readline()
	if lin != '':
		lin=lin.split(":[")
		d[lin[0]]=list()
		d[lin[0]].append("["+lin[1])
		d[lin[0]].append(x[1][1])








