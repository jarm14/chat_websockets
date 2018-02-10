
import sys
from pprint import pprint
from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource


class ProtocoloServidor(WebSocketServerProtocol):
    def onConnect(self, client):
        print("Peticion de conexion desde {}".format(client.peer))

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, message, isBinary):
        print("Mensaje recibido: {}".format(message))
        # self.sendMessage("Mensaje recibido: {}".format(message))
        self.factory.broadcast(message)

    def onClose(self, wasClean, code, reason):
        self.factory.unregister(self)


class TodosContraTodosFactoria(WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super(TodosContraTodosFactoria, self).__init__(*args, **kwargs)
        self.clients = []

    def register(self, client):
        if client not in self.clients:
            print("Cliente registrado: {}".format(client.peer))
            self.clients.append(client)
            pprint(self.clients)

    def unregister(self, client):
        if client in self.clients:
            print("Sesion finalizada: {}".format(client.peer))
            self.clients.remove(client)

    def broadcast(self, message):
        print("Broadcasting mensajes '{}' ..".format(message))
        for client in self.clients:
            client.sendMessage(message.encode('utf8'))
            print("Mensaje enviado a: {}".format(client.peer))


if __name__ == "__main__":
    log.startLogging(sys.stdout)

    root = File(".")

    factory = TodosContraTodosFactoria(u"ws://127.0.0.1:8877")
    factory.protocol = ProtocoloServidor
    resource = WebSocketResource(factory)

    root.putChild(u"ws", resource)

    site = Site(root)
    reactor.listenTCP(8877, site)
    reactor.run()
