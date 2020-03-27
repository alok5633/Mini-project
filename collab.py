# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 17:25:25 2020

@author: Alok
"""
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from scipy import spatial

cat=[[3,1,4,0,5],[5,0,1,5,2],[0,0,2,5,1],[3,5,1,0,0],
     [4,1,2,4,0],[2,3,4,9,0],[3,1,0,1,1],[2,4,4,4,3],
     [1,0,0,5,2],[4,1,2,2,2]]
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


