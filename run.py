import glob
from time import sleep
import csv
import pathlib
import os

try:

	for file in glob.glob(".\YouTube and YouTube Music\playlists\*.csv"):
		print(file)
		sleep(2)
		
		folder = 'converted/' + pathlib.Path(file).stem

		if not os.path.exists(folder):
			os.makedirs(folder)

		with open(file, newline='') as csvfile:
			csvlines = csv.reader(csvfile, delimiter=',')
			
			rownum = 0
			for row in csvlines:
			
				rownum = rownum + 1
				
				if len(row) == 0 or rownum <= 4:
					continue
					
				outname = folder  + '/' + row[0] + '.url'
				
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
	print('Exception', e)
