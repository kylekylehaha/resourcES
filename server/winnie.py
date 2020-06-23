from flask import Flask , render_template , request
import pymysql
import json
import random
import time
import datetime

ts = time.time()
raw_timestamp = datetime.datetime.fromtimestamp(ts)
timestamp = raw_timestamp.strftime('%Y-%m-%d %H:%M:%S')
date_format = "%Y-%m-%d %T"

app = Flask(__name__)

IMG_Path = './static/equip_img/'
PYMYSQL_DUPLICATE_ERROR = 1062

@app.route('/mall/<Name>',methods=['GET'])
def Mall(Name):
    print(Name)
    #------Reservation-----
    print("-----Reservation-----")
   
    cursor = db.cursor()
    cursor.execute('SELECT Flag, Ename, R.Ssn, Renewal_limit, Loan_period, Notice, R.Enum, Ephoto, Max(Rank), DATE_FORMAT(Due_date,%s) FROM RESOURCES AS R JOIN BORROW AS B ON R.Enum=B.Enum WHERE Order_status <> 6 GROUP BY R.Enum',date_format) 
    
    data = cursor.fetchall()
    print(data)

    item_list = {}
    photo_list = {}
    
    for i in data:
       if i[0] == 1:
            item_list[i[6]] = [i[1],i[2],i[3],i[4],i[5],i[6],'需預約',i[8],i[9]]
            photo_list[i[6]] = i[7]
  
    #-----Borrow-----
    print("-----Borrow-----")
    cursor = db.cursor()
    cursor.execute('SELECT Flag, Ename, Ssn, Renewal_limit, Loan_period, Notice, Enum, Ephoto FROM RESOURCES EXCEPT(SELECT Flag, Ename, R.Ssn, Renewal_limit, Loan_period, Notice, R.Enum, Ephoto FROM RESOURCES AS R JOIN BORROW AS B ON R.Enum=B.Enum WHERE Order_status <> 6)')
    data = cursor.fetchall()
    cursor.close()
    print(data)

    for i in data:
        if i[0] == 1:
            item_list[i[6]] = [i[1],i[2],i[3],i[4],i[5],i[6],'可借用']
            photo_list[i[6]] = i[7]

    #print(item_list)
    #print(photo_list)

    print(Name)
    return render_template("index.html",item_list = item_list, photo_list = photo_list)
    
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
    print("-----Reservation-----")
    cursor.execute('SELECT Flag, Ename, R.Ssn, Renewal_limit, Loan_period, Notice, R.Enum, Ephoto, Max(Rank), DATE_FORMAT(Due_date,%s) FROM RESOURCES AS R JOIN BORROW AS B ON R.Enum=B.Enum WHERE Order_status <> 6 AND Ename LIKE %s GROUP BY R.Enum',(date_format,keyword))
    data = cursor.fetchall()
    print(data)

    item_list = {}
    photo_list = {}
    
    for i in data:
        if i[0] == 1:
            item_list[i[6]] = [i[1],i[2],i[3],i[4],i[5],i[6],'需預約',i[8],i[9]]
            photo_list[i[6]] = i[7]

    #-----Borrow-----
    print("-----Borrow-----")
    cursor.execute('SELECT Flag, Ename, Ssn, Renewal_limit, Loan_period, Notice, Enum, Ephoto FROM RESOURCES WHERE Ename LIKE %s EXCEPT(SELECT Flag, Ename, R.Ssn, Renewal_limit, Loan_period, Notice, R.Enum, Ephoto FROM RESOURCES AS R JOIN BORROW AS B ON R.Enum=B.Enum WHERE Order_status <> 6 AND Ename LIKE %s)',(keyword,keyword))
    data = cursor.fetchall()
    print(data)
    
    for i in data:
        if i[0] == 1:
            item_list[i[6]] = [i[1],i[2],i[3],i[4],i[5],i[6],'可借用']
            photo_list[i[6]] = i[7]

    #print(item_list)
    #print(photo_list)
    
    print(Name)
    print(Name2Ssn(Name))

    return render_template("index.html",item_list = item_list, photo_list = photo_list)

