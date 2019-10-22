from Crypto import Random
from Crypto.Cipher import AES


class MyCrypto:
    def __init__(self, key, block_sz=16):
        while(len(key) < 16):
            key += '\0'
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC
        # self.IV = Random.new().read(block_sz)
        self.IV = b'0000000000000000'

    def encrypt(self, data):
        while(len(data) % 16 != 0):
            data += '\0'
        cryptor = AES.new(self.key, self.mode, self.IV)
        encrypted_data = cryptor.encrypt(data)
        return encrypted_data

    def decrypt(self, encrypted_data):
        cryptor = AES.new(self.key, self.mode, self.IV)
        original_data = cryptor.decrypt(encrypted_data)
        return original_data
