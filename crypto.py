from datetime import datetime
from Crypto.Cipher import AES
from configparser import ConfigParser

class myAES:
    def __init__(self, path):
        #从asta.ini读入配置
        self.config = ConfigParser(allow_no_value=True)
        self.config.read(path, encoding="utf-8")
        self.key = self.config.get('GPU_Server', 'KEY').encode('utf-8')
        self.iv = self.config.get('GPU_Server', 'IV').encode('utf-8')
    
    def encrypt(self, start, end):
        #输入两个时间，加密为字符串
        text = str(start.timestamp())+' '+str(end.timestamp())
        l = len(text)&15
        if l>0:
            text += ' '*(16-l)
        self.aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        res = self.aes.encrypt(text.encode('utf-8'))
        return res
    
    def decrypt(self, text):
        #输入密文解密为开始、结束时间
        self.aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        text = self.aes.decrypt(text)
        start, end = [datetime.fromtimestamp(float(a)) for a in text.split()]
        return start, end

if __name__ == "__main__":
    #测试
    a = myAES('asta.ini')
    b = datetime.now()
    c = datetime.now()
    e = a.encrypt(b, c)
    print(e)
    print(a.decrypt(e))