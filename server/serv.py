from flask import Flask , render_template , renuest
import pymysql
import json
import random
import time
import datetime

ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

app = Flask(__name__)

IMG_Path = './static/equip_img/'
PYMYSQL_DUPLICATE_ERROR = 1062

@app.route('/mall',methods=['GET'])
def Mall():
    cursor.execute('SELECT Flag, Ename, R.Ssn, Renewal_limit, Loan_period, Notice, Enumber, Order_status, Ephoto FROM RESOURCES AS R LEFT JOIN BORROW ON Enumber=Enum')
    data = cursor.fetchall()
    print(data)

    cursor.execute('SELECT Enum, COUNT(*) FROM BORROW WHERE Order_status=0 GROUP BY Enum')
    data1 = cursor.fetchall()
    print(data1)
    
    '''
    item_list = {}
    photo_list = {}
    for i in data:
        if i[0] == 1:
            if i[6] in reserv_list:
                reserv_num = reserv_list[i[6]]
            else:
                reserv_num = 0

            if i[10] == 5 or i[10] is None:
                allow_borr = 'Yes'
                item_list[i[3]] = [i[2],i[1],i[7],i[4],i[6],allow_borr]
            else:
                allow_borr = 'No'
                item_list[i[3]] = [i[2],i[1],i[7],i[4],i[6],allow_borr,reserv_num,i[9]]
            photo_list[i[3]] = i[5]
    print(item_list)
    print(photo_list)
    '''

    #return render_template("index.html",item_list = item_list, photo_list = photo_list)
    return "ok"

    
#-----keyword searching-----
@app.route('/keyword',methods=['GET'])
def KeyWord():
    '''
    Objective: keyword(in upper, lower, capitalized form) searching in the RESOURCES table
    Input: keyword from url
    Output: USER name, equipment details(e.g Name, renewal_limit, can borrow or not...)
    '''

    #-----get keyword from url-----
    keyword = str(request.values.get('keyword'))
    upper_key = '%' + keyword.upper() + '%' #keyword in upper form
    lower_key = '%' + keyword.lower() + '%' #keyword in lower form
    keyword = '%' + keyword + '%'

    #-----MYSQL command line-----
    #cursor.execute("SELECT * FROM RESOURCES WHERE Ename LIKE %s AND Ename LIKE %s AND Ename LIKE %s",(keyword,upper_key,lower_key))
    date_format = "%Y-%m-%d %T"
    cursor.execute("SELECT Flag, Renewal_limit, R.Ssn, Ename, Notice, Ephoto, Enumber, Loan_period, DATE_FORMAT(Date_out,%s), DATE_FORMAT(Due_date, %s), Order_status FROM RESOURCES AS R LEFT JOIN BORROW ON Enumber=Enum WHERE Ename LIKE %s AND Ename LIKE %s AND Ename LIKE %s GROUP BY Enumber",(date_format,date_format,keyword, upper_key, lower_key))

    data = cursor.fetchall()

    data1 = cursor.fetchall()
    print(data1)

    reserv_list = {}
    for i in data1:
        reserv_list[i[0]] = i[1]

    print(reserv_list)

    item_list = {}
    photo_list = {}
    for i in data:
        if i[0] == 1:
            if i[6] in reserv_list:
                reserv_num = reserv_list[i[6]]
            else:
                reserv_num = 0

            if i[10] == 5 or i[10] is None:
                allow_borr = 'Yes'
                item_list[i[3]] = [i[2],i[1],i[7],i[4],i[6],allow_borr]
            else:
                allow_borr = 'No'
                item_list[i[3]] = [i[2],i[1],i[7],i[4],i[6],allow_borr,reserv_num,i[9]]
            photo_list[i[3]] = i[5]
    print(item_list)
    print(photo_list)
   
    
    return render_template("index.html",item_list = item_list, photo_list = photo_list)

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
            try:
                cursor.execute('INSERT INTO BORROW VALUES(%s,%s,%s,%s,%s,%s,%s)',(order_num, ssn, enum, timestamp, None, 0,0))
                db.commit()
                print("success")
            except pymysql.Error as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
 
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
    try:
        cursor.execute('INSERT INTO RESOURCES VALUES(%s, %s, %s, %s, %s, %s, %s)',(Flag,Renewal_limit,Ssn,Ename,Notice,Ephoto,Loan_perioad,Enum))
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



#-----update order_status-------
@app.route('/updatestatus',methods = ['GET'])
def UpdateStatus():

    if Apply
    return 'ok':

#-----condition of renew resource-------
@app.route('/renewresource',methods = ['GET'])
def RenewResource():
    '''
    1.當A訂單的Order_status = 3(已領取), 且不存在其他 與A訂單同一個Enum的訂單 的Order_status = 0,
      且已續借次數<器材可續借次數, 且Now()<Due_date)
    2.A訂單使用者即有選擇續借的權利, renew_flag = 1
    #3.A訂單使用者提出申請 ,UPDATE BORROW SET Order_status = 4 WHERE Order_num = %s ;
    #4.等待出借者按下確認鍵, AGREE: UPDATE BORROW SET Order_status = 3 WHERE Order_num = %s , Renewal_times += 1 , Due_date += Loan_period
                         DISAGREE: UPDATE BORROW SET Order_status = 5 WHERE Order_num = %s
                         
    '''

    renew_flag = 0
    Order_num = request.values.get('Order_num')
    cursor.execute('SELECT B.Enum 
                    FROM BORROW AS B, RESOURCES AS R 
                    WHERE B.Order_status = 3 AND B.Due_date > timestamp AND B.Order_num = %s AND B.Renewal_times < B.Renewal_limits AND B.Enum = R.Enum',Order_num)
    db.commit()
    #data[0] = Enum
    data = cursor.fetchone()
    cursor.execute('SELECT DISTINCT Order_status FROM BORROW WHERE Enum = %s AND Order_status = 0',data[0])
    statuses = cursor.fetchone()
    if status == None:
        renew_flag = 1
    
    render_template(renew_flag = renew_flag)
        
    return 'ok'

#-----return equipment-----
@app.route('/returnequip',methods=['GET'])
def ReturnEquip():
    '''
    # Another version: w/o RESERVATION ; add attribute(Rank) into BORROW
    #1. Update BORROW Order_status to 6   
    #2. If now > Due_Date, USER.Violation += 1 ; Check if the user.Violation >= 2
    #3. Update Order_status = 1 where Rank = 1 of this equipment
    #4. Update Rank = Rank - 1 where status != 6 of this equipmen
    

    #-----required data from url-----
    Order_num = request.values.get('Order_num')
    
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
    cursor.execute('UPDATE BORROW SET Order_status = 1 WHERE Enum = %s AND Rank = 1',(data[2]))
    db.commit()
    
    #-----step4-----
    cursor.execute('UPDATE BORROW SET Rank = Rank - 1 WHERE Enum = %s AND Rank <> 6',data[2])
    db.commit()

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
