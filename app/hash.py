import hashlib


async def hash_data(data):
    hash_object = hashlib.sha256()
    hash_object.update(data.encode())
    return hash_object.hexdigest()
