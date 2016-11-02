#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk import word_tokenize
from textblob import TextBlob
import nltk
import glob
import json
import os


fileList =glob.glob('C:\Users\Vinod Chhapariya\Desktop\TDBMS\Project\Nokia6610\*.txt')
i=1;
for filename in fileList:
    f=open('Nokia6610_Reviews_'+str(i), 'w')
    print "starting" + filename
    for line in open(filename, 'r').readlines():
        if line is '\n':
            break
        s=line.split('##')
        try:
            sentence = s[1]
        except IndexError:
            sentence = 'null'   
        f.write(sentence)
    f.close()
    i=i+1
    print '\n'
        
