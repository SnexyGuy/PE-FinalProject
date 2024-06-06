from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import sys

aes_key = get_random_bytes(32)

def encrypt(msg : bytes):
    cipher = AES.new(aes_key,AES.MODE_GCM)
    nonce = cipher.nonce
    cipher_text, tag = cipher.encrypt_and_digest(msg)
    return_enc = [tag,nonce,cipher_text]
    return return_enc

def decrypt(tag : bytes , nonce : bytes , ciphertext : bytes):
    cipher = AES.new(aes_key,AES.MODE_GCM,nonce=nonce)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext,tag)
        return plaintext
    except ValueError:
        print("The message was modified!")
        sys.exit(1)


txt = b'hi hello hi hello'

enc = encrypt(txt)

print(enc[2])

dec = decrypt(enc[0],enc[1],enc[2])

print(dec)

