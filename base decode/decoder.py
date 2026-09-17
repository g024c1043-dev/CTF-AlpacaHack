from base64 import b16decode, b32decode, b64decode

def solve(s, depth=0):
    b = s.encode() if isinstance(s, str) else s
    # もし20層はがしたかつ最初がAlpacaの文字列であれば解読成功になる
    if depth == 20:
        try:
            t = b.decode()
            if t.startswith("Alpaca{"):
                return t
        except UnicodeDecodeError:
            pass
        return None          # 20層剥がして違えば打ち切り
    # base64,32,16それぞれを使ってエンコードされた文字列をデコードする
    for dec in (b64decode, b32decode, b16decode):
        try:
            # もしbase64,32,16のいずれかでデコードを試みて失敗した場合、次の行で例外が発生しexceptへ
            r = solve(dec(b), depth=depth + 1)   # ← depth を正しく積む
            # 再帰で呼んだ引数の中身がゴミだった場合再帰で呼んださきのforのreturnではすべてexceptになりreturnがNoneになる、すなわちexceptになり処理が飛ばされる
            if r:
                return r
        except Exception:
            pass
    return None

with open('output.txt') as f:
    encode = f.read().strip()
print(solve(encode))