#encoding=utf-8
import paramiko,openpyxl,time,os
from threading import *

def cfg_download(ip_value,name,for_i):          #sftp文件下载
    transport = paramiko.Transport((ip_value, 22))
    transport.connect(username='username', password='passwd')
    sftp = paramiko.SFTPClient.from_transport(transport)
    # sftp.put(r'C:\py\test.PAT', r'/ttest.log')  # 将123.py 上传至服务器 /tmp下并改名为test.py
    print(name[for_i]+"_"+ip_value+'.zip')
    sftp.get(r'/vrpcfg.zip', r'C:/py/'+local_time+'/'+name[for_i]+"_"+ip_value+'.zip')
    transport.close()

def gain_cfgIp():                        #设备IP获取
    fd=openpyxl.load_workbook(r"C:\py\DeviceIP.xlsx")
    ip_sheet=fd['ip']
    i=2
    list_ip=[]
    name_sw=[]
    while ip_sheet["B"+str(i)].value!=None:
        # print(ip_sheet["B"+str(i)].value)
        list_ip.append(ip_sheet["B"+str(i)].value)
        name_sw.append(ip_sheet["A"+str(i)].value)
        i=i+1
    return list_ip,name_sw  #返回包含ip和name两个列表的元组,元组不能二次赋值


ip_pool=gain_cfgIp()
for_i=0
local_time=time.strftime('%Y.%m.%d_%H.%M',time.localtime(time.time()))  #创建文件夹
os.mkdir('C:/py/'+local_time)

for i in ip_pool[0]:
    t1=Thread(target=cfg_download,args=((i,ip_pool[1],for_i))) #实例化一个线程,第几次，ip，name
    t1.start()  #启动线程
    for_i=for_i+1

