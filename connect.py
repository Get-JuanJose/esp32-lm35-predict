import network

class connect:
    def __init__(self):
        self.ssid = 'CLARO_WIFI710'
        self.password = 'CLAROI710'

        self.sta_if = network.WLAN(network.STA_IF)
        self.sta_if.active(True)
        self.sta_if.connect(self.ssid, self.password)
        while not self.sta_if.isconnected():
            pass

        print('Conectado a la red Wi-Fi desde connect class')
        print('Dirección IP:', self.sta_if.ifconfig()[0])

    def getIp(self):
        return self.sta_if.ifconfig()[0]

a = connect()
print(a.getIp())