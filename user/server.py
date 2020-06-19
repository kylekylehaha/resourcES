from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/sign_up.html', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        I_Name = request.values.get('Name')
        I_Email = request.values.get('Email')
        I_Ssn = request.values.get('Ssn')
        I_Password = request.values.get('Password')
        I_Department = request.values.get('Department')

        insert_tuple = (I_Name, I_Email, I_Ssn, I_Password, I_Department, None, None)
        print (insert_tuple)
         
        sql_insert_query = "INSERT into USER VALUES (%s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(sql_insert_query, insert_tuple) 
        db.commit()
        
        return 'Hello' + request.values.get('Ssn') 

    return render_template('sign_up.html')

@app.route('/sign_in.html', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        test_Ssn = request.values.get('Ssn')
        test_Password = request.values.get('Password')
        print (test_Password)
        
        sql_select_query = "SELECT Password FROM USER WHERE Ssn = %s;"
        cursor.execute(sql_select_query, test_Ssn)
        data = cursor.fetchone()
        print (data)
        if data is not None:
            if test_Password == data :
                return 'Hello' + test_Ssn
            else:
                return 'Password is wrong. Please try again.'
        else:
            return 'There isn\'t exist your data. Please sign up first.'

    return render_template('sign_in.html')

if __name__ == '__main__':
    #-----mysql connection-----
    f = open("../server/mysqlpasswd.txt",'r')
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
    app.debug = True
    app.run(host="0.0.0.0", port=11290)
