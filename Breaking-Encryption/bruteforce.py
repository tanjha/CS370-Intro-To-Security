import cryp
from alive_progress import alive_bar
import string 

PRINTABLE = set(bytes(string.printable, "ascii"))

def main():
    with open("nonce", "rb") as n:
        nonce = n.read()
    with open("ciphertext", "rb") as ct:
        ciphertext = ct.read()
    bruteforce(nonce, ciphertext)
    print("[END]")



def bruteforce(nonce, ciphertext):
    with alive_bar(None) as bar:
        key_nums = [0] * 6
        while key_nums[5] < 26:
            key = ""
            for i in range(6):
                key += string.ascii_uppercase[key_nums[i]]
            key = key + key + key + key
            key = bytes(key, 'utf-8')

            decrypted = cryp.decrypt(nonce, ciphertext, key)
            if is_valid(decrypted) and check_common(decrypted):
                print(f"[INFO] FOUND KEY - {key}")
                print(f"[INFO] DEC PLAINTEXT - {decrypted}")
                break


            bar()
            key_nums[0] += 1
            for i in range(6):
                if key_nums[i] == 26:
                    if i < 5:
                        key_nums[i] = 0
                        key_nums[i+1] += 1
                    else:
                        print(f"[INFO] REACHED FINAL KEY VALUE")

def is_valid(txt):
    try:
        txt.decode("utf-8")
    except UnicodeDecodeError:
        return False
    printable = sum(b in PRINTABLE for b in txt)
    return printable / len(txt) > 0.95

def check_common(txt):
    common = [
        b"the", b"and", b"that", b"with",
        b"have", b"this", b"from"
    ]
    num_words = sum(word in txt.lower() for word in common)
    return num_words >= 2

if __name__ == "__main__":
    main()