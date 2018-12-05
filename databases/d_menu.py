# author:gongnanxiong
# date:2018/12/5
from util.database import MysqldbHelper as sh

def get_menu(parent_id,menu_permis=-1):#menu_permis 和user表中的is_admin字段对应
    if menu_permis==-1:
        sql = 'select menu_name from menu  where parent_id=%s'
    else:
        sql = 'select menu_name from menu  where parent_id=%s and menu_permis=%s'
    sh().executeSql(sql,(menu_permis,menu_permis))

