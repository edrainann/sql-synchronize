### 1、功能

这是一个多环境时，SQL同步小工具。为了保证各个测试环境的稳定性，解决执行同一条SQL语句时，需要到各个测试环境都执行的琐碎操作。
![image.png](https://upload-images.jianshu.io/upload_images/1683050-1eeb8ecc3a327a5e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
------

### 2、文件路径

connect_db.py：连接MySQL数据库
get_config.py: 通过本地的配置文件，连接服务器，拉取服务器的配置文件
graphic_display.py: 执行同步各环境的SQL的GUI
server_info: 本地的配置文件，需要通过此文件连接服务器。
iniconfig.ini: 从服务器拉取的配置文件。
sql执行记录：通过该小应用执行的SQL记录。
output文件夹：打包的.exe文件

------

### 3、需要模块

执行：python -m pip install -r requirements.txt

paramiko
tkinter
pymysql
auto-py-to-exe

---
### 4、用到知识

1）
参考链接：https://www.jianshu.com/p/95b6a4c1b637
paramiko是用python语言写的一个模块，遵循SSH2协议，支持以加密和认证的方式，用于做远程控制，使用该模块可以对远程服务器进行命令或文件操作。
fabric和ansible内部的远程管理就是使用的paramiko来现实。

2）
参考链接：https://www.cnblogs.com/shwee/p/9427975.html
Tkinter 是使用 python 进行窗口视窗设计的模块。
Tkinter模块("Tk 接口")是Python的标准Tk GUI工具包的接口。
作为 python 特定的GUI界面，是一个图像的窗口，tkinter是python 自带的，可以编辑的GUI界面，我们可以用GUI 实现很多直观的功能。
Tkinter支持16个核心的窗口部件，这个16个核心窗口部件类简要描述如下：Button：一个简单的按钮，用来执行一个命令或别的操作。Canvas：组织图形。这个部件可以用来绘制图表和图，创建图形编辑器，实现定制窗口部件。Checkbutton：代表一个变量，它有两个不同的值。点击这个按钮将会在这两个值间切换。
Entry：文本输入域。
Frame：一个容器窗口部件。帧可以有边框和背景，当创建一个应用程序或dialog(对话）版面时，被用来组织其它的窗口部件。
Label：显示一个文本或图象。
Listbox：显示供选方案的一个列表。listbox能够被配置来得到radiobutton或checklist的行为。
Menu：菜单条。用来实现下拉和弹出式菜单。
Menubutton：菜单按钮。用来实现下拉式菜单。
Message：显示一文本。类似label窗口部件，但是能够自动地调整文本到给定的宽度或比率。
Radiobutton：代表一个变量，它可以有多个值中的一个。点击它将为这个变量设置值，并且清除与这同一变量相关的其它radiobutton。
Scale：允许你通过滑块来设置一数字值。
Scrollbar：为配合使用canvas, entry, listbox, and text窗口部件的标准滚动条。
Text：格式化文本显示。允许你用不同的样式和属性来显示和编辑文本。同时支持内嵌图象和窗口。
Toplevel：一个容器窗口部件，作为一个单独的、最上面的窗口显示。
messageBox：消息框，用于显示你应用程序的消息框。(Python2中为tkMessagebox)
注意在Tkinter中窗口部件类没有分级；所有的窗口部件类在树中都是兄弟关系。

3）参考连接：https://github.com/brentvollebregt/auto-py-to-exe
下载auto-py-to-exe库，可以将.py文件转换成.exe文件。界面上其实是通过各种按钮来添加一些指令，这些指令完全是基于pyinstaller的。
通过在命令行执行```auto-py-to-exe```启动界面，如下图
![image.png](https://upload-images.jianshu.io/upload_images/1683050-707e63c57f7b0513.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4)参考连接：https://zhuanlan.zhihu.com/p/57839415
使用pipreqs生成requirements.txt
pipreqs ./ --encoding=utf-8 --force

---
### 5、出现问题：

Q1、paramiko使用出现CryptographyDeprecationWarning: encode_point has been deprecated on  EllipticCurvePublicNumbers and will be removed in a future version.
A1:
python交互式环境下测试:
import cryptography   #没有问题，可以正常导入
help(cryptography)     #查看版本是2.6.1
本机执行:
pip install cryptography==2.4.2