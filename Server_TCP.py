import socket
import threading
from time import sleep

diachi = ('localhost', 9050)

def send_data(sk, data):
    data1 = data + '\0'
    sk.sendall(data1.encode('utf-8'))

def recv_data(client_sk):
    data = bytearray()
    msg = ''
    while not msg:
        data1 = client_sk.recv(1024)
        if not data1:
            raise ConnectionError()
        data = data + data1
        if b'\0' in data1:
            data = data.rstrip(b'\0')
            msg = data.decode('utf-8')
    return msg

def thread_client(client_sk, client_addr):
    while True:
        # Nhan 1:
        data = recv_data(client_sk)
        print('Client {}: {}'.format(client_addr, data))
        if data == 'bye':
            client_sk.close()
            break
        # Gui 2:
        data = input('Server send to client {}:'.format(client_addr)).strip()
        send_data(client_sk, data)

if __name__=='__main__':
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # cho phép sử dụng lại một địa chỉ đang được sử dụng trên cùng một máy tính
    sk.bind(diachi)
    sk.listen(10)
    print("Server san sang ...")
    
    while True:
        client_sk, client_addr = sk.accept()
        thread = threading.Thread(target=(thread_client), args=[client_sk, client_addr], daemon=1)
        thread.start()
    # Chuong trinh chay mai, khong bao gio stop
    while True:
        sleep(1)
