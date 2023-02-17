# coding = utf-8
from telnetlib import Telnet
import re
from datetime import datetime
import time, os
import shutil


 
# from getpass import getpass
#now_time = str(time.localtime().tm_year) + str(time.localtime().tm_mon) + str(time.localtime().tm_mday)  # 获取当前日期时间
now = datetime.now()
now_time1 = str(now.year) + str(now.month) + str(now.day) # 获取当前日期时间
#username = input('username:')
#password = input('passwd:')
username = "XXXX"           #交换机登陆账号
password = "XXXXX"          #交换机登陆密码
 
ip_add_file = open("/root/h3c/h3cip_add.txt")
#ip_add_file = open(os.getcwd()  + 'ip_add.txt')  # 打开ip地址文件，需要备份的设备IP地址txt文件
path = (r'/root/h3c/backup/' + now_time1)   # 配置文件保存路径
isExists = os.path.exists(path)     # 判断文件是否已经创建
if not isExists:
    os.makedirs(path)               # 如果没有创建，则新建文件夹
    print(path + ' 创建成功！')
else:
    print(path + ' 目录已存在')        # 已经创建提示
 
for line in ip_add_file.readlines():  # for循环读取设备IP地址
    ip = line.strip()
    tn = Telnet(ip, port=60023, timeout=10)  # 远程连接设备
    print('成功登陆设备：' + ip)
    tn.read_until(b"username:",timeout=2)  # 读取输出的账户提示信息
    tn.write(username.encode('utf-8') + b'\n')  # 输入账户
    tn.read_until(b"password:",timeout=2)  # 读取输出的密码提示信息
    tn.write(password.encode('utf-8') + b'\n')  # 输入密码
    tn.read_until('>'.encode('utf-8'))
    tn.write('screen-length disable'.encode('utf-8')  + b'\n') 
    tn.write('system-view'.encode('utf-8') + b'\n')
    #tn.write('user-interface vty 0 4'+'\n')
    #time.sleep(3)
    #tn.write('screen-length 0'.encode('utf-8') + b'\n') # 设置回显内容不分屏显示
    #tn.write('screen-length 0'.encode('utf-8')  + b'\n') # 设置回显内容不分屏显示
    time.sleep(3)
    tn.write('dis cur'.encode('utf-8') + b'\n')  # 查询配置信息
    time.sleep(30)         # 等待结果输出时间，配置越多，输出时间应对应增加
    command_result = tn.read_very_eager().decode('utf-8')
    time.sleep(10)
    #Sw_name = re.findall('<(\w+\_\d\w\_\w+\_\w+)>', command_result)[0] # 提取配置文件中的设备名称
    #backup = open(path + '\\' + Sw_name + '-' + ip + '.txt','a+')  # 备份配置文件保存路径+文件名
    backup = open(path + 'h3c-'  + ip + '.txt','a+')  # 备份配置文件保存路径+文件名
    #print("成功备份：" + Sw_name + '-' + ip)
    print("成功备份：" +  'h3c' + ip)
    backup.write(command_result)   # 将回显内容写入backup这个对象，相当于写入了备份文件中
    backup.close()
tn.close()
print('备份完成！')



# 删除大于30天备份
dest_dir = "/root/h3c/backup"
all_dir = []
for f in list(os.listdir(dest_dir)):
    dir = "{}\\{}".format(dest_dir, f)
    if os.path.isdir(dir):
       all_dir.append(dir)

for i in range(len(all_dir)):
    dir_create_time = time.strftime("%Y%m%d", time.localtime(os.path.getctime(all_dir[i])))
    now_time = time.strftime("%Y%m%d", time.localtime())
    del_time = datetime.date.today() - datetime.timedelta(days=30)
    del_time_str = del_time.strftime("%Y%m%d")
    if int(dir_create_time) < int(del_time_str):
       shutil.rmtree(all_dir[i])
       print("已删除的文件 {}".format(all_dir[i]))
