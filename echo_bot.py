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
from flask import Flask, redirect, url_for, request, got_request_exception, logging
import os
import sys
from logging.handlers import SMTPHandler, RotatingFileHandler
import logging
import traceback
import bugsnag
from bugsnag.flask import handle_exceptions
import math

from datetime import datetime, date, time

bot = telebot.TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])
host = 'aiaas.pandorabots.com'
user_key = '8704f84cef67d2c4c1c487ce9aab7da2'
app_id = '1409612152298'
botname = os.environ['BOT_NAME']
client = MongoClient('mongodb://heroku_qvt5db7v:h93382meaafa953fnu53blnu2r@ds045252.mongolab.com:45252/heroku_qvt5db7v')
db = client.get_default_database()
bugsnag.configure(
  api_key = os.environ['BUGSNAG_API_KEY'],
  project_root = "./",
)

app = Flask(__name__)
handle_exceptions(app)



@bot.message_handler(content_types=['text'])
def index(message):

	try: 
		print "message"
		print message
		# client = MongoClient(os.environ['MONGODB_TOKEN'])

		users = db.users

		possible_user = users.find({ "tid" : message.chat.id })

		
		


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
		# print bot_response

		soup = BeautifulSoup(bot_response, "lxml")
	    # partition = bot_response.partition('<img')

	    
	    
		if soup.img:
			image_portion = soup.img.extract()['src']
			text_portion = soup.text

			
			print message.chat.id


			print image_dictionary.get(image_portion) 

			bot.send_document(message.chat.id, image_dictionary.get(image_portion))

			



		
		
		# end loop
		options = soup.options

		if options:
			soup.options.extract()

			markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
			option_list = options.text.rsplit("\n")

			
			option_list_length = len(option_list)
			num_rows = math.ceil(option_list_length / 3)
			print 'option length'
			print option_list_length
			print option_list
			print 'num rows'
			print num_rows

			for x in range(1,int(num_rows)+1):
				print x
				markup.row(*option_list[(x-1)*3 : (x*3)])
		else:
			markup = types.ReplyKeyboardHide(selective=False)





			

			
			

			# create loop to send new message for every new line
			# then for each item in the loop, look for items in the "options" tag and send them as keyboard markup
		
		for i,v in enumerate(soup.text.rsplit("\n\n")):
			
			
			bot.send_message(message.chat.id, v, reply_markup=markup )
				

		








	except Exception as e:
		exc_type, exc_value, exc_traceback = sys.exc_info()

		bugsnag.notify(sys.exc_info())
	   	traceback.print_exception(exc_type, exc_value, exc_traceback)






@app.route("/boristheanimal5423", methods=['GET', 'POST'])
def hello():
	try:
		print request.json

		if request.json == None:
			message_json = {
							    "message": {
							        "from": {
							            "username": "dpetkevich",
							            "id": 52132249,
							            "first_name": "Dan",
							            "last_name": "Petkevich"
							        },
							        "date": 1443741883,
							        "chat": {
							            "username": "dpetkevich",
							            "id": 52132249,
							            "first_name": "Dan",
							            "last_name": "Petkevich"
							        },
							        "message_id": 21,
							        "text": "Hi"
							    },
							    "update_id": 103067769
							}
			print json.dumps(message_json)
			print message_json['message']
			message = types.Message.de_json(message_json['message'])

			#delete the three lines below!!!!
			
		else:
			incoming_json = request.json
			incoming_json["created_at"] = datetime.utcnow()

			print 'incoming json'
			print incoming_json
			
			db.messages.insert_one(incoming_json)
			
			message_json = incoming_json['message']
			message = types.Message.de_json(message_json)

		messages = [message]
		print message

		bot.process_new_messages(messages) 
		return "Works"

	except Exception:
		exc_type, exc_value, exc_traceback = sys.exc_info()

		bugsnag.notify(sys.exc_info())
	   	traceback.print_exception(exc_type, exc_value, exc_traceback)



if __name__ == "__main__":
	
	app.run(debug=True)
	
	

   
