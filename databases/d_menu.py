# author:gongnanxiong
# date:2018/12/5
from util.database import MysqldbHelper as sh

def get_menu(parent_id,menu_permis):#menu_permis 和user表中的is_admin字段对应
    sql = 'select menu_name from menu  where parent_id=%s and menu_permis=%s'
    return sh().executeSql(sql,(menu_permis,menu_permis))

def get_menu_admin(parent_id,menu_permis):#menu_permis 和user表中的is_admin字段对应
    sql = 'select menu_name from menu  where parent_id=%s and menu_permis>=%s'
    return sh().executeSql(sql,(menu_permis,menu_permis))

