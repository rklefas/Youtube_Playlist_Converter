import glob
from time import sleep
import csv
import pathlib
import os
from googleapiclient.discovery import build
from slugify import slugify
import json


try:

	configs = json.load(open('./config.json', 'r'))

	for file in glob.glob(".\YouTube and YouTube Music\playlists\*.csv"):
		print('')
		print('PLAYLIST', file)
		print('')
		sleep(2)
		
		folder = './converted/' + pathlib.Path(file).stem

		if not os.path.exists(folder):
			os.makedirs(folder)

		with open(file, newline='') as csvfile:
			csvlines = csv.reader(csvfile, delimiter=',')
			rownum = None
			for row in csvlines:
			
				if len(row) == 0:
					continue
				elif row[0] == 'Video Id':
					rownum = 0
					continue
				elif rownum == None:
					continue
				else:
					rownum = rownum + 1
					
				
				service = build('youtube', 'v3', developerKey=configs['developerKey'])
				dataX = service.videos().list(part='snippet', id=row[0]).execute()
				service.close()
				
				try:
					tmp = slugify(dataX['items'][0]['snippet']['title']).replace('-', ' ')
					tmp = tmp + ' - '
					tmp = tmp + slugify(dataX['items'][0]['snippet']['channelTitle']).replace('-', ' ')
					outname = folder  + '/' + tmp + '.url'
				except Exception as e:
					outname = folder  + '/VIDEO ' + row[0] + '.url'
					
				if os.path.isfile(outname):
				
					print('Found', outname)
				else:
				
					with open('template.url', 'r') as file:
						data = file.read()
						
					data = data.replace('[id]', str(row[0]))

					text_file = open(outname, "w")
					text_file.write(data)
					text_file.close()

					print('Created', outname)

except Exception as e:
	raise Exception(e)
