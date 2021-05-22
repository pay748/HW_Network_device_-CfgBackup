#encoding=utf-8
import paramiko,openpyxl,time,re,os,sys,threading
from threading import *
from netmiko import ConnectHandler


def gain_cfgIp():                               #设备IP获取
    fd=openpyxl.load_workbook(sys.path[0]+r'/DeviceIP.xlsx')
    ip_sheet=fd['ip']
    i=2
    list_ip=[]
    name_sw=[]
    while ip_sheet["B"+str(i)].value!=None:
        #print(ip_sheet["B"+str(i)].value)
        list_ip.append("".join(map(lambda x:str(x),re.findall("[0-9,/.]",ip_sheet["B"+str(i)].value))))#IP地址字符过滤，只筛选出数字和.
        name_sw.append(ip_sheet["A"+str(i)].value)
        i=i+1
    return list_ip,name_sw  #返回包含ip和name两个列表的元组,元组不能二次赋值

def save_cfg(ip_value):                         #当前配置保存
    h3c = {
        'device_type':'hp_comware',  #修改对应的device_type对应的值已适配不同的网络厂商，华三：hp_comware，华为：huawei
        'ip':ip_value,
        'username':username,
        'password':password,
        }
    huawei = {
        'device_type':'huawei',  #华三：hp_comware，华为：huawei
        'ip':ip_value,
        'username':username,
        'password':password,
        }    
    pool_sema.acquire()    
    print(ip_value+'：配置保存中....')
    try:
        #connect=ConnectHandler(**huawei)
        connect=ConnectHandler(**h3c)                                 #不同厂商设备选用不同字典：华为使用huawei，华三使用h3c
        output_1 = connect.send_command_timing('save\ny\n\ny\n')      #沿通道发送命令，返回输出（基于时序）
        print(ip_value+'：配置保存完成')
        connect.disconnect()
    except Exception as e:
        print(ip_value+'：登陆失败！！！\n【error info】:',e)
    pool_sema.release()

def cfg_download(ip_value,name,for_i,backup_path):          #sftp文件下载
    pool_sema.acquire() 
    try:
        transport = paramiko.Transport((ip_value, 22))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        # sftp.put(r'C:\py\test.PAT', r'/ttest.log')  # 将123.py 上传至服务器 /tmp下并改名为test.py
        sftp.get(cfg_name,backup_path+'/'+name[for_i]+"_"+ip_value+'.cfg')
        print('配置备份文件生成:'+name[for_i]+"_"+ip_value+'.cfg')
        transport.close()  
    except Exception as e:
        print(name[for_i]+"_"+ip_value+'：配置文件备份失败！！！\n【error info】:',e)
    pool_sema.release()     

def main():
#设备信息拉取
    ip_pool=gain_cfgIp()  
    print(type(ip_pool))
    
#设备当前运行配置保存
    for i in ip_pool[0]:
        t2=Thread(target=save_cfg,args=(i,))
        t2.start()  #启动线程
    time.sleep(60)
    
#设备配置文件下载存储
    for_i=0
    for i in ip_pool[0]:
        if for_i==0:
        #以当前时间为文件名，创建文件夹
            local_time=time.strftime('%Y.%m.%d_%H.%M',time.localtime(time.time()))  #创建文件夹
            try:
                os.mkdir(sys.path[0]+'/'+local_time)
            except Exception as e:    
                print(e)
            backup_path=sys.path[0]+'/'+local_time           
        t1=Thread(target=cfg_download,args=((i,ip_pool[1],for_i,backup_path))) #实例化一个线程,第几次，ip，name
        t1.start()  #启动线程
        for_i=for_i+1

#传参
#DeviceType='hp_comware'         #设备厂商——华三设备——hp_comware、华为：huawei
#DeviceTables_path=sys.path[0]+r'/DeviceIP.xlsx'
max_connections = 100           # 定义最大线程数
cfg_name=r'/startup.cfg'        #修改需要下载的配置文件名，不同厂商配置文件名不同，缺省——华为：vrpcfg.zip、华三：startup.cfg
username='user'                 #输入需要登陆设备的ssh账户
password='password'             #输入需要登陆设备的ssh密码
#传参

pool_sema = threading.BoundedSemaphore(max_connections) # 最大线程限制

if __name__ == "__main__":
    main()
