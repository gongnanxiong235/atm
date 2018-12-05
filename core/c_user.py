from databases import d_user,d_account
import time
#创建新用户
def add_user(name,password):
    response={}
    #先判断用户名是否重复
    query_name=d_user.query_name(name)
    # 代表查询的时候发生了异常
    if isinstance(query_name,str):
        response['code'] = 201
        response['data'] = {'message': query_name}
    else:
        if len(query_name)==0:
            result=d_account.insert_account()
            #表示没有回滚，创建成功
            if not result[1]:
                params=(name,password,result[0],time.strftime('%Y-%m-%d %X'),time.strftime('%Y-%m-%d %X'))
                result_inner=d_user.add_user(params)
                #表示回滚了
                if  result_inner[1] is not None:
                    print('hello',result_inner)
                    pass
                else:
                    response['code']=200
                    response['data']={'message':'OK'}
            else:
                message=result[1]
                response['code']=201
                response['data']={'message': message}
        else:
            response['code'] = 203
            response['data'] = {'message': '已经存在此用户名,请换一个用户名创建'}

    return response

#登录
def login(name,password):
    response={}
    result=d_user.query_name_password(name,password)
    #表示是个字符串，也就是说sql产生了异常
    if isinstance(result,str) :
        response['code']=201
        response['data']={'message':result}
    else:
        if result==-1:
            response['code'] = 203
            response['data'] = {'message': '账户名或密码错误，请重新登录'}
        else:
            #修改登录状态，然后登录成功
            result_login=d_user.update_login(result)
            if result_login is None:
                response['code'] = 200
                response['data'] = {'meaage': '登录成功', 'usdr_id': result}
            else:
                response['code'] = 201
                response['data'] = {'meaage': result_login}
    return response

#退出登录
def login_out(user_id):
    response={}
    result=d_user.update_logout(user_id)
    if result is None:
        response['code'] = 200
        response['data'] = {'meaage': '退出成功'}
    else:
        response['code'] = 201
        response['data'] = {'message': result}
    return response


# 判断是不是管理员
def get_is_admin(user_id):
    response={}
    result=d_user.get_isadmin(user_id)
    print('result',result)
    if result is None:
        response['code'] = 202
        response['data'] = {'message':'没有此用户或者查询不到结果'}
    elif isinstance(result,tuple):
        response['code'] = 200
        response['data'] = {'meaage': '查询成功','is_admin':result[0]}
    else:
        response['code'] = 201
        response['data'] = {'message': result}
    return response

if __name__ == '__main__':
        add_user('zhangsan','123456')

