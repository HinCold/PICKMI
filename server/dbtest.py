from fun import *
import os
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from flask import request
import time
import json
import pymssql
from dbtest import PYSQL
import uuid

user = 'test'
pwd = 'test'
app = Flask(__name__)
order_number = 1

# 查询是否有订单未完成
# 反馈实时位置
# 查询订单状态

# passager get driver data 乘客获取司机信息
@app.route('/quikcar/data')
def getquikcar_data():
    '''
    requery database
    '''
    res = {
        "status": 0,
        "data": {}
    }
    return json.dumps(res)
# driver take quik car order 司机接快车订单
@app.route('/driver/quikcar/tkod')
def takeQcOrder():
    oid = request.form.get("oid")
    driver_id = request.form.get("did")
    '''
    updata database
    '''
    res = {
        "status": 0,
        "msg": "seccess",
        "data": {

        }
    }
    return json.dumps(res)


# passager release quik car order 乘客发布快车订单
@app.route('/quikcar/release')
def releaseQcar():
   user = request.form.get("user")
   pos = request.form.get("pos")
   adress = request.form.get("adr")
   '''
   add into database
   '''
   res = {
       "status": 0,
       "msg": "success"
   }
   return json.dumps(res)

# driver get tail wind car order data 司机获取订单数据
@app.route('/driver/twc/data')
def getTwc_data():
    '''
    requery database
    '''
    res = {
        "status": 0,
        "data": {}
    }
    return json.dumps(res)
# driver take tail wind car order 司机接顺风车订单并返回乘客信息
@app.route('/driver/twc/tkod', methods=['POST'])
def takeTwcOrder():
    oid = request.form.get("oid")
    driver_id = request.form.get("did")
    '''
    updata database
    '''

    res = {
        "status": 0,
        "data": {
            "msg": "seccess"
        }
    }
    return json.dumps(res)

# passager Release tail wind car order 乘客发布顺风车订单
@app.route('/twcar/release')
def releaseTwcOrder():

    startPlace = request.form.get("stp")
    destination = request.form.get("des")
    '''
    add into database
    '''

    orderid = 1
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
    user = request.form.get("user")
    '''
    query database
    '''
    deposit = 1
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
    username = request.form.get("user")
    '''
    query database
    '''
    deposit = 1
    res = {
        "status": 0,
        "data": {"is_deposit": deposit}
    }
    return json.dumps(res)


# is deposit 判断是否已交押金
@app.route('/deposit')
def deposit():

    username = request.form.get("user")

    '''
    add into database
    '''
    res = {
        "status": 0,
        "msg": "deposit success"
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
