import hashlib
import random
import string

def make_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(5)])

def makePasswordHash(password, salt=None):
    if not salt:
        salt = make_salt()
    hash_pass = hashlib.sha256(str.encode(password + salt)).hexdigest()
    return '{0},{1}'.format(hash_pass, salt)

def checkPasswordHash(password, hash):
    salt = hash.split(',')[1]
    if makePasswordHash(password, salt) == hash:
        return True
    return False