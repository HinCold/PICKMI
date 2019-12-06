import pymssql
import traceback
from DBUtils.PooledDB import PooledDB
from time import sleep
'''
#
#
# 数据库操作方法
#
#
#
'''

class PYSQL(object):

    def __init__(self, host, user, pwd, db):
        # print(host)
        self.pool = PooledDB(pymssql, 3, host=host, user=user, password=pwd, database=db, port=1433)
        # self.conn = pymssql.connect(host, user, pwd, db)
        # self.cursor = self.conn.cursor()
    def connect(self):
        self.conn = self.pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
        self.cursor = self.conn.cursor()
    def create_table_func(self,sql):
        self.cursor.execute(sql)
        print('数据表创建完毕')

    def insert_date(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except:
            print(traceback.format_exc())
            self.conn.rollback()
            return False

    def update_data(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            print(traceback.format_exc())
            self.conn.rollback()

    def delete_data(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            print(traceback.format_exc())
            self.conn.rollback()

    def select_data(self, sql):
        self.cursor.execute(sql)
        all_data = self.cursor.fetchall()
        return all_data
    def close(self):
        self.cursor.close()
        self.conn.close()




if __name__ == '__main__':
    my = PYSQL('localhost', 'test', '123', 'pickme')
    user = '1234'
    pwd = 'hh'
    sql = "insert into users values('{}','{}')".format(user, pwd)
    result = my.insert_date(sql)
    if result:
        print('success')
    else:
        print('fail')
    qsql = "select * from users"
    result = my.select_data(qsql)
    print(result)
    my.close()
