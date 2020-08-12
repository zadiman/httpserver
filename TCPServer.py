import socket
import threading
import sys
from os import cpu_count

class TCPserver:

    def __init__(self, port, handle_connection, daemon_threads=False):
        self.host = None
        self.port = port
        self.handle_connection = handle_connection
        self.daemon_threads = daemon_threads
        self.backlog_queue_size = 5
        self.socket = None
        self.semaphore = threading.BoundedSemaphore(value=cpu_count())


    def tcp_server(self):
        self.socket = self.__get_socket()
        
        while True:
            try:
                conn, client_addr = self.socket.accept()
                t = threading.Thread(target=self.__new_connection, args=(conn, client_addr))
                t.daemon = self.daemon_threads
                t.start()
            except KeyboardInterrupt:
                self.socket.close()
                sys.exit('\nServer shutdown')


    def __get_socket(self):
        addr_filter = (
                self.host,
                self.port,
                socket.AF_UNSPEC,
                socket.SOCK_STREAM,
                0,
                socket.AI_PASSIVE,
                )

        print('Starting server.')
        for result in socket.getaddrinfo(*addr_filter):
            addr_family, socktype, proto, _, sockaddr = result
            try:
                sock = socket.socket(addr_family, socktype, proto)
            except OSError:
                sock = None
                continue
            try:
                while True:
                    try:
                        sock.bind(sockaddr)
                        sock.listen(self.backlog_queue_size)
                        if bool(sock) == True:
                            print(f'Server started {sock.getsockname()}')
                            break
                    except:
                        continue
            except OSError as error:
                print(f'OSError {error}')
                sock.close()
                sock = None
                continue
        if sock == None:
            print('Could not open socket')
            sys.exit(1)
        return sock


    def __new_connection(self, conn, client_addr):
        self.semaphore.acquire()
        try:
            self.handle_connection(conn)
        finally:
            print('Release semaphore')
            self.semaphore.release()


    def server_close(self):
        self.socket.close()


def __ping_test(conn, client_addr):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        else:
            conn.sendall(data)

