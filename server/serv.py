from flask import Flask , render_template , request
import pymysql
import json
app = Flask(__name__)

''''
@app.route('/test',methods=['GET'])
def test():
    cursor.execute("INSERT INTO USER(Name,Ssn) VALUES(%s,%s)",("Luben","E94056178"))
    db.commit() 
    return "ok"
'''

@app.route('/',methods=['GET'])
def home():
    cursor.execute("SELECT * FROM USER")
    data = cursor.fetchall()
    #data = json.dumps(data)
   
    name = []
    for i in range(len(data)):
        name.append(data[i][0])

    print(name)
    
    return render_template("index.html",content=name)

if __name__ == '__main__':
    #-----mysql connection-----
    db = pymysql.connect(
        host='220.132.225.158',
        port=8457,
        user='winnie56233',
        passwd='winnie1230',
        db='ResourcES',
        charset='utf8'
    )
    
    #-----create cursor object-----
    cursor = db.cursor()

    app.debug=True
    app.run(host="0.0.0.0" , port = 11230)
