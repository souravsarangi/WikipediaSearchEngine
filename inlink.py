import xml.sax
from collections import defaultdict
import sys
import bz2,json,contextlib
from sortedcontainers import SortedDict
import os.path
import re 

     

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


def extracttitle(data):
  t=re.findall(r"\[\[[^\[\]]+?\]\]", data)
  k=set()
  for i in xrange(len(t)):
    t[i]=t[i].replace("[","")
    t[i]=t[i].replace("]","")
    s=t[i].split("|")
    for j in xrange(len(s)):
      s[j]=s[j].strip()
      k.add(s[j])
  return list(set(k))

def extractlink(data):
  return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)

def paginate(Handler):
  global docs
  docs+=1
  print docs
  data=""
  try:
    data=Handler.text
  except:
    pass
  tit=[]
  link=[]
  if data!="":
    #tit=extracttitle(data)
    link=extractlink(data)
  title=""
  try:
    title=Handler.title
  except:
    pass
  #titledict[title]=tit
  linkdict[title]=link
  if docs%300000==0:
    '''with open("title-titles"+str(docs/300000),"w") as f:
      for i in titledict:
        f.write(i+":")
        f.write(str(titledict[i]))
        f.write("\n")'''
    with open("title-link"+str(docs/300000),"w") as f:
      for i in linkdict:
        f.write(i+":")
        f.write(str(linkdict[i]))
        f.write("\n")
    #titledict.clear()
    linkdict.clear()




def main(sourceFileName):
  source = open(sourceFileName)
  Handler=WikiContentHandler()
  xml.sax.parse(source,Handler)
  

if __name__ == "__main__":
  global docs
  docs=1
  titledict= SortedDict()
  linkdict= SortedDict()
  args=sys.argv
  main(args[1])
  '''with open("title-titles"+str(docs/300000),"w") as f:
    for i in titledict:
      f.write(i+":")
      f.write(str(titledict[i]))
      f.write("\n")'''
  with open("title-link"+str(docs/300000),"w") as f:
    for i in linkdict:
      f.write(i+":")
      f.write(str(linkdict[i]))
      f.write("\n")



