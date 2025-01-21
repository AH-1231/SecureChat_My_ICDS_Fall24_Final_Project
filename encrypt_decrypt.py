import rsa
import os 
from Crypto.Cipher import AES  
from Crypto.Util.Padding import pad,unpad  
import base64
from encode_decode import *
def encrypt_aes(plaintext, aes_key):
    if not isinstance(plaintext, str):
        raise ValueError("Plaintext must be a string")
    if not isinstance(aes_key, bytes) or len(aes_key) not in {16, 24, 32}:
        raise ValueError("AES key must be bytes of length 16, 24, or 32")
    # 生成随机初始化向量 (IV)
    iv = os.urandom(16)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    padded_message = pad(plaintext.encode(), AES.block_size)
    encrypted_message = iv + cipher.encrypt(padded_message)
    # 返回 Base64 编码的密文
    return base64.b64encode(encrypted_message).decode()

def decrypt_aes(ciphertext, aes_key):
    if not isinstance(ciphertext, str):
        raise ValueError("Ciphertext must be a Base64 encoded string")
    if not isinstance(aes_key, bytes) or len(aes_key) not in {16, 24, 32}:
        raise ValueError("AES key must be bytes of length 16, 24, or 32")
    # 解码 Base64 编码的密文
    encrypted_message = base64.b64decode(ciphertext)
    iv = encrypted_message[:16]
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    decrypted_padded_message = cipher.decrypt(encrypted_message[16:])
    # 去除填充并返回解密后的消息
    plaintext = unpad(decrypted_padded_message, AES.block_size)
    return plaintext.decode()

def encryption(target_rsa_key, message):
    aes_key = os.urandom(16)  # 生成 AES 密钥
    target_rsa_key =decode_rsa_key(target_rsa_key)
    encrypted_aes_key = rsa.encrypt(aes_key, target_rsa_key)  # 使用公钥加密 AES 密钥
    encoded_aes_key= encode_aes_key(encrypted_aes_key)  # 将字节对象转换为 Base64 编码的字符串
    encrypted_message = encrypt_aes(message, aes_key)  # 使用 AES 加密消息,已转为字符串
    return encoded_aes_key, encrypted_message

def decryption(private_rsa_key,encrypted_aes_key,encrypted_message):
    encrypted_aes_key = decode_aes_key(encrypted_aes_key)
    aes_key = rsa.decrypt(encrypted_aes_key, private_rsa_key)  # 使用私钥解密 AES 密钥
    decrypted_message = decrypt_aes(encrypted_message, aes_key)  # 使用 AES 解密消息
    return decrypted_message