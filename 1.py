from googleapiclient.discovery import build 
from google_auth_oauthlib.flow import InstalledAppFlow 
from google.auth.transport.requests import Request 
import pickle 
import os.path 
import json
from time import sleep

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'] 

creds = None
if os.path.exists('token.pickle'): 
	with open('token.pickle', 'rb') as token: 
		creds = pickle.load(token) 

if not creds or not creds.valid: 
	if creds and creds.expired and creds.refresh_token: 
		creds.refresh(Request()) 
	else: 
		flow = InstalledAppFlow.from_client_secrets_file('_credentials.json', SCOPES) 
		creds = flow.run_local_server(port=0) 

	# Save the access token in token.pickle file for the next run 
	with open('token.pickle', 'wb') as token: 
		pickle.dump(creds, token) 

service = build('gmail', 'v1', credentials=creds) 

with open('_gmail.json', 'w') as fp:
    json.dump('0', fp)

def getEmails():
	with open('_last_id.json', 'r') as fp:
		last_id = json.load(fp) 

	result = service.users().messages().list(userId='me').execute() 

	messages = result.get('messages') 
	new_id = ''
	for index, msg in enumerate(messages):
		txt = service.users().messages().get(userId='me', id=msg['id'], ).execute() 

		id = txt['id']

		if index == 0:
			new_id = id

		if id == last_id:
			break

		status = False
		datas = txt['payload']['headers']
		for data in datas:
			if data['name'] == "From" and data['value'] == "Winnerodds <info@winnerodds.com>":
				status = True
				break
		if status:
			with open('_gmail.json','w') as fp:
				json.dump('1',fp)
			break
	with open('_last_id.json', 'w') as fp:
		json.dump(new_id, fp) 

if __name__ == "__main__":
	while True:
		try:
			with open('_gmail.json', 'r') as fp:
				result = json.load(fp)
			if str(result) == '0':
				print('reading...')
				getEmails()
		except:
			pass
		print('waiting for 10s...')
		sleep(10)
