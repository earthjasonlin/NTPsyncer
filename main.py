import json
import os
import ntplib
import time
import logging
from datetime import datetime
import win32api

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ASCII 图像和软件信息
ascii_art = r"""
    _   ____________                                     
   / | / /_  __/ __ \    _______  ______  ________  _____
  /  |/ / / / / /_/ /   / ___/ / / / __ \/ ___/ _ \/ ___/
 / /|  / / / / ____/   (__  ) /_/ / / / / /__/  __/ /    
/_/ |_/ /_/ /_/       /____/\__, /_/ /_/\___/\___/_/     
                           /____/                        
"""

software_info = """
NTP syncer v1.0
Version Date: 2024-06-16
Copyright © 2024 earthjasonlin
Homepage: https://git.loliquq.cn/earthjasonlin/NTP-syncer
Description: This tool synchronizes your system time with multiple NTP servers, considering network delay and time correction.

========================================
"""

# 打印 ASCII 图像和软件信息
print(ascii_art)
print(software_info)

# 定义 NTP 服务器池
# ntp_servers = [
#     # 国家授时中心 NTP 服务器
#     "ntp.ntsc.ac.cn", "114.118.7.161", "114.118.7.163",
#     # 中国 NTP 快速授时服务
#     "cn.ntp.org.cn", "223.113.97.98", "114.67.103.73", "119.29.26.206", "120.25.115.20",
#     # 教育网
#     "edu.ntp.org.cn", "202.118.1.130", "202.118.1.81", "116.13.10.10",
#     # 中国计量科学研究院 NIM 授时服务
#     "ntp1.nim.ac.cn", "ntp2.nim.ac.cn", "111.203.6.13",
#     # 国际 NTP 快速授时服务
#     "cn.pool.ntp.org", "120.25.115.20", "111.230.189.174", "119.28.183.184",
#     # 阿里云公共 NTP 服务器
#     "ntp.aliyun.com", "ntp1.aliyun.com", "ntp2.aliyun.com", "ntp3.aliyun.com",
#     "ntp4.aliyun.com", "ntp5.aliyun.com", "ntp6.aliyun.com", "ntp7.aliyun.com",
#     "203.107.6.88", "182.92.12.11", "120.25.108.11",
#     # 腾讯云公共 NTP 服务器
#     "ntp.tencent.com", "ntp1.tencent.com", "ntp2.tencent.com", "ntp3.tencent.com",
#     "ntp4.tencent.com", "ntp5.tencent.com",
#     # 高通中国提供 NTP 服务
#     "time.izatcloud.net", "time.gpsonextra.net",
#     # 教育网（高校自建）
#     "ntp.sjtu.edu.cn", "ntp.neu.edu.cn", "ntp.bupt.edu.cn", "ntp.shu.edu.cn",
#     # 国际 NTP 快速授时服务
#     "pool.ntp.org", "0.pool.ntp.org", "1.pool.ntp.org", "2.pool.ntp.org", "3.pool.ntp.org",
#     "asia.pool.ntp.org", "64.62.194.188", "81.169.199.94",
#     # 谷歌公共 NTP 服务器
#     "time1.google.com", "time2.google.com", "time3.google.com", "time4.google.com",
#     "216.239.35.0", "216.239.35.4", "216.239.35.8", "216.239.35.12",
#     # 苹果公司公共 NTP 服务器
#     "time.apple.com", "time1.apple.com", "time2.apple.com", "time3.apple.com",
#     "time4.apple.com", "time5.apple.com", "time6.apple.com", "time7.apple.com",
#     "17.253.84.123", "17.253.84.125", "17.253.114.253", "17.253.116.253",
#     # Cloudflare NTP 服务器
#     "time.cloudflare.com", "162.159.200.1", "162.159.200.123",
#     # 微软 Windows NTP 服务器
#     "time.windows.com", "20.189.79.72", "52.148.114.188", "40.119.6.228", "51.137.137.111",
#     # 美国标准技术研究院 NTP 服务器
#     "time.nist.gov", "time-nw.nist.gov", "time-a.nist.gov", "time-b.nist.gov",
#     "128.138.141.172", "132.163.96.1", "132.163.96.2", "132.163.97.1", "132.163.97.2",
# ]

