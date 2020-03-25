# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 16:33:39 2020

@author: 91836
"""

from flask import *  
from flask_mysqldb import MySQL

from resumeparser import *
from text import *
app = Flask(__name__)  

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="quiz"

mysql=MySQL(app)
 
pos=['JJ','NN','NNP','NNS','NNPS']
skills=[0,0,0,0]

@app.route('/',methods=['GET','POST'])  
def index():  
    
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['pass']
        
        cur = mysql.connection.cursor()
        
        cur.execute("select email from user where email = %s",(email,))
        print(cur.fetchall())
        cur.execute("Insert into user(name,email,password) values (%s,%s,%s)",(name,email,password))
        
        mysql.connection.commit()
        
        cur.close()
        
        return "success"
        
        
    if request.method == 'GET':
        return render_template("login.html")  
 
@app.route('/register', methods = ['GET','POST'])  
def success():  
    if request.method == 'POST':  
        print("ssadadsda")
        email=request.form['email']
        print(email)
        f = request.files['file']
        print(f.filename)
        f.save("uploaded_files/"+f.filename)
        
        resume=Resume()
        resume_text=resume.convert("uploaded_files/"+f.filename)
        print(len(resume_text))
        resume_text=resume.stopwords(resume_text)
        print(len(resume_text))
        pos_tag=resume.postag(resume_text)
        print(pos_tag)
        
        w=[]
        for words in pos_tag[0]:
            if words[1] in pos:
                w.append(words[0])
        print(w)  
        #predicted = classifier.predict(["android","amqp","wemo","mongodb"])
        times=len(w)//4
        extra=len(w)%4
        count=0
        tracker=0
        while(count!=times):
            predicted = classifier.predict([w[tracker],w[tracker+1],w[tracker+2],w[tracker+3]])
            tracker=tracker+4
            count+=1
            for i in range(0,4):
                skills[predicted[i]]+=1
        print(skills)        
        return render_template("login.html")  
        '''
        resume=Resume()
        resume_string = resume.convert("Alok.pdf")
        resume_string = resume_string.replace(',',' ')
        #Converting all the charachters in lower case
        resume_string = resume_string.lower()
        print(resume.rating('nodejs'))
        return render_template("success.html", name = f.filename) 
        '''
    
    
@app.route('/quiz',methods=['POST'])
def question_upload():
    '''
    domain = request.json['domain']
    ques=request.json['ques']
    a=request.json['a']
    b=request.json['b']
    c=request.json['c']
    d=request.json['d']
    ans=request.json['ans']
    print(domain,ques,a,b,c,d,ans)
    cur = mysql.connection.cursor()
    s="Insert into "+domain
    cur.execute(s+"(set_no,ques,a,b,c,d,ans) values (%s,%s,%s,%s,%s,%s,%s)",(1,ques,a,b,c,d,ans))
    mysql.connection.commit()
    '''
    cur = mysql.connection.cursor()
    cur.execute("select skill from web")
    data=cur.fetchall()
    for row in data:
        web.append(row[0])
    mysql.connection.commit()
    resume=Resume()
    resume_string = resume.convert("resume.pdf")
        #Converting all the charachters in lower case
    resume_string = resume_string.lower()
    print(resume_string)
    st_words_rem=resume.stopwords(resume_string)
    print(st_words_rem)
    pos_tag=resume.postag(st_words_rem)
    print(pos_tag)
    w=[]
    for words in pos_tag[0]:
        if words[1] in pos:
            w.append(words[0])
    print(len(w))  
    print(web)      
    
          
if __name__ == '__main__':  
    app.run()  