#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk import word_tokenize
from textblob import TextBlob
import nltk
import glob
import json

ProductFeatureList=[]

#features list for given product 
with open('C:\Users\Vinod Chhapariya\Desktop\TDBMS\Project\Features_Json_Files\Nokia6610.json') as data_file:    
        data = json.load(data_file)
for key in data:
        ProductFeatureList.append(str(key))
print ProductFeatureList
print len(ProductFeatureList)


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
fileList =glob.glob('C:/Users/Vinod Chhapariya/Desktop/TDBMS/Project/Nokia6610_Reviews/*')
FeatureDictionary={}
#feature dictionary to store feature with its orientation score
for p in ProductFeatureList:
        FeatureDictionary[p]=0


def ButClauseRule(Words,feature):
        for ow in Words.keys():
                if Words[ow]> Words['but']:
                        if ow in OpinionWordsPositive:
                                Orientation=-1
                        elif ow in OpinionWordsNegative:
                                Orientatation=1
                        else:
                                Orientation=0
        return Orientation
                                


#processing each review
for filename in fileList:
    print filename
    for line in open(filename, 'r').readlines():
        # Words dictionary to store each word of the sentence with its position    
        Words = {}
        tokens = word_tokenize(line)
        i = 0
        for t in tokens:
            Words[t] = i
            i += 1
        #print Words
        
        #noun phrases and nouns are possible features storing them in PosiibleFeatures list
        tb = TextBlob(line)
        PossibleFeatures = tb.noun_phrases
        postags = tb.tags
        for t in postags:
            if t[1][0] == 'N':
                PossibleFeatures.append(t[0])
        #print PossibleFeatures



        #calculating word orientation as per algorithm specified in paper 
        for feature in PossibleFeatures:
            #if possible feature is present in product feature list 
            if feature in ProductFeatureList:

                #initilize orientation
                Orientation = 0
                
                #feature is getting added to dictionary first time then initialize its orientation to 0 
                if feature not in FeatureDictionary.keys():
                        FeatureDictionary[feature]=Orientation

                #feaure may have more than one word(eg. 'picture quality'), hence considering only first word to calculate distance of the feature from opinion word.
                token=word_tokenize(feature)

                #checking for opinion word
                for ow in Words:
                    if ow not in token:    
                            #Applying But Clause Rule
                            if 'but' in Words.keys() and Words['but']<Words[token[0]]:  
                                Orientation= ButClauseRule(Words,token[0])

                            #getting orientation for positive opinion word      
                            elif ow in OpinionWordsPositive:
                                #print ow

                                #handling negation rule
                                if 'not' in Words.keys() and Words[ow]==Words['not']+1:
                                        Orientation=-1
                                else:
                                        Orientation=1

                            #getting orientation for negative opinoin word     
                            elif ow in OpinionWordsNegative:
                                #print ow
                        
                                if 'not' in Words.keys() and Words[ow]==Words['not']+1:
                                        Orientation=1
                                else:
                                        Orientation =-1

                            #calculating distance between feature and each ow
                            Distance= Words[ow] - Words[token[0]]
                        
                            #orientation formula based on distance between feature and ow
                            Orientation = (Orientation/(abs(Distance)*1.00))
                            FeatureDictionary[feature] += Orientation
                        
        #printing features with their score. score>0 -->positive orientation and score<0 --->Negative orientation
print FeatureDictionary
print len(FeatureDictionary)

for feature in FeatureDictionary:
        if FeatureDictionary[feature]>=0:
                FeatureDictionary[feature]=1
        elif FeatureDictionary[feature]<0:
                FeatureDictionary[feature]=-1
        #else:
                #FeatureDictionary.pop(feature)

print FeatureDictionary

with open('Nokia6610_Predicted.json', 'w') as outfile:
     json.dump(FeatureDictionary, outfile, sort_keys = True, indent = 4,ensure_ascii=False)


        #Work yet to complete for this algorithm ---
                #context dependant opinion handling
                #adding more negation rules
                #applying synonym antonym rule
                #But caluse rule
                #calculating accuracy of the algorithm
                


                        
        
