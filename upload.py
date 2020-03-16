# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 16:33:39 2020

@author: 91836
"""

from flask import *  
from flask_mysqldb import MySQL

from resumeparser import *
app = Flask(__name__)  

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="quiz"

mysql=MySQL(app)
 
pos=['JJ','NN','NNP','NNS','NNPS']
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
        return render_template("quiz_upload.html")  
 
@app.route('/login', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)  
        print("dsdasd")
        resume=Resume()
        resume_string = resume.convert("Alok.pdf")
        resume_string = resume_string.replace(',',' ')
        #Converting all the charachters in lower case
        resume_string = resume_string.lower()
        print(resume.rating('nodejs'))
        return render_template("success.html", name = f.filename)  
    
    
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
    
          
if __name__ == '__main__':  
    app.run()  