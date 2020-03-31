# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 16:33:39 2020

@author: 91836
"""

from flask import *  
from flask_mysqldb import MySQL
import random
from resumeparser import *
from info import *
from text import *
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)  

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="user"

mysql=MySQL(app)
r=[[43,11,5,20],[30,15,11,25]]
 
pos=['JJ','NN','NNP','NNS','NNPS']
skills=[0,0,0,0]
names=["Devops","IOT","ML","WebApp"]

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
        
        #return "success"
        
        
    if request.method == 'GET':
        return render_template("result.html")  
 
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
        l=[]
        j=0
        '''
        for i in range(0,3):
            if j<extra:
                l.append(w[tracker+j])
                j+=1
            else:
                l.append("")
        predicted = classifier.predict([l])
        for i in range(0,extra):
            skills[predicted[i]]+=1
        '''
        bucket=[]
        for i in range(0,4):
            if(skills[i]>=(0.3*len(w))):
                bucket.append(names[i])
        
        print(skills)
        cur = mysql.connection.cursor()
        
        set_no=cur.execute("select max(set_no) from devops")
        mysql.connection.commit()
        s=random.randint(1,set_no)
        print(s)
        quiz=[]
        for element in bucket:
            query="select * from "+element.lower()
            set_no=cur.execute(query+" where set_no=%s",(s,))
            mysql.connection.commit()
            quiz.append(cur.fetchall())
        print(quiz)
        print(quiz[0])
        sending_data=[]
        for el in quiz[0]:
            l=[]
            for x in el:
                l.append(x)
            sending_data.append(l)    
        return render_template("quiz.html",data=json.dumps(sending_data),s=len(bucket))        
    
    
@app.route('/quiz',methods=['GET'])
def question_upload():
  
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


@app.route('/domain',methods=['POST'])
def domain():
    print("sasadasd");
    domain=request.json['domain']
    cur = mysql.connection.cursor()
    query="select * from "+domain
    cur.execute(query)
    resumes=cur.fetchall()
    ans=[]
    for i in range(0,2):
        l=[]
        for resume in resumes:
            res=[resume[3],resume[4],resume[5],resume[6]]
            result =(cosine_similarity([res], [r[i]])) * 4 + resume[7] * 0.6
            print(type(result))
            l.append(result[0][0])
        ans.append(l) 
    print(ans)
    
    second_stage=[0]*5
    for l in ans:
        for i in range(0,5):
            second_stage[i]+=l[i]
    for i in range(0,5):        
        second_stage[i] /=2        
    
    data=[]
    i=0
    for resume in resumes:
        info=Info(resume[0],resume[1],resume[2],second_stage[i])
        data.append(info)
        i+=1
    print(data)
    ids=[]
    name=[]
    score=[]
    sorted_data=merge_sort(data)
    sorted_data=sorted_data[::-1]
    for i in range(0,5):
        print(sorted_data[i].marks,end=" ")
        print(sorted_data[i].id_no,end=" ")
        print(sorted_data[i].name)
        score.append(sorted_data[i].marks)
        name.append(sorted_data[i].name)
        ids.append(sorted_data[i].id_no)
        
    print(name)
    print(ids)
    print(score)
    
    #return render_template("result.html",name=json.dumps(name),score=json.dumps(score),ids=json.dumps(ids),s=len(sorted_data))    



    
if __name__ == '__main__':  
    app.run()  