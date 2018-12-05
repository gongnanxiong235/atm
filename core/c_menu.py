# author:gongnanxiong
# date:2018/12/5
from databases import d_menu,d_user
def getHomePageMenu(user_id):
    #先获取是否管理员
    response = {}
    result = d_user.get_isadmin(user_id)
    print('result', result)
    if result is None:
        response['code'] = 202
        response['data'] = {'message': '查询不到此用户的管理员类型'}
    #查询出管理员状态码
    elif isinstance(result, tuple):
        admin_code=result[0]
        if admin_code==0:
            result_menu=d_menu.get_menu(0)
        else:
            result_menu = d_menu.get_menu(0, admin_code)
        if isinstance(result_menu,tuple):
            menu_list=[x[0] for x in result_menu ]
            response['code'] = 200
            response['data'] = {'message': '查询成功', 'dt': menu_list}
        else:
            response['code'] = 201
            response['data'] = {'message': result_menu}

    #查询时管理员的时候发生了异常
    else:
        response['code'] = 201
        response['data'] = {'message': result}
    return response


if __name__ == '__main__':
    hello=getHomePageMenu(1)
    print(hello)