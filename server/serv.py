from flask import Flask , render_template , request
import pymysql
import json

app = Flask(__name__)

IMG_Path = './static/equip_img/'

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
    cursor.execute("SELECT Flag, Renewal_limit, R.Ssn, Ename, Notice, Ephoto, Enumber, Loan_period, DATE_FORMAT(Date_out,%s), DATE_FORMAT(Due_date, %s), Order_status, COUNT(*) FROM RESOURCES AS R LEFT JOIN BORROW ON Enumber=Enum WHERE Ename LIKE %s AND Ename LIKE %s AND Ename LIKE %s GROUP BY Enumber",(date_format,date_format,keyword, upper_key, lower_key))
    data = cursor.fetchall()
    print(data)

    item_list = {}
    photo_list = {}
    for i in data:
        if i[0] == 1:
            print(type(i[10]))
            if i[10] == 5 or i[10] is None:
                allow_borr = 'Yes'
                item_list[i[3]] = [i[2],i[1],i[7],i[4],i[6],allow_borr]
            else:
                allow_borr = 'No'
                item_list[i[3]] = [i[2],i[1],i[7],i[4],i[6],allow_borr,i[11],i[9]]
            photo_list[i[3]] = i[5]
    print(item_list)
    print(photo_list)
    
    return render_template("index.html",item_list = item_list, photo_list = photo_list)

@app.route('/addreservation',methods=['GET'])
def AddReservation():

    return "ok"

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
    
    return render_template("index.html", dept_list = dept_list, item_list = item_list, photo_list = photo_list)

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
