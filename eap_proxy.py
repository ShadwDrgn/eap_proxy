import socket
from threading import Thread
import signal
import ctypes
import fcntl
import sys

class Sniffer():

    class ifreq(ctypes.Structure):
        _fields_ = [("ifr_ifrn", ctypes.c_char * 16),
                    ("ifr_flags", ctypes.c_short)]


    def __init__(self, iface_ont, iface_int):
        self.s_ont=socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x888e))
        self.s_ont.bind((iface_ont,0))
        self.s_int=socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x888e))
        self.s_int.bind((iface_int,0))
        self.sniff = True
        self.promisc(True)

    def proxy(self, s_sock, d_sock):
        print('Sniffing on: ' + s_sock.getsockname()[0])
        while(self.sniff):
            pkt = s_sock.recv(2048)
            d_sock.send(pkt)
            print('Sent ' + str(len(pkt)) + ' bytes')

    def promisc(self, tog):
        IFF_PROMISC = 0x100
        SIOCGIFFLAGS = 0x8913
        SIOCSIFFLAGS = 0x8914

        # ONT Promisc
        ifr = self.ifreq()
        ifr.ifr_ifrn = self.s_ont.getsockname()[0]
        fcntl.ioctl(self.s_ont.fileno(), SIOCGIFFLAGS, ifr)
        if tog:
            ifr.ifr_flags |= IFF_PROMISC
        else:
            ifr.ifr_flags &= ~IFF_PROMISC
        fcntl.ioctl(self.s_ont.fileno(), SIOCSIFFLAGS, ifr)

        # INT Pro
        ifr.ifr_ifrn = self.s_int.getsockname()[0]
        fcntl.ioctl(self.s_int.fileno(), SIOCGIFFLAGS, ifr)
        if tog:
            ifr.ifr_flags |= IFF_PROMISC
        else:
            ifr.ifr_flags &= ~IFF_PROMISC
        fcntl.ioctl(self.s_int.fileno(), SIOCSIFFLAGS, ifr)


def signal_handler(signal, frame):
    print 'Caught signal, exiting...'
    snf.sniff = False
    for thread in threads:
        if thread.isAlive():
            try:
                thread._Thread__stop()
            except:
                print(str(thread.getName()) + ' could not be terminated')
    snf.promisc(False)
    sys.exit(0)


if __name__ == "__main__":
    threads = []
    snf = Sniffer(sys.argv[1], sys.argv[2])

    threads.append(Thread(target=snf.proxy, args=[ snf.s_ont, snf.s_int ]))
    threads.append(Thread(target=snf.proxy, args=[ snf.s_int, snf.s_ont ]))

    for t in threads: t.start()
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()