import socket
import connect as c
import cloudData as cd

cd = cd.cloudData()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('', 80)  
server_socket.bind(server_address)

server_socket.listen(1)
print('Servidor web listo para recibir conexiones')

listY = cd.loadData()
listX = cd.getListLabelX()
print("y:", listY)
print("x:", cd.getListLabelX())

while True:
    print('Esperando una nueva conexión...')
    client_socket, client_address = server_socket.accept()
    print('Conexión establecida desde:', client_address)

    request = client_socket.recv(4096).decode()
    print('Solicitud recibida:')
    print(request)

    response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n\n'
    response += '<head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous"><title>Time VS Temperature</title></head><body><h1 class="text-center mt-5 mb-5 text-primary">Time VS Temperature</h1><div class="container"><div class="card"><div class="card-body"><table class="table table-bordered"><thead><th scope="col">Time</th><th scope="col">Temperature</th></thead><tbody>\n'
    i=1
    for elementoX, elementoY in zip(listX, listY):
        if (i % 4 == 0 and elementoY >= 22.3):
            response += '<tr style="background-color:salmon">\n'
            response += '<td>{}</td><td>{} ON</td>\n'.format(elementoX, elementoY)
        else:
            response += '<tr>\n'
            response += '<td>{}</td><td>{}</td>\n'.format(elementoX, elementoY)
        response += '</tr>'
        i = i+1
        
    response += '</tbody></table></div></div></div></body>\n'
    client_socket.sendall(response.encode())
    client_socket.close()

