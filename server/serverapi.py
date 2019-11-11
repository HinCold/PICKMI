from fun import *
import os
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from flask import request
import time
import json
import pymssql
from dbtest import PYSQL
import uuid

app = Flask(__name__)

# 查询是否有订单未完成
# 反馈实时位置
# 查询订单状态
# 评价
@app.route('/remark', methods=['POST'])
def remark():
    ident = request.form.get('ide')
    oid = request.form.get('oid')
    remark = request.form.get('remark')
    my = PYSQL('localhost', 'test', '123', 'pickme')
    if ident == 'passager':
        sql = "insert into order(comment1) values('{}') where orderid='{}'".format(remark, oid)
    else:
        sql = "insert into order(comment2) values('{}') where orderid='{}'".format(remark, oid)
    result = my.insert_date(sql)
    msg = 'success'
    res = {
        "status": 0,
        "msg": msg
    }
    my.close()
    return json.dumps(res)
# passager get driver data 乘客获取司机信息
@app.route('/quikcar/data')
def getquikcar_data():
    oid = request.args.get("oid")
    '''
    requery database
    '''
    my = PYSQL('localhost', 'test', '123', 'pickme')
    sql = "SELECT dusername FROM orders WHERE orderid = '{}'".format(oid)
    did1 = my.select_data(sql)
    did2 = did1[0]
    did = did2[0]
    sql = "SELECT dname,dsex,year(getdate())-year(dbirth),cycletype,dtel FROM driver WHERE dusername = '{}'".format(did)
    suer1 = my.select_data(sql)
    suer = suer1[0]
    res = {
        "status": 0,
        "data": {
            "msg": "seccess",
            "username": did,
            "name": suer[0],
            "sex": suer[1],
            "age": suer[2],
            "type": suer[3],
            "tel":suer[4]
        }
    }
    return json.dumps(res, ensure_ascii=False)
# driver take quik car order 司机接快车订单
@app.route('/driver/quikcar/tkod')
def takeQcOrder():
    oid = request.args.get("oid")
    driverid = request.args.get("did")
    '''
    updata database
    '''
    my = PYSQL('localhost', 'test', '123', 'pickme')
    sql = "UPDATE orders SET dusername ='{}' WHERE orderid ='{}'".format(driverid, oid)
    my.update_data(sql)
    sql = "SELECT susername FROM orders WHERE orderid = '{}'".format(oid)
    susername1 = my.select_data(sql)
    susername2 = susername1[0]
    susername = susername2[0]
    sql = "SELECT sname,ssex,year(getdate())-year(sbirth),stel FROM student WHERE susername = '{}'".format(susername)
    suer1 = my.select_data(sql)
    suer = suer1[0]
    res = {
        "status": 0,
        "data": {
            "msg": "seccess",
            "username": susername,
            "name": suer[0],
            "sex": suer[1],
            "age": suer[2],
            "tel": suer[3]
        }
    }
    return json.dumps(res, ensure_ascii=False)


# passager release quik car order 乘客发布快车订单  价钱待加
@app.route('/quikcar/release')
def releaseQcar():
    username = request.args.get("user")
    startPlace = request.args.get("stp")
    destination = request.args.get("des")
    date = request.args.get("date")
    time = request.args.get("time")

    '''
    add into database
    '''
    my = PYSQL('localhost', 'test', '123', 'pickme')
    sql = "INSERT INTO orders(susername,fast_car,startpoint,endpoint,sdate,stime) VALUES('{}',1,'{}','{}','{}','{}')".format(username,startPlace,destination, date,time)
    my.insert_date(sql)
    sql =  "SELECT orderid FROM orders WHERE susername='{}' AND startpoint ='{}' AND endpoint = '{}'AND sdate ='{}'AND stime ='{}'".format(username, startPlace, destination, date,time)
    orderid1 = my.select_data(sql)

    my.close()
    orderid2 = orderid1[0]
    orderid = orderid2[0]
    res = {
        "status": 0,
        "msg": "success",
        "data": {"oid": orderid}
        }
    return json.dumps(res)

