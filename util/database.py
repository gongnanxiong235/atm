# author:gongnanxiong
# date:2018/12/4

# -*- coding: UTF-8 -*-
import re
import pymysql
from util.config import ConfigUtil as c
class MysqldbHelper(object):
    """操作mysql数据库，基本方法

        """
    hp=c()
    host_name=hp.read_config_database('host')
    username_name=hp.read_config_database('username')
    password_name=hp.read_config_database('password')
    port_name=int(hp.read_config_database('port'))
    database_name=hp.read_config_database('database')
    def __init__(self , host=host_name, username=username_name, password=password_name, port=port_name, database=database_name):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.con = None
        self.cur = None
        try:
            self.con = pymysql.connect(host=self.host, user=self.username, passwd=self.password, port=self.port, db=self.database)
            # 所有的查询，都在连接 con 的一个模块 cursor 上面运行的
            self.cur = self.con.cursor()
        except:
            raise Exception("DataBase connect error,please check the db config.")

    def close(self):
        """关闭数据库连接

        """
        if not  self.con:
            self.con.close()
        else:
            raise Exception("DataBase doesn't connect,close connectiong error;please check the db config.")

    def getVersion(self):
        """获取数据库的版本号

        """
        self.cur.execute("SELECT VERSION()")
        return self.getOneData()

    def getOneData(self):
        # 取得上个查询的结果，是单个结果
        data = self.cur.fetchone()
        return data

    def creatTable(self, tablename, attrdict, constraint):
        """创建数据库表

            args：
                tablename  ：表名字
                attrdict   ：属性键值对,{'book_name':'varchar(200) NOT NULL'...}
                constraint ：主外键约束,PRIMARY KEY(`id`)
        """
        if self.isExistTable(tablename):
            return
        sql = ''
        sql_mid = '`id` bigint(11) NOT NULL AUTO_INCREMENT,'
        for attr,value in attrdict.items():
            sql_mid = sql_mid + '`'+attr + '`'+' '+ value+','
        sql = sql + 'CREATE TABLE IF NOT EXISTS %s ('%tablename
        sql = sql + sql_mid
        sql = sql + constraint
        sql = sql + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'
        print ('creatTable:'+sql)
        self.executeCommit(sql)

    '''
    返回值：
    1.元祖:表明查询到了结果
    2.None：表明没有查询到结果
    3.字符串：表明已经捕捉到了异常
    rtype:返回类型，如果etype=dict 以字典的形式返回查询到的数据，相反则以二维元祖的形式返回数据
    
    '''
    def executeSql(self,sql='',args='',type='all',rtype=''):
        #执行sql语句，针对读操作返回结果集
        if rtype=='dict':
            self.cur = self.con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            self.cur.execute(sql,args=args)
            print ('sql',self.cur._last_executed ) # 打印sql语句
            if type=='one':
                records = self.cur.fetchone()
            else:
                records = self.cur.fetchall()
            print('records',records)
        except Exception as e:
            print('e:',e)
            records = 'MySQL execute failed! ERROR (%s): %s' %(e.args[0],e.args[1])
            print ('erro:',records)
        return records

    '''
        返回值:
        1.None：表明已经执行成功
        2.字符串：表明已经捕捉到了异常
        '''
    def executeCommit(self,sql='',args=''):
        """执行数据库sql语句，针对更新,删除,事务等操作失败时回滚

        """
        try:
            self.cur.execute(sql,args)
            print ( self.cur._last_executed )  # 打印sql语句
            self.con.commit()
        except pymysql.Error as e:
            self.con.rollback()
            error = 'MySQL execute failed! ERROR (%s): %s' %(e.args[0],e.args[1])
            print ("error:", error)
            return error

    def insert(self, tablename, params):
        """创建数据库表

            args：
                tablename  ：表名字
                key        ：属性键
                value      ：属性值
        """
        key = []
        value = []
        for tmpkey, tmpvalue in params.items():
            key.append(tmpkey)
            if isinstance(tmpvalue, str):
                value.append("\'" + tmpvalue + "\'")
            else:
                value.append(tmpvalue)
        attrs_sql = '('+','.join(key)+')'
        values_sql = ' values('+','.join(value)+')'
        sql = 'insert into %s'%tablename
        sql = sql + attrs_sql + values_sql
        print ('_insert:'+sql)
        self.executeCommit(sql)
        return self.cur.lastrowid

    def select(self, tablename, cond_dict='', order='', fields='*'):
        """查询数据

            args：
                tablename  ：表名字
                cond_dict  ：查询条件
                order      ：排序条件

            example：
                print mydb.select(table)
                print mydb.select(table, fields=["name"])
                print mydb.select(table, fields=["name", "age"])
                print mydb.select(table, fields=["age", "name"])
        """
        consql = ' '
        if cond_dict!='':
            list=[]
            for k, v in cond_dict.items():
                # consql = consql+k + '=' + v + ' and'
                print(k)
                print(v)
                hello=k + '=' + v
                print(hello)
                list.append(k + '=' + v)
                print('list',list)
        consql='and'.join(consql)
        print('hhhh',consql)
        # consql = consql + ' 1=1 '
        if fields == "*":
            sql = 'select * from %s where ' % tablename
        else:
            if isinstance(fields, list):
                fields = ",".join(fields)
                sql = 'select %s from %s where ' % (fields, tablename)
            else:
                raise Exception("fields input error, please input list fields.")
        sql = sql + consql + order
        print ('select:' + sql)
        return self.executeSql(sql)


    def insertMany(self,table, attrs, values):
        """插入多条数据

            args：
                tablename  ：表名字
                attrs        ：属性键
                values      ：属性值

            example：
                table='test_mysqldb'
                key = ["id" ,"name", "age"]
                value = [[101, "liuqiao", "25"], [102,"liuqiao1", "26"], [103 ,"liuqiao2", "27"], [104 ,"liuqiao3", "28"]]
                mydb.insertMany(table, key, value)
        """
        values_sql = ['%s' for v in attrs]
        attrs_sql = '('+','.join(attrs)+')'
        values_sql = ' values('+','.join(values_sql)+')'
        sql = 'insert into %s'% table
        sql = sql + attrs_sql + values_sql
        print ('insertMany:'+sql)
        try:
            print (sql)
            for i in range(0,len(values),20000):
                    self.cur.executemany(sql,values[i:i+20000])
                    self.con.commit()
        except Exception as e:
            self.con.rollback()
            error = 'insertMany executemany failed! ERROR (%s): %s' %(e.args[0],e.args[1])
            print (error)

    def delete(self, tablename, cond_dict):
        """删除数据

            args：
                tablename  ：表名字
                cond_dict  ：删除条件字典

            example：
                params = {"name" : "caixinglong", "age" : "38"}
                mydb.delete(table, params)

        """
        consql = ' '
        if cond_dict!='':
            for k, v in cond_dict.items():
                if isinstance(v, str):
                    v = "\'" + v + "\'"
                consql = consql + tablename + "." + k + '=' + v + ' and '
        consql = consql + ' 1=1 '
        sql = "DELETE FROM %s where%s" % (tablename, consql)
        print (sql)
        return self.executeCommit(sql)

    def update(self, tablename, attrs_dict, cond_dict):
        """更新数据

            args：
                tablename  ：表名字
                attrs_dict  ：更新属性键值对字典
                cond_dict  ：更新条件字典

            example：
                params = {"name" : "caixinglong", "age" : "38"}
                cond_dict = {"name" : "liuqiao", "age" : "18"}
                mydb.update(table, params, cond_dict)

        """
        attrs_list = []
        consql = ' '
        for tmpkey, tmpvalue in attrs_dict.items():
            attrs_list.append("`" + tmpkey + "`" + "=" +"\'" + tmpvalue + "\'")
        attrs_sql = ",".join(attrs_list)
        print ("attrs_sql:", attrs_sql)
        if cond_dict!='':
            for k, v in cond_dict.items():
                if isinstance(v, str):
                    v = "\'" + v + "\'"
                consql = consql + "`" + tablename +"`." + "`" + k + "`" + '=' + v + ' and '
        consql = consql + ' 1=1 '
        sql = "UPDATE %s SET %s where%s" % (tablename, attrs_sql, consql)
        print (sql)
        return self.executeCommit(sql)

    def dropTable(self, tablename):
        """删除数据库表

            args：
                tablename  ：表名字
        """
        sql = "DROP TABLE  %s" % tablename
        self.executeCommit(sql)

    def deleteTable(self, tablename):
        """清空数据库表

            args：
                tablename  ：表名字
        """
        sql = "DELETE FROM %s" % tablename
        self.executeCommit(sql)

    def isExistTable(self, tablename):
        """判断数据表是否存在

            args：
                tablename  ：表名字

            Return:
                存在返回True，不存在返回False
        """
        sql = "select * from %s" % tablename
        result = self.executeCommit(sql)
        if result is None:
            return True
        else:
            if re.search("doesn't exist", result):
                return False
            else:
                return True

if __name__ == "__main__":
    '''
    mydb = MysqldbHelper()
    print (mydb.getVersion())
    table='test_mysqldb'
    attrs={'name':'varchar(200) DEFAULT NULL','age':'int(11) DEFAULT NULL'}
    constraint='PRIMARY KEY(`id`)'
    print (mydb.creatTable(table, attrs, constraint))
    params = {"name" : "caixinglong", "age" : "38"}
    mydb.insert('test_mysqldb', params)
    print (mydb.select(table))
    print (mydb.select(table, fields=["name", "age"]))
    print (mydb.select(table, fields=["age", "name"]))
    key = ["id" ,"name", "age"]
    value = [[101, "liuqiao", "25"], [102,"liuqiao1", "26"], [103 ,"liuqiao2", "27"], [104 ,"liuqiao3", "28"]]
    mydb.insertMany(table, key, value)
    mydb.delete(table, params)
    cond_dict = {"name" : "liuqiao", "age" : "18"}
    mydb.update(table, params, cond_dict)
    # mydb.deleteTable(table)
    # mydb.dropTable(table)
    print (mydb.select(table+ "1"))
    print (mydb.isExistTable(table+ "1"))
    '''
