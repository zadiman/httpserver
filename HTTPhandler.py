import socket

class HTTPhandler:

    END_HTTP_REQ = '\r\n\r\n'
    buffer = 4096
    recv_timeout = 3

    def __init__(self, conn):
        self.conn = conn
        # self.client_addr = client_addr
        self.in_data = ''


    def req_from_sock(self, conn):
        try:
            conn.settimeout(self.recv_timeout)
            while True:
                if self.END_HTTP_REQ in self.in_data:
                    print(self.in_data)
                    end_of_request_index = self.in_data.index(self.END_HTTP_REQ)
                    request_string = self.in_data[:end_of_request_index]
                    self.in_data = self.in_data[end_of_request_index + len(self.END_HTTP_REQ):]
                    return self.__verify_http_req(request_string)

                data = conn.recv(self.buffer).decode('utf-8')
                if not data:
                    break
                self.in_data += data
        except socket.timeout:
            print('Timeout on socket')
        return None


    def __verify_http_req(self, req):
        request_line = req.partition('\r\n')[0]
        request_line_comp = request_line.split(' ')
        method, path, http_version = request_line_comp
        if len(request_line_comp) != 3:
            self.__send_response(400, '400: Headline must have 3 parts')
        elif method != 'GET':
            self.__send_response(400, '400: This server only supports GET method.')
        elif http_version != 'HTTP/1.1':
            self.__send_response(400, '400: Only HTTP/1.1 is supported.')
        else:
            print(HTTPresponse.doc_root(path))
            self.__send_response(200, HTTPresponse.doc_root(path))


    def __send_response(self, code, body):
        response = HTTPresponse(code, body)
        if 'html' in response.body:
            doctype = 'html'
        else:
            doctype = 'plain'
        self.conn.sendall(bytes(response.formatted_response(doctype), 'utf-8'))
        self.conn.sendall(bytes(response.body, 'utf-8'))
        self.conn.close()


    def close(self):
        self.conn.close()

class HTTPresponse:

    CRLF = '\r\n'
    CODE_DESCRIPTION = {
        200: 'OK',
        400: 'Bad Request',
        404: 'Not Found'
        }

    def __init__(self, code, body, path=None, header=None):
        self.code = code
        self.body = body
        self.path = path
        self.header = header


    def formatted_response(self, type):
        response_lines = [f'HTTP/1.1 {self.code} {self.CODE_DESCRIPTION[self.code]}']
        response_lines.append('Server: Xad-server')
        if self.code == 400:
            response_lines.append(f'Connection: close')
        response_lines.append('Content-Type: text/{}; charset=utf-8'.format(type))
        response_lines.append('Content-Length: ' + str(len(self.body)))
        return self.CRLF.join(response_lines) + (self.CRLF * 2)


    @staticmethod
    def doc_root(path):
        if path is not None and '/':
            index = open('./docroot/index.html')
            return index.read()
