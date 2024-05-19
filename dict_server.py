"""
服务端
"""
import sys
from socket import *
from threading import Thread
from operation_db import *
import time

# 全局变量
HOST = '0.0.0.0'
PORT = 1245
ADDR = (HOST,PORT)

def main():
    # 创建数据库对象
    db = Databae()

    # 创建TCP
    s = socket()
    s.bind(ADDR)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.listen(3)

    # 等待客户端连接
    print("listen port 1245...")
    while True:
        try:
            c, addr = s.accept()
            print("connect from:", addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        # 创建线程
        t = Thread(target=do_request,args=(c,db))
        t.setDaemon(True)
        t.start()

# 处理客户端请求
def do_request(c,db):
    db.create_cursor()
    while True:
        data = c.recv(1024).decode()
        if not data or data[0] == 'E':
            c.close()
            sys.exit("客户端退出")
        elif data[0] == 'L':
            do_login(c,db,data)
        elif data[0] == 'R':
            do_register(c,db,data)
        elif data[0] == 'Q':
            do_query(c,db,data)
        elif data[0] == 'H':
            do_hist(c,db,data)


# 处理注册
def do_register(c,db,data):
    tem = data.split(' ')
    name = tem[1]
    passwd = tem[2]
    if db.register(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'FAIL')

# 处理登录
def do_login(c,db,data):
    tem = data.split(' ')
    name = tem[1]
    passwd = tem[2]
    if db.login(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'FAIL')

# 处理查询
def do_query(c,db,data):
    tem = data.split(' ')
    name = tem[1]
    word = tem[2]
    # 插入历史记录
    db.insert_history(name,word)
    mean = db.query(word)
    if not mean:
        c.send("没有找到该单词".encode())
    else:
        msg = "%s : %s"%(word,mean)
        c.send(msg.encode())

# 处理历史查询
def do_hist(c,db,data):
    name = data.split(' ')[1]
    history = db.history(name)
    if not history:
        c.send(b'FAIL')
        return
    c.send(b'OK')
    for his in history:
        msg = "%s   %s  %s"%(his)
        time.sleep(0.1)
        c.send(msg.encode())
    time.sleep(0.1)
    c.send(b'##')


if __name__ == "__main__":
    main()
