from telebot import types
import telebot
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from urllib import urlopen
from PIL import Image
from io import BytesIO
from StringIO import StringIO
from image_paths import image_dictionary
from zendesk_call import *
from flask import Flask, redirect, url_for, request
import os



bot = telebot.AsyncTeleBot("92161996:AAHKneZA0oHz3iGRiSLY0DczLlp90XCAKB4")
host = 'aiaas.pandorabots.com'
user_key = '8704f84cef67d2c4c1c487ce9aab7da2'
app_id = '1409612152298'
botname = 'benjamin'

app = Flask(__name__)

# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     bot.reply_to(message, "Hody, how are you doing?")
@bot.message_handler(func=lambda message: True)
def index(message):

	print "message"
	print message
	# client = MongoClient(os.environ['MONGODB_TOKEN'])
	client = MongoClient('mongodb://heroku_qvt5db7v:h93382meaafa953fnu53blnu2r@ds045252.mongolab.com:45252/heroku_qvt5db7v')

	db = client.get_default_database()
	users = db.users

	possible_user = users.find({ "tid" : message.chat.id })

	# print "chat id"
	# print possible_user[0].get('tid')
	# print"session_id"
	# print possible_user[0].get('session_id')
	# print "client_name"
	# print possible_user[0].get('client_name')


	


	if possible_user.count() == 0:
		# session_id = str(message.chat).split(':')[0]
		# client_name = str(message.chat).split(':')[1]

		query = "https://aiaas.pandorabots.com/atalk/" + str(app_id) + "/" + str(botname) 
		payload1 = {
		'user_key' : str(user_key).encode('utf-8'),
		"input": str(message.text).encode('utf-8')
		}

		r=requests.post(query, data = payload1)

		full_bot_response = r.json()

		users.insert_one(
			{"tid": message.chat.id,
			"session_id": full_bot_response['sessionid'], 
			"client_name": full_bot_response['client_name'] })
	else:
		session_id = possible_user[0].get('session_id')

		client_name = possible_user[0].get('client_name')

		query = "https://aiaas.pandorabots.com/atalk/" + str(app_id) + "/" + str(botname)

		payload1 = {
		'user_key' : str(user_key).encode('utf-8'),
		"input": str(message.text).encode('utf-8'),
		"client_name": str(client_name).encode('utf-8'),
		'sessionid': str(session_id).encode('utf-8')

		}

		r=requests.post(query, data = payload1)

		full_bot_response = r.json()
		

	

	bot_response = full_bot_response["responses"][0]
	print "bot resposne is"

	soup = BeautifulSoup(bot_response, "lxml")
    # partition = bot_response.partition('<img')

    
    
	if soup.img:
		image_portion = soup.img.extract()['src']
		text_portion = soup.text

		# print image_portion
		response = requests.get(image_portion)
		# photo = Image.open(BytesIO(response.content))
		# print 'size'
		# print photo.size
		# print photo.info
		print 'hola'

		print message.chat.id


		print image_dictionary.get(image_portion) 

		bot.reply_to(message, text_portion)
		bot.send_document(message.chat.id, image_dictionary.get(image_portion))


		# string_buffer = BytesIO()
		# string_buffer.write(response.content)
		# img = Image.open(string_buffer)

		# output = BytesIO()
		# img.save(output, format='GIF')
		# output.seek(0)

		# url = 'https://api.telegram.org/bot125944210:AAElCWTL82MdbKQGxk8ZPvm-yIGe4HkasDM/sendDocument'
		# # files = {'document': ('somefilename.gif', output, 'image/GIF')}

		# files = {'document': ('somefilename.gif', open('./introowl.gif'), 'image/GIF')}

		# payload = {'chat_id': message.chat.id}

		# # payload1 = { 
		# # 	'document' : ('newowl.gif', output, 'image/GIF'),
		# # 	"chat_id" : message.chat.id
		# # }

		# headers = {'content-type': 'multipart/form-data'}

		# r = requests.post(url, headers = headers, data = payload, files = files )
		# print 'hihi'
		# print r.json()

	else:

		bot.reply_to(message, soup.text)


	callZendesk(message.chat, message.text)

	# bot.polling()


@app.route("/boristheanimal5423", methods=['POST'])
def hello():

	print request.json


	message_json = request.json['message']
	message = types.Message.de_json(message_json)

	messages = [message]
	print message

	bot.process_new_messages(messages) 
	return "Works"


if __name__ == "__main__":
    app.run()

