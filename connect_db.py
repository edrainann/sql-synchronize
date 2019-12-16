#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/02/16
# @Author  : Edrain
import pymysql


def connect_db_server(host, username, password, port, sql):
    """连接数据库服务器"""
    conn = pymysql.connect(host=host, user=username, passwd=password, port=port, charset='utf8')
    cursor = conn.cursor()
    count = cursor.execute("%s" % sql)
    message = f'there has {count} rows record'
    cursor.close()
    conn.commit()
    conn.close()
    return message
