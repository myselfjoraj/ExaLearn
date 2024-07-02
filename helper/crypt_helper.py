from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import misc.cred as cred


class Crypt:

    def __init__(self):
        salt = cred.SALT_KEY
        key = cred.CRYPT_KEY
        self.key = key.encode('utf-8')
        self.salt = salt.encode('utf8')
        self.enc_dec_method = 'utf-8'
        self.enc_mode = AES.MODE_CFB

    def encrypt(self, plain):
        try:
            aes_obj = AES.new(self.key, self.enc_mode, self.salt)
            hx_enc = aes_obj.encrypt(plain.encode('utf8'))
            ret = b64encode(hx_enc).decode(self.enc_dec_method)
            return ret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                print('Encryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                print('Encryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else:
                print(value_error)

    def decrypt(self, plain):
        try:
            aes_obj = AES.new(self.key,  self.enc_mode, self.salt)
            str_tmp = b64decode(plain.encode(self.enc_dec_method))
            str_dec = aes_obj.decrypt(str_tmp)
            ret = str_dec.decode(self.enc_dec_method)
            return ret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                print('Decryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                print('Decryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else:
                print(value_error)
