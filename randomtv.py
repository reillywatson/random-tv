from Tkinter import *

def ismovie(file):
	extensions = ['.asf', '.avi', '.divx', '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpeg', '.mpg', '.wmv']
	fileext = file[file.rfind('.'):].lower()
	return fileext in extensions

def findFiles(base):
	import os
	files = []
	for root, dirnames, filenames in os.walk(base):
		for f in filenames:
			files.append(os.path.join(root, f))
	return [a for a in files if ismovie(a)]

def randomShows(basePath, numFiles):
	import random
	files = findFiles(basePath)
	random.shuffle(files)
	return files[:numFiles]

def centerWindow(window, width, height):
	w = window.winfo_screenwidth()
	h = window.winfo_screenheight()
	rootsize = (width, height)
	x = w/2 - rootsize[0]/2
	y = h/2 - rootsize[1]/2
	geom = "%dx%d+%d+%d" % (rootsize + (x, y))
	window.geometry(geom)

def writePlaylist(path, episodes):
	import urllib
	f = open(path, 'w')
	f.write('''<?xml version="1.0" encoding="UTF-8"?><playlist version="1" xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/"><title>Playlist</title><trackList>''')
	for episode in episodes:
		f.write('<track><location>file://'+urllib.quote(episode)+'</location></track>')
	f.write('</trackList></playlist>')
	f.close()

def main():
	import os
	import sys
	
	# stuff to modify if you want to run this on another machine
	shows = [
	'Arrested Development',
	'Clone High',
	'Dinosaurs',
	'Extras',
	'Family Guy',
	'Fawlty Towers',
	'Futurama',
	'Golden Girls, The',
	'How I Met Your Mother',
	"It's Always Sunny In Philadelphia",
	'Looney Tunes',
	'Modern Family',
	'Office, The',
	'Robot Chicken',
	'Simpsons, The',
	'Trailer Park Boys'
	]
	basePath = '/Volumes/EXTERNAL/'
	defaultShow = 'Simpsons, The'

	master = Tk()
	master.title('Random TV!')
	master.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
	master.config(menu=Menu(master))
	selectedShow = StringVar(master)
	selectedShow.set(defaultShow)
	options = OptionMenu(master, selectedShow, *shows)
	options.pack(side=TOP)
	button = Button(master, text='OK', command=master.quit)
	button.pack(side=RIGHT, padx=20)
	numEpisodes = Entry(master)
	numEpisodes.pack(side=BOTTOM, padx=20)
	numEpisodes.insert(0, '1')
	numEpisodes.selection_range(0, END)
	numEpisodes.bind('<Return>', lambda _: master.quit())
	centerWindow(master, 200, 55)
	numEpisodes.focus()
	master.mainloop()
	epsToWatch = 1
	if numEpisodes.get().isdigit():
		epsToWatch = int(numEpisodes.get())
	episodes = randomShows(basePath+selectedShow.get(), epsToWatch)
	path = '/tmp/playlist.xspf'
	writePlaylist(path, episodes)
	os.popen('open ' + path + ' --args -f')

if __name__ == '__main__':
	main()