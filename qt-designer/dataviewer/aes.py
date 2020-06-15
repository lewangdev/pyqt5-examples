import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

bs = AES.block_size

def encrypt(raw, key):
    key256 = _sha256(key)
    raw_paded = _pad(raw)
    iv = Random.new().read(bs)
    cipher = AES.new(key256, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw_paded.encode()))

def decrypt(enc, key):
    data = base64.b64decode(enc)
    iv = data[:bs]
    key256 = _sha256(key)
    cipher = AES.new(key256, AES.MODE_CBC, iv)
    return _unpad(cipher.decrypt(data[bs:])).decode('utf-8')

def _sha256(s):
    return hashlib.sha256(s.encode()).digest()

def _pad(s):
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

def _unpad(s):
    return s[:-ord(s[len(s)-1:])]

if __name__ == '__main__':
    raw = '{"data":null}'
    print(raw)
    key = "0oGMm1"
    enc = encrypt(raw, key)
    print(enc)
    raw_back = decrypt(enc, key)
    print(raw_back)

    enc = 'bGJtT1M0ZzFHbDhjYkQ5Uqyi0dcdVE3eAfNwpCJXHZ9LyRovcehEllrg/BM0OH4cklbp5yyPh8d/N7XU/2LebO/LoT47SJMFqNTWMLzJzNKgOrWz3X0TMuGKlNwzhENluiKxYx3B5rtYjPJVCfpFlF5vV/ldoUEKfFNYJ6x9jjI='
    key = 'nc97WJ'
    raw_back = decrypt(enc, key)
    print(raw_back)