# driver get tail wind car order data 司机获取订单数据(order 代表订单类型1是快车，2是顺风车)
@app.route('/driver/twc/data')
def getTwc_data():
    order = request.args.get("order")
    date = request.args.get("date")
    time1 = request.args.get("time1")
    time2 = request.args.get("time2")
    data =[]
    '''
    requery database
    '''
    if order ==1:
        my = PYSQL('localhost', 'test', '123', 'pickme')
        sql = "SELECT orderid,susername,startpoint,endpoint FROM orders WHERE dusername is NULL AND fast_car = 1 AND  sdate = '{}' AND stime BETWEEN '{}' AND '{}'".format(
            date, time1, time2)
        data1 = my.select_data(sql)
        for vi in data1:
            susername = vi[1]
            sql = "SELECT sname ,ssex,year(getdate())-year(sbirth)FROM student WHERE susername = '{}'".format(susername)
            data2 = my.select_data(sql)
            data3 = data2[0]
            data4 = {"oid": vi[0], "startpoint": vi[2], "endpoint": vi[3], "name": data3[0], "sex": data3[1],
                     "age": data3[2]}
            data.append(data4)
    else:
        my = PYSQL('localhost', 'test', '123', 'pickme')
        sql = "SELECT orderid,susername,startpoint,endpoint FROM orders WHERE dusername is NULL AND free_ride = 1 AND  sdate = '{}' AND stime BETWEEN '{}' AND '{}'".format(
            date, time1, time2)
        data1 = my.select_data(sql)
        for vi in data1:
            susername = vi[1]
            sql = "SELECT sname ,ssex,year(getdate())-year(sbirth)FROM student WHERE susername = '{}'".format(susername)
            data2 = my.select_data(sql)
            data3 = data2[0]
            data4 = {"oid": vi[0], "startpoint": vi[2], "endpoint": vi[3], "name": data3[0], "sex": data3[1],
                     "age": data3[2]}
            data.append(data4)
    res = {
        "status": 0,
        "data": data
    }
    return json.dumps(res, ensure_ascii=False)
# driver take tail wind car order 司机接顺风车订单并返回乘客信息
@app.route('/driver/twc/tkod', methods=['POST'])
def takeTwcOrder():
    oid = request.form.get("oid")
    driverid = request.form.get("did")
    '''
    updata database
    '''
    my = PYSQL('localhost', 'test', '123', 'pickme')
    sql = "UPDATE orders SET dusername ='{}' WHERE orderid ='{}'".format(driverid,oid)
    my.update_data(sql)
    sql = "SELECT susername FROM orders WHERE orderid = '{}'".format(oid)
    susername1 = my.select_data(sql)
    susername2 =susername1[0]
    susername = susername2[0]
    sql = "SELECT sname,ssex,year(getdate())-year(sbirth),stel FROM student WHERE susername = '{}'".format(susername)
    suer1 = my.select_data(sql)
    suer = suer1[0]
    res = {
        "status": 0,
        "data": {
            "msg": "seccess",
            "username":susername,
            "name":suer[0],
            "sex":suer[1],
            "age":suer[2],
            "tel":suer[3]
        }
    }
    return json.dumps(res, ensure_ascii=False)

# passager Release tail wind car order 乘客发布顺风车订单   价钱待加
@app.route('/twcar/release')
def releaseTwcOrder():
    username = request.args.get("user")
    startPlace = request.args.get("stp")
    destination = request.args.get("des")
    date = request.args.get("date")
    time = request.args.get("time")
    '''
    add into database
    '''
    my = PYSQL('localhost', 'test', '123', 'pickme')
    sql = "INSERT INTO orders(susername,free_ride,startpoint,endpoint,sdate,stime) VALUES('{}',1,'{}','{}','{}','{}')".format(username,startPlace,destination, date,time)
    my.insert_date(sql)
    sql =  "SELECT orderid FROM orders WHERE susername='{}' AND startpoint ='{}' AND endpoint = '{}'AND sdate ='{}'AND stime ='{}'".format(username, startPlace, destination, date,time)
    orderid1 = my.select_data(sql)

    my.close()
    orderid2 = orderid1[0]
    orderid = orderid2[0]
    res = {
        "status": 0,
        "msg": "success",
        "data": {"oid": orderid}
    }
    return json.dumps(res)

