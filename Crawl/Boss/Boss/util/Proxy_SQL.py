#
# -*- coding: utf-8 -*-
# Proxy_SQL.py 
# Created by MacBook Air PyCharm on 2020/3/24 9:45 下午 
# Copyright © 2020 LiYang. All rights reserved.
#
import pymysql
import pymysql.cursors


class SQLConnect:
    def __init__(self):
        self.user = 'root'
        self.passwd = 'liyangLY'
        self.post = '127.0.0.1'
        self.dbname = 'Boss'

    # 插入
    def dowmload(self, data):
        conn = pymysql.connect(self.post, self.user, self.passwd, self.dbname, charset='utf8')
        cursor = conn.cursor()
        insert_sql = """
            insert into Proxy(IP_ID, LeiXing, IP, Port)
            values (%s,%s,%s,%s)
        """
        try:
            cursor.execute(insert_sql, (data['IP_ID'], data['LeiXing'], data['IP'], data['Port']))
            conn.commit()
        except Exception as e:
            print('❌:' + str(e))
        finally:
            conn.close()

    # 弹出
    def put_one(self):
        conn = pymysql.connect(self.post, self.user, self.passwd, self.dbname, charset='utf8')
        cursor = conn.cursor()
        select_sql = """
            SELECT * from Proxy LIMIT 1
        """
        try:
            number = cursor.execute(select_sql)
            if number:
                proxy = cursor.fetchall()[0]
                sql_ = SQLConnect()
                sql_.delete(proxy[0])
                return proxy
            else:
                return None
        except Exception as e:
            print('❌:' + str(e))
        finally:
            conn.close()

    # 删除
    def delete(self, ip_id):
        conn = pymysql.connect(self.post, self.user, self.passwd, self.dbname, charset='utf8')
        cursor = conn.cursor()
        try:
            delete_sql = '''
            DELETE FROM Proxy WHERE IP_ID='%s'
            ''' % ip_id
            cursor.execute(delete_sql)
            conn.commit()
        except Exception as e:
            print('❌:' + str(e))
        finally:
            conn.close()
