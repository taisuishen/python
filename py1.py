import os, hashlib

def get_all_files(file_dir):   
    for root, dirs, files in os.walk(file_dir):
        for fn in files:
            path = os.path.join(root, fn)
            yield path

def get_file_hash(fn):
    with open(fn, "rb") as f:
        s1 = hashlib.sha1()
        while True:
            datas = f.read(64*1024)
            if not datas:
                break
            s1.update(datas)
    return s1.hexdigest()
    

d = {}
for e in get_all_files("D:\github"):
    hash_ = get_file_hash(e)
    if hash_ in d:
        print(e)
    else:
        d[hash_] = e

