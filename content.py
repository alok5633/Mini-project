# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:30:35 2020

@author: Alok
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from scipy import spatial

cat=[[0,60,10,20],[30,90,15,40],[25,67,80,91],[65,50,30,20],
     [30,40,60,10],[55,20,10,45],[40,55,12,10],[65,20,10,14],
     [70,42,25,85],[25,40,60,10]]
a=np.array(cat)
print(a.shape)
b=a[::-1]
ans=[]
for i in range(0,10):
    l=cat[i]
    out=[]
    for j in range(0,10):
        result =cosine_similarity([l], [cat[j]])
        out.append(result)
    ans.append(out)    


      