# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 22:24:05 2020

@author: Alok
"""

import sklearn
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np

from sklearn import linear_model,preprocessing

data=pd.read_csv("classifier.data")
print(data.head)
'''
le=preprocessing.LabelEncoder()
cl=le.fit_transform(list(data["class"])) 
'''
predict="class"

#print(cl)
print(data["web"])


X=list(zip(data["ml"],data["web"],data["iot"],data["devops"]))
y=list(data["class"])
print(X)
print(y)

x_train,x_test,y_train,y_test=sklearn.model_selection.train_test_split(X,y,test_size=0.2)
names=["ml","web","iot","devops"]

model=KNeighborsClassifier(n_neighbors=6)
model.fit(x_train,y_train)
acc=model.score(x_test,y_test)
print(acc)

predicted=model.predict(x_test)

for x in range(len(predicted)):
    print("Predicted: ",names[predicted[x]],"Data: ",x_test[x],"Actual: ",names[y_test[x]])
    

