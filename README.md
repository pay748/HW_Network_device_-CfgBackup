# HW_Network_device_-CfgBackup-MultithreadingSftp-
MultithreadingSftp，多设备配置自动下载保存，配置文件自动命名

该PY脚本用于从指定的网络设备上下载文件名为vrpcfg.zip的配置文件，并以各设备名做为文件命名保存在以时间节点创建的文件夹中。

使用说明：
  1.DeviceIP.xlsx用于存储需要备份的设备ip、设备名称。
  2.使用前需要根据脚本下载后存放的磁盘位置以及备份文件的存储位置修改DeviceCfgBackup_v2.0.py脚本中的绝对路径信息。
  3.暂未添加线程数限制，后期会加入。
