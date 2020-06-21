from flask import Flask, render_template, request, flash, redirect, url_for
import pymysql
import os
import random
import time
import datetime

ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
app = Flask(__name__)
app.secret_key = os.urandom(24)
IMG_Path = './static/equip_img/'

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/sign_up.html', methods=['GET', 'POST'])
#-----Sign up function-----
def sign_up():
    sql_select_query = "SELECT Dnum, Dname FROM DEPARTMENT;"
    cursor.execute(sql_select_query)
    data = cursor.fetchall()
    Dept_list= {}
    for i in data:
        Dept_list[i[0]]=i[1]
    
    if request.method == 'POST':
        I_Name = request.values.get('Name')
        I_Email = request.values.get('Email')
        I_Ssn = request.values.get('Ssn')
        I_Password = request.values.get('Password')
        I_Department = request.values.get('Department')
        for i in data:
            if I_Department == i[1]:
                I_Department = i[0]
                break

        insert_tuple = (I_Name, I_Email, I_Ssn, I_Password, I_Department, None, None)
        sql_insert_query = "INSERT into USER VALUES (%s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(sql_insert_query, insert_tuple) 
        db.commit()
        
        return render_template('member.html', Name=I_Name) 
    
    return render_template('sign_up.html')

@app.route('/sign_in.html', methods=['GET', 'POST'])
#-----Sign in function-----
def sign_in():
    if request.method == 'POST':
        test_Ssn = request.values.get('Ssn')
        test_Password = request.values.get('Password')
        sql_select_query = "SELECT Password, Name FROM USER WHERE Ssn = %s;"
        cursor.execute(sql_select_query, test_Ssn)
        data = cursor.fetchall()
        S_data = data[0][0]
        S_Name = data[0][1]
        if data is not None:
            if test_Password == S_data :
                return redirect(url_for('member', Name=S_Name))
            else:
                return render_template('sign_in.html')
        else:
            return render_template('sign_up.html')

    return render_template('sign_in.html')

@app.route('/member/<Name>')
#----- member interface -----
def member(Name):
    return render_template('member.html', Name = Name)

@app.route('/search', methods=['GET', 'POST'])
#----- search interface -----
def search():
    if request.method == 'POST':
        search_item = request.values.get('search_query')
        print (search_item)
        #----- Add winnie's search fucntion -----
        return 'Found' + search_item
    return render_template('search.html')

@app.route('/member_info/<Name>')
#----- member information -----
def member_info(Name):
    #----- select Name information -----
    
    sql_select_query = "SELECT Name, Ssn, Department, Email, Violation FROM USER WHERE Name = %s;"
    cursor.execute(sql_select_query, Name)
    data = cursor.fetchall()
    S_Name = data[0][0] 
    S_Ssn = data[0][1]
    S_Dept = data[0][2]
    S_Email = data[0][3]
    S_Violation = data[0][4]
    sql_selectname_query = "SELECT Dname FROM DEPARTMENT WHERE Dnum = %s"
    cursor.execute(sql_selectname_query, S_Dept)
    data_dept = cursor.fetchall()
    S_Dname = data_dept[0][0]
    return render_template('member_info.html', Name=S_Name, Ssn=S_Ssn, Dept=S_Dname, Email=S_Email, Violation=S_Violation )
    
@app.route('/mall', methods=['GET'])
def mall():
    #----- equiment mall homepage -----
    cursor.execute("SELECT Dnum, Dname FROM DEPARTMENT")
    data = cursor.fetchall()
    
    dept_list= {}
    for i in data:
        dept_list[i[0]]=i[1]

    cursor.execute("SELECT * FROM RESOURCES WHERE Ename LIKE '%Arduino%' GROUP BY Ssn")
    data = cursor.fetchall()

    item_list = {}
    photo_list = {}
    for i in data:
        if i[0] == 1:
            item_list[i[3]] = [i[2],i[1],i[7],i[4]]
            photo_list[i[3]] = i[5]
    
    return render_template("mall.html", dept_list = dept_list, item_list = item_list, photo_list = photo_list)


@app.route('/add',methods=['GET'])
def Add():
    #-----required data from url-----
    addtype = request.values.get('type') #reservation or borrow
    value = request.values.get('value') # yes or no
    ssn = request.values.get('ssn') #student id
    enum = request.values.get('enum') #equipment number
    
    if value == "yes":
        if addtype == 'Reservation':
            print("reservation")
            cursor.execute('SELECT MAX(Rank) FROM RESERVATION WHERE Enum = %s',(enum))
            data = int(cursor.fetchone()[0])
            print(type(data))
            
            try:
                cursor.execute('INSERT INTO RESERVATION(Ssn, Rank, Enum) VALUES (%s, %s, %s)',(ssn, data+1, enum))
                db.commit()
                print("commit finish")
            except pymysql.Error as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
                if e.args[0] == PYMYSQL_DUPLICATE_ERROR:
                    return("duplicated")
        if addtype == 'Borrow':
            print("borrow")
            order_num = GenerateCode(4,1)
            print(enum)
            try:
                cursor.execute('INSERT INTO BORROW VALUES(%s,%s,%s,%s,%s,%s,%s)',(order_num, ssn, enum, timestamp, None, 0,0))
                db.commit()
                print("success")
            except pymysql.Error as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
 
    return "ok"

#----- other function -----
def GenerateCode(l,n):
    #l: number of letters
    #n: number of numbers

    ret = ""
    for i in range(l):
        letter = chr(random.randint(97, 122))
        Letter = chr(random.randint(65, 90))
        s = str(random.choice([letter, Letter]))
        ret += s
    for i in range(n):
        number = str(random.randint(0,9))
        ret += number
    return ret

if __name__ == '__main__':
    #----- mysql connection -----
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
