# server.py

import socket                   # Import socket module

port = 50000                    # Reserve a port for your service.
s = socket.socket()             # Create a socket object
host = '128.237.251.59'     # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print 'Server listening....'

while True:
    conn, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    data = conn.recv(1024)
    print('Server received', repr(data))
    for i in xrange(1):
        filename='home/pi/YungSpaceRanger/hardware/packet.tar'.format(i)
        f = open(filename,'rb')
        l = f.read(1024)
        while (l):
            conn.send(l)
            print('Sent ',repr(l))
            l = f.read(1024)
        f.close()

    print('Done sending')
    conn.send('Thank you for connecting')
    conn.close()

