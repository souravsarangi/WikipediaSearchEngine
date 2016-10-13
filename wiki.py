import xml.sax
from  tokenise import *
from collections import defaultdict
import sys
import bz2,json,contextlib
from sortedcontainers import SortedDict
import os.path
#import TextProcess 


def findInfoBoxTextCategory(data):                                        #find InfoBox, Text and Category
  info=[]
  bodyText=[]
  category=[]
  links=[]
  references=[]
  flagext=0
  flagrefer=0
  flagbody=1
  flaginfo=0
  lines = data.split('\n')
  for i in xrange(len(lines)):
    if lines[i].startswith("[[Category"):
      flagext=0
      s=lines[i]
      try:
        start = s.index("[[Category:") + len("[[Category:")
        end = s.index( "]]", start )
        category.append(s[start:end])
      except ValueError:
        pass
      continue

    elif lines[i].startswith("==External") or lines[i].startswith("== External") or flagext==1:
      flagrefer=0
      flagext=1
      if lines[i].startswith('* [') or lines[i].startswith('*['):
        word=""
        temp=lines[i].split(' ')
        for key in temp:
          if 'http' not in key or '*' not in key:
            word=word+' '+key
        links.append(word)
      continue

    elif lines[i].startswith('==Referen') or lines[i].startswith("== Referen") or flagrefer==1:
      flagbody=0
      if flagrefer==1 and lines[i].startswith('=='):
        flagrefer=0
        continue
      flagrefer=1
      temp=lines[i][1:].split(' ')
      word=""
      for key in temp:
        if 'http' not in key:
          word=word+' '+key
        references.append(word)
      continue


    elif lines[i].startswith('{{Info') or lines[i].startswith('{{ info') or flaginfo==1:
      if flaginfo==0:
        try:
          temp=lines[i].split('{{Infobox')[1]
          info.append(temp)
          flaginfo=1
        except IndexError:
          flaginfo=0
      else:
        try:
          temp=lines[i].split('=')[1]
          info.append(temp)
        except IndexError:
          flaginfo=0

    elif flagbody==1:
      if lines[i].startswith('==See A')or lines[i].startswith("== See A"):
        flagbody=0
      else:
        bodyText.append(lines[i])
    
  
  category=tokenise(' '.join(category))
  info=tokenise(' '.join(info))
  bodyText=tokenise(' '.join(bodyText))
  links=tokenise(' '.join(links))
  references=tokenise(' '.join(references))
  
  global tfdoc
  tfdoc+=len(category)+len(info)+len(bodyText)+len(links)+len(references)
  
  temp=defaultdict(int)
  for key in info:
    temp[key]+=1
  info=temp

  temp=defaultdict(int)
  for key in bodyText:
    temp[key]+=1
  bodyText=temp

  temp=defaultdict(int)
  for key in category:
    temp[key]+=1
  category=temp

  temp=defaultdict(int)
  for key in references:
    temp[key]+=1
  references=temp

  temp=defaultdict(int)
  for key in links:
    temp[key]+=1
  links=temp
  
  return info, bodyText, category, references, links
     

class WikiContentHandler(xml.sax.ContentHandler):
  def __init__(self):
    xml.sax.ContentHandler.__init__(self)
    self.flag = 0
    self.redirect = "#REDIRECT"
    self.var = ""
    global title
    global ids
    global text
    title=""
    ids=""
    text=""
 
  def startElement(self, name, attrs):
    if name == "page":
      self.flag = 1
      self.var = ""
    
    elif name == "title" or name == "id" or name == "text":
      if self.flag != 1:
        print "Wrong"
      else:   
        self.flag += 1
        
       
  def endElement(self, name):
    if name == "title":
      self.flag -= 1
      self.title=self.var
    if name == "id":
      self.flag -= 1
      self.id=self.var
    if  name == "text":
      self.flag -= 1
      self.text=self.var
    self.var=""
    if name== "page":
      self.flag=0
      paginate(self)
 
  def characters(self, content):
    if self.flag == 2:
      if self.redirect in content:
        self.var = ""
        self.flag = 0
      else:  
        self.var = self.var + content.encode('utf-8')
      

def update1(dict1,dict2,ids):
  for key,values in dict2.iteritems():
    try:
      dict1[key][0]+=','+ids+'-'+str(values)
    except KeyError:
      dict1[key]=[]
      dict1[key].append(','+ids+'-'+str(values))


 
def paginate(Handler):
  global pages
  global docs
  global tfdoc
  tfdoc=0

  docs+=1
  data=""
  try:
    data=Handler.text
  except:
    pass
  
  infoBox, bodyText, category, references, externalLinks = findInfoBoxTextCategory(data) 
  title=""
  try:
    title=Handler.title
    title=tokenise(title)
    tfdoc+=len(title)
    temp=defaultdict(int)
    for key in title:
      temp[key]+=1
    title=temp
  except:
    pass
  Did=""
  try:
    Did=Handler.id
  except:
    pass
  if title!="" and Did!="":
    update1(bodydict,bodyText,Did)
    update1(catdict,category,Did)
    update1(refdict,references,Did)
    update1(titledict,title,Did)
    update1(infodict,infoBox,Did)
    update1(extdict,externalLinks,Did)
    fp=open("DocInfo","a")
    #print tfdoc
    fp.write(Did+">"+Handler.title+"|"+str(tfdoc)+"\n")
    fp.close()

  print docs
  if len(bodydict)>150000:
    writeIndex(str(pages))
    pages+=1
  
def writeIndex(filename):
  #with contextlib.closing(bz2.BZ2File(filename, 'wb')) as f:
   # json.dump(worddict, f)
  path2=os.path.join(path,'body'+filename)
  with open(path2,'wb') as f:
    for i in bodydict.keys():
      f.write(i+":"+bodydict[i][0]+"\n")
  path2=os.path.join(path,'cat'+filename)
  with open(path2,'wb') as f:
    for i in catdict.keys():
      f.write(i+":"+catdict[i][0]+"\n")  
  path2=os.path.join(path,'ref'+filename)
  with open(path2,'wb') as f:
    for i in refdict.keys():
      f.write(i+":"+refdict[i][0]+"\n")
  path2=os.path.join(path,'title'+filename)
  with open(path2,'wb') as f:
    for i in titledict.keys():
      f.write(i+":"+titledict[i][0]+"\n")
  path2=os.path.join(path,'info'+filename)
  with open(path2,'wb') as f:
    for i in infodict.keys():
      f.write(i+":"+infodict[i][0]+"\n")
  path2=os.path.join(path,'ext'+filename)
  with open(path2,'wb') as f:
    for i in extdict.keys():
      f.write(i+":"+extdict[i][0]+"\n")

  #sortdict.clear()
  print len(bodydict)
  bodydict.clear()
  catdict.clear()
  refdict.clear()
  titledict.clear()
  infodict.clear()
  extdict.clear()


def main(sourceFileName):
  source = open(sourceFileName)
  Handler=WikiContentHandler()
  xml.sax.parse(source,Handler)
  

if __name__ == "__main__":
  global pages
  pages=1
  global docs
  docs=1
  global tfdoc
  tfdoc=0
  fp=open("DocInfo","w")
  fp.write("")
  fp.close()
  path='./smallindex/'
  titledict= SortedDict()
  bodydict= SortedDict()
  refdict= SortedDict()
  extdict= SortedDict()
  infodict= SortedDict()
  catdict= SortedDict()
  args=sys.argv
  main(args[1])
  writeIndex(str(pages))
  pages+=1

