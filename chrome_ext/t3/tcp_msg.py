import socket
import json
import time
from typing import Dict, Any

class TCP_msg:
    """
    一个用于发送 JSON 数据的 TCP 客户端模块。

    这个类提供了一种简单的方式来连接到 TCP 服务器并发送 JSON 格式的消息。
    """
    def __init__(self, host:str ='127.0.0.1', port : int =18880):
        """
        使用服务器的主机和端口初始化 TCP_msg 客户端。

        参数:
            host (str): 服务器的 IP 地址。
            port (int): 服务器的端口号。
        """
        self.host = host
        self.port = port
        self.connection = None
        print(f"TCP_msg 客户端已初始化，目标为 {self.host}:{self.port}")

    def connect(self) -> bool:
        """
        建立与服务器的连接。

        返回:
            bool: 如果连接成功则返回 True，否则返回 False。
        """
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.host, self.port))
            #print("连接成功！")
            return True
        except ConnectionRefusedError:
            print(f"tcp_msg.py::连接失败：服务器 {self.host}:{self.port} 拒绝了连接。请确保服务器正在运行并监听该端口。")
            self.connection = None
            return False
        except socket.timeout:
            print("tcp_msg.py::连接超时。")
            self.connection = None
            return False
        except Exception as e:
            print(f"tcp_msg.py::连接时发生错误: {e}")
            self.connection = None
            return False

    def send(self, **kwargs: Any):
        """
        向已连接的服务器发送 JSON 数据。

        此方法会自动将传入的关键字参数打包成字典并发送。
        如果连接未激活，它会尝试重新连接。

        参数:
            **kwargs: 要发送的数据，以键值对形式传入。
        """
        message_data = kwargs
        if not self.connection:
            #print("没有活动的连接。正在尝试连接...")
            if not self.connect():
                print("tcp_msg.py::由于连接问题，发送数据失败。")
                return

        try:
            message_json = json.dumps(message_data)
            message_bytes = message_json.encode('utf-8')

            #print(f"发送数据: {message_json}")
            self.connection.sendall(message_bytes)
            #print("数据发送成功。")
            #time.sleep(0.1)

        except BrokenPipeError:
            print("tcp_msg.py::连接已断开。正在尝试重新连接并重新发送...")
            self.connection.close()
            self.connection = None
            self.send(**kwargs)  # 递归调用以重新发送
        except Exception as e:
            print(f"tcp_msg.py::发送数据时发生错误: {e}")
        self.close()

    def close(self):
        """
        关闭与服务器的连接。
        """
        if self.connection:
            self.connection.close()
            #print("连接已关闭。")
            self.connection = None

if __name__ == "__main__":
    # --- 示例用法 ---
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 18880

    # 1. 创建 TCP_msg 客户端实例。
    # 这时不会立即连接。
    client = TCP_msg(SERVER_IP, SERVER_PORT)
    
    # 2. 循环发送数据。
    # send() 方法会自动处理连接。
    for i in range(20):
        # 使用关键字参数传入数据，这比手动创建字典更方便。
        client.send(message1="Hello from Python!", message2=str(i), message3="Sending JSON data to C#.")
        time.sleep(0.5)
    
    # 3. 在所有发送完成后，显式关闭连接。
    client.close()


    #usage
    from tcp_msg import TCP_msg

    tcp_debugger = TCP_msg()
    DEBUG_tcp =True

    if DEBUG_tcp==True :tcp_debugger.send(message1="Hello from Python!", message2=str(14), message3="Sending JSON data to C#.")