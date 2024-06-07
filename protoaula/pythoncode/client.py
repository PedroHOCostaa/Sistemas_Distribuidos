
# python client
import socket
import addressbook_pb2

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 7000))

person = addressbook_pb2.Person()
person.id = 234
person.name = "Rodrigo Campiolo"
person.email = "rcampiolo@ibest.com.br"

msg = person.SerializeToString()
size = len(msg)

client_socket.send((str(size) + "\n").encode())
client_socket.send(msg)

client_socket.close()
