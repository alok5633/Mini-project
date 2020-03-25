import csv
import re
import spacy
import sys
#reload(sys)
import pandas as pd
#sys.setdefaultencoding('utf8')
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt
import numpy as np
import wikipedia
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen
from tika import parser
import PyPDF2
import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import stopwords

stopwords=set(stopwords.words("english"))


#Function converting pdf to string

class Resume:
   
    def __init__(self):
         self.web={"web":True,"browser":True,"mobile":True,"open-source":True,"mediawiki":True,"nodejs":True}
         self.database={"nosql":True,"server":True}
         self.w=0
         self.d=0;
    
    def rating(self,skill):
        
        a=wikipedia.WikipediaPage(title = 'nodejs').summary.lower()
        print(a)
        lis = []
        words=a.split()
        for word in words:
            lis.append(word)
            if word in self.web:
                 self.w +=1
            if word in self.database:
                 self.d +=1
        return(self.w)          
        
    def convert(self,path,pages=None):
        pdfFileObj = open(path, 'rb') 
  
        # creating a pdf reader object 
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
          
        # printing number of pages in pdf file 
        print(pdfReader.numPages) 
          
        # creating a page object 
        pageObj = pdfReader.getPage(0) 
          
        # extracting text from page 
        return (pageObj.extractText()) 
          
        # closing the pdf file object 
       
    def stopwords(self,string):
        #stopwords=set(stopwords.words("english"))
        print("stopwords list")
        custom_sent_tokenizer = PunktSentenceTokenizer()
        words = custom_sent_tokenizer.tokenize(string)
        fil_sent=[w for w in words if not w in stopwords]
        s=""
        for w in fil_sent:
            s=s+w+" "
        return s
        #return text
    def postag(self,string):
        custom_sent_tokenizer = PunktSentenceTokenizer()
        tokenized = custom_sent_tokenizer.tokenize(string)
        s=1
        try:
            for i in tokenized:
                words=nltk.word_tokenize(i)
                tagged=nltk.pos_tag(words)
                return (tagged,"dwqwdqwqwd")
                
                
        except Exception as e:
                print(str(e))
    #Function to extract names from the string using spacy
    def extract_name(self,string):
        r1 = str(string)
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(r1)
        for ent in doc.ents:
            if(ent.label_ == 'PER'):
                print(ent.text)
                break
    #Function to extract Phone Numbers from string using regular expressions
    def extract_phone_numbers(self,string):
        r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
        phone_numbers = r.findall(string)
        return [re.sub(r'\D', '', number) for number in phone_numbers]
    #Function to extract Email address from a string using regular expressions
    def extract_email_addresses(self,string):
        r = re.compile(r'[\w\.-]+@[\w\.-]+')
        return r.findall(string)

