import telebot
from telebot import types
from urllib.parse import urlencode

bot = telebot.TeleBot('6416356071:AAHZpm96EgbrbyjnDm1DmTnbvZIDKHI-7VU')

@bot.message_handler(commands=['start'])
def start(message):
	if (message.from_user.username == "Victor_Pestov" or message.from_user.username == "yaroslavesolovievs"):
		pass
	else:
		return
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	button = types.KeyboardButton("Создать ссылку")
	button1 = types.KeyboardButton("Изменить политику конфиденциальности")
	button2 = types.KeyboardButton("Изменить оферту")
	markup.add(button)
	markup.add(button1)
	markup.add(button2)
	bot.send_message(message.from_user.id, 'Посылочка USA - управление', reply_markup=markup)


service = {}
price = {}
f = {}
flag_policy = False
flag_ofera = False


@bot.message_handler(content_types=['document'])
def save_doc(message):
	global flag_policy
	global flag_ofera
	if (message.from_user.username == "Victor_Pestov" or message.from_user.username == "yaroslavesolovievs"):
		pass
	else:
		return
	if flag_policy:
		file_info = bot.get_file(message.document.file_id)
		downloaded_file = bot.download_file(file_info.file_path)
		with open('/Parcel_Usa/public/privacy_policy.docx', 'wb') as new_file:
			new_file.write(downloaded_file)
		flag_policy = False
		bot.send_message(message.from_user.id, 'Политика конфиденциальности успешно загружена')
	elif flag_ofera:
		file_info = bot.get_file(message.document.file_id)
		downloaded_file = bot.download_file(file_info.file_path)
		with open('/Parcel_Usa/public/offer.docx', 'wb') as new_file:
			new_file.write(downloaded_file)
		flag_ofera = False
		bot.send_message(message.from_user.id, 'Оферта успешно загружена')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	global flag_policy
	global flag_ofera
	if (message.from_user.username == "Victor_Pestov" or message.from_user.username == "yaroslavesolovievs"):
		pass
	else:
		return
	if message.text == 'Создать ссылку':
		f[message.from_user.id] = 'Создать ссылку'
		bot.send_message(message.from_user.id, 'Укажите услугу')
	elif message.text == 'Изменить политику конфиденциальности':
		bot.send_message(message.from_user.id, 'Приложите файл')
		flag_policy = True
	elif message.text == 'Изменить оферту':
		bot.send_message(message.from_user.id, 'Приложите файл')
		flag_ofera = True
	elif (message.from_user.id not in service) and (message.from_user.id not in price) and (f[message.from_user.id] == 'Создать ссылку') and (message.text != 'Услуга указана неверно') and (message.text != 'Услуга указана верно'):
		service[message.from_user.id] = message.text
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		button1 = types.KeyboardButton("Услуга указана верно")
		button2 = types.KeyboardButton("Услуга указана неверно")
		markup.add(button1)
		markup.add(button2)
		bot.send_message(message.from_user.id, f'Проверьте, правильно ли указана услуга: {service[message.from_user.id]}', reply_markup=markup)
	elif (message.from_user.id in service) and (message.from_user.id not in price) and (message.text == 'Услуга указана верно') and (f[message.from_user.id] == 'Создать ссылку'):
		bot.send_message(message.from_user.id, 'Укажите цену')
	elif (message.from_user.id in service) and (message.from_user.id not in price) and (message.text == 'Услуга указана неверно') and (f[message.from_user.id] == 'Создать ссылку'):
		bot.send_message(message.from_user.id, 'Укажите услугу')
		del service[message.from_user.id]
	elif (message.from_user.id in service) and (message.from_user.id not in price) and (f[message.from_user.id] == 'Создать ссылку'):
		price[message.from_user.id] = message.text
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		button1 = types.KeyboardButton("Правильно")
		button2 = types.KeyboardButton("Не правильно")
		markup.add(button1)
		markup.add(button2)
		bot.send_message(message.from_user.id, f'Проверьте, правильно ли указана цена: {price[message.from_user.id]}', reply_markup=markup)
	elif (message.from_user.id in service) and (message.from_user.id in price) and (message.text == 'Не правильно') and (f[message.from_user.id] == 'Создать ссылку'):
		bot.send_message(message.from_user.id, 'Укажите цену')
		del price[message.from_user.id]
	elif (message.from_user.id in service) and (message.from_user.id in price) and (message.text == 'Правильно') and (f[message.from_user.id] == 'Создать ссылку'):
		params = {'price': price[message.from_user.id], 'service': service[message.from_user.id]}
		queryString = urlencode(params)
		url = f'http://parcel-usa.ru/pay?{queryString}'
		bot.send_message(message.from_user.id, f'[Ссылка на сайт: ]{url}', parse_mode='Markdown')
		del f[message.from_user.id]
		del service[message.from_user.id]
		del price[message.from_user.id]
		f[message.from_user.id] = ''
		bot.send_message(message.from_user.id, 'Заказ создан')
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		button = types.KeyboardButton("Создать ссылку")
		button1 = types.KeyboardButton("Изменить политику конфиденциальности")
		button2 = types.KeyboardButton("Изменить оферту")
		markup.add(button)
		markup.add(button1)
		markup.add(button2)
		bot.send_message(message.from_user.id, 'Посылочка USA - управление', reply_markup=markup)

bot.polling(none_stop=True, interval=0)