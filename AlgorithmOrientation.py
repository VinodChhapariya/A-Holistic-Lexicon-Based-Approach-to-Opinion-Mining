#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk import word_tokenize
from textblob import TextBlob
import nltk
import glob
import json
from nltk.corpus import wordnet as wn

ProductFeatureList=[]
PossibleFeatureList=[]

#features list for given product 
with open('C:\Users\Vinod Chhapariya\Desktop\TDBMS\Project\Features_Json_Files\HitachiRouter.json') as data_file:    
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
                OpinionWordsPositive.append(tags.upper())

#getting negative opinion words to list
OpinionWordFile2 = glob.glob('C:/Users/Vinod Chhapariya/Desktop/TDBMS/Project/Opinion Words/negative-words.txt')
for filename in OpinionWordFile2:
        for line in open(filename, 'r').readlines():
            t=word_tokenize(line)
            for tags in t:
                    OpinionWordsNegative.append(tags.upper())


#getting reviews for product
fileList =glob.glob('C:/Users/Vinod Chhapariya/Desktop/TDBMS/Project/HitachiRouter_Reviews/*')

#feature dictionary to store feature with its orientation score
FeatureDictionary={}
FeatureAdjectiveDictionary={}
for p in ProductFeatureList:
        FeatureDictionary[p]=0

#rule for sentences having but clause  
def ButClauseRule(Words,feature):
        for ow in Words.keys():
                if Words[ow]> Words['BUT']:
                        if ow in OpinionWordsPositive:
                                Orientation=-1
                        elif ow in OpinionWordsNegative:
                                Orientatation=1
                        else:
                                Orientation=0
        return Orientation
                                


AdjDictionary={}

#processing each review
for filename in fileList:
    print filename
    for line in open(filename, 'r').readlines():
        # Words dictionary to store each word of the sentence with its position    
        Words = {}
        tokens = word_tokenize(line)
        i = 0
        for t in tokens:
            Words[t.upper()] = i
            i += 1
        
        #noun phrases and nouns are possible features storing them in PosiibleFeatures list
        tb = TextBlob(line)
        Features = tb.noun_phrases
        PossibleFeatures=[]
        for f in Features:
                f=f.upper()
                PossibleFeatures.append(f)
        postags = tb.tags
        for t in postags:
            if t[1][0] == 'N':
                PossibleFeatures.append(t[0].upper())
        



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

                #Applying But Clause Rule
                if 'BUT' in Words.keys():
                        if Words['BUT']<Words[token[0]]:  
                                Orientation= ButClauseRule(Words,token[0])
                        else:
                                del Words['BUT']
                
                #checking for opinion word
                for ow in Words:
                    if ow not in token:    
                            
                            #getting orientation for positive opinion word      
                            if ow in OpinionWordsPositive:
                                #handling negation rule
                                if 'NOT' in Words.keys() and Words[ow]==Words['NOT']+1 or 'TOO' in Words.keys() and Words[ow]==Words['TOO']+1:
                                        Orientation=-1
                                else:
                                        Orientation=1

                            #getting orientation for negative opinoin word     
                            elif ow in OpinionWordsNegative:
                                #print ow
                        
                                if 'NOT' in Words.keys() and Words[ow]==Words['NOT']+1 or 'TOO' in Words.keys() and Words[ow]==Words['TOO']+1:
                                        Orientation=1
                                else:
                                        Orientation =-1

                            #calculating distance between feature and each ow
                            x=len(token)
                            Distance= Words[ow] - Words[(token[x-1])]
                        
                            #orientation formula based on distance between feature and ow
                            Orientation = (Orientation/(abs(Distance)*1.00))
                            FeatureDictionary[feature] += Orientation

                
               

                
                tb = TextBlob(feature)
                posfeature = tb.tags
                for t in posfeature:
                    if t[1][0] == 'J':
                            if feature in AdjDictionary.keys():
                                AdjDictionary[feature] += Orientation
                            else:
                                 AdjDictionary[feature] = Orientation   
                    else:
                            for ow in Words.keys():
                                    tb=TextBlob(ow)
                                    postag=tb.tags
                                    for t in postag:
                                            if t[1][0]=='J':
                                                    FeatureAdjective=[feature,t[0]]
                                                    if (feature,t[0]) in  FeatureAdjectiveDictionary.keys():
                                                            FeatureAdjectiveDictionary[(feature,t[0])] += [Orientation,Orientation]
                                                    else:
                                                            FeatureAdjectiveDictionary[(feature,t[0])]=[0,0]

                # Context dependent opinion words handling
                    if FeatureDictionary[feature]==0:
                            tb = TextBlob(feature)
                            posfeature = tb.tags
                            for t in posfeature:
                                    if t[1][0] == 'J':
                                            FeatureDictionary[feature] = AdjDictionary[feature]
                                    else:
                                            for i in wn.synsets(ow):
                                                    for j in i.lemmas(): # Iterating through lemmas for each synset.
                                                            if j.name() in OpinionWordsPositive:
                                                                    FeatureDictionary[feature]=1
                                                            elif j.name() in OpinionWordsNegative:
                                                                    FeatureDictionary[feature]=-1
                                                                    for k in j.antonyms():
                                                                            if k.name() in OpinionWordsPositive:
                                                                                    FeatureDictionary[feature]=-1

                                                                            elif k.name() in OpinionNWrdsNegative:
                                                                                    FeatureDictionary[feature]=1




print FeatureDictionary

for feature in  FeatureDictionary.keys():
        if FeatureDictionary[feature]>=0:
                FeatureDictionary[feature]=1
        elif FeatureDictionary[feature]<0:
                FeatureDictionary[feature]=-1
       
                        
        #printing features with their score. score>0 -->positive orientation and score<0 --->Negative orientation
print FeatureDictionary
print len(FeatureDictionary)


with open('HitachiRouter_Predicted.json', 'w') as outfile:
     json.dump(FeatureDictionary, outfile, sort_keys = True, indent = 4,ensure_ascii=False)


        #Work yet to complete for this algorithm ---
                #context dependant opinion handling
                #adding more negation rules
                #applying synonym antonym rule
                #But caluse rule - done
                #calculating accuracy of the algorithm - done


                        
        
