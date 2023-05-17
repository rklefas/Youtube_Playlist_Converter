import glob
from time import sleep
import os
import configparser
import filedate
import pathlib


def finished(msg, countdown):
	print(msg)
	
	for ix in range(0, countdown):
		print('.' * (countdown - ix))
		sleep(1)




folder = input('What folder? ')

fileglob = glob.glob(folder + "*.url")

print(len(fileglob), 'files found')
sleep(5)

for file in fileglob:

	newfile = pathlib.Path(file).stem
	
	print('Current: ', newfile)
	
	parts = newfile.split(" - ")
	newfile = str(pathlib.Path(file).parent) + '/' + parts[1] + " - " + parts[0]  + " - yt.url"
	
	print('  New: ', newfile)

	os.rename(file, newfile)
		




finished('Done', 5)
