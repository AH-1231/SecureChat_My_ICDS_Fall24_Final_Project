import base64
import rsa
def encode_rsa_key(key):
    key_pem = key.save_pkcs1(format='PEM') # rsa_key_data to bytes_data
    key_pem_str = key_pem.decode() # bytes_data to str_data
    return key_pem_str
def decode_rsa_key(key):
    key=key.encode() #str_data to bytes_data
    loaded_key = rsa.PublicKey.load_pkcs1(key) #bytes_data to rsa_key_data
    return loaded_key
def encode_aes_key(key):
    #Change bytes(aes_key_data) to str
    key_b64 = base64.b64encode(key).decode()  
    return key_b64
def decode_aes_key(key):
    #Change str to bytes
    decoded_aes_key = base64.b64decode(key)
    return decoded_aes_key

