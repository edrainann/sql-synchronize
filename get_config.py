#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/02/16
# @Author  : Edrain
import configparser
import os

import paramiko


def get_config_file(cmd):
    """从系统上获取数据库的配置文件"""
    config = configparser.ConfigParser()
    config.read(f'{cmd}/server_info')  # 读取本地路径文件，名称为 server_info的文件，改文件需要和程序放在相同目录下
    sections = config.sections()
    print("这是获取本地的配置文件：", sections)
    host = config.get("info", "host")
    username = config.get("info", "user")
    password = config.get("info", "password")
    t = paramiko.Transport(host, 22)  # 用于做远程控制
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    src = '/home/simplecredit/config/iniconfig.ini'  # 远程路径和文件名
    des = os.path.join(cmd, 'iniconfig.ini')  # 拼接保存本地路径和文件名
    sftp.get(src, des)  # 下载文件
    t.close()
