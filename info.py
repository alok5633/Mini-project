# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 19:43:57 2020

@author: Alok
"""

class Info:
    def __init__(self,id_no,name,mobile,marks):
        self.id_no=id_no
        self.name=name
        self.mobile=mobile
        self.marks=marks
        
        
def merge_sort(arr):#time comp nlogn
    if(len(arr)>1):
        m = len(arr)//2
        L = arr[:m]
        R = arr[m:]
        print(L)
        print(R)
        merge_sort(L)
        merge_sort(R)

        i = j = k = 0
        while(i<len(L) and j<len(R)):
            if(L[i].marks < R[j].marks):
                arr[k] = L[i]
                i+=1
            else:
                arr[k] = R[j]
                j+=1
            k+=1

        while(i<len(L)):
            arr[k] = L[i]
            i+=1
            k+=1

        while(j<len(R)):
            arr[k] = R[j]
            j+=1
            k+=1
    return arr      
        
    
        
        
           
        