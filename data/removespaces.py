import re
f=open("title-l","r")
k=f.readline()
while k!="":
	#print k
	if not re.match(r'^\s*$', k):
		print k,
	k=f.readline()


