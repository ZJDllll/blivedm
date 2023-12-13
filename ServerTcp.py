import socket
import threading

# socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# socket_server.bind(('127.0.0.1',12345))
# socket_server.listen(1)
# print("start listen")
# result = socket_server.accept()
# conn = result[0]
# print(f'client:{result[1]}')
# while True:
#     data = conn.recv(1024).decode("UTF-8")
#     print(f'get:---{data}')
#     conn.send(f'接收到你的消息-{data}'.encode("UTF-8"))
#     msg = input("输入：")
#     if msg=="exit":
#         conn.send(f'exit'.encode("UTF-8"))
#         break
# conn.close()
# socket_server.close()

class MyServer(object):
    def __init__(self):
        # 初始化socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置服务器IP地址
        host = '127.0.0.1'
        # 设置服务器端口号
        port = 12345
        # 绑定IP地址和端口
        self.server.bind((host, port))
        # 设置最大监听数
        self.server.listen(5)
        # 设置一个字典，用来保存每一个客户端的连接和身份信息
        self.socket_mapping = {}
        # 设置接收的最大字节数
        self.maxSize = 1024
        self.isrun=True
    def run(self):
        self.isrun=True
        # 创建线程，负责监听客户端连接
        threading.Thread(target=self.linten).start()
        # 创建线程，负责获取键盘输入并发送给客户端
        # threading.Thread(target=self.send_to_client).start()

    def linten(self):
        print('开始监听')
        while self.isrun:
            socket, addr = self.server.accept()
            # 发送信息，提示客户端已成功连接
            socket.send('success！'.encode('utf-8'))
            print(addr,'+conn')
            # 将客户端socket等信息存入字典
            self.socket_mapping[socket] = addr
            # 创建线程，负责获取键盘输入并发送给客户端
            # threading.Thread(target=self.send_to_client).start()
            # 创建线程，负责接收客户端信息并转发给其他客户端
            threading.Thread(target=self.recv_from_client, args=(socket,)).start()
        print('tui-listen')
    def terminate(self):
        self.isrun = False
        self.server.close()
        print('tui')
    def send_to_client(self):
        """
        获取键盘输入并发送给客户端
        :param socket:
        :return:
        """
        while self.isrun:
            info = input("输入发送:")
            if info == "quit":
                self.terminate()
                print('quit??')
            for socket in self.socket_mapping.keys():
                socket.send(info.encode("utf-8"))
    
    #向所有客户端发送相同信息
    def send_to_all_client(self, msg):
        """
        向所有客户端发送相同信息
        """
        for socket in self.socket_mapping.keys():
            socket.send(msg.encode("utf-8"))

    def recv_from_client(self, socket:socket):
        """
        接收客户端信息并转发给其他客户端
        :param socket:
        :return:
        """
        while self.isrun:
            recv_info = socket.recv(self.maxSize).decode('utf-8')
            if not recv_info:
                print(f'close:{self.socket_mapping[socket]}')
                del self.socket_mapping[socket]
                socket.close()
                break
            print('client{} say: '.format(self.socket_mapping[socket]), recv_info)
            # for i_socket in self.socket_mapping.keys():
            #     if i_socket != socket:
            #         i_socket.send(recv_info.encode("utf-8"))
#my_server = MyServer()
#my_server.run()