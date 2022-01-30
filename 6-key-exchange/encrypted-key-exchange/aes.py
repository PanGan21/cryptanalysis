from Crypto.Cipher import AES
import Padding


def encrypt(plaintext, key, mode=AES.MODE_ECB):
    plaintext = Padding.appendPadding(
        plaintext, blocksize=Padding.AES_blocksize, mode=0)
    encobj = AES.new(key, mode)
    return(encobj.encrypt(plaintext.encode()))


def decrypt(ciphertext, key, mode=AES.MODE_ECB):
    encobj = AES.new(key, mode)
    b = encobj.decrypt(ciphertext)
    rtn = Padding.removePadding(b.decode(), mode=0)
    return(rtn)
