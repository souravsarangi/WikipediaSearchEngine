f=open("title-lins","r")
line_offset = []
offset = 0
k=f.readline()
c=0
while k!="":
	print c
	line_offset.append(offset)
	offset += len(k)
	k=f.readline()
	c+=1
    
with open("offsets2","w") as f2:
	f2.write(str(line_offset))
