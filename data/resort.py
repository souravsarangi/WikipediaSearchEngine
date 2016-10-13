from sortedcontainers import SortedDict
dic=SortedDict()
off=map(int,open("offset2","r").read()[1:-1].split(","))
c=0
with open("tit2",'r') as f:
	for line in f:
		dic[line]=off[c]
		c+=1
print "no of titles",c
k=0
with open("title-lins","w") as f:
	f.write('')
g=open("title-li","r")
for line in dic:
	with open("title-lins","a") as f:
		g.seek(dic[line])																																																																																																																																																																																																																																													
		f.write(g.readline())
	k+=1
	print k



