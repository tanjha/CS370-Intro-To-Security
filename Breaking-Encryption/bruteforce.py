import cryp
from tqdm import tqdm
from alive_progress import alive_bar
import string
import multiprocessing

PRINTABLE = set(bytes(string.printable, "ascii"))
L = tqdm.get_lock()
pbar = tqdm()

num_workers = 10


def main():
    manager = multiprocessing.Manager()
    queue = manager.Queue()

    with open("nonce", "rb") as n:
        nonce = n.read()
    with open("ciphertext", "rb") as ct:
        ciphertext = ct.read()
    # bruteforce(nonce, ciphertext)

    # MULTIPROCESS
    total = 26**6
    args = [
        (
            i * total // num_workers,
            (i + 1) * total // num_workers,
            nonce,
            ciphertext,
            queue,
        )
        for i in range(num_workers)
    ]

    with alive_bar() as bar:
        with multiprocessing.Pool(processes=num_workers) as pool:
            results = [pool.apply_async(worker, arg) for arg in args]

            while any(not r.ready() for r in results):
                while not queue.empty():
                    n = queue.get_nowait()
                    bar(n)

            for r in results:
                try:
                    r.get()
                except Exception as e:
                    print(f"[ERROR] Worker failed: {e}")

            while not queue.empty():
                bar(queue.get_nowait())

    print("[END]")


def worker(start, end, nonce, ciphertext, queue):
    batch = 10_000
    count = 0

    for n in range(start, end):
        key = int_to_key(n)

        decrypted = cryp.decrypt(nonce, ciphertext, key)

        if is_valid(decrypted) and check_common(decrypted):
            print(f"[INFO] FOUND KEY - {key}")
            print(f"[INFO] DEC PLAINTEXT - {decrypted}")
            return

        count += 1
        if count % batch == 0:
            queue.put(batch)
    return


def int_to_key(n):
    n, a = divmod(n, 26)
    n, b = divmod(n, 26)
    n, c = divmod(n, 26)
    n, d = divmod(n, 26)
    n, e = divmod(n, 26)
    return bytes([a + 65, b + 65, c + 65, d + 65, e + 65, n % 26 + 65]) * 4


def is_valid(txt):
    try:
        txt.decode("utf-8")
    except UnicodeDecodeError:
        return False
    printable = sum(b in PRINTABLE for b in txt)
    return printable / len(txt) > 0.95


def check_common(txt):
    common = [b"the", b"and", b"that", b"with", b"have", b"this", b"from"]
    num_words = sum(word in txt.lower() for word in common)
    return num_words >= 2


if __name__ == "__main__":
    main()
