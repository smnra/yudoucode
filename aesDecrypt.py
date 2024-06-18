import os
import base64
from hashlib import md5
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from urllib.parse import unquote



def decodeUrl(str):
    # print(unquote(str))
    return unquote(str)





def pad(s):
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16).encode()

def unpad(s):
    return s[0:-ord(s[len(s)-1:])]

def bytes_to_key(data, salt, output=48):
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]

def encrypt(data, passphrase):
    salt = os.urandom(8)
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(pad(data)) + encryptor.finalize()
    cipherbyte = base64.b64encode(b"Salted__" + salt + encrypted)
    return cipherbyte

def decrypt(data, passphrase):
    data = base64.b64decode(data)
    assert data[:8] == b'Salted__'
    salt = data[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    plainbyte = unpad(decryptor.update(data[16:]) + decryptor.finalize())
    return plainbyte

if __name__ == '__main__':
    data = b'123456'
    passphrase = b'6677'
    encrypt_data = b'U2FsdGVkX1+vre5IwFcApDUvQbej0739jskLwjVrd9anP/6Ds83UQZXaHddo9WgPPFAqN6JK+UFjvrMBxp/SBPy3qz6cuf2rF1ME4+Ok3k4cURzkVxsweoyDyLYMI8rXtbnw7ecbaqL6eMBb89jjvp3lCuPNSzxR+D17ywKW6k2TdtpMHahjP3wOkz2o6l/JWKOlsrqOV69hABsrllvg7EUYU6HP1Z/kj8oVM2EhF3gp1tQ4VAn339hkA2OSV8eIiJDXa353RaMoSL5JA+h1p98MctxzjVs3JI/QVUm4ENmFt9IVkpQsQgYPzvYzd/7aKU6opp3Flny1AOhhxePBmQlO0Sxk+evy48G0DB4RmsivEa+3L6WBituLFBSsimKJYESuX+7xYyCs3lQHmIs/n4gwg4CmEwirI3dglok+2vZvkxsDmXkey1xIjEIsw6PR5agUOc5PdSWqvkGSMQS0kJgSydOFLc34H8lp3B0XNR3iTOBy0zWQPe33kASA6l9adPkiAxYdv3VIPYmHXeDbYfREiCWF/QjV6Jy51TUQaA0J8KxIvVwTookcjMmozHGKC+QHZ7uCoBFbh0pfbRWcKOXTY4KcOU+PDglAcQr7a0PKFMyqZN2tHSLPD11sLjdLUjAHbWXnDxizex+SlNnHK4w/FNCDI8JIA/3mv3KpvjRfN5VTXuWUcAdgU5V1qXiN2NKKwTXS6wj7DY9Xe9RluJjGo6+DET3PeDVdTBC+Tg4HSCSv/MM+9RL4KOLeMlfUsrj/ML08L1bb28o0fM0Y2rcxMSanQ9xwJChucauOpPWeRFqAv+fCl/UDQVDiwBqU60kXH3flSOGqoMHgQ/2SQZ5ZHUw3sIzjkFd1JlF7MIoSRog0n7BakhR3aR+VNWddX5H8l0LqiHbGaLZ+dtkrMqNc3RagibAK2DQ+36W3n0TT6uddDNBruORh0q/kLcmU0YpMc1JAPD6dEd2rWDjxw9OXgEm4ELojmof7HCHupNLmOiK63zAdiPi09WTVF09vJRMvrS0h4/5YcGY7CKf79Xe6KqjlCHW/DZ48+5tkTucR93iV9dQVO61BKmuPTNMqaVRYDEWgHrsYcxtZe3apl4YnxIHp6NLcCl+c3ONaAIaMWur92kkGcDga0ElQW0nz0MzqP67Axh3rl2n9FCSkAr+WIlcM0L0llbed0c6JDkB1X+oKzfPLBCd5lmYFSLyuivSPJL7tTeLXxkA1dR3swNLRUlDnGZd4M6HtC50fksW264bnBqTUXO5MTARYQe2xMnrhyLkuUQAiRnquPfKZblx3iQP7rKwCZETA7+AGcyr9WlOa0TRgmB6VdJx+2Oe59m4yaPEnbhYvdDxEdzgxVeAk9aFff2qKBQY57lVVlpAneDDzXTQdK5C/S/e/nzjsYCOvBk17lQiRV4lPLEDCMNsPUnkU0jvQC99zr4MaqwH0/M9bmG6XFVFGcP/olQtrhCDwvVqoDeyoSZ7SXRMSx0kt4fCjU/8Q+iBsZmgazm4sBlQFTPeYFivtSIEwpaD4wq9EGSQz/232EusJ3bJTzNWQ+wYvF+M+msPVgGa0HeyoYCSoLobohxoVxZaYYbPYLzZvjURd9B1jkST0NVXS4Ob6mRW50PfZaLW6ELo7CRByRqTxDrJW0L0YAAKCtf8Vpi+7UXrSHq+C4zLye5DueXCGT44nZRihHf7TVQ0Ug5rIw+OL76NdY9o5GkT1cTSue2zxIN1iGt7YudpufYQYbw=='
    # encrypt_data = encrypt(data, passphrase)
    # print('encrypt_data:', encrypt_data)


    decrypt_data = decrypt(encrypt_data, passphrase)
    decrypt_data = decodeUrl(decrypt_data)
    print('decrypt_data:', decrypt_data)