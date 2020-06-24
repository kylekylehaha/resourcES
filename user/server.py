from flask import Flask, render_template, request, flash, redirect, url_for
import pymysql
import os
import random
import time
import datetime

ts = time.time()
raw_timestamp = datetime.datetime.fromtimestamp(ts)
timestamp = raw_timestamp.strftime('%Y-%m-%d %H:%M:%S')
app = Flask(__name__)
app.secret_key = os.urandom(24)
date_format = "%Y-%m-%d %T"

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

        insert_tuple = (I_Name, I_Email, I_Ssn, I_Password, I_Department, None, 0)
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
    #------Reservation-----
    cursor.execute('SELECT Flag, Ename, R.Ssn, Renewal_limit, Loan_period, Notice, R.Enum, Ephoto, Max(Rank), DATE_FORMAT(Due_date,%s) FROM RESOURCES AS R JOIN BORROW AS B ON R.Enum=B.Enum WHERE Order_status <> 6 GROUP BY R.Enum',date_format) 
    
    data = cursor.fetchall()
    item_list = {}
    photo_list = {}
    
    for i in data:
        if i[0] == 1:
            item_list[i[6]] = [i[1],i[2],i[3],i[4],i[5],i[6],'需預約',i[8],i[9]]
            photo_list[i[6]] = i[7]
  
    #-----Borrow-----
    cursor.execute('SELECT Flag, Ename, Ssn, Renewal_limit, Loan_period, Notice, Enum, Ephoto FROM RESOURCES EXCEPT(SELECT Flag, Ename, R.Ssn, Renewal_limit, Loan_period, Notice, R.Enum, Ephoto FROM RESOURCES AS R JOIN BORROW AS B ON R.Enum=B.Enum WHERE Order_status <> 6)')
    data = cursor.fetchall()

    for i in data:
        if i[0] == 1:
            item_list[i[6]] = [i[1],i[2],i[3],i[4],i[5],i[6],'可借用']
            photo_list[i[6]] = i[7]

    return render_template("mall.html",item_list = item_list, photo_list = photo_list, Name=Name)
    
#-----keyword searching-----
@app.route('/keyword/<Name>',methods=['GET'])
def KeyWord(Name):
    '''
    Objective: keyword(in upper, lower, capitalized form) searching in the RESOURCES table
    Input: keyword from url
    Output: USER name, equipment details(e.g Name, renewal_limit, can borrow or not...)
    '''

    #-----get keyword from url-----
    keyword = '%'+ str(request.values.get('keyword')) + '%'

    #-----MYSQL command line-----
    #------Reservation-----
    cursor.execute('SELECT Flag, Ename, R.Ssn, Renewal_limit, Loan_period, Notice, R.Enum, Ephoto, Max(Rank), DATE_FORMAT(Due_date,%s) FROM RESOURCES AS R JOIN BORROW AS B ON R.Enum=B.Enum WHERE Order_status <> 6 AND Ename LIKE %s GROUP BY R.Enum',(date_format,keyword))
    data = cursor.fetchall()

    item_list = {}
    photo_list = {}
    
    for i in data:
        if i[0] == 1:
            item_list[i[6]] = [i[1],i[2],i[3],i[4],i[5],i[6],'需預約',i[8],i[9]]
            photo_list[i[6]] = i[7]

    #-----Borrow-----
    cursor.execute('SELECT Flag, Ename, Ssn, Renewal_limit, Loan_period, Notice, Enum, Ephoto FROM RESOURCES WHERE Ename LIKE %s EXCEPT(SELECT Flag, Ename, R.Ssn, Renewal_limit, Loan_period, Notice, R.Enum, Ephoto FROM RESOURCES AS R JOIN BORROW AS B ON R.Enum=B.Enum WHERE Order_status <> 6 AND Ename LIKE %s)',(keyword,keyword))
    data = cursor.fetchall()
    
    for i in data:
        if i[0] == 1:
            item_list[i[6]] = [i[1],i[2],i[3],i[4],i[5],i[6],'可借用']
            photo_list[i[6]] = i[7]

    return render_template("mall.html",item_list = item_list, photo_list = photo_list)

