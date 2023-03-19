from parser import suntime_scraping
from parser import weather_and_uv_index_scraping

import machine
import ntptime
import time


# подключение датчика
pot_soil_moisture = machine.ADC(machine.Pin(34))
pot_soil_moisture.atten(machine.ADC.ATTN_11DB) 

# подключение реле
# досветка
relay_1 = machine.Pin(26, machine.Pin.OUT)
relay_1.value(0)
# полив
relay_2 = machine.Pin(25, machine.Pin.OUT)
relay_2.value(0)

# подключение кнопки
button = machine.Pin(13, machine.Pin.IN)

# список хорошей погоды
good_weather = [
	'Облачно',
	'Солнечно',
	'Преимущественно облачно',
	'В основном облачно',
	'Переменная облачность',
	'Ясно',
	'Солнечно',
	'Небольшая морось'
]

# список плохой погоды
bad_weather = [
    'Мгла',
    'Снег',
    'Кратковременный снег',
    'Кратковременный дождь',
    'Дождь',
    'Небольшой кратковременный дождь',
    'Местами туман',
    'Туман',
    'Гром',
    'Кратковременный снег',
    'Небольшой кратковременный снег',
    'Небольшой снег',
    'Небольшой дождь/Гроза'
]

# счетчик хорошей погоды
good_weather_count = 0
# счетчик плохой погоды
bad_weather_count = 0

# погода
weather = 0

# УФ индекс
uv_index = 0
# средний УФ индекс
uv_average = 0

# время досветки
time_lightning = 0

# время восход
sunrise = 0
# время захода
sunset = 0
# дневные часы
daylight_hours = 0


# часовой пояс
ntptime.host = '2.europe.pool.ntp.org'

try:
	ntptime.settime()
except:
	print('Error syncing time')


# текущее время
current_hours = time.localtime()[3] + 2
current_minutes = time.localtime()[4]


while True:
	# отключение системы
	if button.value is True:
		break
	# чтение данных с датчика влажности
	pot_soil_moisture_value = (pot_soil_moisture.read() - 1100) / 100

	# контроль влажности
	while pot_soil_moisture_value > 60:
		# включение полива
		relay_2.value(1)

	# выключение полива
	relay_2.value(0)

	# log
	print(current_hours, current_minutes, sep=':')
	time.sleep(10)

	if current_hours == 0:
		sunrise, sunset = suntime_scraping()

		daylight_hours = sunset - sunrise

		# log
		print(sunset, sunrise, daylight_hours)

	if (current_hours >= sunrise) and (current_hours <= sunset):
		weather_and_uv_index = weather_and_uv_index_scraping()
		weather = weather_and_uv_index[0]
		uv_index += weather_and_uv_index[1]

		if weather in good_weather:
			good_weather_count += 1

		if weather in bad_weather:
			bad_weather_count += 1

		# log
		print(weather)

	if current_hours == sunset:
		if uv_index != 0:
			uv_average = uv_index / daylight_hours
		else:
			uv_average = 0

		if good_weather_count >= bad_weather_count:
			time_lightning += 1
		if bad_weather_count > good_weather_count:
			time_lightning += 2

		if uv_average < 3:
			time_lightning += 2
		if (uv_average >= 3) and (uv_average < 6):
			time_lightning += 0.5
		if (uv_average >= 3) and (uv_average < 6):
			time_lightning == 0

		if isinstance(time_lightning, float):
			conditional_1 = current_hours == time_lightning - 0.5 + sunset
			conditional_2 = current_minutes != 30

			while conditional_1 and conditional_2:
				# включение досветки
				relay_1.value(1)

				# log
				print(True)
				time.sleep(10)

			# выключение досветки
			relay_1.value(0)

		if isinstance(time_lightning, int):
			while current_hours == time_lightning + sunset:
				# включение досветки
				relay_1.value(1)

				# log
				print(time_lightning)
				time.sleep(10)

			# выключение досветки
			relay_1.value(0)
