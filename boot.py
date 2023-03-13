import machine
import network


def connect():
	wlan = network.WLAN(network.STA_IF)

	if not wlan.isconnected():
		print('Connecting to network...')

		wlan.active(True)
		wlan.connect('ESP32', 'm2io9a1g?')

		while not wlan.isconnected():
			pass

	print('Network config: ', wlan.ifconfig())

	
if __name__ == '__main__':
	try:
		connect()
	except:
		machine.reset()
