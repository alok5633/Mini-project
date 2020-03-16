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
    #Converting pdf to string
    


'''
    #Information Extraction Function
    def extract_information(self,string):
        string.replace (" ", "+")
        query = string
        soup = BeautifulSoup(urlopen("https://en.wikipedia.org/wiki/" + query), "html.parser")
        #creates soup and opens URL for Google. Begins search with site:wikipedia.com so only wikipedia
        #links show up. Uses html parser.
        for item in soup.find_all('div', attrs={'id' : "mw-content-text"}):
            print(item.find('p').get_text())
            print('\n')
     
         
    with open('techatt.csv', 'rt') as f:
        reader = csv.reader(f)
        your_listatt = list(reader)
        print(your_listatt)
    with open('techskill.csv', 'rt') as f:
        reader = csv.reader(f)
        your_list = list(reader)
        print(your_list)
    with open('nontechnicalskills.csv', 'rt') as f:
        reader = csv.reader(f)
        your_list1 = list(reader)
        print(your_list1)
    #Sets are used as it has a a constant time for lookup hence the overall the time for the total code will not exceed O(n)
    s = set(your_list[0])
    s1 = your_list
    s2 = your_listatt
    skillindex = []
    skills = []
    skillsatt = []
    print('\n')
    extract_name(resume_string1)
    print('\n')
    print('Phone Number is')
    y = extract_phone_numbers(resume_string)
    y1 = []
    for i in range(len(y)):
        if(len(y[i])>9):
            y1.append(y[i])
    print(y1)
    print('\n')
    print('Email id is')
    print(extract_email_addresses(resume_string))
    print(s)
    for word in resume_string.split(" "):
        if word in s:
            skills.append(word)
    print(skills)        
    skills1 = list(set(skills))
    print('\n')
    print("Following are his/her Technical Skills")
    print('\n')
    np_a1 = np.array(your_list)
    for i in range(len(skills1)):
        item_index = np.where(np_a1==skills1[i])
        skillindex.append(item_index[1][0])
    
    nlen = len(skillindex)
    for i in range(nlen):
        print(skills1[i])
        #rating(skills1[i])
        #print(s2[0][skillindex[i]])
        print('\n')
    print(w)
    print(d)
    #Sets are used as it has a a constant time for lookup hence the overall the time for the total code will not exceed O(n)
    s1 = set(your_list1[0])
    nontechskills = []
    for word in resume_string.split(" "):
        if word in s1:
            nontechskills.append(word)
    nontechskills = set(nontechskills)
    print('\n')
    
    print("Following are his/her Non Technical Skills")
    list5 = list(nontechskills)
    print('\n')
    for i in range(len(list5)):
        print(list5[i])
    print('\n \n')
'''
