import urequests
import network
import machine
import random
import time
import utime
import connect as c

class cloudData:
    c = c.connect()
    def __init__(self):
        self.list=[]
        self.pinMotor = machine.Pin(5, machine.Pin.OUT)

    def setListLabelX(self, lista):
        self.list = lista
    
    def getListLabelX(self):
        return self.list
    
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

    def loadData(self):
        for k in range(5):
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

                xUnico = []
                for elemento in x:
                    xUnico.extend(elemento)
                
                self.setListLabelX(xUnico)
                file.close()
                
                with open("data.csv", "r+") as file:
                    for lineas in file:
                        columnas = lineas.strip().split(",")
                        if len(columnas) > 1:  
                            temperature = columnas[1]
                            y.append(temperature)
                                
                    y.pop(0)
                    
                    intList = [(float(elemento)) for elemento in y]
                    predict = sum(intList)/len(intList)
                    print("predict:", predict)
                    
                    hora = utime.localtime()
                    now = self.now(hora)
                    file.write("\n")
                    file.write(str(now))
                    file.write(",")
                    file.write(str(predict))
                    intList.append(predict)
                    xUnico.append(now)
                    self.setListLabelX(xUnico)

                    if(predict>=22.3):
                        ledPin = machine.Pin(2, machine.Pin.OUT)  
                        ledPin.on()
                        self.pinMotor.value(1)
                        utime.sleep(5)
                        

                file.close()

        return intList

