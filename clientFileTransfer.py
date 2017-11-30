import socket                   # Import socket module

s = socket.socket()             # Create a socket object
host = '128.237.244.81'     # Get local machine name
port = 60001                    # Reserve a port for your service.

s.connect((host, port))
s.send("Hello server!")

with open('pac.zip', 'wb') as f:
    print 'file opened'
    while True:
        print('receiving data...')
        data = s.recv(1024)
        print('data=%s', (data))
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully got the file')
s.close()
print('connection closed')
