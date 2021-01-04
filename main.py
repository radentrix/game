#qpy:console
import sys
import time
import random
import threading
import ServerInfo
import ServerConfig
import ServerPinger
import ServerHandler
ru = lambda text: text.decode('utf-8', 'ignore')

class Server:

    def __init__(self):
        self.long = 18
        self.sets = ServerConfig.Sets()
        self.name = ServerInfo.Info('name').get_info()
        self.ver = ServerInfo.Info('ver').get_info()
        self.form = ServerInfo.Info('about').get_info()
        self.auth = ServerInfo.Info('by').get_info()
        self.mail = ServerInfo.Info('mail').get_info()
        self.noyes = [ru('No'), ru('Yes')]
        self.version = [ru('Default'), ru('HTTP/1.0'), ru('HTTP/1.1')]
        self.method = [ru('HEAD'),
         ru('GET'),
         ru('POST'),
         ru('DELETE'),
         ru('CONNECT'),
         ru('OPTIONS'),
         ru('TRACE'),
         ru('PUT')]
        self.line = [ru('\\r\\n'), ru('\\n')]
        self.split = [ru('Default'),
         ru('%s' % (self.line[self.sets.ILINE] * self.sets.ILINE)),
         ru('%s' % (self.line[self.sets.ILINE] * self.sets.ILINE)),
         ru('%s' % (self.line[self.sets.ILINE] * self.sets.ILINE)),
         ru('%s' % (self.line[self.sets.ILINE] * self.sets.ILINE)),
         ru('%s' % (self.line[self.sets.ILINE] * self.sets.ILINE))]

    def subs(self, data = '', cut = False):
        if data:
            data = data
        else:
            data = 'None'
        if cut:
            if len(data) > 5:
                data = '%s...' % data[:5]
        return data

    def about(self, title = ''):
        self.info = []
        self.info.append('[ %s ]%s\n' % (title, '' * (self.long - len(title) - 5)))
        self.info.append('Name : %s\n' % self.name)
        self.info.append('Version : %s\n' % self.ver)
        self.info.append('Dev : %s\n' % self.auth)
        self.info.append('Email : %s\n' % self.mail)
        self.info.append('\n\n')
        return ru(''.join(self.info))

    def config(self, title = ''):
        self.info = []
        self.info.append('[ inject ready ]\n\n')
        return ru(''.join(self.info))

    def log(self, title = ''):
        self.info = []
        self.info.append('=[ %s ]=\n' % (title))
        self.info.append('\n\n')
        return ru(''.join(self.info))

    def log(self, title = ''):
        self.info = []
        self.info.append('    [ %s %s]\n' % (title, '' * (self.long - len(title) - 5)))
        self.info.append('\n')
        return ru(''.join(self.info))

    def show(self):
        sys.stderr.write(self.about('Information'))
        sys.stderr.write(self.config('Configuration'))
        time.sleep(2)

    def run(self):
        ServerHandler.LogWindow(True)
        ServerHandler.HTTPProxyService().serve_forever()

    def log(self, text):
        sys.stderr.write(text)
              
    def pinger(self):
        while 1:
            time.sleep(random.randint(30, 300))
            ServerPinger.Pinger().check()


if __name__ == '__main__':
    Server().show()
    services = [threading.Thread(target=Server().run, args=()), threading.Thread(target=Server().pinger, args=())]
    for serving in services:
        serving.start()