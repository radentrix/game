print(' ' + '\033[35;1m' )

print(' SELAMAT DATANG DI SCRIPT RADEN TRIX ' )

print(' MOHON ISI USERNAME DAN PASWOORD ' )
     
user = raw_input(" Username: ")

import getpass

sandi = getpass.getpass()

if sandi == 'Trix' and user == 'Raden':

	print "Kamu Berhasil Login"
	
else:

	print "Username atau Password Salah !"

import os
import sys
import random
import socket
import select
import datetime
import threading

lock = threading.RLock(); os.system('cls' if os.name == 'nt' else 'clear')

def real_path(file_name):
    return os.path.dirname(os.path.abspath(__file__)) + file_name

def filter_array(array):
    for i in range(len(array)):
        array[i] = array[i].strip()
        if array[i].startswith('#'):
            array[i] = ''

    return [x for x in array if x]

def colors(value):
    patterns = {
        'R1' : '\033[31;1m', 'R2' : '\033[31;2m',
        'G1' : '\033[32;1m', 'Y1' : '\033[33;1m',
        'P1' : '\033[35;1m', 'CC' : '\033[0m'
    }

    for code in patterns:
        value = value.replace('[{}]'.format(code), patterns[code])

    return value

def log(value, status='BERBURU JANDA', color='[CC]'):
    value = colors('{color}''[CC]''[{time}] [CC]{color}{status} [CC]{color}{value}[CC]'.format(
        time=datetime.datetime.now().strftime('%H:%M:%S'),
        value=value,
        color=color,
        status=status
    ))
    with lock: print(value)

def log_replace(value, status='WARNING', color='[Y1]'):
    value = colors('{}{} ({})        [CC]\r'.format(color, status, value))
    with lock:
        sys.stdout.write(value)
        sys.stdout.flush()

class inject(object):
    def __init__(self, inject_host, inject_port):
        super(inject, self).__init__()

        self.inject_host = str(inject_host)
        self.inject_port = int(inject_port)

    def log(self, value, color='[G1]'):
        log(value, color=color)

    def start(self):
        try:
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_server.bind((self.inject_host, self.inject_port))
            socket_server.listen(1)
            frontend_domains = open(real_path('/config.ini')).readlines()
            frontend_domains = filter_array(frontend_domains)
            if len(frontend_domains) == 0:
                self.log('Frontend Domains not found. Please check config.ini', color='[Y1]')
                return
            self.log('SIAP!'.format(self.inject_host, self.inject_port))
            while True:
                socket_client, _ = socket_server.accept()
                socket_client.recv(65535)
                domain_fronting(socket_client, frontend_domains).start()
        except Exception as exception:
            self.log('error sialakan  close psiphon dan qpyton dan mulai ulang'.format(self.inject_host, self.inject_port), color='[R1]')

class domain_fronting(threading.Thread):
    def __init__(self, socket_client, frontend_domains):
        super(domain_fronting, self).__init__()

        self.frontend_domains = frontend_domains
        self.socket_tunnel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client = socket_client
        self.buffer_size = 65535
        self.daemon = True

    def log(self, value, status='[P1]CARI APA KAWAN', color='[CC]'):
        log(value, status=status, color=color)
        
    def handler(self, socket_tunnel, socket_client, buffer_size):
        sockets = [socket_tunnel, socket_client]
        timeout = 0
        while True:
            timeout += 1
            socket_io, _, errors = select.select(sockets, [], sockets, 3)
            if errors: break
            if socket_io:
                for sock in socket_io:
                    try:
                        data = sock.recv(buffer_size)
                        if not data: break
                        # SENT -> RECEIVED
                        elif sock is socket_client:
                            socket_tunnel.sendall(data)
                        elif sock is socket_tunnel:
                            socket_client.sendall(data)
                        timeout = 0
                    except: break
            if timeout == 30: break

    def run(self):
        try:
            self.proxy_host_port = random.choice(self.frontend_domains).split(':')
            self.proxy_host = self.proxy_host_port[0]
            self.proxy_port = self.proxy_host_port[1] if len(self.proxy_host_port) >= 2 and self.proxy_host_port[1] else '443'
            self.log('[R1]JANDA BOLONG LEPAS '.format(self.proxy_host, self.proxy_port))
            self.socket_tunnel.connect((str(self.proxy_host), int(self.proxy_port)))
            self.socket_client.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
            self.handler(self.socket_tunnel, self.socket_client, self.buffer_size)
            self.socket_client.close()
            self.socket_tunnel.close()
            self.log('[G1] JANDA MUDA DAPET''[CC]'.format(self.proxy_host, self.proxy_port), color='[CC]')
        except OSError:
            self.log('Connection Error', color='[CC]')
        except TimeoutError:
            self.log('{} Not Responding'.format(self.proxy_host), color='[R1]')

def main():
    print(colors('\n'.join([
     '[R1]                  TELKOMSEL GAMEMAX','[CC]'
     '[G1] ','[CC]'
     '[G1]               YOUTUBE : RADEN TRIX     ','[CC]'
     '[G1]                SUBSCRIBE YA KAWAN   ','[CC]'
     '[P1]       ','[CC]'
     '[Y1] JANDA LEBIH MENGGODA','[CC]'
     '[Y1] BOKEPER DOSA DI TANGGUNG SENDIRI ','[CC]'
     '[G1] ','[CC]'
     '[R1] HOST : 127.0.0.1 ','[CC]'
     '[R1] PORT : 8080 ','[CC]'
   
    ])))    
    inject('127.0.0.1', '8080 ').start()

if __name__ == '__main__':
    main()