# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 13:03:23 2020

@author: Alok
"""





import sklearn.datasets as skd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from sklearn import metrics
from sklearn.metrics import accuracy_score
import numpy as np

categories = ['web','ml']
news_train=skd.load_files('C:/Users/Alok/Pictures/Dataset/training',categories=categories,encoding='ISO-8859-1')
news_test=skd.load_files('C:/Users/Alok/Pictures/Dataset/testing',categories=categories,encoding='ISO-8859-1')


text_clf = Pipeline([('vect', TfidfVectorizer()), 
                      ('clf', MultinomialNB()) ])

# train the model
text_clf.fit(news_train.data, news_train.target)
# Predict the test cases
predicted = text_clf.predict(news_test.data)



print('Accuracy achieved is ' + str(np.mean(predicted == news_test.target)))
print(metrics.classification_report(news_test.target, predicted, target_names=news_test.target_names)),
metrics.confusion_matrix(news_test.target, predicted)


 