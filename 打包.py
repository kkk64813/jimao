"""幾貓加密打包：輸入 SealNote 帳號密碼，把 几猫.html 加密成 g.bin。

密碼只在這個視窗裡出現，不會被寫進任何檔案，也不會上傳。
用法：雙擊 打包.bat，或 python 打包.py
"""
import os, sys, base64, getpass, secrets

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
except ImportError:
    print("缺少 cryptography，請先執行：pip install cryptography")
    input("按 Enter 結束...")
    sys.exit(1)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_CANDIDATES = [
    os.path.join(HERE, "几猫.html"),
    r"C:\Users\4607\Desktop\Jack\几猫.html",
]
ITER = 130000


def read_plain():
    for p in SRC_CANDIDATES:
        if os.path.exists(p):
            data = open(p, "rb").read()
            print("來源：%s  (%.0f KB)" % (p, len(data) / 1024))
            return data
    print("找不到 几猫.html。請把它放在本資料夾，或維持在桌面 Jack 目錄。")
    input("按 Enter 結束...")
    sys.exit(1)


def derive(password, salt):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER)
    return kdf.derive(password.encode("utf-8"))


def main():
    print("=" * 52)
    print(" 幾貓 · 加密打包")
    print("=" * 52)
    print("請輸入你的 SealNote 密碼（輸入時不會顯示）")
    pw1 = getpass.getpass(" 密碼：")
    pw2 = getpass.getpass(" 再輸入一次：")
    if pw1 != pw2:
        print("兩次不一致，取消。")
        input("按 Enter 結束...")
        return
    if len(pw1) < 6:
        print("太短了，至少 6 碼。")
        input("按 Enter 結束...")
        return

    plain = read_plain()
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derive(pw1, salt)
    ct = AESGCM(key).encrypt(nonce, plain, None)

    open(os.path.join(HERE, "g.bin"), "wb").write(ct)
    meta = base64.b64encode(salt).decode() + "\n" + base64.b64encode(nonce).decode() + "\n"
    open(os.path.join(HERE, "g.key"), "w", encoding="utf-8").write(meta)

    # 自檢
    assert AESGCM(derive(pw1, salt)).decrypt(nonce, ct, None) == plain
    print("\n完成：g.bin (%.0f KB)" % (len(ct) / 1024))
    print("自檢通過：用同一組密碼可正確解回原文。")
    print("\n接下來：把 index.html、g.bin、g.key 三個檔一起上傳。")
    input("按 Enter 結束...")


if __name__ == "__main__":
    main()
