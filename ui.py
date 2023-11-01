import tkinter as tk
from tkinter import filedialog
import configparser
import subprocess
from tkinter import messagebox
import time
import ctypes
import base64
from qq import img
import os


#服务状态：
SERVICE_STATUS = ""

def select_folder():
    folder_path = filedialog.askdirectory()
    folder_path_label.config(text=folder_path)

def save_config():
    if folder_path_label.cget('text') and pause_time_label.cget("text") and days_entry.get():
        config = configparser.ConfigParser()
        config['settings'] = {
            'folder_path': folder_path_label.cget('text'),
            'pause_time': pause_time_entry.get(),
            'days': days_entry.get()
        }
        with open('config.ini', 'w') as config_file:
            config.write(config_file)
        messagebox.showinfo('保存配置', '配置已保存')
    else:
        messagebox.showinfo('错误', '不得为空，单位为秒')
        
def check_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()

def install_service():
    if check_admin():
        result = subprocess.run(['CMD', '/C', 'WinSW-x64.exe', 'install', 'WinSW-x64.xml'], shell=True, capture_output=True, text=True)
        if "successfully" in result.stdout:
            messagebox.showinfo('安装系统服务', result.stdout)
            check_service_status()
            time.sleep(2)
            resultstart = subprocess.run(['CMD', '/C', 'net start DeleteOverdueFiles'], shell=True, capture_output=True, text=True)
            messagebox.showinfo('启动系统服务', resultstart.stdout)
            check_service_status()
        else:
            messagebox.showinfo('安装系统服务', result.stdout)
            check_service_status()
    else:
        messagebox.showinfo('提示', '未以管理员权限运行，请使用管理员权限运行')
        
def uninstall_service():
    if check_admin():
        result = subprocess.run(['CMD', '/C', 'WinSW-x64.exe', 'uninstall', 'WinSW-x64.xml'], shell=True, capture_output=True, text=True)
        messagebox.showinfo('卸载系统服务', result.stdout)
        check_service_status() 
        if "successfully" in result.stdout:
            time.sleep(2)
            resultstop = subprocess.run(['CMD', '/C', 'net stop DeleteOverdueFiles'], shell=True, capture_output=True, text=True)
            messagebox.showinfo('停止系统服务', resultstop.stdout)
            check_service_status()
        else:
            messagebox.showinfo('卸载系统服务', result.stdout)
            check_service_status()            
    else:
        messagebox.showinfo('提示', '未以管理员权限运行，请使用管理员权限运行')        
    
def check_service_status():
    result = subprocess.run(['CMD', '/C', 'sc', 'query', 'DeleteOverdueFiles'], shell=True, capture_output=True, text=True)
    if 'SERVICE_NAME' in result.stdout and 'DeleteOverdueFiles' in result.stdout:
        if 'STATE' in result.stdout and 'RUNNING' in result.stdout:
            service_status_label.config(text='服务状态：运行中')
        else:
            service_status_label.config(text='服务状态：未运行')
    else:
        service_status_label.config(text='服务状态：未安装')


    
root = tk.Tk()
#调整窗口大小并居中
screen_width,screen_height = root.maxsize()#获取屏幕最大长宽
w = int((screen_width-240)/2)
h = int((screen_height-480)/2)
root.geometry(f'240x480+{w}+{h}')#设置窗口大小为240x480，调整位置
root.resizable(width=False,height=False)#False表示不可以缩放，True表示可以缩放
root.title('定时删除文件')

# 将import进来的icon.py里的数据转换成临时文件tmp.ico，作为图标
tmp = open("tmp.ico","wb+")  
tmp.write(base64.b64decode(img))#写入到临时文件中
tmp.close()
root.iconbitmap("tmp.ico") #设置图标
os.remove("tmp.ico") 

folder_path_label = tk.Label(root, text='')
folder_path_label.pack()

select_folder_button = tk.Button(root, text='选择文件夹路径', command=select_folder)
select_folder_button.pack()

pause_time_label = tk.Label(root, text='软件扫描时间间隔/秒')
pause_time_label.pack()

pause_time_entry = tk.Entry(root)
pause_time_entry.pack()

days_label = tk.Label(root, text='删除时间间隔/秒')
days_label.pack()

days_entry = tk.Entry(root)
days_entry.pack()

save_config_button = tk.Button(root, text='保存配置', command=save_config)
save_config_button.pack()

service_status_label = tk.Label(root, text='服务状态：')
service_status_label.pack()


install_service_button = tk.Button(root, text='将程序安装为系统服务', command=install_service)
install_service_button.pack()

uninstall_service_button = tk.Button(root, text='卸载系统服务', command=uninstall_service)
uninstall_service_button.pack()
  
check_service_status_button = tk.Button(root, text='检查服务状态', command=check_service_status)
check_service_status_button.pack()
root.mainloop()