@app.route('/add',methods=['GET'])
def Add():
    #-----required data from url-----
    addtype = request.values.get('type') #reservation or borrow
    value = request.values.get('value') # yes or no
    name = request.values.get('name') #student id
    enum = request.values.get('enum') #equipment number
    
    ssn = Name2Ssn(name)

    if value == "yes":
        cursor.execute('SELECT Violation FROM USER WHERE Ssn=%s',ssn)
        data = int(cursor.fetchone()[0])

        if data >= 2:
            return "inviolation"

        if addtype == 'Reservation':
            cursor.execute('SELECT Order_status FROM BORROW WHERE Enum=%s AND Ssn=%s AND Order_status <> 6',(enum,ssn))
            data = cursor.fetchone()
           
            if data is None:
                cursor.execute('SELECT MAX(Rank) FROM BORROW WHERE Enum = %s',(enum))
                data = int(cursor.fetchone()[0])

                try:
                    order_num = GenerateCode(4,1)
                    cursor.execute('INSERT INTO BORROW VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(order_num, ssn , enum, None, None, 0, 0, data+1))
                    db.commit()
                except pymysql.Error as e:
                    print("Error %d: %s" % (e.args[0], e.args[1]))
                    if e.args[0] == PYMYSQL_DUPLICATE_ERROR:
                        return("duplicated")
            else:
                #print("cannotreserved")
                return "cannotreserved"

        if addtype == 'Borrow':
            print("borrow")
            cursor.execute('SELECT Ssn FROM RESOURCES WHERE Enum=%s',enum)
            data = str(cursor.fetchone()[0])
            
            if data == ssn:
                print("yourself")
                return "yourself"

            order_num = GenerateCode(4,1)
            try:
                cursor.execute('INSERT INTO BORROW VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(order_num, ssn, enum, timestamp, None, 1, 0,0))
                db.commit()
            except pymysql.Error as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
 
    return "ok"


@app.route('/borrowing/<Name>')
def borrowing(Name):
    sql_select_Ssn_query = "SELECT Ssn FROM USER WHERE Name = %s;"
    cursor.execute(sql_select_Ssn_query, Name)
    data = cursor.fetchall()
    Ssn = data[0][0]
    sql_select_borrow_query = "SELECT Enum, Rank, Date_out, Due_Date, Renewal_times, Order_status, Order_num FROM BORROW WHERE Ssn = %s;"
    cursor.execute(sql_select_borrow_query, Ssn)
    data_borrow = cursor.fetchall()

    #----- borrow_list(Enum, Rank, Date_out, Due_Date, Renewal_times, Order_status, Order_num, Ephoto, Renewal_flag) -----
    borrow_list = [[None for x in range(9)]for y in range(len(data_borrow))]
    
    for i in range(len(data_borrow)):
        for j in range(len(data_borrow[i])):
            borrow_list[i][j] = data_borrow[i][j]
    
    status_name = ['預約中', '待審核', '待領取', '已領', '續租審核', '拒租用', '已歸還']

    # ----- select Ename & Ephoto-----
    for i in range(len(borrow_list)):
        sql_select_Ename_query = "SELECT Ename, Ephoto FROM RESOURCES WHERE Enum = %s;"
        cursor.execute(sql_select_Ename_query, borrow_list[i][0])
        data_Ename_Ephoto = cursor.fetchall()
        borrow_list[i][0] = data_Ename_Ephoto[0][0]
        borrow_list[i][7] = data_Ename_Ephoto[0][1]
        #----- select Order_status name -----
        borrow_list[i][5] = status_name[borrow_list[i][5]]
        # ----- check whether Renewal_flag == 1 -----
        if RenewResource(borrow_list[i][6]) == 1:
            borrow_list[i][8] = 1
        else:
            borrow_list[i][8] = 0


    # ----- renewal flag request -----
    if request.method == 'POST':
        change_flag_index = request.values.get('Renewal_flag')
        sql_update_query = "UPDATE BORROW SET Order_status = 4 WHERE Order_num = %s;"
        cursor.execute(sql_update_query, borrow_list[change_flag_index][6])
        db.commit()
        return url_for('borrowing', Name=Name)


    return render_template('borrowing.html', borrow_list = borrow_list, Name=Name)

@app.route('/lend/<Name>', methods=['GET', 'POST'])
def lend(Name):
    #----- select Ssn -----
    sql_select_Ssn_query = "SELECT Ssn FROM USER WHERE Name = %s;"
    cursor.execute(sql_select_Ssn_query, Name)
    data_Ssn = cursor.fetchall()
    Ssn = data_Ssn[0][0]

    #----- receive new resources to insert into DB------
    if request.method == 'POST':
        I_Ename = request.values.get('Ename')
        I_Ephoto = request.values.get('Ephoto')
        if I_Ephoto == '':
            print ("fuck")
            I_Ephoto = "https://financemj.com/wp-content/uploads/2016/05/nophoto.png"

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
        #----- insert new resources -----
        sql_insert_query = "INSERT into RESOURCES VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        val = (I_Flag, I_Renewal_limit, Ssn, I_Ename, I_Notice, I_Ephoto, I_Loan_period, I_Enum)
        cursor.execute(sql_insert_query,val) 
        db.commit()

        #----- select lended equipment ------
        sql_select_lended_equip_query = "SELECT Enum, Renewal_limit, Loan_period, Notice, Flag FROM RESOURCES WHERE Ssn = %s;"
        cursor.execute(sql_select_lended_equip_query, Ssn)
        data_equip = cursor.fetchall()

        #-----create equip_list -----
        equip_list = [[None for x in range(5)]for y in range(len(data_equip))]
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

    #----- select lended equipment ------
    sql_select_lended_equip_query = "SELECT Enum, Renewal_limit, Loan_period, Notice, Flag FROM RESOURCES WHERE Ssn = %s;"
    cursor.execute(sql_select_lended_equip_query, Ssn)
    data_equip = cursor.fetchall()


    #-----create equip_list -----
    equip_list = [[None for x in range(5)]for y in range(len(data_equip))]
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

@app.route('/status/<Name>',methods=['GET'])
def Status(Name):
    '''
    * Required information:
    1. Name
    2. query for "lend" information or "borrow" information
    '''
    ssn = Name2Ssn(Name)
    infotype = request.values.get('type')

    if infotype == 'lend':
        #-----Order is not complete-----
        #print("lend")
        cursor.execute('SELECT Order_num, Flag, Ename, Renewal_limit, Loan_period, Notice, R.Enum, Ephoto, MAX(Order_status), MAX(Rank), Due_date FROM RESOURCES AS R JOIN BORROW AS B ON R.Enum=B.Enum WHERE R.Ssn=%s AND Order_status <> 0 AND Order_status <> 6 GROUP BY R.Enum',ssn)
        data = cursor.fetchall()
        #print(data)

        status = ""
        flag = ""
        item_list = {}
        photo_list = {}
        for i in data:
            if i[1] == 1:
                flag = "yes"
            else:
                flag = "no"

            if i[8] == 1:
                status = '待審核'
            if i[8] == 2:
                status = '待領取'
            if i[8] == 3:
                status = '已領取'
            if i[8] == 4:
                status = '續租審核'
            if i[8] == 5:
                status = '拒租用'

            #print(status)
            item_list[i[6]] = [i[0],flag,i[2],i[3],i[4],i[5],i[6],i[9],status,i[10]]
            photo_list[i[6]] = i[7]

        return render_template("status.html",item_list = item_list, photo_list = photo_list)

    if infotype == 'borrow':
        print("borrow")
        cursor.execute('SELECT Order_num, Ename, Renewal_limit, Loan_period, Notice, R.Enum, Ephoto, Order_status, Rank, Renewal_times, Due_date FROM RESOURCES AS R JOIN BORROW AS B ON R.Enum=B.Enum WHERE B.Ssn=%s AND Order_status <> 6',ssn)
        data = cursor.fetchall()
        #print(data)

        status = ""
        item_list = {}
        photo_list = {}
        flag_list = {}
        for i in data:
            if i[7] == 0:
                status = "預約中"
            if i[7] == 1:
                status = "待審核"
            if i[7] == 2:
                status = "待領取"
            if i[7] == 3:
                status = "已領取"
            if i[7] == 4:
                status = "續租審核中"
            if i[7] == 5:
                status = "拒租用請如期歸還"

            #print(status)
            if i[7] == 3:
                flag = RenewResource(i[0])
                flag_list[i[5]] = flag

            if i[7] != 0 and i[7] != 1 and i[7] != 2:
                item_list[i[5]] = [i[0],i[1],i[2],i[3],i[4],i[5],status,i[9],i[10]]
                photo_list[i[5]] = i[6]
            else:
                item_list[i[5]] = [i[0],i[1],i[2],i[3],i[4],i[5],status,i[8]]
                photo_list[i[5]] = i[6]
            
        #print(item_list)
        #print(photo_list)
        return render_template("borrow.html",item_list = item_list, photo_list = photo_list,flag_list = flag_list)
    
    if infotype == 'history_borrow':
        cursor.execute('SELECT Order_num, Ename, Renewal_limit, Loan_period, Notice, R.Enum, Ephoto, Order_status FROM RESOURCES AS R JOIN BORROW AS B ON R.Enum=B.Enum WHERE B.Ssn=%s AND Order_status = 6',ssn)
        data = cursor.fetchall()

        item_list = {}
        photo_list = {}
        for i in data:
            status = "訂單已完成"
            item_list[i[5]] = [i[0],i[1],i[2],i[3],i[4],i[5],status]
            photo_list[i[5]] = i[6]

        return render_template("history_borrow.html",item_list = item_list, photo_list = photo_list)

    if infotype == 'history_lend':
        cursor.execute('SELECT Order_num, Ename, Renewal_limit, Loan_period, Notice, R.Enum, Ephoto, Order_status FROM RESOURCES AS R JOIN BORROW AS B ON R.Enum=B.Enum WHERE R.Ssn=%s AND Order_status = 6',ssn)
        data = cursor.fetchall()

        item_list = {}
        photo_list = {}
        for i in data:
            status = "訂單已完成"
            item_list[i[5]] = [i[0],i[1],i[2],i[3],i[4],i[5],status]
            photo_list[i[5]] = i[6]
        
        return render_template("history_lend.html",item_list = item_list, photo_list = photo_list)
        
@app.route('/update_status',methods=['GET'])
def UpdateStatus():
    name = request.values.get('name')
    order_num = request.values.get('order_num')
    operation = request.values.get('operation')

    #-----Order_status = 1 or 4-----
    cursor.execute('SELECT Order_status FROM BORROW WHERE Order_num=%s',order_num)
    order_status = int(cursor.fetchone()[0])

    if order_status == 1:
        if operation == 'accept':
            cursor.execute('UPDATE BORROW SET Order_status = 2 WHERE Order_num = %s',order_num)
            db.commit()
        if operation == 'reject':
            cursor.execute('UPDATE BORROW SET Order_status = 5 WHERE Order_num = %s',order_num)
            db.commit()

    if order_status == 4:
        if operation == 'accept':
            cursor.execute('UPDATE BORROW SET Order_status = 3 WHERE Order_num = %s',order_num)
            db.commit()
            cursor.execute('UPDATE BORROW SET Renewal_times = Renewal_times + 1 WHERE Order_num = %s',order_num)
            db.commit()

            cursor.execute('SELECT R.Loan_period FROM RESOURCES AS R,BORROW AS B WHERE R.Enum = B.Enum AND B.Order_num = %s',order_num)
            db.commit()
            data = int(cursor.fetchone()[0])
            delta_time = datetime.timedelta(days = data)

            cursor.execute('SELECT Due_date FROM BORROW WHERE Order_num = %s', order_num)
            db.commit()
            due_date = cursor.fetchone()[0]
            due_date = (delta_time + due_date).strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute('UPDATE BORROW SET Due_date = %s WHERE Order_num= %s', (due_date, order_num))
            db.commit()
        if operation == 'reject':
            cursor.execute('UPDATE BORROW SET Order_status = 5 WHERE Order_num = %s',order_num)
            db.commit()
    #-----Order_status = 2-----
    if operation == 'out':
        cursor.execute('SELECT Loan_period FROM RESOURCES AS R JOIN BORROW AS B ON R.Enum=B.Enum WHERE Order_num=%s',order_num)
        db.commit()
        data = int(cursor.fetchone()[0])
        delta = datetime.timedelta(days=data)

        current_time = raw_timestamp
        due_date = (raw_timestamp + delta).strftime('%Y-%m-%d %H:%M:%S')
        print(due_date)

        try:
            cursor.execute('UPDATE BORROW SET Order_status=3,Date_out=%s,Due_date=%s WHERE Order_num=%s',(timestamp,due_date,order_num))
            db.commit()

        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
    
    #-----Order_status = 3-----
    if operation == 'apply_renew_resources':
        cursor.execute('UPDATE BORROW SET Order_status = 4 WHERE Order_num = %s',order_num)
        db.commit()

    #-----Order_status = 3 or 5-----
    if operation == 'done':
        cursor.execute('UPDATE BORROW SET Order_status = 6 WHERE Order_num = %s',order_num)
        db.commit()
        ReturnEquip(order_num)

    return "ok"

#-----add resources-----
@app.route('/addresources',methods=['GET'])
def AddResources():
    Ephoto = request.values.get('Ephoto')
    Ename = request.values.get('Ename')
    Ssn = request.values.get('Ssn')
    Notice = request.values.get('Notice') 
    Loan_period = request.values.get('Loan_period')
    Renewal_limit= request.values.get('Renewal_limit')
    Flag = request.values.get('Flag')
    Enum = GenerateCode(3,2)
    try:
        cursor.execute('INSERT INTO RESOURCES VALUES(%s, %s, %s, %s, %s, %s, %s, %s)',(Flag, Renewal_limit, Ssn, Ename, Notice, Ephoto, Loan_perioad, Enum))
        db.commit()
    except pymysql.Error as e:
        print('Error %d: %s' % (e.args[0], e.args[1]))

    return("ok")

#-----make resources (not) in use-----
@app.route('/flagto0or1',methods = ['GET'])
def FlagToZeroOrOne():
    Flag = request.values.get('Flag')
    Enum = request.values.get('Enum')
    cursor.execute('UPDATE RESOURCES SET Flag = %s WHERE Enum = %s',(Flag, Enum))
    db.commit()

#-----return equipment-----
def ReturnEquip(Order_num):
    '''
     Another version: w/o RESERVATION ; add attribute(Rank) into BORROW
    1. If now > Due_Date, USER.Violation += 1 ; Check if the user.Violation >= 2
    2. Update Order_status = 1 where Rank = 1 of this equipment
    3. Update Rank = Rank - 1 where status != 6 of this equipment
    '''
    #-----step1-----
    cursor.execute('SELECT DATE_FORMAT(Due_date,%s),Ssn,Enum FROM BORROW WHERE Order_num = %s',(date_format,Order_num))
    #data[0] = Due_date ; date[1] = Ssn ; data[2] = Enum 
    data = cursor.fetchone()
    print(data)
    if timestamp >= data[0]:
        cursor.execute('UPDATE USER SET Violation = Violation + 1 WHERE Ssn = %s',(data[1]))
        cursor.execute('SELECT Violation FROM USER WHERE Ssn=%s',data[1])
        Violation = cursor.fetchone()
        if Violation[0] >= 2:
            Punishment(data[1])

    #-----step2-----
    cursor.execute('UPDATE BORROW SET Order_status = 1 WHERE Enum = %s AND Rank = 1',(data[2]))
    db.commit()

    #-----step3-----
    cursor.execute('UPDATE BORROW SET Rank = Rank - 1 WHERE Enum = %s AND Order_status <> 6',data[2])
    db.commit()

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

def Name2Ssn(Name):
    cursor.execute('Select Ssn FROM USER WHERE Name=%s',Name)
    data = str(cursor.fetchone()[0])
    print(data)
    return data

def RenewResource(order_num):
    '''
    1. 當A訂單的Order_status = 3(已領取), 且不存在其他 與A訂單同一個Enum的訂單 的Order_status = 0,
       且已續借次數<器材可續借次數, 且Now() < Due_date)
    2. A訂單使用者即有選擇續借的權利, renew_flag = 1
    '''
    Renew_flag = 0
    cursor.execute('SELECT B.Enum FROM BORROW AS B, RESOURCES AS R WHERE B.Order_status = 3 AND B.Due_date > %s AND B.Order_num = %s AND B.Renewal_times < R.Renewal_limit AND B.Enum = R.Enum',(timestamp,order_num))
    db.commit()
    #data[0] = Enum
    data = cursor.fetchone()
    
    if data != None:
        cursor.execute('SELECT DISTINCT Order_status FROM BORROW WHERE Enum = %s AND Order_status = 0',data[0])
        status = cursor.fetchone()
        if status is None:
            Renew_flag = 1
    else:
        print("data none")
    return Renew_flag


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
