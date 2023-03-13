# модуль для парсинга с веб-страницы
import urequests
# модуль управления платой
import esp


# отключение режима отладки
esp.osdebug(None)


# вывод времени рассвета и заката
def suntime_scraping():
	# парсинг веб-страницы
	response = urequests.get('http://timezone.ru/suncalc.php?tid=22')
	# перевод результата парсинга в текст
	response_text = response.text
	# восход
	sunrise = 0
	# закат
	sunset = 0

	expected_table_section = '<table class="table table-hover"'
	expected_tbody_section = '<tbody>'
	expected_tr_section = '</tr>'

	# нахождение времени восхода и заката
	for i1 in range(len(response_text)):
		table_section = response_text[i1:i1 + 32]

		if table_section == expected_table_section:
			for i2 in range(len(response_text)):
				current_i = i1 + i2
				tbody_section = response_text[current_i:current_i + 7]

				if tbody_section == expected_tbody_section:
					for i3 in range(len(response_text)):
						current_i = i1 + i2 + i3
						tr_section = response_text[current_i:current_i + 5]

						if tr_section == expected_tr_section:
							time_count = 0
							for i4 in range(len(response_text)):
								current_i = i1 + i2 + i3 + i4
								time_section = response_text[current_i:current_i + 17]

								# восход
								if time_count == 0:
									if (time_section[6] == ':') and (time_section[9] == ':'):
										sunrise = int(time_section[4:6])

										time_count += 1
										continue

								# закат
								if time_count == 1:
									if (time_section[6] == ':') and (time_section[9] == ':'):
										sunset = int(time_section[4:6]) + 1

										break

							break

					break

			break

	# удаление лишних переменных
	del (
		response,
		response_text,
		expected_table_section,
		expected_tbody_section,
		expected_tr_section,
		i1,
		table_section,
		i2,
		current_i,
		i3,
		tr_section,
		time_count,
		i4,
		time_section
	)

	# возврат часов восхода и захода 
	return [sunrise, sunset]


# вывод погоды и УФ индекса
def weather_and_uv_index_scraping():
	# парсинг веб-страницы
	response = urequests.get('https://a-weather.ru/district/d-4913/')
	# перевод результата парсинга в текст
	response_text = response.text
	# погода
	weather = ''
	# УФ индекс
	uv_index = 0
	# счетчик
	weather_count = 0

	for i in range(len(response_text)):
		# нахождение погоды
		expected_weather_section = '<div class="text">'
		weather_section = response_text[i:i + 18]

		# нахождение УФ индекса
		expected_uv_index_section = 'УФ индекс - '
		uv_index_section = response_text[i:i + 12]

		if weather_section == expected_weather_section:
			while True:
				if response_text[i + 18 + weather_count] == '<':
					break
				else:
					weather += response_text[i + 18 + weather_count]

				weather_count += 1

		if uv_index_section == expected_uv_index_section:
			uv_index = int(response_text[i + 18])
			break

	# удаление лишних переменных
	del (
		response,
		response_text,
		weather_count,
		i,
		expected_weather_section,
		weather_section,
		expected_uv_index_section,
		uv_index_section
	)

	# возврат погоды и УФ индекса
	return [weather, uv_index]