# get adress and position 获取地址和坐标
@app.route('/pos')
def get_pos():

    return "Function not completed"

# refund 退押金
@app.route('/refund')
def refund():
    oid = request.args.get("oid")
    '''
    query database
    '''
    my = PYSQL('localhost', 'test', '123', 'pickme')
    sql = "SELECT deposit FROM orders WHERE orderid ='{}'".format(oid)
    deposit1 =my.select_data(sql)
    sql = "UPDATE orders SET deposit=0 WHERE orderid ='{}'".format(oid)
    my.update_data(sql)
    my.close()
    deposit2 = deposit1[0]
    deposit = deposit2[0]

    if deposit:
        msg = "success return {} yuan to you".format(deposit)
        '''
        updata database
        '''
    else:
        msg = "you have not ever deposit"
    res = {
        "status": 0,
        "msg": msg
    }
    return json.dumps(res)

# query is_deposit 交押金
@app.route('/query/deposit')
def query_deposit():
    oid = request.args.get("oid")
    deposit = request.args.get("deposit")
    print(oid)
    print(deposit)
    '''
    query database
    '''
    if deposit:
        my = PYSQL('localhost', 'test', '123', 'pickme')
        sql ="UPDATE orders SET deposit={} WHERE orderid ='{}'".format(deposit, oid)
        my.update_data(sql)
        my.close()
        status = 0
        msg = 'success'
    else:
        status = -1
        msg = 'fail'
    res = {
        "status": status,
        "msg":msg,
        "data": {"is_deposit": deposit}
    }
    return json.dumps(res)


# is deposit 判断是否已交押金
@app.route('/deposit')
def deposit():

    oid = request.args.get("oid") #订单号
    print(oid)
    '''
    add into database
    '''
    my = PYSQL('localhost', 'test', '123', 'pickme')
    sql = "SELECT deposit FROM orders WHERE orderid ='{}'".format(oid)
    data1 = my.select_data(sql)
    my.close()
    if data1:
        msg = 'success'
        status = 0
    else:
        msg = 'fail'
        status = -1
    res = {
        "status": status,
        "msg": msg
    }
    return json.dumps(res)


# student valid
@app.route('/valid', methods=['POST'])
def valid():
    username = request.form.get("user")
    sname = request.form.get("name")
    ssex = request.form.get("sex")
    userid = request.form.get("idnum")
    sinfo = request.form.get("scard")
    stel = request.form.get("tel")
    # idcar photo
    f = request.files['idcard']
    useridphoto = upphoto(f)
    print(useridphoto)
    # student card photos
    f1 = request.files['stcard']
    sidphoto = upphoto(f1)
    # head photos

    # insert into database
    my = PYSQL('localhost', 'test', '123', 'pickme')
    sql = "insert into student(susername, sname, ssex, userid, useridphoto, sinfo, sidphoto, stel) " \
          "values('{}','{}','{}','{}','{}','{}','{}','{}')".format(username, sname, ssex, userid, useridphoto, sinfo,
                                                                   sidphoto, stel)
    result = my.insert_date(sql)
    if result:
        msg = 'success'
        status = 1
    else:
        status = -1
        sql = "select susername from student where susername='{}'".format(username)
        result = my.select_data(sql)
        if result:
            msg = '该用户已认证'
        else:
            sql = "select userid from student where userid='{}'".format(userid)
            result = my.select_data(sql)
            if result:
                msg = '身份证已被使用'
            else:
                sql = "select sinfo from student where sinfo='{}'".format(sinfo)
                result = my.select_data(sql)
                if result:
                    msg = '学号已被使用'
                else:
                    msg = 'unkown wrong'
    my.close()
    # print(msg)
    res = {
        "status": status,
        "msg": msg
    }
    return json.dumps(res,ensure_ascii=False)


