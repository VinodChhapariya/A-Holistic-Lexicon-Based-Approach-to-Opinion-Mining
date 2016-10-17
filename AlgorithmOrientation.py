#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk import word_tokenize
from textblob import TextBlob
import nltk
import glob
import json

#features list for given product 
ProductFeatureList = [
    'canon powershot g3',
    'use',
    'picture',
    'picture quality',
    'camera',
    'features',
    'options',
    ]

#lists to store positive and negative opinion words
OpinionWordsPositive = []
OpinionWordsNegative = []

#getting positive opinion words to list
OpinionWordFile1 = glob.glob('C:/Users/Vinod Chhapariya/Desktop/TDBMS/Project/Opinion Words/positive-words.txt')
for filename in OpinionWordFile1:
        for line in open(filename, 'r').readlines():
            t=word_tokenize(line)
            for tags in t:
                OpinionWordsPositive.append(tags)

#getting negative opinion words to list
OpinionWordFile2 = glob.glob('C:/Users/Vinod Chhapariya/Desktop/TDBMS/Project/Opinion Words/negative-words.txt')
for filename in OpinionWordFile2:
        for line in open(filename, 'r').readlines():
            t=word_tokenize(line)
            for tags in t:
                    OpinionWordsNegative.append(tags)

#getting reviews for product
fileList =glob.glob('C:/Users/Vinod Chhapariya/Desktop/TDBMS/Project/Benchmark Dataset/CannonG3_Review_1.txt')

#feature dictionary to store feature with its orientation score
FeatureDictionary = {}

#processing each review
for filename in fileList:
    
    for line in open(filename, 'r').readlines():
        # Words dictionary to store each word of the sentence with its position    
        Words = {}
        tokens = word_tokenize(line)
        i = 0
        for t in tokens:
            Words[t] = i
            i += 1
        print Words
        
        #noun phrases and nouns are possible features storing them in PosiibleFeatures list
        tb = TextBlob(line)
        PossibleFeatures = tb.noun_phrases
        postags = tb.tags
        for t in postags:
            if t[1][0] == 'N':
                PossibleFeatures.append(t[0])



        #calculating word orientation as per algorithm specified in paper 
        for feature in PossibleFeature:
            #if possible feature is present in product feature list 
            if feature in ProductFeatureList:

                #initilize orientation
                Orientation = 0
                FeatureDictionary[feature]=Orientation

                #checking for opinion word
                for ow in Words:
                    if ow in OpinionWordsPositive:
                        print ow

                        #handling negation rule
                        if 'not' in Words.keys() and Words[ow]==Words['not']+1:
                                Orientation=-1
                        else:
                                Orientation =1

                        #feaure may have more than one word(eg. 'picture quality'), hence considering only first word to calculate distance of the feature from opinion word.
                        token=word_tokenize(feature)
                        
                        #calculating distance between feature and each ow
                        Distance= Words[ow] - Words[token[0]]
                        
                        #orientation formula based on distance between feature and ow
                        Orientation = (Orientation/(abs(Distance)*1.00))
                        FeatureDictionary[feature] += Orientation

                    #perform same for negative opinoin words     
                    elif ow in OpinionWordsNegative:
                        print ow
                        if 'not' in Words.keys() and Words[ow]==Words['not']+1:
                                Orientation=1
                        else:
                                Orientation =-1

                        tokens =word_tokenize(feature)
                        Distance= Words[ow] - Words[tokens[0]]
                        print Distance
                        Orientation = (Orientation/(abs(Distance)*1.00))
                        FeatureDictionary[feature] += Orientation
                        
        #printing features with their score. score>0 -->positive orientation and score<0 --->Negative orientation
        print FeatureDictionary


        #Work yet to complete for this algorithm ---
                #context dependant opinion handling
                #adding more negation rules
                #applying synonym antonym rule
                #But caluse rule
                #calculating accuracy of the algorithm
                

