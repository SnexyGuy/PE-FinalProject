from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import sys





def generate_aes_key():
    aes_key = get_random_bytes(32)
    return aes_key


def encrypt(aes_key : bytes, msg : bytes):
    cipher = AES.new(aes_key,AES.MODE_GCM)
    nonce = cipher.nonce
    cipher_text, tag = cipher.encrypt_and_digest(msg)
    return_enc = [tag,nonce,cipher_text]
    return return_enc

def decrypt(aes_key : bytes, tag : bytes , nonce : bytes , ciphertext : bytes):
    cipher = AES.new(aes_key,AES.MODE_GCM,nonce=nonce)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext,tag)
        return plaintext
    except ValueError:
        print("The message was modified!")
        sys.exit(1)


def rsa_key_generator():
    key = RSA.generate(2048)
    private_key = key.exportKey()
    public_key = key.public_key().export_key()
    return (private_key,public_key)

def encrypt_aes_key(aes_key : bytes, public_rsa_key_in_bytes : bytes):
    public_rsa_key = RSA.import_key(public_rsa_key_in_bytes)
    rsa_cipher = PKCS1_OAEP.new(public_rsa_key)
    encrypted_aes_key = rsa_cipher.encrypt(aes_key)
    return encrypted_aes_key

def decrypt_aes_key(encrypted_aes_key : bytes, private_rsa_key_in_bytes : bytes):
    private_rsa_key = RSA.import_key(private_rsa_key_in_bytes)
    rsa_cipher = PKCS1_OAEP.new(private_rsa_key)
    decrypted_aes_key = rsa_cipher.decrypt(encrypted_aes_key)
    return decrypted_aes_key



msg = 'hi my name is yarin zagovalov weeeeeeeeeee weeeeeeeee woooooooo woooooooooooooo'.encode()

aes_key = generate_aes_key()

print(f'aes key: {aes_key}')

priv,publ= rsa_key_generator()

print(f'private key: {priv}  public key: {publ}')

tag,nonce,enc_msg = encrypt(aes_key,msg)

print(f'tag: {tag}  nonce: {nonce}  encrypted msg: {enc_msg}')

enc_aes = encrypt_aes_key(aes_key,publ)

print(f'encrypted aes key: {enc_aes}')

#----------------------------------------

dec_aes = decrypt_aes_key(enc_aes,priv)

print(f'decrypted aes key: {dec_aes}')
print(f'the decrypted is equal to the original aes key: {aes_key==dec_aes}')

dec_msg = decrypt(dec_aes,tag,nonce,enc_msg)

print(f'decrypted msg: {dec_msg}')



