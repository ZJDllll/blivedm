import socket

socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket_server.bind(('127.0.0.1',12345))
socket_server.listen(1)
print("start listen")
result = socket_server.accept()
conn = result[0]
print(f'client:{result[1]}')
while True:
    data = conn.recv(1024).decode("UTF-8")
    print(f'get:---{data}')
    conn.send(f'接收到你的消息-{data}'.encode("UTF-8"))
    msg = input("输入：")
    if msg=="exit":
        conn.send(f'exit'.encode("UTF-8"))
        break
conn.close()
socket_server.close()