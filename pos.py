# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 19:31:42 2020

@author: Alok
"""

import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer

#sample_text=state_union.raw("sample.txt")
f=open("sample.txt", "r")
custom_sent_tokenizer = PunktSentenceTokenizer()
tokenized = custom_sent_tokenizer.tokenize(f.read())
s=1
try:
    for i in tokenized:
        words=nltk.word_tokenize(i)
        tagged=nltk.pos_tag(words)
        print(tagged,"dwqwdqwqwd")
        print(s)
        s+=1
        
except Exception as e:
        print(str(e))