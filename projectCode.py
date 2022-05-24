from _thread import start_new_thread
from email.utils import formatdate # referenced from https://stackoverflow.com/questions/225086/rfc-1123-date-representation-in-python
from datetime import datetime
import time
import os.path
import threading
import socket

# Handle the HTTP request.
def recieveRequest(client_connection):
    prevData = ""
    while True:
        # Get the client request
        request = client_connection.recv(1024).decode()
        if (request == ""):
            print("closed connection")
            break
        else:
            # client port
            strConnection = str(client_connection)
            strConnection = strConnection.split(" ")
            port = strConnection[-1]
            port = port[:-2]

            print("Request with client port " + port + " passed to child " + str(threading.get_ident()) + ":")
            print(request)

        # Parse HTTP headers
        # windows with \r\n
        if "\r\n" in request:
            headers = request.split('\r\n')
        # linux with \n
        else:
            headers = request.split('\n')
        fields = headers[0].split()
        #print("resqiset is" +str(headers))
        methodType = fields[0]
        file = fields[1]
        response = ["0", "0"]

        clientIp = socket.gethostbyname(socket.gethostname())

        # append record to log file
        logFile = open("log file.txt", "a")
        accessTime = datetime.now()
        formatTime = time.mktime(accessTime.timetuple())
        logFile.write(clientIp + " " + formatdate(timeval=formatTime, localtime=False, usegmt=True) + " " + " " + file[
                                                                                                                  1:] + " ")  # with reference from https://stackoverflow.com/questions/225086/rfc-1123-date-representation-in-python

        # execute request
        if methodType == 'GET':
            try:
                filename = file[1:]
                fileExtension = filename.split(".", 1)
                fin = open(filename)
                fin.close()

                # requests text file
                if (fileExtension[1] == "html") or (fileExtension[1] == "txt"):
                    fin = open(filename)
                    data = fin.read()
                    data = data.encode()

                # requests image file
                elif (fileExtension[1] == "png"):
                    fin = open(filename, 'rb')
                    data = fin.read()

                # head cmd
                response[0] = "HTTP/1.1 200 OK\r\n".encode()
                # date
                accessTime = datetime.now()
                formatTime = time.mktime(accessTime.timetuple())
                response[0] += ("Date: " + formatdate(timeval=formatTime, localtime=False,
                                                      usegmt=True) + " GMT\r\n").encode()
                # print("time is "+ formatdate(timeval=formatTime, localtime=False, usegmt=True))

                # last-modified
                modifiedTime = os.path.getmtime(filename)
                # print("modified time is  :" + str(modifiedTime))
                # print("modified ftime is :" + formatdate(timeval=modifiedTime, localtime=False, usegmt=True))
                response[0] += ("Last-Modified: " + formatdate(timeval=modifiedTime, localtime=False, usegmt=True) +
                                "\r\n").encode()
                # keep-alive field (bonus)
                length = len(data)
                response[0] += ("Content-length: " + str(length) + "\r\n").encode()
                #print(str(length))
                keepAlive = "Keep-Alive: timeout=5, max=30\r\n"
                response[0] += keepAlive.encode()
                connection = "Connection: keep-alive\r\n\r\n"
                response[0] += connection.encode()

                response[0] += data
                response[1] = data
                fin.close()

                # 304 data cached
                if (response[1] == prevData):
                    response[0] = 'HTTP/1.1 304 not modified\n\n'.encode()
                    logFile.write("304 NOT MODIFIED")
                else:
                    logFile.write("200 OK")

            # 404 file not found
            except FileNotFoundError:
                response[0] = 'HTTP/1.1 404 Not Found\n\nFile Not Found'.encode()
                logFile.write("404 NOT FOUND")
        else:
            # 400 invalid http method like POST
            response[0] = 'HTTP/1.1 400 Bad Request\n\nRequest Not Supported'.encode()
            logFile.write("400 BAD REQUEST")

        logFile.write("\n")
        logFile.close()

        # Send HTTP response
        encodedResponse = response[0]
        # if cache needs update
        if (response[1] != 0):
            prevData = response[1]

        client_connection.sendall(encodedResponse)


# Define socket host and port
SERVER_HOST = 'localhost'
SERVER_PORT = 80

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind server
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print('Listening on port %s ...' % SERVER_PORT)
prevData = "".encode()

while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    #
    # # Get the client request
    # request = client_connection.recv(1024).decode()
    # print('request:')
    # print(request)

    # # Send HTTP response
    # response = recieveRequest(request, prevData)
    # encodedResponse = response[0]
    # # if cache needs update
    # if (response[1] != 0):
    #     prevData = response[1]
    #
    # client_connection.sendall(encodedResponse)

    start_new_thread(recieveRequest,(client_connection,))
    print("child has started to take request")

# Close connection
client_connection.close()
newThread.join()

# Close socket
server_socket.close()