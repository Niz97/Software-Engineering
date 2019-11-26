'''
@Description: A simple web server for the Spotify authentication
@Version: 1.1.0.20191118
@Author: William Staff (driver) and Jichen Zhao (observer)
@Date: 2019-11-18 02:48:06
@Last Editors: Jichen Zhao
@LastEditTime: 2019-11-20 15:27:22
'''

from bottle import WSGIRefServer, run
from threading import Thread
import time

class WebServer(WSGIRefServer):
    def run(self, app):
        from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
        from wsgiref.simple_server import make_server
        import socket

        class FixedHandler(WSGIRequestHandler):
            def address_string(self):
                return self.client_address[0]

        handler_cls = self.options.get('handler_class', FixedHandler)
        server_cls  = self.options.get('server_class', WSGIServer)

        if ':' in self.host: # for IPv6 addresses
            if getattr(server_cls, 'address_family') == socket.AF_INET:
                class server_cls(server_cls):
                    address_family = socket.AF_INET6

        srv = make_server(self.host, self.port, app, server_cls, handler_cls)
        self.srv = srv
        srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown() # shut down the server programmatically