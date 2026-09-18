# Vending Machine (Revised Version) 解説

## 問題概要
前回の自動販売機のバグ修正版。`f`（flag）は選べないが、別のバグを突いて取り出す。

## 前回からの変更点

### 1. `pop(-1)` の穴を修正
```python
loc = self.stock.find(mark)
if loc < 0:
    print("The product is sold out.")
    return
```
`find` が `-1` を返しても弾かれるようになった（前回の攻略法は封じられた）。

### 2. 選択チェックの書き換え（新しい狙い目）
```python
# 変更前
# if mark not in ['a', 'b', 'c', 'd', 'e']:
# 変更後
if 'abcde'.find(mark) < 0:
    print("Invalid choice.")
    return
```
ここに新たな穴がある。

## 脆弱性: 空文字列と find
- `find('')` は「空文字列は位置0にある」とみなし、常に **`0`** を返す。
- そのため空入力 `''` はチェックを通過する（`0 < 0` は偽）。
- `loc = self.stock.find('')` も `0` を返す。
- `pop(0)` で**先頭**の要素が消える。

## 攻略手順
1. 空入力（Enterのみ）は毎回「先頭」を削る動き。
2. 在庫は `aaa...bbb...ccc...ddd...eee...f` の順で、`f` は末尾。
3. 先頭から200個（a30+b60+c20+d50+e40）消すと在庫は `'f'` だけ。
4. 201回目の空入力で先頭 = `f` が取れてフラグ表示。

## 攻略コード

```python
import pwn

HOST, PORT = "34.170.146.252", 40913
p = pwn.remote(HOST, PORT)

for _ in range(201):
    p.sendlineafter(b'choice> ', b'')

print(p.recvall(timeout=3).decode())
```

## コード解説
-pwnとは
    CTF（Capture The Flag）やバイナリの脆弱性分析（Pwn）で使われるPythonライブラリです。Pwntoolsの主な機能プロセスやネットワークの操作: ローカルのバイナリ実行や、リモートサーバーへの接続（TCP/Netcat）を簡単に自動化できます。データの送受信: recvuntil() や sendline() を使って、対話的な入力や出力の取得がスムーズに行えます。便利なユーティリティ: エクスプロイト（攻撃コード）に必要なバイト列への変換（p32, p64, u32, u64）や、アセンブル・逆アセンブルをサポートします。

- `import pwn`: 通信を自動化するライブラリ pwntools。
- `pwn.remote(HOST, PORT)`: サーバに接続。`p` が送受信の窓口（`nc` をコードで行うイメージ）。
- `for _ in range(201)`: 201回くり返す。`_` は「使わない変数」の慣習名。
- `sendlineafter(b'choice> ', b'')`: `choice> ` が出るまで待ち、空を送る。`sendline` は末尾に改行を付けるのでEnterと同じ。
- `recvall(timeout=3)`: 接続が閉じるまで残りを全部受信（3秒待つ）。
- `.decode()`: バイト列を読める文字列に変換。

## 用語補足
- **文字列 (str)**: 人間が読む文字。`'abc'`。
- **バイト列 (bytes)**: 通信でやり取りする生データ。`b'abc'`。通信はバイト列が標準。
- **b'' を付ける理由**: pwntools の送受信はバイト列で行うため。付けないと `BytesWarning` が出る。
- **decode()**: バイト列 → 文字列に戻す。受信データを読みやすくする。
- **find**: 位置を返す。見つからなければ `-1`。空文字列 `''` を渡すと常に `0`。
- **pop(0)**: リストの先頭を取り出して削除。

## まとめ
前回は `find` の `-1` を `pop(-1)` に渡すバグ。今回は修正で残った `find('') == 0` を突き、空入力で先頭を削り続けて `f` を先頭に持ってくる攻撃。
