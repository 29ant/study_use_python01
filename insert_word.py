import re

import pymysql

fd = open("mywords.txt")
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     password='root',
                     database='dict',
                     charset='utf8')
cur = db.cursor()
sql = 'insert into words (word,mean) values (%s,%s)'
for line in fd:
    # line表示文件中的每一行,re.findall(r'(\w+)\s+(.+)',line)查到的根据目标字符串匹配的内容列表
    # re.findall(r'(\w+)\s+(.*)', line)[0]取出内容列表的第一项
    # tup = re.findall(r'(\w+)\s+(.+)',line)[0]
    tup = re.findall(r'(\w+)\s+(.*)',line)[0]
    try:
        # 完全匹配的内容元祖（word,mean）
        cur.execute(sql,tup)
        db.commit()
    except Exception as e:
        db.rollback()
fd.close()
cur.close()
db.close()