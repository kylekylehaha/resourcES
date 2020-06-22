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
    
@app.route('/mall/<Name>', methods=['GET'])
def mall(Name):
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
    return "ok"
@app.route('/search', methods=['POST'])
def search():
    return "search function"


@app.route('/borrowing/<Name>')
def borrowing(Name):
    sql_select_Ssn_query = "SELECT Ssn FROM USER WHERE Name = %s;"
    cursor.execute(sql_select_Ssn_query, Name)
    data = cursor.fetchall()
    Ssn = data[0][0]
    sql_select_borrow_query = "SELECT Enum, Rank, Date_out, Due_Date, Renewal_times, Order_status FROM BORROW WHERE Ssn = %s;"
    cursor.execute(sql_select_borrow_query, Ssn)
    data_borrow = cursor.fetchall()

    borrow_list = [[None for x in range(6)]for y in range(len(data_borrow))]
    
    for i in range(len(data_borrow)):
        for j in range(len(data_borrow[i])):
            borrow_list[i][j] = data_borrow[i][j]
    
    # ----- select Ename -----
    for i in range(len(borrow_list)):
        sql_select_Ename_query = "SELECT Ename FROM RESOURCES WHERE Enum = %s;"
        cursor.execute(sql_select_Ename_query, borrow_list[i][0])
        data_Ename = cursor.fetchall()
        borrow_list[i][0] = data_Ename[0][0]
    
    return render_template('borrowing.html', borrow_list = borrow_list, Name=Name)

@app.route('/lend/<Name>', methods=['GET', 'POST'])
def lend(Name):
    #----- select Ssn -----
    sql_select_Ssn_query = "SELECT Ssn FROM USER WHERE Name = %s;"
    cursor.execute(sql_select_Ssn_query, Name)
    data_Ssn = cursor.fetchall()
    Ssn = data_Ssn[0][0]

    #----- receive new resources to insert into DB------
    I_Ename = request.values.get('Ename')
    I_Ephoto = request.values.get('Ephoto')
    I_Renewal_limit = request.values.get('Renewal_limit')
    I_Loan_period = request.values.get('Loan_period')
    Y_outside = request.values.get('Y_outside')
    N_outside = request.values.get('N_outside')
    I_Notice = request.values.get('Notice')
    if Y_outside == 'on':
        I_Flag = 1
    else:
        I_Flag = 0

    I_Enum = GenerateCode(3, 2)
    print (I_Renewal_limit)
    #----- insert new resources -----
    sql_insert_query = "INSERT into RESOURCES VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    val = (I_Flag, I_Renewal_limit, Ssn, I_Ename, I_Notice, I_Ephoto, I_Loan_period, I_Enum)
    cursor.execute(sql_insert_query,val) 
    db.commt()
    #----- select lended equipment ------
    sql_select_lended_equip_query = "SELECT Enum, Renewal_limit, Loan_period, Notice FROM RESOURCES WHERE Ssn = %s;"
    cursor.execute(sql_select_lended_equip_query, Ssn)
    data_equip = cursor.fetchall()


    #-----create equip_list -----
    equip_list = [[None for x in range(4)]for y in range(len(data_equip))]
    for i in range(len(data_equip)):
        for j in range(len(data_equip[i])):
            equip_list[i][j] = data_equip[i][j]

    #----- select Ename -----
    for i in range(len(equip_list)):
        sql_select_Ename_query = "SELECT Ename FROM RESOURCES WHERE Enum = %s;"
        cursor.execute(sql_select_Ename_query, equip_list[i][0])
        data_Ename = cursor.fetchall()
        equip_list[i][0] = data_Ename[0][0]

    return render_template('lend.html', Name=Name, equip_list=equip_list)

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
