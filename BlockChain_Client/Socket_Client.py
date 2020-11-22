import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


host = input(str("Sender : "))
port = 8080
s.connect((host, port))
print("Connected !!")

filename = input(str("Please Enter :"))
file = open(filename, 'wb')
file_data = s.recv(1024000)
file.write(file_data)
file.close()
print("File Has Moved")
