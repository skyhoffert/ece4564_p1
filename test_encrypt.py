
import hashlib
from cryptography.fernet import Fernet

key = Fernet.generate_key()

print('key: ', key)

f = Fernet(key)

# encrypt
text = b'hello, world'
print('text to be sent: ', text)
token = f.encrypt(text)

print('token: ', token)

# hash
hasher = hashlib.md5()
hasher.update(token)
checksum = hasher.hexdigest()

print('checksum: ', checksum)

# channel
val = (key, token, checksum)

print('Val to be sent over channel: ', val)

# decrypt
dec = f.decrypt(token)

print('decrypted: ', dec)
