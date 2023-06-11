import urequests
import network
import machine
import random
import time
import utime
import socket

class cloudData:
    def __init__(self, n):
        self.listX=[]
        self.listY=[]
        self.ssid = ''
        self.password = ''

        self.sta_if = network.WLAN(network.STA_IF)
        self.sta_if.active(True)
        self.sta_if.connect(self.ssid, self.password)
        while not self.sta_if.isconnected():
            pass
        print('Conectado a la red Wi-Fi desde connect class')
        print('Dirección IP:', self.sta_if.ifconfig()[0])
        self.pinMotor = machine.Pin(23, machine.Pin.OUT)

    def setListLabelX(self, lista):
        self.listX = lista
    
    def getListLabelX(self):
        return self.listX
    
    def setListLabelY(self, lista):
        self.listY = lista
    
    def getListLabelY(self):
        return self.listY
    
    def now(self, e):
        i=0
        tiempo = ""
        for elemento in e:
            if(i>=3 and i<6):
                if(i==3):
                    tiempo += str(elemento)
                else:    
                    tiempo += ":"
                    tiempo += str(elemento)
            i = i+1
        return tiempo
    
    def webServer(self):
        listX = self.getListLabelX()
        listY = self.getListLabelY()
     
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('', 80)  
        server_socket.bind(server_address)

        server_socket.listen(1)
        print('Servidor web listo para recibir conexiones')

        while True:
            print('Esperando una nueva conexión...')
            client_socket, client_address = server_socket.accept()
            print('Conexión establecida desde:', client_address)

            request = client_socket.recv(4096).decode()
            print('Solicitud recibida:')
            print(request)

            response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n\n'
            response += '<head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous"><title>Time VS Temperature</title></head><body><h1 class="text-center mt-5 mb-5 text-primary">Time VS Temperature</h1><div class="container"><div class="card"><div class="card-body"><table class="table table-bordered"><thead><th scope="col">Time (HH:MM:SS)</th><th scope="col">Temperature (°C)</th><th scope="col">ON/OFF</th></thead><tbody>\n'
            i=1
            for elementoX, elementoY in zip(listX, listY):
                if (i % 4 == 0):
                    response += '<tr style="background-color:salmon">\n'
                    if (elementoY >= 22.3):
                        response += '<td>{}</td><td>{}</td>\n'.format(elementoX, elementoY)
                        response += '<td>ON</td>\n'
                    else:
                        response += '<td>{}</td><td>{}</td>\n'.format(elementoX, elementoY)
                        response += '<td>OFF</td>\n'
                else:
                    response += '<tr>\n'
                    response += '<td>{}</td><td>{}</td>\n'.format(elementoX, elementoY)
                response += '</tr>'
                i = i+1
                
            response += '</tbody></table></div></div></div></body>\n'
            client_socket.sendall(response.encode())
            client_socket.close()

    def loadData(self):
        for k in range(1):
            with open("data.csv", "r+") as file:
                x=[]
                y=[]
                file.write("time")
                file.write(",")
                file.write("temperatura")
                
                for i in range(0,3):
                    utime.sleep(2)
                    hora = utime.localtime()
                    now = self.now(hora)
                    temp = random.uniform(22,23)
                    print(temp)
            
                    url = "https://api.thingspeak.com/update?api_key=QF7FU9H41G6SWWX5&afield1={:.2s}&field2={:.2f}".format(now, temp)
                    response = urequests.get(url)
                    if response.status_code == 200:
                        print("Datos enviados correctamente a ThingSpeak.")
                    else:
                        print("Error al enviar los datos a ThingSpeak:", response.status_code)
                    print("temperatura", temp)
                        
                    try:
                        file.write("\n")
                        file.write(str(now))
                        file.write(",")
                        file.write(str(temp))
                        response.close()
                    except Exception as e:
                        raise
                file.close()
                
                file=open("data.csv", "r")
                for linea in file:
                    columnas = linea.strip().split(",")
                    time=[columnas[0]]
                    x.append(time)

                x.pop(0)

                listX = []
                for elemento in x:
                    listX.extend(elemento)
                
                self.setListLabelX(listX)
                file.close()
                
                with open("data.csv", "r+") as file:
                    for lineas in file:
                        columnas = lineas.strip().split(",")
                        if len(columnas) > 1:  
                            temperature = columnas[1]
                            y.append(temperature)
                                
                    y.pop(0)
                    
                    listY = [(float(elemento)) for elemento in y]
                    
                    predict = sum(listY)/len(listY)
                    print("predict:", predict)
                    
                    hora = utime.localtime()
                    now = self.now(hora)
                    file.write("\n")
                    file.write(str(now))
                    file.write(",")
                    file.write(str(predict))
                    listY.append(predict)
                    listX.append(now)
                    self.setListLabelX(listX)
                    self.setListLabelY(listY)
                    
                    if(predict>=22.3):
                        ledPin = machine.Pin(2, machine.Pin.OUT)  
                        ledPin.on()
                        self.pinMotor.value(1)
                        utime.sleep(5)
                        ledPin.off()
                        self.pinMotor.value(0)
                        
                file.close()
    
test = cloudData(5)
test.loadData()
test.webServer()
