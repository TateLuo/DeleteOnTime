import os, stat
import time
import configparser
import shutil


# 设置扫描间隔和未修改天数的常量

def read_config_file():
    # 读取配置文件
    config = configparser.ConfigParser()
    if not os.path.exists('config.ini'):
        
        '''
        # 如果配置文件不存在，则提示用户输入文件夹路径
        folder_path = input('请输入文件夹路径：')
        pause_time = input('请输入扫描间隔（秒）：')
        days = input('请输入未修改天数（秒）：')
        write_config_file(folder_path, pause_time, days)
        '''
        message = '配置文件不存在，请创建配置文件'
        print(message)
        log(message)
        return False
    else:
        config.read('config.ini')
        if 'settings' not in config or 'folder_path' not in config['settings'] or 'pause_time' not in config['settings'] or 'days' not in config['settings']:
            '''
            # 如果配置文件不全，则提示用户输入全部参数
            folder_path = input('请输入文件夹路径：')
            pause_time = input('请输入扫描间隔（秒）：')
            days = input('请输入未修改天数（秒）：')
            write_config_file(folder_path, pause_time, days)
            '''
            message = '配置文件参数不全，请填写完整配置文件内的参数'
            print(message)
            log(message)
            return False
        else:
            folder_path = config.get('settings', 'folder_path')
            pause_time = config.get('settings', 'pause_time')
            days = config.get('settings', 'days')
    return folder_path, days, pause_time

def write_config_path(folder_path):
    # 创建配置文件
    config = configparser.ConfigParser()
    config.add_section('settings')
    
    # 将路径、天数和暂停时间写入配置文件
    config.set('settings', 'folder_path', folder_path)
    with open('config.ini', 'w') as f:
        config.write(f)
'''
def write_config_file(folder_path, days, pause_time):
    # 创建配置文件
    config = configparser.ConfigParser()
    config.add_section('settings')
    
    # 将路径、天数和暂停时间写入配置文件
    config.set('settings', 'folder_path', folder_path)
    config.set('settings', 'days', days)
    config.set('settings', 'pause_time', pause_time)
    with open('config.ini', 'w') as f:
        config.write(f)
'''

def check_folder_path_format(folder_path):
    # 检测文件夹路径格式是否正确
    if not os.path.isabs(folder_path):
        return False
    return True

def check_folder_path_exists(folder_path):
    # 检测文件夹路径是否存在
    if not os.path.exists(folder_path):
        return False
    return True

def delete_old_files(folder_path, days):
    # 扫描文件夹中的文件并删除超过n天未修改的文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        message = "当前扫描目录"+folder_path
        print(message)
        message ="扫描到文件"+filename
        print(message)
        # 判断文件是否超过n天未修改
        if os.stat(file_path).st_mtime < time.time() -  days:
            try:
                os.chmod(file_path, stat.S_IWRITE)
                #如果是C盘，无权限无法删除
                print(f'给 文件{filename}赋予读写权限')
                log(f'给 文件{filename}赋予读写权限')
                os.remove(file_path)
                #shutil.rmtree(file_path)
                print(f'已删除文件 {filename}')
                log(f'已删除文件 {filename}')
            except PermissionError:
                print(f'无法删除文件 {filename}，权限不足')
                log(f'无法删除文件 {filename}，权限不足')

def log(message):
    # 将日志信息写入日志文件
    with open('log.txt', 'a') as f:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        log_message = f'{timestamp} - {message}\n'
        f.write(log_message)
        
def sec_to_data(y):
#秒转化为天
    h=int(y//3600 % 24)
    d = int(y // 86400)
    m =int((y % 3600) // 60)
    s = round(y % 60,2)
    h=convert_time_to_str(h)
    m=convert_time_to_str(m)
    s=convert_time_to_str(s)
    d=convert_time_to_str(d)
    # 天 小时 分钟 秒
    return d + "天" + h + "小时" + m + "分钟" + s + "秒"
def convert_time_to_str(time):
    #时间数字转化成字符串，不够10的前面补个0
    if (time < 10):
        time = '0' + str(time)
    else:
        time=str(time)
    return time

def main():
    while True:
        if read_config_file():
            # 读取配置文件
            folder_path, days, pause_time = read_config_file()
    
            # 检测文件夹路径是否存在
            if not check_folder_path_exists(folder_path):
                message = '文件夹路径不存在！请检查配置文件中的路径是否正确。'
                print(message)
                log(message)
            else:
                n_days = sec_to_data(int(days))#将秒转化为天
                message = '\n开始删除超过'+str(n_days) +'天未修改的文件...'
                print(message)
                log(message)
            
                # 删除超过30天未修改的文件
                delete_old_files(folder_path, float(days))

                message = '删除完成。'
                print(message)
                log(message)

                # 记录下一次程序执行时间
            next_execution_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + float(pause_time)))
            print(f'下一次程序执行时间：{next_execution_time}')
            log(f'下一次程序执行时间：{next_execution_time}')
            # 暂停5个小时
            time.sleep(float(pause_time))
        else:
            # 暂停5个小时
            time.sleep(10)

if __name__ == '__main__':
    main()
