import hashlib


async def hash_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

if __name__ == "__main__":
    raise "Please, start main.py"