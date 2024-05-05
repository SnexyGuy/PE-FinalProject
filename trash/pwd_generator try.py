import secrets
import string
alphabet =string.hexdigits
password = ''.join(secrets.choice(alphabet) for i in range(10))  # for a 20-character password
print(password)

a=secrets.compare_digest(password,password)
print(a)
txt=secrets.token_hex(32)
print(txt)