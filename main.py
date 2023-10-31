import telebot
from telebot import types
from urllib.parse import urlencode
import os
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', \
       'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)

sheetName = '1ZB-NZBQLMI1bPiwYpUMffJN4s1cwiBgSaZ_TFKiUeBQ'


bot = telebot.TeleBot('6416356071:AAHZpm96EgbrbyjnDm1DmTnbvZIDKHI-7VU')
sheet = client.open_by_key(sheetName)

def add_order_to_google_table(category, features, images):
	try:
		worksheet = sheet.worksheet(base64.b64decode(category.decode('utf-8')).decode('utf-8'))
	except:
		worksheet = sheet.add_worksheet(title=base64.b64decode(category.decode('utf-8')).decode('utf-8'), rows=100, cols=20)
	len_col = len(worksheet.col_values(1))
	if (len_col < 1):
		i = 0
		for key, value in features.items():
			worksheet.update(f'{chr(65+i)}1', base64.b64decode(key.decode('utf-8')).decode('utf-8'))
			i += 1
	keys_list = worksheet.row_values(1)
	for key, value in features.items():
		for i in range(len(keys_list)):
			if (base64.b64decode(key.decode('utf-8')).decode('utf-8') == keys_list[i]):
				worksheet.update(f'{chr(65+i)}{len_col+1}', base64.b64decode(value.decode('utf-8')).decode('utf-8'))
	for i in range(len(images)):
		urli = f'=IMAGE("{images[i]}")'
		print(urli)
		worksheet.update(f'{chr(65+i+len(keys_list))}{len_col+1}', urli, value_input_option='USER_ENTERED')

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
	button3 = types.KeyboardButton("Добавить товар в каталог")
	markup.add(button)
	markup.add(button1)
	markup.add(button2)
	markup.add(button3)
	bot.send_message(message.from_user.id, 'Посылочка USA - управление', reply_markup=markup)

if not os.path.exists('../Parcel_Usa/public/goods'):
	os.mkdir('../Parcel_Usa/public/goods')
	os.mkdir('../Parcel_Usa/public/goods/pictures')

service = {}
price = {}
f = {}
flag_policy = False
flag_ofera = False

