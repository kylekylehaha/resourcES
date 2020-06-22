from flask import Flask , render_template , request
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


@app.route('/test',methods=['GET'])
def test():
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
    
    return render_template("mall.html", dept_list = dept_list, item_list = item_list, photo_list = photo_list)

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
    
    app.debug=True

app.run(host="0.0.0.0" , port = 11290)
