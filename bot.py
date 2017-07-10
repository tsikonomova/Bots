#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
from telegram import InlineQueryResultPhoto
from telegram import InputTextMessageContent

# bot properties
token = '218864402:AAEXp1ME2Mazd9gnk0TonERavsGzNZyf6ZA'
url = 'https://api.telegram.org/bot' + token + '/'
default_chat_id = '38810017'

# the error object
class Error(object):
   text = ''

"""Function to make post requests to the telegram api 

   @param   string  the request name 
   @param   string  the request type 
   @param   object	the request parameters
   @return  object 	the response (dict or Error)
"""
def postRequest(name, type, params):
	if type == 'data':
		post = requests.post(url + name, data = params)
	elif type == 'files':
		post = requests.post(url + name, files = params)

	if post.status_code == 200:
		return post.json()
	else:
		error = Error()
		error.text = post.status_code
		return error

"""Function to make get requests to the telegram api 

   @param   string  the request name 
   @return  object 	the response (dict or Error)
"""
def getRequest(type):
	get = requests.get(url+type)

	if get.status_code == 200:
		return get.json()
	else:
		error = Error()
		error.text = get.status_code
		return error

"""Function to make get request to get the bot data

   @return  object 	the response
"""
def getMe():
	return getRequest('getMe')

"""Function to make post request to send message to a chat 

   @param   integer  the chat id to which to send the text
   @param   string   the text to send
   @return  object 	 the response
"""
def sendMessage(chat_id, text):
	params = {'chat_id': chat_id, 'text': text}
	return postRequest('sendMessage', 'data', params )

"""Function to make post request to send photo to a chat 

   @param   integer  the chat id to which to send the photo
   @param   string   the path to the photo to send
   @return  object 	 the response
"""
def sendPhoto(chat_id, photo):
	params = {'chat_id': str(chat_id), 'photo': open(photo, 'rb')}	
	return postRequest('sendPhoto?chat_id=' + str(chat_id), 'files', params)

"""Function to make post request to send answer to an inline query

   @param   string                       the inline query id to which to send the answer
   @param   array of InlineQueryResult   the answer array
   @return  object 	                     the response
"""
def answerInlineQuery(inline_query_id, results):
	params = {'inline_query_id': str(inline_query_id), 'results': results}	
	return postRequest('answerInlineQuery', 'data', params)

"""Function to make get request to get messages written to the bot

   @return  object 	the response
"""
def getUpdates():
	return postRequest('getUpdates', 'data', {'offset' : 3, 'limit' : 100})

"""Function to set an outgoing webhook to receive incoming updates 

   @return  object 	the response
"""
def setWebhook():
	return postRequest('setWebhook', 'data', {'url' : 'https://www.pi.virgon.eu/' + token})

# set the outgoing webhook 
#setWebhook() 

# updates properties
all_updates = [];
last_update = 0
starttime=time.time()

# neverending loop 
while True:

    # get the updates
    updates = getUpdates()

    # do we have updates at all?
    if isinstance(updates, Error) is False:

   		# the count of the not processed updates
   		not_updated = 0
   		
   		# store the last udate or update the count of the not processed updates
   		if last_update == 0:
   			last_update = len(updates['result'])-1
   		elif len(updates['result'])-1 > last_update: 
   			not_updated = len(updates['result'])-1 - last_update

   		# loop to process the updates
   		for counter in range(1, not_updated+1):
   			
   			# the index of the current update
   			index = last_update + counter

   			# get the current update
   			result = updates['result'][index]

   			# convert the message or the unline query
   			if 'message' in result:
   				message = result['message']['text']
   				name = result['message']['from']['first_name']
   				chat_id = result['message']['chat']['id']
			else:
			    message = result['inline_query']['query']
			    name = result['inline_query']['from']['first_name']
			    chat_id = default_chat_id
			    print(result['inline_query'])
			    input_message_content = InputTextMessageContent({ 'message_text': 'input_message_content' })
			    #input_query_photo = InlineQueryResultPhoto({'type': 'photo', 'id': '123', 'photo_url': 'http://modigi.ir/wp-content/uploads/2017/01/561e5c39dcc9e581274137.png', 'thumb_url': 'https://avatars1.githubusercontent.com/u/6422482?v=3&s=400'})
			    input_query_photo = InlineQueryResultPhoto('photo', '123', 'https://core.telegram.org/file/811140327/1/zlN4goPTupk/9ff2f2f01c4bd1b013', 'https://telegram.org/file/811140614/2/flKQKZ7xUOE.27938.gif/5574a04570218c9e11')
			    print(answerInlineQuery(result['inline_query']['id'], input_query_photo))
		

			# in the last iteration update the last update
   			if counter == not_updated:
   				last_update = index
			
			# process the ascii and non-ascii messages
			try:
				message.decode('ascii')
			except UnicodeEncodeError:
				if message.encode('utf-8') == 'Здрасти':
					sendMessage(chat_id, 'Здравей!')
				elif message.encode('utf-8') == 'Бот':
					sendMessage(chat_id, 'Човек?')
				elif message.encode('utf-8') == 'Ехо':
					sendMessage(chat_id, 'Как си?')
				elif message.encode('utf-8') == 'Как си?':
					sendMessage(chat_id, 'Радвам се да си поговорим!')
				elif message.encode('utf-8') == 'Обичам те':
					sendMessage(chat_id, 'И аз!')
				elif message.encode('utf-8') == 'Как изглеждаш?':
					sendPhoto(chat_id, 'images/bot.jpg')
				elif message.encode('utf-8') == 'Жив ли си?':
					sendMessage(chat_id, 'Толкова колкото и ти си ;)')
				elif message.encode('utf-8') == 'И сега какво?':
					sendMessage(chat_id, name + '-готин')
				elif message.encode('utf-8') == 'Лош бот':
					sendMessage(chat_id, 'На мен ли говориш?')
				else:
					sendMessage(chat_id, 'Кажи ми повече')
			else:
				if message == 'hi':
					sendMessage(chat_id, 'hi, man!')
				elif message == 'bot':
					sendMessage(chat_id, 'How are you, man?')
				elif message == 'echo':
					sendMessage(chat_id, 'Whats up?')
				elif message == 'How are you?':
					sendMessage(chat_id, 'Happy to talk to you!')
				elif message == 'I love you':
					sendMessage(chat_id, 'I love you too')
				elif message == 'How do you look like?':
					sendPhoto(chat_id, 'images/bot.jpg')
				elif message == 'Are you alive':
					sendMessage(chat_id, 'As alive as you ;)')
				elif message == 'and now what?':
					sendMessage(chat_id, name + '-cool')
				elif message == 'Bad bot':
					sendMessage(chat_id, 'Are you talking to me?')
				else:
					sendMessage(chat_id, 'Tell me something more')
    else:
	    print 'Error: ' + updates.text 

    # iterate every 10 seconds
    time.sleep(10.0 - ((time.time() - starttime) % 10.0))


