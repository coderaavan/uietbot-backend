from flask import Flask, render_template, request
import requests
import json
from support import keyWordExtractor
app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/response', methods=['GET','POST'])
def resp():
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

@app.route('/signup', methods=['POST'])
def signup():
    if request.method=='POST':
        signupdetail={}
        signupdetail["name"]=request.form['name']
        signupdetail["username"]=request.form['username']
        signupdetail["password"]=request.form['psw']
        d=json.dumps(signupdetail)
        r=requests.post("https://uiet-bot.glitch.me/users/register",json=d)
        print r.status_code
        if r.status_code=="200" or r.status_code==200:
            return "Signup Succesful!"
        else:
            return "Some Error"

if __name__=='__main__':
    app.run(debug=True)