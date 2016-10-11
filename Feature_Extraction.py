import glob
import re
import nltk
from nltk import pos_tag, word_tokenize
import csv
import os
from fp_growth import find_frequent_itemsets

pattern = re.compile("[A-Za-z0-9]+")

re4='.*?'	
re5='(#)'	
re6='(#)'

rg2 = re.compile(re4+re5+re6,re.IGNORECASE|re.DOTALL)
#Input Review Files to be processed
fileList=glob.glob("/home/sherin/Desktop/Rashmi/DBMS Project/Feature_ext_FP_Code/FP_Output/*.txt")
print "Extracting sentences..."
for filename in fileList:
	head, tail = os.path.split(filename)
	base=os.path.splitext(tail)[0]
	print base
	inFile = open(filename, 'r').read().split('\n')
	outFile=open(head+"/Processed Files/"+base+".txt",'w')
	#Remove the manually extracted features from each review sentence which starts with "#"
	for lines in inFile:
		
		modifiedLine = re.sub(rg2," ", lines)
		outFile.write('\n'+modifiedLine)
	outFile.close()
print "POS tagging..."
print "Extracting features..."
#Save the pre-processed files in the Processed Files Folder
modifiedFileList=glob.glob("/home/sherin/Desktop/Rashmi/DBMS Project/Feature_ext_FP_Code/FP_Output/Processed Files/*.txt")
for filename in modifiedFileList:
	sentenceNounList=[]
	head2, tail2 = os.path.split(filename)
	base=os.path.splitext(tail2)[0]
	posFile=open(head+"/POS tagged/"+base+".txt",'w')
	#POS Tagging for each word in the Review Sentence, save the Tagged Pairs <word,POS_Tag> in the POS Tagged Folder
	for line in open(filename,'r').readlines():
		tokens = word_tokenize(line)
		tags=pos_tag(tokens)
		nouns=[]
		#Save only Noun tags in the "noun" list for further processing in each review sentence
		for t in tags:
			m = re.match(pattern,t[0])
     			if m:
				if len(t[0])>2:
					posFile.write('\n'+str(t))	
					if t[1][0] == 'N':
						nouns.append(t[0])
                #Save all the Noun Tags in each Review File/Database in sentenceNounList	
		sentenceNounList.append(nouns)
	posFile.close()
	with open(head+"/CSV/"+base+".csv", "w") as f:
		writer = csv.writer(f)
		writer.writerows(sentenceNounList)
	f.close()

	#Save the Frequent Noun Phrases in NounPhrases Folder for each Review File/Database
	npFile=open(head+"/NounPhrases/"+base+".txt",'w')
	
	#Find the frequent Noun Phrases in each Review File/Database
	for itemset in find_frequent_itemsets(sentenceNounList,3):
		npFile.write('\n'+str(itemset))	
	npFile.close()
