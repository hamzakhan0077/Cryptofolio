from hashlib import sha256


def encode():
    val = input("Please enter CODE to generate the secret key: ")
    return sha256(val.encode()).hexdigest()


if __name__ == '__main__':
    print(encode())
