import hashlib


def xor(x, y):
    return bytes(x[i] ^ y[i] for i in range(min(len(x), len(y))))


def hmac_sha1(key_K, data):
    if len(key_K) > 64:
        raise ValueError('The key must be <= 64 bytes in length')
    padded_K = key_K + b'\x00' * (64 - len(key_K))
    ipad = b'\x36' * 64
    opad = b'\x5c' * 64
    h_inner = hashlib.sha1(xor(padded_K, ipad))
    h_inner.update(data)
    h_outer = hashlib.sha1(xor(padded_K, opad))
    h_outer.update(h_inner.digest())
    return h_outer.digest()


def main():
    k = b'\x0b' * 20
    data = b"Hi There"

    result = hmac_sha1(k, data)
    print(result.hex())


main()
