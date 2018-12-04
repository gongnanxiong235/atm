from util.database import MysqldbHelper as mysql
from util import random_util
import time
def insert_account():
    con=mysql()
    params=(random_util.get_card_no (), '123456', 15000, time.strftime ( '%Y-%m-%d %X' ), time.strftime ( '%Y-%m-%d %X' ))
    sql='insert into account(card_no,card_pwd,card_limit,add_time,update_time) values(%s,%s,%s,%s,%s)'
    erro=con.executeCommit(sql,params)
    return (con.cur.lastrowid,erro)  #打印主键和报错信息


if __name__ == '__main__':

    values=(random_util.get_card_no(),'123456',15000,time.strftime('%Y-%m-%d %X'),time.strftime('%Y-%m-%d %X'))
    print(insert_account())