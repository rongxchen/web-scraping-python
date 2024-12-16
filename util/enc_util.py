import base64
import hashlib
from Crypto.Cipher import AES


SEC_KEY = "b9ef0b9340e6401509a289cb10e10ba444ea0c1c018a16c70df7617b4207daea"[:16]
BLOCK_SIZE = 16

pad = lambda x: x + (BLOCK_SIZE - len(x) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(x) % BLOCK_SIZE)
unpad = lambda x: x[:-ord(x[len(x)-1:])]


# AES encryption and decryption
def aes_encrypt(text: str, sec_key: str = SEC_KEY, iv: str = None) -> str:
    cipher = AES.new(sec_key.encode(), AES.MODE_CBC, iv.encode()) if iv is not None \
        else AES.new(sec_key.encode(), AES.MODE_ECB)
    padded_text = pad(text)
    cipher_text = cipher.encrypt(padded_text.encode())
    encrypted_data = base64.b64encode(cipher_text).decode()
    return encrypted_data


def aes_decrypt(cipher_text: str, sec_key: str = SEC_KEY, iv: str = None):
    try:
        encrypted_data = base64.b64decode(cipher_text)
        cipher = AES.new(sec_key.encode(), AES.MODE_CBC, iv.encode()) if iv is not None \
            else AES.new(sec_key.encode(), AES.MODE_ECB)
        decrypted_data = cipher.decrypt(encrypted_data)
        plaintext = unpad(decrypted_data).decode()
        return plaintext
    except:
        return None


# SHA
def sha256_enc(text: str):
    hash = hashlib.sha256(text.encode())
    enc = hash.hexdigest()
    return enc


# MD5
def md5_enc(text: str):
    md5_hash = hashlib.md5()
    md5_hash.update(text.encode('utf-8'))
    enc = md5_hash.hexdigest()
    return enc


sec = {
    "secretKey": "fsdsogkndfokasodnaso",
    "aesKey": "B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl",
    "aesIv": "C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4"
}

enc = aes_decrypt(
    cipher_text="Z21kD9ZK1ke6ugku2ccWu-MeDWh3z252xRTQv-wZ6jddVo3tJLe7gIXz4PyxGl73nSfLAADyElSjjvrYdCvEP4pfohVVEX1DxoI0yhm36ytQNvu-WLU94qULZQ72aml6MdaC9LzSO4qdlPmtuyg_YvDQQMdLTVnTMYtInG0ZBrNPOPNzjjiq-jHBIXclo3bdhEzfuCQJrHD9t_lAkSsXJJMWMnE2HZm_g86NPlGORn2w21mrfqMP_Mc96pue4l-upHy_Dlw8NKfIiqjkfVSG6kxyE3oj-56 b5O7rjrKZ1ddUeivB627dvhzgf1Q5iugT-mU2NUPmcPsbp6iVXQ24ol07NwF1jJZmICT4Jc4qv4dt5oxft01Fv6RKqUSspdQjl1ePM9YiH_1iKjo-LN5UnVOp3wvbZSKvNIBKC-Th1NLSPkSEYMTl3AfBb7TKDSw3HDpsfZSAs-I78hplaQdsUjfG9YiyYER_pWstmNdsnMzzUV7GSp6vp5Jh8BkYA6hjQr93DYTafwAeXml0PoFr3hM1GKC2HSoN-k40A06hKJ0P6I-dFnKyvn0MyEcoUh2ggzQLyd4FukFaKxQzQfaA5Z7ZByF-7 jA5HCbwQeeJgUV4IY9iGyZ5xkYG_AlegcuXVGroLs21GWfY-SBaom7DUzkBTC38fotkVCfzd5gPsZofTr_ZmWmM_CIa4WLulYT5xsvKVUFpguspyPrcEXs6koZhny5ZCzbrIxhMJX7uyEF9rxwnIoYfoH4KTiZIUoSUju7N8Vo-APiKOoBkeCrSwfyDXNRKxDEN4Yg8afiW-QMP5LhdOWtLPgZZJDXpgU7jXV5wLLk8UA_eTKifbRI3OzxinwsV3l3xGZnnbS6NGZKfJrLGkdGjZVB9LZhECOMKD8OM-bnJRKKpI6-5 juw1lDeTLyxewCx8aAF9BAW9JqZIVtMLw7wMKwVip27BbLmCUKT0oaWDK8DTos-_gIwkF5tCzphT8FQL2ysIO-Q92IZ8oRPYQzm9QlUNN_6vC-Y-HQN0-S8WPAHVri2tdmTy8_uZm5bzZ-oLQXNSZWItt6-f3NpKQvPOidJTTq8ody2eBXJa8ImoF1I4ZeX0quLMme7T4SsuMMI0pKCXETNU5ae30Vm818QSbt2yqZAZe7_OLE-gUgBtX0KgwTxMlaswrRkq4q76NvXY3Pz0uwzW24aTx_iH3gcXu6Nywdl5Jk20jDDYlozu74RyrJZYj3Xol1roY3LD8HqyqZUqbssKYHeFI7VNqi8dQ9SboWSC43J_Uv0exurLIXtEYFWuKp-TgKdXdYn1lPXIINwsPx2Ohpc=", 
    sec_key=sec["aesKey"][:16],
    iv=sec["aesIv"][:16],
)
print(enc)
