import random

import requests


def objTest():
    res = requests.request(
        method='get',
        url='http://127.0.0.1:5000/user/register/')
    print(res.json())


def objReg():
    number = 0
    while number <= 100:
        name = "".join(i for i in random.sample(
            """赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许金魏陶姜戚谢邹喻柏水窦章
            云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤""", 3))
        num = int('181' + ''.join(i for i in random.sample('0123456789', 8)))
        email = ''.join(i for i in random.sample('0123456789', 10)) + '@qq.com'
        print(email)
        address = random.sample(['江西', '福建', '广东', '四川', '湖南', '浙江', '河北'], 1)[0]

        res = requests.request(
            method='post',
            url='http://127.0.0.1:5000/user/register/',
            data={
                "username": name,
                "password": '123456',
                "assertPwd": '123456',
                "phone": num,
                "email": email,
                "address": address
            })
        number += 1
        print(res.json(), number)

if __name__ == "__main__":
    # objTest()
    objReg()
    # num =int('181' + ''.join(i for i in random.sample('0123456789', 8)))
    # print(type(num))
    #
    # address = random.sample(['江西', '福建', '广东', '四川', '湖南', '浙江', '河北'], 1)[0]
    # print(address)
