

import sys
from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource


class ProtocoloServidor(WebSocketServerProtocol):
    def onConnect(self, request):
        print("Peticion de conexion desde {}".format(request))

    def onMessage(self, playload, isBinary):
        self.sendMessage("Mensaje recibido")


if __name__ == "__main__":
    log.startLogging(sys.stdout) 
    
    # Archivos estaticos
    root = File(".")

    factory = WebSocketServerFactory(u"ws://127.0.0.1:8877")
    factory.protocol = ProtocoloServidor
    resource = WebSocketResource(factory)

    root.putChild(u"ws", resource)

    site = Site(root)
    reactor.listenTCP(8877, site)
    reactor.run()
