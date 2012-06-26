import os

class RPCFunctions:
    def __init__(self, ircbot, channel):
        self.ircbot = ircbot
        self.channel = channel

    def notice(self, string):
        self.ircbot.notice(self.channel, string)
        return "OK"

def rpcgw(ircbot, host, port, channel):
    import SimpleXMLRPCServer
    server = SimpleXMLRPCServer.SimpleXMLRPCServer((host, port))

    functions = RPCFunctions(ircbot, channel)
    server.register_instance(functions)

    server.serve_forever()