# 默认配置
default_config = {
    "ntp_servers": [
        "ntp.ntsc.ac.cn",
        "114.118.7.161",
        "114.118.7.163",
        "cn.ntp.org.cn",
        "223.113.97.98",
        "114.67.103.73",
        "119.29.26.206",
        "120.25.115.20",
        "edu.ntp.org.cn",
        "202.118.1.130",
        "202.118.1.81",
        "116.13.10.10",
        "ntp1.nim.ac.cn",
        "ntp2.nim.ac.cn",
        "111.203.6.13",
        "cn.pool.ntp.org",
        "120.25.115.20",
        "111.230.189.174",
        "119.28.183.184",
        "ntp.aliyun.com",
        "ntp1.aliyun.com",
        "ntp2.aliyun.com",
        "ntp3.aliyun.com",
        "ntp4.aliyun.com",
        "ntp5.aliyun.com",
        "ntp6.aliyun.com",
        "ntp7.aliyun.com",
        "203.107.6.88",
        "182.92.12.11",
        "120.25.108.11",
        "ntp.tencent.com",
        "ntp1.tencent.com",
        "ntp2.tencent.com",
        "ntp3.tencent.com",
        "ntp4.tencent.com",
        "ntp5.tencent.com",
        "time.izatcloud.net",
        "time.gpsonextra.net",
        "ntp.sjtu.edu.cn",
        "ntp.neu.edu.cn",
        "ntp.bupt.edu.cn",
        "ntp.shu.edu.cn",
        "pool.ntp.org",
        "0.pool.ntp.org",
        "1.pool.ntp.org",
        "2.pool.ntp.org",
        "3.pool.ntp.org",
        "asia.pool.ntp.org",
        "64.62.194.188",
        "81.169.199.94",
        "time1.google.com",
        "time2.google.com",
        "time3.google.com",
        "time4.google.com",
        "216.239.35.0",
        "216.239.35.4",
        "216.239.35.8",
        "216.239.35.12",
        "time.apple.com",
        "time1.apple.com",
        "time2.apple.com",
        "time3.apple.com",
        "time4.apple.com",
        "time5.apple.com",
        "time6.apple.com",
        "time7.apple.com",
        "17.253.84.123",
        "17.253.84.125",
        "17.253.114.253",
        "17.253.116.253",
        "time.cloudflare.com",
        "162.159.200.1",
        "162.159.200.123",
        "time.windows.com",
        "20.189.79.72",
        "52.148.114.188",
        "40.119.6.228",
        "51.137.137.111",
        "time.nist.gov",
        "time-nw.nist.gov",
        "time-a.nist.gov",
        "time-b.nist.gov",
        "128.138.141.172",
        "132.163.96.1",
        "132.163.96.2",
        "132.163.97.1",
        "132.163.97.2",
    ],
    "update_interval": 600
}

# 从 JSON 文件中读取 NTP 服务器列表和更新间隔
def load_config(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(default_config, file, ensure_ascii=False, indent=4)
        logging.info(f"The configuration file {file_path} does not exist. A default configuration file has been created.")
        logging.info("=" * 40)  # 分隔符
    with open(file_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config['ntp_servers'], config['update_interval']

# 定义初始配置文件路径
config_file_path = 'ntp_config.json'

# 加载 NTP 服务器列表和更新间隔
ntp_servers, update_interval = load_config(config_file_path)
last_successful_index = 0

def get_ntp_time(server):
    client = ntplib.NTPClient()
    
    try:
        send_time = time.time()
        response = client.request(server, version=3)
        receive_time = time.time()
        
        # 计算延迟
        delay = (receive_time - send_time) / 2
        
        # 计算调整后的时间
        ntp_time = response.tx_time + delay
        return ntp_time, delay, response.tx_time
    except ntplib.NTPException as e:
        logging.warning(f"Unable to get NTP time from {server}: {e}")
        return None, None, None

def update_system_time(ntp_time):
    try:
        # 获取当前系统时间（更新前）
        current_system_time = datetime.utcnow()
        
        # 格式化 NTP 时间为 datetime 对象（使用 UTC 时间）
        dt = datetime.utcfromtimestamp(ntp_time)
        
        # 获取星期几 (0 是星期一, 6 是星期日)
        day_of_week = dt.weekday() + 1  # Windows API 需要 1 (星期一) 到 7 (星期日)

        # 调用 win32api 设置系统时间
        win32api.SetSystemTime(
            dt.year,        # 年
            dt.month,       # 月
            day_of_week,    # 星期几
            dt.day,         # 日
            dt.hour,        # 时
            dt.minute,      # 分
            dt.second,      # 秒
            int(dt.microsecond / 1000)  # 毫秒
        )
        
        # 获取当前系统时间（更新后）
        new_system_time = datetime.utcnow()

        # 计算时间偏移（更新后的系统时间与NTP时间的差异）
        correction = (new_system_time - current_system_time).total_seconds()
        
        logging.info(f"System time updated to: {dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} UTC")
        logging.info(f"Time correction: {correction*1000:.3f} ms")
    except Exception as e:
        logging.error(f"Unable to update system time: {e}")

def main():
    global last_successful_index
    
    while True:        
        for i in range(len(ntp_servers)):
            index = (last_successful_index + i) % len(ntp_servers)
            server = ntp_servers[index]
            
            ntp_time, delay, raw_ntp_time = get_ntp_time(server)
            
            if ntp_time:
                last_successful_index = index
                logging.info(f"Got NTP time from {server}: {datetime.utcfromtimestamp(raw_ntp_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} UTC")
                logging.info(f"Network delay: {delay*1000:.3f} ms")
                
                update_system_time(ntp_time)
                break
        else:
            logging.warning("All NTP servers attempted but unable to get time. Waiting for next attempt...")
        
        # 每隔一段时间检查一次
        time.sleep(update_interval)
        
        logging.info("=" * 40)  # 分隔符

if __name__ == "__main__":
    main()