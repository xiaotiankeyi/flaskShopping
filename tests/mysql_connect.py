import pymysql

# 打开数据库连接
conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    db='flaskshopping')

# 生成游标对象
handle = conn.cursor(cursor=pymysql.cursors.DictCursor)
#
# sql = "create table s1(id tinyint, name varchar(10))"
# # 执行sql
# handle.execute(sql)
#
data = handle.execute("SELECT VERSION()")  # 显示数据条数
print(data)
#
# # 获取单条数据
# print(handle.fetchone())
#
# # 获取所有结果
# # print(handle.fetchall())
#
# # handle.scroll(-1, mode="relative")  # 相对位置
# # handle.scroll(2,mode="absolute")    #绝对位置
#
# # 显示十条数据
# print(handle.fetchmany(10))
#
# # 提交数据库执行
# conn.commit()

# 关闭光标对象
handle.close()
# 关闭数据库连接
conn.close()
