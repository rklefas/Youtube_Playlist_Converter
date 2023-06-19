import glob
from time import sleep
import json
import sys
from googleapiclient.discovery import build
import configparser
import filedate


def finished(msg, countdown):
	print(msg)
	
	for ix in range(0, countdown):
		print('.' * (countdown - ix))
		sleep(1)



def converted_duration(duration):

	duration = duration.replace('PT', '')
	duration = duration.split('H')

	parts = {'hours': 0, 'minutes': 0, 'seconds': 0}
	
	if len(duration) == 2:
		parts['hours'] = int(duration[0])
		duration = duration[1].split('M')
	else:
		duration = duration[0].split('M')

	if len(duration) == 2:
		parts['minutes'] = int(duration[0])
		duration = duration[1].split('S')
	else:
		duration = duration[0].split('S')
	
	if len(duration) == 2:
		parts['seconds'] = int(duration[0])

	return parts





configs = json.load(open('./config.json', 'r'))

folder = input('What folder? ')

fileglob = glob.glob(folder + "*.url")

print(len(fileglob), 'files found')
sleep(5)

for file in fileglob:

	
	inifile = configparser.ConfigParser()
	inifile.read(file)

	if inifile['InternetShortcut'].get('length'):
		print('Length found')
		continue
		
	print('Open', file)
	
	try:
		
		
		
		justid = inifile['InternetShortcut']['url']
		justid = justid.replace('https://www.youtube.com/watch?v=', '')
	
		print('  Fetching', justid)

		# cache the data here...
		# getting the contentDetails.duration would be useful
		service = build('youtube', 'v3', developerKey=configs['developerKey'])
		dataX = service.videos().list(part='contentDetails', id=justid).execute()
		service.close()
		
		duration = dataX['items'][0]['contentDetails']['duration']
		inifile['InternetShortcut']['length'] = duration
		duration = converted_duration(duration)
		
		padding = 'S' * duration.get('seconds')
		padding = padding + 'M' * (duration.get('minutes') * 60)
		padding = padding + 'H' * (duration.get('hours') * 3600)
		padding = padding * 16
		inifile['InternetShortcut']['size_padding'] = padding

		print('  Time', inifile['InternetShortcut']['length'])
		
		with open(file, 'w') as configfile:
			inifile.write(configfile)
			
		filedate.File(file).set(
			created = inifile['InternetShortcut']['DateModified'],
			modified = inifile['InternetShortcut']['DateModified']
		)
			
			
	except Exception as e:
		print(e)
		print('Error in', file)
		continue
		
	



input('Enter to exit')