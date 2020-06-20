from flask import Flask , render_template , request
import pymysql
import json
import os

#EQUIP_FOLDER = os.path.join('static','equip_img')  
app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = EQUIP_FOLDER


@app.route('/',methods=['GET'])
def home():
    cursor.execute("SELECT Dnum, Dname FROM DEPARTMENT")
    data = cursor.fetchall()
    #data = json.dumps(data)
   
    dept_list= {}
    for i in data:
        dept_list[i[0]]=i[1]
    #print(dept_list)

    cursor.execute("SELECT Due_date FROM USER,BORROW WHERE Violation = 2 AND USER.Ssn=BORROW.Ssn" )
    due_dates = cursor.fetchall()
    for due_date in due_dates:
        borrowing = due_date
        print(borrowing)
    

    #-----fetch photo test-----
 

    


    return render_template("index.html", dept_list = dept_list)

#def borrowing_time():

if __name__ == '__main__':
    #-----mysql connection-----
    f = open("mysqlpasswd.txt",'r')
    info=[]
    for line in f:
        line=line.strip('\n')
        info.append(line)

    db = pymysql.connect(
        host=info[0],
        port=int(info[1]),
        user=info[2],
        passwd=info[3],
        db='ResourcES',
        charset='utf8'
    )
    
    #-----create cursor object-----
    cursor = db.cursor()

    app.debug=True
    app.run(host="0.0.0.0" , port = 11230)
