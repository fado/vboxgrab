from SimpleXMLRPCServer import SimpleXMLRPCServer

server = SimpleXMLRPCServer(('', 9000), logRequests=True, allow_none=True)
server.register_introspection_functions()
server.register_multicall_functions()

class GrabberService:
    
    def get_url(self):
        with open('# DECRYPT MY FILES #.txt', 'r') as inF:
            for line in inF:
                if 'onion' in line:
                    return line

server.register_instance(GrabberService())

try:
    print "Use Control-C to exit."
    server.serve_forever()
except KeyboardInterrupt:
    print "Exiting."

