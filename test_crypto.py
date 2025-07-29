from Crypto.Cipher import AES


key = b'1234567812345678'
cipher = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(b'abcdefghijklmnop')
print(ciphertext)
