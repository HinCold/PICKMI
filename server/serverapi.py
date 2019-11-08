from flask import Flask,request
from flask import request
import time
from flask_request_params import bind_request_params
import json
import pymssql
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


# valid 认证
@app.route('/driver/valid', methods=['POST'])
def dri_valid():
    username = request.form.get("user")
    name = request.form.get("name")
    sex = request.form.get("sex")
    idnum = request.form.get("idnum")
    # carnum = request.form.get("carnum")
    con = pymssql.connect('127.0.0.1', 'test', '123', 'pickme')
    cursor = con.cursor()
    sql = "SELECT dusername FROM driver where dusername='{}'".format(username)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        msg = 'you have already register'
    else:

        sql = "SELECT userid FROM driver where userid='{}'".format(idnum)
        cursor.execute(sql)
        idout = cursor.fetchone()
        if idout == None:
            sql = "insert into driver(dusername,dname,dsex,userid) values('{}','{}','{}','{}')".format(username, name, sex, idnum)
            con.commit()
    cursor.close()
    res = {
        "status": 0,
        "msg": "success"
    }
    return json.dumps(res)


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
    con = pymssql.connect('127.0.0.1', 'test', '123', 'pickme')
    cursor = con.cursor()
    # print(cursor)
    sql = "SELECT username FROM users where username='{}'".format(username)
    cursor.execute(sql)
    res = cursor.fetchone()
    if res == None:
        sql = "insert into users values('{}','{}')".format(username, password)
        cursor.execute(sql)
        con.commit()
        msg = 'success'
    else:
           msg = 'username has been registered'
    # res = cursor.fetchone()
    # print(res)
    cursor.close()
    res = {
        "status": 0,
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

    con = pymssql.connect('127.0.0.1', 'test', '123', 'pickme')
    cursor = con.cursor()
    # print(cursor)
    cursor.execute("SELECT username,userpwd FROM users")
    res = cursor.fetchone()
    # print(res)
    user = res[0].strip()
    pwd = res[1].strip()

    cursor.close()
    if username == user and password == pwd:
        res = {
            "status": 0,
            "msg": "success"
        }
        return json.dumps(res)
    else:
        res = {
            "status": 0,
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
    return 'Hello World!\nwelcome to PICKME'


if __name__ == '__main__':
    # app.run(host="www.pickmi.club", port=8090)
    app.run(host='0.0.0.0', port=80)
    # 6bf6c9ddca23383f
