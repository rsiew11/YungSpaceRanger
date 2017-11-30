# server.py

import socket                   # Import socket module
import time
import sys



port = 60002
s = socket.socket()             # Create a socket object
host = '128.237.244.81'     # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.


s.settimeout(35)   #set the timeout to be 30 seconds so that the script terminates
print 'Server listening....'



conn, addr = s.accept()     # Establish connection with client.
print 'Got connection from', addr

data = conn.recv(1024)


while True:
    try:

        print('Server received', repr(data))
        for i in xrange(1):
            filename='/home/pi/YungSpaceRanger/hardware/pac.zip'.format(i)
            f = open(filename,'rb')
            l = f.read(1024)
            while (l):
                conn.send(l)
                print('Sent ',repr(l))
                l = f.read(1024)
            f.close()

        print('Done sending waiting for next packet')
        #conn.send('Thank you for connecting')

        #sleep for 15 seconds to wait for next new packet
        time.sleep(15)

    except KeyboardInterrupt:
        print 'Ctrl-C caught.. closing conn'
        conn.close()
        sys.exit(0)
        print 'closed connection'


