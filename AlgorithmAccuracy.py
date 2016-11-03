#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk import word_tokenize
from textblob import TextBlob
import nltk
import glob
import json
import numpy as np
import scipy
import sklearn.metrics
from sklearn.metrics import precision_recall_fscore_support

ProductFeatureOrientationGiven=[]
ProductFeatureOrientationPredicted=[]


#features list for given product 
with open('C:\Users\Vinod Chhapariya\Desktop\TDBMS\Project\Features_Json_Files\Nokia6610.json') as data_file:    
        ProductFeaturesGiven = json.load(data_file)
for key in ProductFeaturesGiven:
        ProductFeatureOrientationGiven.append(ProductFeaturesGiven[key])

with open('C:\Users\Vinod Chhapariya\Desktop\TDBMS\Project\Features_Json_Files_Predicted\Nokia6610_Predicted.json') as data_file:    
        ProductFeaturesPredicted = json.load(data_file)
for key in ProductFeaturesPredicted:
        ProductFeatureOrientationPredicted.append(ProductFeaturesPredicted[key])


y_true = np.array(ProductFeatureOrientationGiven)
y_pred = np.array(ProductFeatureOrientationPredicted)
print 'Product Name - Nokia6610'
print precision_recall_fscore_support(y_true, y_pred, average='binary')