product_class = ''
product_name = ''
product_info = ''
product_feature = {}
product_feauture_boolean = False
feauture = ''
product_pictures = []
product_price = 0


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
		with open('../Parcel_Usa/public/privacy_policy.docx', 'wb') as new_file:
			new_file.write(downloaded_file[1::])
		flag_policy = False
		bot.send_message(message.from_user.id, 'Политика конфиденциальности успешно загружена')
	elif flag_ofera:
		file_info = bot.get_file(message.document.file_id)
		downloaded_file = bot.download_file(file_info.file_path)
		with open('../Parcel_Usa/public/offer.docx', 'wb') as new_file:
			new_file.write(downloaded_file[1::])
		flag_ofera = False
		bot.send_message(message.from_user.id, 'Оферта успешно загружена')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	global product_name
	global flag_policy
	global flag_ofera
	global product_class
	global product_name
	global product_info
	global feauture
	global product_feauture_boolean
	global product_feature
	global product_pictures
	global product_price
	if (message.from_user.username == "Victor_Pestov" or message.from_user.username == "yaroslavesolovievs"):
		pass
	else:
		return

	if message.text == 'Добавить товар в каталог':
		f[message.from_user.id] = 'Добавить товар в каталог'
		bot.send_message(message.from_user.id, 'Укажите класс товара (Кроссовки, одежда, очки)')
	elif (f[message.from_user.id] == 'Добавить товар в каталог') and (product_class == ''):
		product_class = base64.b64encode(message.text.encode('utf-8'))
		bot.send_message(message.from_user.id, 'Укажите название товара')
	elif (f[message.from_user.id] == 'Добавить товар в каталог') and (product_name == ''):
		product_name = base64.b64encode(message.text.encode('utf-8'))
		bot.send_message(message.from_user.id, 'Укажите описание товара')
	elif f[message.from_user.id] == 'Добавить товар в каталог' and product_info == '':
		product_info = base64.b64encode(message.text.encode('utf-8'))
		bot.send_message(message.from_user.id, 'Укажите цену товара')
	elif f[message.from_user.id] == 'Добавить товар в каталог' and product_price == 0:
		product_price = base64.b64encode(message.text.encode('utf-8'))
		bot.send_message(message.from_user.id, 'Готово! Теперь приступим к указанию характеристик товара.')
		bot.send_message(message.from_user.id, 'Укажи характеристику товара. Например: размер . Когда все характеристики товара будут указаны - нажмите готово')
	elif message.text == 'Все фотографии добавлены':
		i = 0
		while True:
			if not os.path.isfile(f'../Parcel_Usa/public/goods/{i}.order'):
				break
			else:
				i += 1
		with open(f'../Parcel_Usa/public/goods/{i}.order', 'w') as order_file:
			order_file.write(str(product_class)[1::])
			order_file.write('\n')
			order_file.write(str(product_name)[1::])
			order_file.write('\n')
			order_file.write(str(product_info)[1::])
			order_file.write('\n')
			order_file.write(str(product_price)[1::])
			order_file.write('\n')
			for key, value in product_feature.items():
				order_file.write(str(key)[1::])
				order_file.write('\n')
				order_file.write(str(value)[1::])
				order_file.write('\n')
		with open(f'../Parcel_Usa/public/goods/{i}_pictures.order', 'w') as order_file:
			for src in product_pictures:
				order_file.write(str(src))
				order_file.write('\n')
		bot.send_message(message.from_user.id, 'Отлично! Каталог обновлен')
		bot.send_message(message.from_user.id, 'Посылочка USA - управление')
		product_feature[base64.b64encode('Цена'.encode('utf-8'))] = product_price
		product_feature[base64.b64encode('Модель'.encode('utf-8'))] = product_name
		product_feature[base64.b64encode('Информация'.encode('utf-8'))] = product_info
		add_order_to_google_table(product_class, product_feature, product_pictures)
		f[message.from_user.id] = ''
		product_class = ''
		product_name = ''
		product_info = ''
		product_feature = {}
		product_feauture_boolean = False
		feauture = ''
		product_pictures = []
		product_price = 0
	elif message.text == 'Все характеристики готовы':
		product_feauture_boolean = True
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		button = types.KeyboardButton("Все фотографии добавлены")
		markup.add(button)
		bot.send_message(message.from_user.id, 'Все характеристики введены, теперь приступим к фотографиям. Прикладывайте последовательно каждую фотографию, я их запомню. Когда приложите все фотографии - нажмите готово', reply_markup=markup)
	elif (f[message.from_user.id] == 'Добавить товар в каталог') and (product_price != 0) and (product_feauture_boolean == False):
		if (feauture == ''):
			feauture = base64.b64encode(message.text.encode('utf-8'))
			if (len(product_feature) == 0):
				bot.send_message(message.from_user.id, 'Первая характеристика готова. Теперь укажи значение этой характеристики. Например: 44')
			else:
				bot.send_message(message.from_user.id, 'Характеристика готова. Теперь введите ее значение.')
		else:
			product_feature[feauture] = base64.b64encode(message.text.encode('utf-8'))
			feauture = ''
			service[message.from_user.id] = base64.b64encode(message.text.encode('utf-8'))
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			button = types.KeyboardButton("Все характеристики готовы")
			markup.add(button)
			bot.send_message(message.from_user.id, 'Отлично. Вводите следующую характеристику или закончите.', reply_markup=markup)
	elif message.text == 'Создать ссылку':
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
		button3 = types.KeyboardButton("Добавить товар в каталог")
		markup.add(button)
		markup.add(button1)
		markup.add(button2)
		markup.add(button3)
		bot.send_message(message.from_user.id, 'Посылочка USA - управление', reply_markup=markup)

@bot.message_handler(content_types=['photo'])
def get_photo(message: types.Message):
	i = 0
	while True:
		if not os.path.isfile(f'../Parcel_Usa/public/goods/pictures/pic_{i}.png'):
			break
		else:
			i += 1
	photo = message.photo[-1]
	file_info = bot.get_file(photo.file_id)
	downloaded_file = bot.download_file(file_info.file_path)
	save_path = f'../Parcel_Usa/public/goods/pictures/pic_{i}.png'
	with open(save_path, 'wb') as new_file:
		new_file.write(downloaded_file)
	product_pictures.append(f'http://10.100.20.21/goods/pictures/pic_{i}.png')
	bot.reply_to(message, 'Загрузил! Прикрепляй следующее фото или нажми готово')

bot.polling(none_stop=True, interval=0)