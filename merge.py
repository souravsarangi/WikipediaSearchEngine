import sys
import os
from collections import defaultdict
from math import log
from math import sqrt
import linecache

N_docs = 1700000
max_lines = 1000
divide = {'zate': 26, 'a': 0, 'c': 2, 'b': 1, 'e': 4, 'd': 3, 'g': 6, 'f': 5, 'i': 8, 'h': 7, 'k': 10, 'j': 9, 'm': 12, 'l': 11, 'o': 14, 'n': 13, 'q': 16, 'p': 15, 's': 18, 'r': 17, 'u': 20, 't': 19, 'w': 22, 'v': 21, 'y': 24, 'x': 23, 'z': 25}
key = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'zate']
az_size = {'zate': 0, 'a': 0, 'c': 0, 'b': 0, 'e': 0, 'd': 0, 'g': 0, 'f': 0, 'i': 0, 'h': 0, 'k': 0, 'j': 0, 'm': 0, 'l': 0, 'o': 0, 'n': 0, 'q': 0, 'p': 0, 's': 0, 'r': 0, 'u': 0, 't': 0, 'w': 0, 'v': 0, 'y': 0, 'x': 0, 'z': 0}
az_constant = {'zate': 0, 'a': 0, 'c': 0, 'b': 0, 'e': 0, 'd': 0, 'g': 0, 'f': 0, 'i': 0, 'h': 0, 'k': 0, 'j': 0, 'm': 0, 'l': 0, 'o': 0, 'n': 0, 'q': 0, 'p': 0, 's': 0, 'r': 0, 'u': 0, 't': 0, 'w': 0, 'v': 0, 'y': 0, 'x': 0, 'z': 0}
previous = ""
count = 0
flag = 0

def score(file_name):
	name = file_name[4]
	if name == "t":
		return 100
	elif name == "c" or name == "i":
		return 30
	elif name == "r" or name == "l":
		return 15
	else:
		return 5

def scoring(line, d_score):
	new_docs = list()
	first = line.split(":")
	docs = first[1]
	docs.strip()
	docs = docs.split(",")[1:]
	n = len(docs)
	for i in docs:
		doc = i.split("-")
		tf = int(doc[1])
		new_score = tf_idf(n, d_score, tf)
		new_docs.append(doc[0] + ":" + str(new_score))
	return new_docs	

def tf_idf(n, d_score, tf):
	tf = 1 + int(log(tf)/log(10))
	idf = log(N_docs/n)/log(10)
	result = round(d_score*tf*idf, 2)
	return result

def merge(file_name):
	global flag
	global count
	global previous
	global az_size
	az_size = az_constant
	previous = ""
	count = 0
	flag = 0
	files = 1
	flist = list()
	final_open = list()
	block_list = defaultdict(str)
	flag_list = list()
	index_list = list()
	end_list = list()
	d_score = score(file_name)
	fname = file_name + str(files)

	while(os.path.isfile(fname)):
		files += 1
		fname = file_name + str(files)

	for i in xrange(files-1):
		flag_list.append(0)
		index_list.append(0)
		end_list.append(max_lines) 	
	
	if files >= 2:
		for i in xrange(files-1):
			fname = file_name + str(i+1)			
			fopen = open(fname, "r")
			flist.append(fopen)
			block_list[i] = list()
			for j in xrange(max_lines):
				line = flist[i].readline()
				if line == "":
					flag_list[i] = -1
					end_list[i] = j	
					break
				block_list[i].append(line)

		for i in key:
			fname = file_name + "_" + str(i)			
			fopen = open(fname, "w")
			final_open.append(fopen)
	
		block_list[files] = list()
		for i in xrange(max_lines):
			block_list[files].append("")

		begin = 0

		while 1:
			for i in xrange(files-1):
				if flag_list[i] == 0 and end_list[i] == index_list[i]:
					for j in xrange(max_lines):
						if not flist[i].closed:
							line = flist[i].readline()
							if line == "":
								flag_list[i] = -1
								end_list[i] = j-1
								flist[i].close()	
								break
							block_list[i][j] = line
					index_list[i] = 0						

			if begin == max_lines:
				for i in xrange(max_lines):
					line = block_list[files][i]
					block_list[files][i] = ""
					line = post_sort(line, d_score)
					char = line.split("=")[0][0]
					if char.isdigit():
						char = "zate"	
					
					if flag == 0:
						previous = char
						flag = 1
					if previous != char:
						print file_name, previous
						az_size[previous] = count
						ind = divide[previous]
						final_open[ind].close()
						previous = char
						count = 0
					count += 1
					ind = divide[char]
					if final_open[ind].closed:
						final_open[ind] = open(fname + "_" + char, "a+")
					final_open[ind].write(line)
				begin = 0	

			for j in xrange(files-1):
				if flag_list[j] == -1 and end_list[j] == index_list[j]:
					continue
				index = index_list[j]
				if block_list[files][begin] == "":
					block_list[files][begin] = block_list[j][index]
					select = j
				elif compare(block_list[files][begin], block_list[j][index]) == 0:
					block_list[files][begin] = block_list[j][index]
					select = j
				elif compare(block_list[files][begin], block_list[j][index]) == 1:
					line = 	block_list[j][index].split(":")[1]
					block_list[files][begin] = block_list[files][begin].strip()
					block_list[files][begin] += line
					index_sel = index_list[select]
					block_list[select][index_sel] = block_list[select][index_sel].strip()
					block_list[select][index_sel] += line
					index_list[j] += 1
				
			if block_list[files][begin] == "":
				break
			index_list[select] += 1
			begin += 1
		
		for i in xrange(max_lines):
			line = block_list[files][i]
			if line == "":
				break
			block_list[files][i] = ""
			char = line.split("=")[0][0]
			if char.isdigit():
				char = "zate"	
			ind = divide[char]
			line = post_sort(line, d_score)
			if final_open[ind].closed:
				final_open[ind] = open(fname + "_" + char, "a+")
			final_open[ind].write(line)

def compare(a, b):
	a = a.split(":")[0]
	b = b.split(":")[0]
	if a == b:
		return 1
	elif a > b:
		return 0
	else:
		return 2		

def post_sort(line, d_score):
	first = line.split(":")
	term = first[0]
	docs = scoring(line, d_score)
	docs = sorted(docs, cmp=comp)
	s = "|"
	new_line = term + "=" + "|" + s.join(docs) + "\n"
	return new_line

def comp(item1, item2):
	#print item1
	i1 = float(item1.split(":")[1])
	i2 = float(item2.split(":")[1])
	if i1 < i2:
		return 1
	elif i1 > i2:
		return -1
	else:
		return 0

def second_index(fname):
	for i in az_size.keys():
		if az_size[i] > 10000:
			n = az_size[i]
			fname1 = fname + "_" + i
			fname2 = fname1 + "2"
			fp = open(fname2, "w")
			interval = int(round(sqrt(n)))
			for i in range(1, n, interval):
				if fp.closed:
					fp = open(fname2, "a+")
				line = linecache.getline(fname1, i)
				wline = line.split("=")[0] + "-" + str(i) + "\n"
				fp.write(wline)
			fp.close()	

def main():
	finfo = "index/info"
	fbody = "index/body"
	ftitle = "index/title"
	fref = "index/ref"
	flink = "index/ext"
	fcat = "index/cat"
	sort_list = [ftitle, finfo, fbody, fref, flink, fcat]
	for i in sort_list:
		merge(i)
		second_index(i)

if __name__ == "__main__":
 	main()
