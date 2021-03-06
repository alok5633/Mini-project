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
devops=[[43,11,5,20],[30,15,11,25]]
 
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
    d=[["Alok","Hitesh"],[1,2],[9.1,9,3]]    
        
    if request.method == 'GET':
        return render_template("result.html",data=json.dumps(d))  
 
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

@app.route('/ratings',methods=['POST'])
def ratings():
    resume_id=request.json['resume_id']
    rating=request.json['rating']
    rid=request.json['rid']
    print(resume_id)
    print(rating)
    print(rid)
    cur = mysql.connection.cursor()
    cur.execute("select rid from recruiter_rating where rid=%s",(rid,))
    data=cur.fetchall()
    print(len(data))
    if(len(data)==0):
        cur.execute("insert into recruiter_rating(rid,resumes,rating) values (%s,%s,%s)",(rid,resume_id,rating))
        mysql.connection.commit()
    else:
        cur.execute("select * from recruiter_rating where rid=%s",(rid,))
        data=cur.fetchall()
        resumes=data[0][1]
        ratings=data[0][2]
        resumes=resumes+","+resume_id
        ratings=ratings+","+rating
        print(resumes)
        print(ratings)
        
        cur.execute("update recruiter_rating set resumes=%s,rating=%s where rid=%s",(resumes,ratings,rid))
        mysql.connection.commit()
        
        
    return jsonify()

@app.route('/notification',methods=['POST'])
def notification():
    rid=request.json['rid']
    cur = mysql.connection.cursor()
    cur.execute("select * from recruiter_rating where rid=%s",(rid,))
    data=cur.fetchall()
    main_rec_resumes=data[0][1]
    main_rec_ratings=data[0][2]
    main_rec_resumes=main_rec_resumes.split(",")
    main_rec_ratings=main_rec_ratings.split(",")
    print(main_rec_resumes)
    print(main_rec_ratings)
    cur = mysql.connection.cursor()
    cur.execute("select * from recruiter_rating where rid!=%s",(rid,))
    data=cur.fetchall()
    users=[]
    match=[]
    for i in range(0,len(data)):
        count=0
        current_resume=data[i][1]
        current_resume=current_resume.split(",")
        for resume in main_rec_resumes:
            if resume in current_resume:
                count+=1
        users.append(data[i][0])
        match.append(count)
    print(users)
    print(match)        
            
        
    
    return jsonify()


@app.route('/domain',methods=['POST'])
def domain():
    print("sasadasd");
    domain=request.json['domain']
    
    cur = mysql.connection.cursor()
    query="select * from "+domain
    cur.execute(query)
    resumes=cur.fetchall()
    ans=[]
    exec("%s = %d" % (domain,2))
    for i in range(0,2):
        l=[]
        for resume in resumes:
            res=[resume[3],resume[4],resume[5],resume[6]]
            result =(cosine_similarity([res], [devops[i]])) * 4 + resume[7] * 0.6
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
    ds=[]
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
    ds=[name,ids,score]
    
    return jsonify({ 'var1': ds })   



    
if __name__ == '__main__':  
    app.run()  