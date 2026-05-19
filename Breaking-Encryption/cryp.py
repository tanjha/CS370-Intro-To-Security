from Crypto.Cipher import AES
import random
import string

def main():
    plaintext = "go beavs".encode('utf-8')
    print(f"[INFO] PLAINTEXT: {plaintext}")
    
    key_string = ''.join(random.choices(string.ascii_uppercase, k=6))
    key_string = key_string + key_string + key_string + key_string
    key_bytes = bytes(key_string, 'utf-8')
    key = key_bytes
    print(f"[INFO] KEY: {key}")
    nonce, ciphertext = encrypt(plaintext, key)
    print(f"[INFO] CIPHERTEXT: {ciphertext}")
    decrypted_plaintext = decrypt(nonce, ciphertext, key)
    print(f"[INFO] DECRYPTED PLAINTEXT: {decrypted_plaintext}")
    print("[END]")

def encrypt(plaintext, key):
    cipher_enc = AES.new(key, AES.MODE_EAX)
    nonce = cipher_enc.nonce
    ciphertext, _ = cipher_enc.encrypt_and_digest(plaintext)
    return nonce, ciphertext 


def decrypt(nonce, ciphertext, key):
    cipher_dec = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher_dec.decrypt(ciphertext)
    return plaintext

if __name__ == "__main__":
    main()