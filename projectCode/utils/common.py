
ErrorCode = {
    10000: "处理成功",
    10011: "用户名格式错误",
    10012: "用户名已被注册",
    10021: "密码格式不正确",
    10022: "两次密码不一致",
    10031: "手机号码格式不正确",
    10041: "邮箱格式不正确",
    20001: "用户名和密码错误",
    20002: "异常错误",
    20003: "必填项不能为空",
    30000: "未获取token值",
    30001: "token值无效",
}


def errorRetult(status=10000, message=None, data=None):
    return {
        "status": status,
        "data": data,
        # ?前端没返回就返回默认的错误信息
        "message": message if message else ErrorCode.get(status)
    }


if __name__ == "__main__":
    val = errorRetult(message="注册成功!")
    print(val)
