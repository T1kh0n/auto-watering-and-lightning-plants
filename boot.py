import machine
import network
import time


# подключение кнопки
button = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)

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

		while not wlan.isconnected():
			pass

	print('Network config: ', wlan.ifconfig())


if __name__ == '__main__':
	try:
		connect()
	except:
		while True:
			if butt0n.value() == 0:
				break
			relay_1.value(1)
			time.sleep(3)
			relay_1.value(0)
			time.sleep(6)
