import sys
from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site
from twisted.internet import reactor

log.startLogging(sys.stdout)
root = File(".")
site = Site(root)
reactor.listenTCP(8877, site)
reactor.run()
