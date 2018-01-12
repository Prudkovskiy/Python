import json
import socket
import threading
import logging

import queue

HOST = "127.0.0.1"
PORT = 9999
send_queues = {}
lock = threading.Lock()

logger = logging.getLogger("chat-server")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("server_activity.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

def handle_client_recv(sock, addr):
    """
    Получаем сообщения от клиента и транслируем их на
    других клиентов, пока клиент не отключится
    """
    while True:
        data = sock.recv(4096)
        print("Got data from", sock.getpeername(), data.decode())
        logger.info('message from {}: {}'.format(sock.getpeername(), data.decode('UTF-8')))
        if not data:
            handle_disconnect(sock)
            break

        broadcast(data, addr, sock.fileno())


def handle_client_send(sock, q):
    """
    Мониторим очередь на наличие новых сообщений и отсылаем их другим клиентам,
    как только новое сообщение от данного клиента приходит
    """
    while True:
        data = q.get()
        if data is None:
            break
        try:
            res = json.dumps(data)
            sock.send(res.encode())
        except (IOError, ):
            handle_disconnect(sock)
            break


def broadcast(data, addr, info):
    """
    Добавляем сообщение в очередь отправки каждого подключенного клиента
    """
    print("Broadcast:", data.decode())
    st = json.loads(data.decode())
    with lock:
        for q in send_queues.keys():
            if q != info:
                send_queues[q].put([addr].extend(st))


def handle_disconnect(sock):
    """
    Убеждаемся в том, что очередь очищена
    и сокет закрыт когда клиент отсоединяется
    """
    fd = sock.fileno()
    with lock:
        # Получаем очередь отправки для данного клиента
        q = send_queues.get(fd, None)

    # Если мы найдем очередь, то это разъединение еще не обработано
    if q:
        q.put(None)
        del send_queues[fd]
        addr = sock.getpeername()
        res = json.dumps([addr, 'disconnected'])
        sock.send(res.encode())
        print('Client {} disconnected'.format(addr))
        logger.info('Client {} disconnected'.format(addr))
        sock.close()


def main():
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind((HOST, PORT))
    listen_sock.listen(5)

    while True:
        client_sock, addr = listen_sock.accept()
        q = queue.Queue()

        with lock:
            send_queues[client_sock.fileno()] = q
            res = json.dumps([addr, 'connected'])
            client_sock.send(res.encode())
        threading.Thread(
            target=handle_client_recv,
            args=[client_sock, addr], daemon=True
        ).start()
        threading.Thread(
            target=handle_client_send,
            args=[client_sock, q], daemon=True
        ).start()
        print('Connection from {}'.format(addr))


if __name__ == '__main__':
    main()