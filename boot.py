import machine
import network
import time

# подключение реле
# досветка
relay_1 = machine.Pin(26, machine.Pin.OUT)
relay_1.value(0)


def connect():
    wlan = network.WLAN(network.STA_IF)

    if not wlan.isconnected():
        print('Connecting to network...')

        wlan.active(True)
        wlan.connect('ASUS_30', 'giant_5447')

    print('Network config: ', wlan.ifconfig())
count = 0

try:
	connect()
except:
	print('Error')
	for i in range(10):
		relay_1.value(1)
		time.sleep(3)
		relay_1.value(0)
		time.sleep(3)
