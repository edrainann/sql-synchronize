#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/02/16
# @Author  : Edrain
import configparser
import os
import tkinter as tk
import tkinter.messagebox
from tkinter import *
from tkinter import ttk

from connect_db import connect_db_server
from get_config import get_config_file


class GraphicDisplay(object):
    """同步SQL小工具的界面展示"""

    def __init__(self):
        """程序页面布局"""
        window = tk.Tk()  # 实例化object，建立窗口window
        window.title('SQL多环境执行')  # 给窗口的可视化起名字
        window.geometry('600x350')  # 设定窗口的大小(长 * 宽)
        # 输入SQL下方的提示框，文字
        # 在图形界面上设定标签。
        check_label = Label(window, text='请输入需要执行的SQL：')
        check_label.pack(anchor=NW)  # 放置标签。Label内容content区域放置位置，自动调节尺寸

        # 输入sql编辑框
        self.input_sql_text = Text(window, height=10)
        self.input_sql_text.pack()

        # 选择更新环境文字窗口，文字
        environment_label = Label(window, text="\n\n选择要更新的环境, 不选默认为所有测试环境执行")
        environment_label.pack()
        # 选择更新环境文字窗口
        number = tk.StringVar()
        self.number_chosen = ttk.Combobox(window, width=20, textvariable=number)  # 选择环境窗口大小
        environment_list = ["ALL", '10', '11', '12']  # 需要同步的环境
        self.number_chosen['values'] = environment_list
        self.number_chosen.pack()
        self.number_chosen.current(0)
        self.number_chosen.bind("<<ComboboxSelected>>", self.get_shell())
        check_label = Label(window, text='\n\n注意:请先输入SQL后检查，然后执行。执行完成后请检查执行结果~')
        check_label.pack(anchor=SW)  # 放置标签。Label内容content区域放置位置，自动调节尺寸

        # 下方按钮
        # bg为背景，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
        confirm_button = Button(window, text='确认SQL', bg='blue', fg='white', font=('Arial', 12), width=10,
                                command=self.confirm_sql)
        confirm_button.pack(side=LEFT, fill=Y, expand=YES)
        execute_button = Button(window, text='执行SQL', bg='green', fg='white', font=('Arial', 12), width=10,
                                command=self.exe_sql)
        execute_button.pack(side=LEFT, fill=Y, expand=YES)
        clear_button = Button(window, text='清空SQL', bg='red', fg='white', font=('Arial', 12), width=10,
                              command=self.delete_all)
        clear_button.pack(side=LEFT, fill=Y, expand=YES)

        mainloop()  # 主窗口循环显示,所有的窗口文件都必须有类似的mainloop函数。如果没有mainloop,就是一个静态的window,传入进去的值就不会有循环

    def get_shell(self):
        """获取环境"""
        system_choose = self.number_chosen.get()
        return system_choose

    def confirm_sql(self):
        """确认SQL"""
        get_confirm_sql = self.input_sql_text.get("0.0", "end")
        if get_confirm_sql != "\n":
            print("开始了")
            tkinter.messagebox.showinfo(title='请确认SQL', message=get_confirm_sql)
        else:
            print("SQL输入框为空")
            tkinter.messagebox.showinfo(title='提示', message='请输入要执行的SQL')

    def delete_all(self):
        """清空SQL"""
        self.input_sql_text.delete("0.0", "end")

    def exe_sql(self):
        """执行SQL"""
        right_result = []
        env = []
        error_message = []
        result = []
        get_execute_sql = self.input_sql_text.get("0.0", "end")  # 获取输入框的sql,获取会有换行
        print("这是需要执行的sql:", get_execute_sql)
        if get_execute_sql != "\n":
            sql = get_execute_sql
            cmd = os.getcwd()
            get_config_file(cmd)
            # 在本地路径下，保存sql执行记录
            execution_record_path = f'{cmd}\\sql执行记录.log'
            execution_record = open(execution_record_path, 'a', encoding='utf8')
            execution_record.write("\n" + "--" * 80 + "\n")
            execution_record.writelines(sql)
            execution_record.close()
            # 读取本地路径下，各个环境服务器的配置信息
            config = configparser.ConfigParser()
            config.read(f'{cmd}\\iniconfig.ini')
            sections = config.sections()
            print("所有的环境列表", sections)
            server_info = self.get_shell()
            user = []
            if not server_info:
                user = sections
            else:
                user.append(server_info)

            for env_name in user:
                host = config.get(env_name, "host")
                user = config.get(env_name, "user")
                passwd = config.get(env_name, "password")
                port_str = config.get(env_name, "port")
                port = int(port_str)
                print(f'execute {env_name} start')
                try:
                    miss = connect_db_server(host, user, passwd, port, sql)
                    right_result.append(miss)
                    env.append(env_name)
                except Exception as e:
                    print(e)
                    env.append(env_name)
                    right_result.append(e)
            print("当前SQL执行环境为：", env)
            print("right result: ", right_result)
            print(error_message)
            if right_result:
                if len(right_result) == 1:
                    tkinter.messagebox.showinfo(title='执行完成',
                                                message=f'Environment {env[0]} execute result is: {right_result[0]}')
                else:
                    for i in range(len(env)):
                        result_i = f'测试环境 {env[i]} 执行结果{[i + 1]}: {right_result[i]}'
                        result.append(result_i)
                    tkinter.messagebox.showinfo('执行完成',
                                                f'Please check your result:\n'
                                                f'{result[0]}\n\n'
                                                f'{result[1]}\n\n'
                                                f'{result[2]}\n\n'
                                                f'{result[3]}\n\n'
                                                f'{result[4]}\n\n'
                                                f'{result[5]}\n\n'
                                                f'{result[6]}\n\n'
                                                f'{result[7]}\n')
            else:
                tkinter.messagebox.showinfo('执行失败', "执行失败的哇~")
        else:
            tkinter.messagebox.showinfo('提示', '请输入要执行的SQL！')


if __name__ == '__main__':
    GraphicDisplay()
