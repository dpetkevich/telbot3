from zenpy import Zenpy
import requests
import json

zenpy = Zenpy('textbenjamin', 'daniel@textbenjamin.com', 'SoC5ZLSVqnJHAUd2ABJj7AnEsqMeZqKHurrHV5Ij')
user = 'daniel@textbenjamin.com'
pwd = 'boris5423'

def callZendesk(chat, message):

	

	url = "https://textbenjamin.zendesk.com/api/v2/users/search.json"

	payload = { "external_id": chat.id }

	possible_existing_user = requests.get(url, auth=(user, pwd), params=payload).json()

	print possible_existing_user

	if possible_existing_user.get('count') > 0:

		updateZendeskTicket(possible_existing_user['users'][0], message)

	else:

		createZendeskTicket(chat,message)


def createZendeskTicket(chat, message):

	url = 'https://textbenjamin.zendesk.com/api/v2/tickets.json'

	#set data 
	data = {
	    "ticket": {
	        "requester": {
	            "name" : str(chat.first_name) + " " + str(chat.last_name),
	            'external_id' : str(chat.id),
	            "details" : 'telegram'
	            
	            },
	        "comment":{ 
	            "body": message
	        },
	        "subject": 'Request'
	    }
	}

	# set headers
	headers = {'content-type': 'application/json'}

	# make request to create ticket
	createTicketResponse = requests.post(url, data=json.dumps(data), auth=(user, pwd), headers=headers)

	print "creat ticket respoinse"
	print createTicketResponse


def updateZendeskTicket(relevant_user, message):

	print relevant_user

	# lookup the ticket belonging to this user
	relevant_ticket = zenpy.search(type='ticket', requester_id = relevant_user.get('id')).next()


	## prepare update ticket request
	# set url
	url = 'https://textbenjamin.zendesk.com/api/v2/tickets/' + str(relevant_ticket.id) + '.json'

	#set data 
	data = {
	    "ticket": {
	        "comment":{ 
	            "body": message
	        }
	    }
	}

	# set headers
	headers = {'content-type': 'application/json'}

	# make request
	updated_ticket_response = requests.put(url, data = json.dumps(data), auth=(user, pwd), headers=headers)

	print 'updated ticket response'
	print user
	print pwd

	print updated_ticket_response.text









