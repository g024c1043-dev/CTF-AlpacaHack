import pwn

HOST, PORT = "34.170.146.252", 40913
p = pwn.remote(HOST, PORT) 

for _ in range(201):
    p.sendlineafter(b'choice> ', b'')

d = p.recvuntil(b'choice> ')
print(d.decode())