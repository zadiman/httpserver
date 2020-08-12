from TCPServer import TCPserver
from HTTPhandler import HTTPhandler

class HTTPServer(TCPserver):
    def __init__(self, port):
        TCPserver.__init__(self, port, self.handle_tcp_connection, daemon_threads=True)

    def handle_tcp_connection(self, conn):
        http_connection = HTTPhandler(conn)
        try:
            http_connection.req_from_sock(conn)
        except:
            pass

server = HTTPServer(10000)
server.tcp_server()
