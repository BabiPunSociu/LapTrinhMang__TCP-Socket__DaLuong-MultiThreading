
import socket

diachi = ('localhost', 9050)

def send_data(sk, data):
    data1 = data + '\0'
    sk.sendall(data1.encode('utf-8'))

def recv_data(sk):
    data = bytearray()
    msg = ''
    while not msg:
        data1 = sk.recv(1024)
        if not data1:
            raise ConnectionError()
        data = data + data1
        if b'\0' in data1:
            data = data.rstrip(b'\0')
            msg = data.decode('utf-8')
    return msg

if __name__=='__main__':
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect(diachi)
    while True:
        # Gui 1
        data = input('Client:')
        send_data(sk, data)
        if data == 'bye':
            sk.close()
            break
        # Nhan 2
        data = recv_data(sk)
        print('Server:{}'.format(data))