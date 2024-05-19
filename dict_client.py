"""
客户端
"""

from socket import *
import getpass

HOST = '127.0.0.1'
PORT = 1245
ADDR = (HOST,PORT)
# 创建网络连接
s = socket()
s.connect(ADDR)

def main():
    while True:
        print("""
        ===================Welcome===============
                   英英在线词典解析平台
                        1.注册
                        2.登录
                        3.退出     
        =========================================
        """)
        cmd = input("输入选项：")
        if cmd == '1':
            do_register()
        elif cmd == '2':
            do_login()
        elif cmd == '3':
            s.send(b'E')
            print("谢谢使用")
            return
        else:
            print("请输入正确命令！")

# 注册
def do_register():
    while True:
        print("-----------用户注册------------")
        name = input("请输入用户名：")
        # passwd = getpass("请输入密码：")
        passwd = input("请输入密码：")
        # passwd1 = getpass("再次输入密码：")
        passwd1 = input("再次输入密码：")
        if (' ' in name) or (' ' in passwd):
            print("用户名或密码有空格")
            continue
        if passwd != passwd1:
            print("两次密码不一致")
            continue
        msg = "R %s %s"%(name,passwd)
        s.send(msg.encode())

        data = s.recv(128).decode()
        if data == 'OK':
            print("注册成功")
        else:
            print("注册失败")
        return
# 登录
def do_login():
    print("-----------用户登录------------")
    name = input("请输入用户名：")
    passwd = input("请输入密码：")
    msg = "L %s %s"%(name,passwd)
    s.send(msg.encode())
    data = s.recv(122).decode()
    if data == 'OK':
        print("登录成功")
        login(name)
    else:
        print("登录失败")

# 二级界面
def login(name):
    while True:
        print("""
                ================Welcome %s===============
                           英英在线词典解析平台
                                1.查单词
                                2.历史记录
                                3.注销     
                =========================================
                """%name)
        cmd = input("输入选项：")
        if cmd == '1':
            do_query(name)
        elif cmd == '2':
            do_hist(name)
        elif cmd == '3':
            return
        else:
            print("请输入正确命令！")

# 单词查询操作
def do_query(name):
    while True:
        word = input("单词：")
        if word == "##":
            break
        msg = "Q %s %s"%(name,word)
        s.send(msg.encode())
        data = s.recv(2048).decode()
        print(data)

# 历史记录
def do_hist(name):
    msg = "H %s"%name
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            if data == "##":
                break
            print(data)
    else:
        print("还没有历史记录")

if __name__ == "__main__":
    main()
