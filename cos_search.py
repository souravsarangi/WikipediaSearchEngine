import sys
import linecache
import glob
import subprocess
from nltk import stem
import math
stemmer=stem.PorterStemmer()
N=5311

args=sys.argv
if args[1]!="all":
	filens=["index/"+args[1]]
else:
	filens=["index/title","index/body","index/ref","index/info","index/cat","index/link"]

terms=args[2:]
tfidf={}
fname=''
idfterms={}
scoredocs={}
for filen in filens:
	for search in terms: # list contains the list of search keys
		search=stemmer.stem_word(search)
		fname=filen+"_"+search[0]
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
	  	if search == line[0]:
			docs=line[1].split("|")[1:]

		try:
			idfterms[search]|=set(docs)
		except:
			idfterms[search]=set(docs)

		for doc in docs:
			docid,score=doc.split(":")
			try:
				scoredocs[int(docid)].update({search:float(score)})
			except KeyError:
				scoredocs[int(docid)]={}
				scoredocs[int(docid)].update({search:float(score)})
			try:
				tfidf[int(docid)]+=float(score)
			except KeyError:
				tfidf[int(docid)]=float(score)

ranked_docs=sorted(tfidf.items(), key=lambda x: x[1])

for search in terms:
	idfterms[search]=math.log(2)*math.log(N/len(idfterms[search]))
records=0

coscore_docs={}
for doc in reversed(ranked_docs):
	lines=subprocess.check_output("wc -l "+"Docinfo",shell=True)
	lines=int(lines.split(" ")[0])
	left, right = 1, lines + 1 
 	while left <= right:
  		mid = (left + right) / 2
  		line=linecache.getline("Docinfo", mid)
  		line=line.split('>')
  		#print line
		if doc[0] > int(line[0]):
			left = mid + 1
		elif doc[0] < int(line[0]):
			right = mid - 1
		else:
			break
	info=line[1].split("|")
	#print line[0],info
	lend=int(info[1])

	for key,value in scoredocs[doc[0]].iteritems():
		try:
			coscore_docs[doc[0]]+=idfterms[key]*value
		except KeyError:
			coscore_docs[doc[0]]=idfterms[key]*value

	coscore_docs[doc[0]]/=lend




ranked_docs2=sorted(coscore_docs.items(), key=lambda x: x[1])
for doc in reversed(ranked_docs2):
	lines=subprocess.check_output("wc -l "+"Docinfo",shell=True)
	lines=int(lines.split(" ")[0])
	left, right = 1, lines + 1 
 	while left <= right:
  		mid = (left + right) / 2
  		line=linecache.getline("Docinfo", mid)
  		line=line.split('>')
		if doc[0] > int(line[0]):
			left = mid + 1
		elif doc[0] < int(line[0]):
			right = mid - 1
		else:
			break
	info=line[1].split("|")
	if info[0]!="Doraemon":
		print doc[1],info[0]
		records+=1
	if records==10:
		break

	



