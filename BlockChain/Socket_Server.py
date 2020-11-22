import socket

s = socket.socket()

host = socket.gethostname()
port = 8080
s.bind((host, port))
s.listen(1)
print("Waiting....")
conn, adr = s.accept()
print(adr, " Has Connected !! ")

filename = input(str("Please Enter File Name : "))
file = open(filename, 'rb')
file_data = file.read()
conn.send(file_data)
print("Data Has Transmitted")
