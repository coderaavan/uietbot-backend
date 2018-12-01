from flask import Flask, render_template, request
import requests
import json
from support import keyWordExtractor
app = Flask(__name__, static_folder="static")
s = 'a'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/response', methods=['GET','POST'])
def resp():
    headers={'Authorization':s}
    if request.method=='POST':
        string=request.form['q']
        keywords=dict()
        keywords= keyWordExtractor(string)
        print keywords
        api_url=" "
        if keywords["Event"]=="assignments":
            api_url="https://uiet-bot.glitch.me/"+keywords["Event"]+"/"+keywords["Branch"]+"/"+keywords["Sem"]+"/"+keywords["Section"]+"?date="+keywords["Date"]+"&boa="+keywords["BOA"]
        elif keywords["Event"]=="exams":
            api_url="https://uiet-bot.glitch.me/"+keywords["Event"]+"/"+keywords["Branch"]+"/"+keywords["Sem"]+"?date="+keywords["Date"]+"&boa="+keywords["BOA"]
        print api_url
        query_data=json.loads(requests.get(api_url).text)
        print query_data
        return render_template('result.html', qd=query_data)

@app.route('/signup', methods=['POST','GET'])
def signup():
    headers={'Authorization': s}
    if request.method=='POST':
        signupdetail={}
        signupdetail["name"]=request.form['name']
        signupdetail["username"]=request.form['username']
        signupdetail["password"]=request.form['password']
        r=requests.post("https://uiet-bot.glitch.me/users/register",json=signupdetail, headers=headers)
        print r.status_code
        if r.status_code=="200" or r.status_code==200:
            return "Signup Succesful!"
        else:
            return "Some Error"

    elif request.method=='GET':
        return render_template('signupview.html')


@app.route('/login', methods=['POST','GET'])
def login():
    headers={'Authorization':s}
    if request.method=='POST':
        logindetail={}
        logindetail["username"]=request.form['username']
        logindetail["password"]=request.form['password']
        r=requests.post("https://uiet-bot.glitch.me/users/login",json=logindetail, headers=headers)
        print r.status_code
        if r.status_code=="200" or r.status_code==200:
            global s 
            s=json.loads(r.text)['token']
            return render_template('dashboard.html')
        else:
            return render_template('loginview.html',cond=True)

    elif request.method=='GET':
        return render_template('loginview.html',cond=False)

@app.route('/uploadAsgn', methods=['POST'])
def uploadAsgn():
    headers={'Authorization':s}
    if request.method=="POST":
        asgndetails={}
        asgndetails["title"]=request.form['title']
        asgndetails["branch"]=request.form['branch']
        asgndetails["semester"]=request.form['semester']
        asgndetails["section"]=request.form['section']
        asgndetails["details"]=request.form['details']
        asgndetails["date"]=request.form['date']
        r=requests.post("https://uiet-bot.glitch.me/assignments/put",json=asgndetails,headers=headers)
        if r.status_code==200 or r.status_code=="200":
            return render_template('dashboard.html')
        else:
            return render_template('dashboard.html')


@app.route('/uploadExam', methods=['POST'])
def uploadExam():
    headers={'Authorization':s}
    if request.method=="POST":
        examdetails={}
        examdetails["title"]=request.form['title']
        examdetails["branch"]=request.form['branch']
        examdetails["semester"]=request.form['semester']
        examdetails["subject"]=request.form['subject']
        examdetails["date"]=request.form['date']
        r=requests.post("https://uiet-bot.glitch.me/exams/put",json=asgndetails,headers=headers)
        if r.status_code==200 or r.status_code=="200":
            return render_template('dashboard.html')
        else:
            return render_template('dashboard.html')





if __name__=='__main__':
    app.run(debug=True)