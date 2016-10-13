import sys
import linecache
from itertools import islice
import glob
import subprocess



termsnv=["'Information security'"]
no_of_terms=355																																																																																																																																																																																																				
cur=0
lin=0
f3=open("offsets","r")
offset=f3.read()[1:-1].split(",")
f4=open("offsets2","r")
offset2=f4.read()[1:-1].split(",")
with open("wikiurls","w") as f:
	f.write("")
f=open("title-tits")
g=open("title-lins")

for search2 in termsnv:
	print "1",search2
	search=search2.strip("' ")
	print "2",search[0]


	cur+=1
	#print cur
	#print "size now"+str(len(termsnv))
	#lines=subprocess.check_output("wc -l "+f,shell=True)
	#lines=int(lines.split(" ")[0])
	lines=15999475
	left, right = 1, lines + 1 
	while left <= right:
		lin+=1
		mid = (left + right) / 2
		f.seek(int(offset[mid]))
		line=f.readline()
		line=line.split(':[')
		if search > line[0]:
			left = mid + 1
		elif search < line[0]:
			right = mid - 1
		else:
			break
	if left <= right:
		print "###### Found",search
		new=line[1][0:-2].split(',')
		for i in new:
			if i not in termsnv:
				termsnv.append(i)
		lines2=15999468
		left, right = 1, lines2 + 1 
		while left <= right:
			lin+=1
			mid = (left + right) / 2
			g.seek(int(offset2[mid]))
			line=g.readline()
			line=line.split(':[')
			if search > line[0]:
				left = mid + 1
			elif search < line[0]:
				right = mid - 1
			else:
				break
		if left <= right:
			g.seek(int(offset2[mid]))
			line2=g.readline()
			for i in line2.split(":[")[1][0:-2].split(","):
				with open("wikiurls","a") as fi:
					fi.write(i+"\n")
	else:
		print "~~~~~~~~~~~~~~~not found",search

	if cur>no_of_terms:
		break

