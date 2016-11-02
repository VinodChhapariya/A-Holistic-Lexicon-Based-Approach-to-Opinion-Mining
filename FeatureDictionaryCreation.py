#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk import word_tokenize
from textblob import TextBlob
import nltk
import glob
import json
import re

#getting reviews for product
fileList =glob.glob('C:\Users\Vinod Chhapariya\Desktop\TDBMS\Project\Nokia6610\*.txt')
FeatureDictionary={}
#processing each review
for filename in fileList:
    print "starting" + filename
    for line in open(filename, 'r').readlines():
        if line is '\n':
            break
        
        str=[]
        tokens = word_tokenize(line)
        for k in range(0,len(tokens)):
            if tokens[k]=='#':
                break
            
            if tokens[k] == '[' and tokens[k+1].startswith('-') or tokens[k+1].startswith('+'):  
                i=int(tokens[k+1])
                if i > 0:
                    orientation=1
                
                else:
                    orientation=-1
                feature=""
                for st in str:
                    if st==str[0]:
                        feature = feature+st
                    else:
                        feature = feature +" " + st
                if feature in FeatureDictionary:
                    FeatureDictionary[feature]=FeatureDictionary[feature]+orientation
                else:
                    FeatureDictionary[feature]=orientation
                
                str[:]=[]
            if tokens[k]=='[' or tokens[k]=='}'or tokens[k]=='u' or tokens[k]=='t'or tokens[k]=='p' or tokens[k]== '+1'or tokens[k] == '+2'or tokens[k] =='+3'or tokens[k] == '-1' or tokens[k] == '-2' or tokens[k] == '-3' or tokens[k] == ']' or tokens[k] == ',':
                continue            
            str.append(tokens[k])

       
        

print FeatureDictionary


for feature in FeatureDictionary:
        if FeatureDictionary[feature]>=0:
                FeatureDictionary[feature]=1
        elif FeatureDictionary[feature]<0:
                FeatureDictionary[feature]=-1

print FeatureDictionary
print len(FeatureDictionary)

with open('Nokia6610.json', 'w') as outfile:
     json.dump(FeatureDictionary, outfile, sort_keys = True, indent = 4,ensure_ascii=False)


