import random

'''
随机一个10位数的卡,全是数字
'''
def get_card_no():
    card_no=''
    for i in range(10):
        card_no+=str(random.randint(0,9))
    return card_no




