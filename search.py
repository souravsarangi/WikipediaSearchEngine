import sys
import linecache
import glob
import subprocess
from nltk import stem
stemmer=stem.PorterStemmer()


args=sys.argv
if args[1]!="all":
	filens=["smallindex/"+args[1]]
else:
	filens=["smallindex/title","smallindex/body","smallindex/ref","smallindex/info","smallindex/cat","smallindex/ext"]
terms=args[2:]
tfidf={}
fname=''
for filen in filens:
	for search in terms: # list contains the list of search keys
		search=stemmer.stem_word(search)
		if search[0]>='a' and search[0]<='z':
			fname=filen+"_"+search[0]
		else:
			fname=filen+"_zate"
		if fname+"2" in glob.iglob(fname+"*"):
			lines=subprocess.check_output("wc -l "+fname+"2",shell=True)
			lines=int(lines.split(" ")[0])
			left, right = 1, lines + 1 
		 	while left <= right:
		  		mid = (left + right) / 2
		  		line=linecache.getline(fname+"2", mid)
		  		line=line.split('-')
				if search > line[0]:
					left = mid + 1
				elif search < line[0]:
					right = mid - 1
				else:
					break
			line=linecache.getline(fname+"2", mid)
		  	line=line.split('-')
			left=int(line[1])
			line=linecache.getline(fname+"2", mid+1)
		  	line=line.split('-')
			right=int(line[1])+1
		else:
			lines=subprocess.check_output("wc -l "+fname,shell=True)
			lines=int(lines.split(" ")[0])
			left, right = 1, lines + 1 


	 	while left <= right:
	  		mid = (left + right) / 2
	  		line=linecache.getline(fname, mid)
	  		line=line.split('=')
			if search > line[0]:
				left = mid + 1
			elif search < line[0]:
				right = mid - 1
			else:
				break
		docs=[]
	  	if search == line[0]:
			docs=line[1].split("|")[1:]
		for doc in docs:
			docid,score=doc.split(":")
			try:
				tfidf[int(docid)]+=float(score)
			except KeyError:
				tfidf[int(docid)]=float(score)

ranked_docs=sorted(tfidf.items(), key=lambda x: x[1])


records=0
for doc in reversed(ranked_docs):
	lines=subprocess.check_output("wc -l "+"Docinfo2",shell=True)
	lines=int(lines.split(" ")[0])
	left, right = 1, lines + 1 
	print doc,
 	while left <= right:
  		mid = (left + right) / 2
  		line=linecache.getline("Docinfo2", mid)
  		line=line.split('>')
		if doc[0] > int(line[0]):
			left = mid + 1
		elif doc[0] < int(line[0]):
			right = mid - 1
		else:
			break

	
	print line[1].split("|")[0]
	records+=1
	if records==10:
		break

	



