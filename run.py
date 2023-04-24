import glob
from time import sleep
import csv
import pathlib
import os
from googleapiclient.discovery import build
from slugify import slugify
import json
import filedate


def niceslug(tmp):
	tmp = tmp.replace('\'', '')
	tmp = slugify(tmp)
	tmp = tmp.replace('-', ' ')

	return tmp


def finished(msg, countdown):
	print(msg)
	
	for ix in range(0, countdown):
		print('.' * (countdown - ix))
		sleep(1)


finished('Starting', 5)

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
				
				if rownum == configs['conversionMax']:
					print('Reached conversion max')
					continue
				if rownum > configs['conversionMax']:
					continue
				
				try:
					# cache the data here...
					service = build('youtube', 'v3', developerKey=configs['developerKey'])
					dataX = service.videos().list(part='snippet', id=row[0]).execute()
					service.close()
					
					tmp = niceslug(dataX['items'][0]['snippet']['title'])
					tmp = tmp + ' - '
					tmp = tmp + niceslug(dataX['items'][0]['snippet']['channelTitle'])
					
					outname = folder  + '/' + tmp + ' - youtube.url'
				except Exception as e:
					print('Skipping', row[0])
					continue
					
				if os.path.isfile(outname):
				
					print('Found', rownum, outname)
				else:
				
					with open('template.url', 'r') as file:
						data = file.read()
						
					data = data.replace('[id]', str(row[0]))
					data = data + "DateModified=" + row[1]

					text_file = open(outname, "w")
					text_file.write(data)
					text_file.close()
					
					filedate.File(outname).set(
						created = row[1],
						modified = row[1]
					)

					print('Created', rownum, outname)

except Exception as e:
	raise Exception(e)


finished('All done', 10)
