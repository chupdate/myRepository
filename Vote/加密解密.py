__author__ = 'YouYou'
# coding=utf-8
from Crypto.Cipher import AES
from binascii import a2b_hex,b2a_hex,b2a_base64
import base64

class prpcrypt():

    def __init__(self,key,iv):
        #a2b:ascii转化为bytes
        self.key = a2b_hex(key)
        self.mode = AES.MODE_CBC
        self.iv=a2b_hex(iv)

    def encrypt(self,text):
        cryptor = AES.new(self.key,self.mode,self.iv)
        self.ciphertext = cryptor.encrypt(text)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        #所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    def decrypt(self,text):
        cryptor = AES.new(self.key,self.mode,self.iv)
        plain_text  = cryptor.decrypt(a2b_hex(text))
        return plain_text

if __name__ == '__main__':
    pc = prpcrypt('0e0e020104050d0707090b0b0c0d0e0a','0a0e0d070b0a090a07060304030d010b') #初始化密钥
    e = pc.encrypt(b'xy@520520       ') #加密,后面用空格补齐32个字符
    d = pc.decrypt(e) #解密
    #print("加密:",base64.b64encode(e))
    print("加密:",base64.b64encode(a2b_hex(e)))
    print("解密:",d)


