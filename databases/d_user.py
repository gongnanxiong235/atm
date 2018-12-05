# author:gongnanxiong
# date:2018/12/4

from util.database import MysqldbHelper as sh
import time

'''
add user return user_id
'''
def add_user(params):
    mysql=sh()
    sql='insert into user (name,password,account_id,add_time,update_time) values (%s,%s,%s,%s,%s)'
    erro_info=mysql.executeCommit(sql,params)
    user_id=mysql.cur.lastrowid
    return (user_id,erro_info)

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
    return sh().executeCommit(sql, id)

def update_logout(id):
    sql = 'update user set is_login=0 where id=%s'
    return sh().executeCommit(sql, id)

def get_isadmin(id):
    sql='select is_admin from user where id=%s'
    return sh().executeSql(sql,id,type='one')



if __name__ == '__main__':
    mysql = sh()
    sql = 'select * from user'
    info = mysql.executeSql(sql,(),type='all',rtype='dict')
    addtime=info[1].get('add_time')
    print(type(addtime))



