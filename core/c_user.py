from databases import d_user,d_account
import time
def add_user(name,password):
    response={}

    #先判断用户名是否重复
    d_user.query_name(name)
    result=d_account.insert_account()
    #表示没有回滚，创建成功
    if not result[1]:
        params=(name,password,result[0],time.strftime('%Y-%m-%d %X'),time.strftime('%Y-%m-%d %X'))
        result_inner=d_user.add_user(params)
        #表示回滚了
        if not result_inner[1]:
            psss
        else:
            response['code']=200
            response['data']={'message':'OK'}
    else:
        message=result[1]
        response['code']=201
        response['data']={'message': message}


if __name__ == '__main__':
    a=add_user('lisi','123456')
    print(a)

