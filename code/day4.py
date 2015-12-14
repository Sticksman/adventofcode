import hashlib


def find_hash_key(num=5):
    key = 'ckczppom'
    counter = 1
    while True:
        md5 = hashlib.md5()
        md5.update('%s%s' % (key, counter))
        digest = md5.hexdigest()
        if digest[:num] == '0' * num:
            break
        counter += 1

    return counter

if __name__ == '__main__':
    print find_hash_key(num=6)