@app.route('/add',methods=['GET'])
def Add():
    #-----required data from url-----
    addtype = request.values.get('type') #reservation or borrow
    value = request.values.get('value') # yes or no
    name = request.values.get('name') #student id
    enum = request.values.get('enum') #equipment number
    
    ssn = Name2Ssn(name)
    print(ssn)

    if value == "yes":
        if addtype == 'Reservation':
            print("reservation")

            cursor.execute('SELECT Order_status FROM BORROW WHERE Enum=%s AND Ssn=%s AND Order_status <> 6',(enum,ssn))
            data = cursor.fetchone()
            print(data)
           
            if data is None:
                print("make a reservation")
                
                cursor.execute('SELECT MAX(Rank) FROM BORROW WHERE Enum = %s',(enum))
                data = int(cursor.fetchone()[0])

                try:
                    order_num = GenerateCode(4,1)
                    cursor.execute('INSERT INTO BORROW VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(order_num, ssn , enum, None, None, 0, 0, data+1))
                    db.commit()
                    print("commit finish")
                except pymysql.Error as e:
                    print("Error %d: %s" % (e.args[0], e.args[1]))
                    if e.args[0] == PYMYSQL_DUPLICATE_ERROR:
                        return("duplicated")
            else:
                print("cannotreserved")
                return "cannotreserved"

        if addtype == 'Borrow':
            print("borrow")
            order_num = GenerateCode(4,1)
            try:
                cursor.execute('INSERT INTO BORROW VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(order_num, ssn, enum, timestamp, None, 1, 0,0))
                db.commit()
                print("success")
            except pymysql.Error as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
 
    return "ok"

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
        print("lend")
        cursor.execute('SELECT Order_num, Flag, Ename, Renewal_limit, Loan_period, Notice, R.Enum, Ephoto, MAX(Order_status), MAX(Rank) FROM RESOURCES AS R JOIN BORROW AS B ON R.Enum=B.Enum WHERE R.Ssn=%s AND Order_status <> 0 AND Order_status <> 6 GROUP BY R.Enum',ssn)
        data = cursor.fetchall()
        print(data)

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
            if i[8] == 5:
                status = '拒租用'

            print(status)
            item_list[i[6]] = [i[0],flag,i[2],i[3],i[4],i[5],i[6],i[9],status]
            photo_list[i[6]] = i[7]

        return render_template("status.html",item_list = item_list, photo_list = photo_list)
 
    if infotype == 'borrow':
        print("borrow")
        cursor.execute('SELECT Order_num, Ename, Renewal_limit, Loan_period, Notice, R.Enum, Ephoto, Order_status, Rank, Renewal_times FROM RESOURCES AS R JOIN BORROW AS B ON R.Enum=B.Enum WHERE B.Ssn=%s',ssn)
        data = cursor.fetchall()
        print(data)

        status = ""
        item_list = {}
        photo_list = {}
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
                status = "續租審核"
            if i[7] == 5:
                status = "拒租用"

            print(status)
            if i[7] != 0:
                item_list[i[5]] = [i[0],i[1],i[2],i[3],i[4],i[5],status,i[9]]
                photo_list[i[5]] = i[6]
            else:
                item_list[i[5]] = [i[0],i[1],i[2],i[3],i[4],i[5],status,i[8]]
                photo_list[i[5]] = i[6]
            
        print(item_list)
        print(photo_list)
        return render_template("borrow.html",item_list = item_list, photo_list = photo_list)

    #return "ok"

@app.route('/update_status',methods=['GET'])
def UpdateStatus():
    name = request.values.get('name')
    order_num = request.values.get('order_num')
    operation = request.values.get('operation')

    #-----Order_status = 1-----
    if operation == 'accept':
        cursor.execute('UPDATE BORROW SET Order_status = 2 WHERE Order_num = %s',order_num)
        db.commit()
    if operation == 'reject':
        cursor.execute('UPDATE BORROW SET Order_status = 5 WHERE Order_num = %s',order_num)
        db.commit()

    #-----Order_status = 2-----
    if operation == 'out':
        cursor.execute('SELECT Loan_period FROM RESOURCES AS R JOIN BORROW AS B ON R.Enum=B.Enum WHERE Order_num=%s',order_num)
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

    #-----Order status = 5-----
    #if operation == 'return':
        

    return "ok"

#-------yuyun-------
@app.route('/violation',methods=['GET'])
def Violation():
    cursor.execute('SELECT Ssn FROM USER WHERE Violation>=2')
    Ssns=cursor.fetchall()
    for Ssn in Ssns:
        cursor.execute('SELECT Borrowing_time FROM USER WHERE Ssn=%s',Ssn[0])
        db.commit()
        Borrowing_time = cursor.fetchone()
        print(Borrowing_time[0])
        if Borrowing_time[0] is None:
            cursor.execute('UPDATE USER SET Borrowing_time = %s + interval 1 month WHERE Ssn=%s',(timestamp,Ssn[0]))
            db.commit()
        else:
            cursor.execute('UPDATE USER SET Borrowing_time = Borrowing_time + interval 1 month WHERE Ssn=%s',(Ssn[0]))
            db.commit()
    return 'ok'

#-----return equipment-----
@app.route('/returnequip',methods=['GET'])
def ReturnEquip():
    '''
    1. Update BORROW Order_status 
    1-2.If now > Due_Date, USER.Violation += 1 ; Check if the user.Violation >= 2
    2. Check if there is any reservation of this equipment
    3. Get the information of rank = 1 of this equipment from RESERVATION
    4. DELETE Rank = 1
    (e.g. DELETE FROM RESERVATION WHERE Enum='ael23' AND Rank = 1)
    5. Update Rank
    (e.g. UPDATE RESERVATION SET Rank=Rank-1 WHERE Enum='ael23')
    '''
    '''
    Another version: w/o RESERVATION ; add attribute(Rank) into BORROW
    1. Update BORROW Order_status 
    2. If now > Due_Date, USER.Violation += 1 ; Check if the user.Violation >= 2
    3. Update Rank = 1 to Rank = 0 of this equipment from BORROW
    4. Check if there is any reservation (Rank != 0)of this equipment
    5. Update Rank
    6. Update Order_status = 1 where Rank=1 
    '''
    '''
    1. Update BORROW Order_status to 6   
    2. If now > Due_Date, USER.Violation += 1 ; Check if the user.Violation >= 2
    3. Update Rank = Rank - 1 where status != 6 of this equipment
    4. Update Order_status = 1 where Rank = 0 and Order_status != 6
 
    '''
    #QQ假定傳回來的是Order_num

    #-----required data from url-----
#   Order_num = request.values.get('Order_num')
    Order_num = 'aaaa0'
    #-----step1-----
    cursor.execute('UPDATE BORROW SET Order_status = %s WHERE Order_num=%s',(5,Order_num))
    #-----step2-----
    date_format = "%Y-%m-%d %T"    
    cursor.execute('SELECT DATE_FORMAT(Due_date,%s),Ssn,Enum FROM BORROW WHERE Order_num = %s',(date_format,Order_num))
    #data[0] = Due_date ; date[1] = Ssn ; data[2] = Enum 
    data = cursor.fetchone()
    if timestamp >= data[0]:
        cursor.execute('UPDATE USER SET Violation = Violation + 1 WHERE Ssn = %s',(data[1]))
        cursor.execute('SELECT Violation FROM USER WHERE Ssn=%s',data[1])
        Violation = cursor.fetchone()
        if Violation[0] >= 2:
            Punishment(data[1])
    #-----step3-----
    cursor.execute('UPDATE BORROW SET Rank = %s WHERE Order_num = %s',(0,Order_num))
    db.commit()
    #-----step4&5-----
    print(data[2])
    cursor.execute('UPDATE BORROW SET Rank = Rank - 1 WHERE Enum = %s AND Rank <> 0',data[2])
    db.commit()
    #-----step6------
    cursor.execute('UPDATE BORROW SET Order_status = 1 WHERE Enum = %s AND Rank = 1',(data[2:]))

    return "ok"

@app.route('/test',methods=['GET'])
def test():
    '''
    date = raw_timestamp
    print(date)
    delta = datetime.timedelta(days=30)
    print(date+delta)
    '''
    cursor.execute('SELECT Loan_period FROM RESOURCES WHERE Enum=%s','ael23')
    delta = int(cursor.fetchone()[0])
    print(delta)

    
    #cursor.execute("INSERT INTO USER(Name,Ssn) VALUES(%s,%s)",("Luben","E94056178"))
    #db.commit() 
    return "ok"

@app.route('/',methods=['GET'])
def home():
    cursor.execute("SELECT Dnum, Dname FROM DEPARTMENT")
    data = cursor.fetchall()
    #data = json.dumps(data)
    
    '''
    content=[] #data type : list
    for i in range(len(data)):
        value = list(data[i])
        content[i] = value
    '''
    dept_list= {}
    for i in data:
        dept_list[i[0]]=i[1]
    #print(dept_list)

    cursor.execute("SELECT * FROM RESOURCES WHERE Ename LIKE '%Arduino%' GROUP BY Ssn")
    data = cursor.fetchall()
    print(data)

    item_list = {}
    photo_list = {}
    for i in data:
        if i[0] == 1:
            item_list[i[3]] = [i[2],i[1],i[7],i[4]]
            photo_list[i[3]] = i[5]
    print(item_list)
    print(photo_list)
    
    return render_template("index.html", dept_list = dept_list, item_list = item_list, photo_list = photo_list)

#-----Other functions-----
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


def Punishment(Ssn):
    cursor.execute('SELECT borrowing_time FROM USER WHERE Ssn=%s',Ssn)
    db.commit()
    Borrowing_time = cursor.fetchone()
    print(Borrowing_time[0])
    if Borrowing_time[0] is None:
        cursor.execute('UPDATE USER SET Borrowing_time = %s + interval 1 month WHERE Ssn=%s',(timestamp,Ssn))
        db.commit()
    else:
        cursor.execute('UPDATE USER SET Borrowing_time = Borrowing_time + interval 1 month WHERE Ssn=%s',(Ssn))
        db.commit()
    return 'ok'

def Name2Ssn(Name):
    cursor.execute('Select Ssn FROM USER WHERE Name=%s',Name)
    data = str(cursor.fetchone()[0])
    return data

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

app.run(host="0.0.0.0" , port = 11240)
