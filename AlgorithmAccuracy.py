#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk import word_tokenize
from textblob import TextBlob
import nltk
import glob
import json
import pandas as pd



ProductFeatureOrientationGiven=[]
ProductFeatureOrientationPredicted=[]

#features list for given product 
with open('C:\Users\Vinod Chhapariya\Desktop\TDBMS\Project\Features_Json_Files\DVDPlayer.json') as data_file:    
        ProductFeaturesGiven = json.load(data_file)
for key in ProductFeaturesGiven:
        ProductFeatureOrientationGiven.append(ProductFeaturesGiven[key])

with open('C:\Users\Vinod Chhapariya\Desktop\TDBMS\Project\Features_Json_Files_Predicted\DVDPlayer_Predicted.json') as data_file:    
        ProductFeaturesPredicted = json.load(data_file)
for key in ProductFeaturesPredicted:
        ProductFeatureOrientationPredicted.append(ProductFeaturesPredicted[key])

print  ProductFeatureOrientationGiven
print len(ProductFeatureOrientationGiven)
print  ProductFeatureOrientationPredicted
print len(ProductFeatureOrientationPredicted)

F_Given = pd.Series(ProductFeatureOrientationGiven,name='Given')
F_Predicted = pd.Series(ProductFeatureOrientationPredicted,name='Predicted')
df_confusion = pd.crosstab(F_Given,F_Predicted)
print df_confusion
