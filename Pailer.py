import random
import paillier.keygen as keygen
import paillier.crypto as crypto

# Alice生成自己的公私钥(足够长)
pk, sk = keygen.generate_keys()


# 比较Alice的财富a和Bob的财富b
def compare(a, b):
    # Bob生成两个随机数x和y
    x = random.getrandbits(100)
    y = random.getrandbits(128)

    # Alice公布自己公钥pk
    print("Alice: pk =", pk)

    # Alice计算a的密文并公布
    e_a = crypto.encrypt(pk, a)
    print("Alice: E(a) =", e_a)

    # Bob计算b*x+y的密文并公布
    n, _ = pk
    e_bxy = crypto.encrypt(pk, b * x + y)
    print("Bob: E(b*x+y) =", e_bxy)

    # Bob计算a*x+y的密文并公布
    e_axy = crypto.secure_addition(
        crypto.scalar_multiplication(e_a, x, n),
        crypto.encrypt(pk, y),
        n,
    )
    print("Bob: E(a*x+y) =", e_axy)

    # Alice根据密文反解出b*x+y
    bxy = crypto.decrypt(pk, sk, e_bxy)

    # Alice根据密文反解出a*x+y
    axy = crypto.decrypt(pk, sk, e_axy)

    # Alice公布最终的大小结果
    if axy > bxy:
        print("winner: Alice")
    elif bxy > axy:
        print("winner: Bob")
    else:
        print("tie")


if __name__ == '__main__':
    alice_a = 2578466
    bob_b = 2333333
    compare(alice_a, bob_b)