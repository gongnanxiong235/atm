# author:gongnanxiong
# date:2018/12/4

from util.database import MysqldbHelper as sh
import time

'''
add user return user_id
'''
tb_name='user'
def add_user(params):
    return sh().insert(tb_name,params)


def query_name(value):
    sql='select * from user where name=%s'
    return sh().executeSql(sql,value)

def query_name_password(name,password):
    sql='select id from user where name=%s and password=%s'
    result=sh().executeSql(sql,(name,password))
    if len(result)==0:return -1
    else:return result[0][0]

def update_login(id):
    sql='update user set is_login=1 where id=%s'
    sh().executeCommit(sql, id)

def update_logout(id):
    sql = 'update user set is_login=0 where id=%s'
    sh().executeCommit(sql, id)
if __name__ == '__main__':
    hello=query_name_password('zhangsan','1234567')
    print(hello)