# valid 认证
@app.route('/driver/valid', methods=['POST'])
def dri_valid():
    dusername = request.form.get("user")
    dname = request.form.get("name")
    dsex = request.form.get("sex")
    userid = request.form.get("idnum")
    dbirth = request.form.get("birth")
    dtel = request.form.get("tel")
    # carnum = request.form.get("carnum")
    my = PYSQL('localhost', 'test', '123', 'pickme')
    sql = "insert into driver(dusername, dname, dsex, userid, dbirth, dtel) " \
          "values('{}','{}','{}','{}','{}','{}')".format(dusername, dname, dsex, userid, dbirth, dtel)
    result = my.insert_date(sql)

    if result:
        msg = 'success'
        status = 1
    else:
        status = -1
        sql = "select dusername from driver where dusername='{}'".format(dusername)
        result = my.select_data(sql)
        if result:
            msg = '该用户已认证'
        else:
            sql = "select userid from driver where userid='{}'".format(userid)
            result = my.select_data(sql)
            if result:
                msg = '身份证已被使用'
            else:
                '''
                sql = "select sinfo from student where sinfo='{}'".format(sinfo)
                result = my.select_data(sql)
                if result:
                    msg = '学号已被使用'
                else:
                '''

                msg = 'unkown wrong'
    my.close()
    # print(msg)
    res = {
        "status": status,
        "msg": msg
    }
    return json.dumps(res, ensure_ascii=False)


# get info 获取用户信息
@app.route('/info')
def get_info():
    username = request.args.get("user")

    '''
    query database
    '''
    con = pymssql.connect('127.0.0.1', 'test', '123', 'pickme')
    cursor = con.cursor()
    # print(cursor)
    sql = "SELECT username FROM users where username='{}'".format(username)
    cursor.execute(sql)
    res = cursor.fetchone()

    if res == None:
        msg = 'can not find the user'
    else:
        sql = "SELECT * FROM users where username='{}'".format(username)
        cursor.execute(sql)
        result = cursor.fetchone()
        '''
        return result
        '''
        msg = 'success'
    cursor.close()
    res = {
        "status": 0,
        "data": {
            "msg": msg
        }
    }
    return json.dumps(res)


# register 注测
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('user')
    password = request.form.get('pwd')
    # identify = request.form.get('identify')
    '''
    add new user into database
    '''
    my = PYSQL('localhost', 'test', '123', 'pickme')
    sql = "insert into users values('{}','{}')".format(username, password)
    result = my.insert_date(sql)
    if result:
        print('success')
        status = 0
        msg = 'success'
    else:
        print('fail')
        status = -1
        msg = 'username has been registered'
    my.close()
    res = {
        "status": status,
        "msg": msg
    }
    return json.dumps(res)


# login 登录
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('user')
    password = request.form.get('pwd')

    # identify = request.form.get('identify')
    if username == None or password == None:
        res = {
            "status": 1000,
            "msg": "a bad way to request"
        }
        return json.dumps(res)
    '''
    query database
    '''
    # print(res)
    my = PYSQL('localhost', 'test', '123', 'pickme')

    sql = "SELECT username,userpwd FROM users where username='{}' and userpwd='{}'".format(username, password)
    result = my.select_data(sql)
    print(result)
    if len(result):
        res = {
            "status": 1,
            "msg": "success"

        }
    else:
        res = {
            "status": -1,
            "msg": "username or password is not match"
        }


    return json.dumps(res)


@app.route('/',methods=['GET', 'POST'])
def hello_world():
    print('\nconnect in {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    #print(request.form.get('user'))
    # req = request.get_data()

    #print(type(j))
    # print(json.loads(s))
    return '欢迎使用PICKME'

@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    # print(request)
    if request.method == 'POST':

        f = request.files['file']
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        print(basepath)
        src_imgname = str(uuid.uuid1()) + ".jpg"
        upload_path = os.path.join(basepath, 'images/')
        if os.path.exists(upload_path) == False:
            os.makedirs(upload_path)
        print(upload_path + src_imgname)
        f.save(upload_path + src_imgname)

        return 'ok'

if __name__ == '__main__':
    # app.run(host="www.pickmi.club", port=8090)
    app.run(host='0.0.0.0', port=80)
    # 6bf6c9ddca23383f
