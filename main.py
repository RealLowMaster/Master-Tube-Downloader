from tkinter import Tk, Label, Entry, StringVar, Button, Frame, Scrollbar, messagebox, filedialog, ttk
from tkinter.constants import CENTER, DISABLED, END, W, LEFT
from PIL import ImageTk, Image
from os import mkdir, listdir, remove
from os.path import isdir
from moviepy.editor import VideoFileClip, AudioFileClip
from threading import Thread
import requests
import pafy

win = Tk()
win.title("Master Tube Downloader v1.0.0")
win.iconbitmap('./icon.ico')

win_width = 500
win_height = 510
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
win.geometry(f"{win_width}x{win_height}+{int((screen_width/2)-(win_width/2))}+{int((screen_height/2)-(win_height/2))}")
win.resizable(False, False)

# Global Values
path = ""
yt = None
convert_video = False
yt_streams_index = None
yt_quality_choises = None
downloadList = []
downloadListCounter = 0

if (isdir('temp')):
	for i in listdir('temp'):
		remove('temp\\'+i)
else:
	mkdir('temp')

""" functions """
def bytesto(bytes, to, bsize=1024):
	a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
	r = float(bytes)
	for i in range(a[to]):
		r = r / bsize

	return int(r)

def set_thumb():
	overviewImage = ImageTk.PhotoImage(Image.open(requests.get(yt.thumb, stream=True).raw).resize((190, 140), Image.ANTIALIAS))
	overviewImageLabel.configure(image=overviewImage)
	overviewImageLabel.image = overviewImage

def get_youtube():
	global yt
	global yt_streams_index
	global yt_quality_choises
	global convert_video
	yt = None
	yt_streams_index = None
	yt_quality_choises = None
	url = youtubeInput.get()
	errMsgLabel.config(text="Waiting", fg='orange')
	overviewImageLabel.configure(image=None)
	overviewImageLabel.image = None
	overviewTitleLabel.config(text="")
	overviewTimeLabel.config(text="")
	qualitySelector.config(values=None, state=DISABLED)
	downloadButton.config(state=DISABLED)
	if (len(url) > 10):
		youtubeInput.config(state=DISABLED)
		try:
			yt = pafy.new(url)
			youtubeInput.config(state='normal')
			errMsgLabel.config(text="Video Found", fg='green')
			Thread(target=set_thumb).start()
			overviewTitleLabel.config(text=yt.title)
			overviewTimeLabel.config(text=yt.duration)

			videos = []
			videos_index = []
			audios = []
			audios_index = []
			video_type = 'normal'
			if convert_video:
				video_type = 'video'
			for i in range(0, len(yt.allstreams)):
				if (yt.allstreams[i].mediatype == video_type and yt.allstreams[i].extension == 'mp4'):
					if (videos.count('Video: '+yt.allstreams[i].quality+'p') == 0):
						videos.append('Video: '+yt.allstreams[i].quality+'p')
						videos_index.append(i)
					else:
						videos_index[videos.index('Video: '+yt.allstreams[i].quality+'p')] = i
				elif (yt.allstreams[i].mediatype == 'audio' and yt.allstreams[i].extension == 'mp3' or yt.allstreams[i].extension == 'm4a'):
					audios.append('Audio: '+yt.allstreams[i].extension+' '+yt.allstreams[i].quality)
					audios_index.append(i)
			
			for i in range(0, len(audios)):
				videos.append(audios[i])
				videos_index.append(audios_index[i])
			
			yt_quality_choises = videos
			yt_streams_index = videos_index
			qualitySelector.config(values=videos, state='readonly')
			downloadButton.config(state='normal')
		except Exception as err:
			youtubeInput.config(state='normal')
			err = str(err)
			if 'Need 11 character' in err:
				errMsgLabel.config(text="Please Enter a currect Url", fg='red')
			elif 'Video unavailable' in err:
				errMsgLabel.config(text="Video not Found", fg='red')
			else:
				errMsgLabel.config(text="Video not Found or there is no format for it", fg='red')
	else:
		errMsgLabel.config(text="Please Enter a currect Url", fg='red')

def input_callback():
	Thread(target=get_youtube).start()

def chooseLoaction():
	global path
	path = filedialog.askdirectory()
	if (len(path) > 3):
		errSavePathMsgLabel.config(text=path, fg='green')
	else:
		errSavePathMsgLabel.config(text='Please Choose a Location.', fg='red')

def yt_dl_callback(total_size, dl_size, percent, dl_speed, tokhmam):
	pass

def Download():
	global downloadListCounter
	global convert_video
	index = yt_quality_choises.index(qualitySelector.get())
	if 'Audio' in qualitySelector.get():
		downloadList.append([yt, yt_streams_index[index], path, convert_video, False])
	else:
		downloadList.append([yt, yt_streams_index[index], path, convert_video, True])
	
	if (downloadList[0][3] and downloadList[0][4]):
		downloadListWidget.insert(parent='', index=END, iid=downloadListCounter, values=(yt.title, yt_quality_choises[index], str(bytesto((yt.allstreams[yt_streams_index[index]].get_filesize() + yt.getbestaudio().get_filesize()), 'm'))+'mb', 0, 0, 0))
		downloadListCounter += 1
		downloadList[0][0].allstreams[downloadList[0][1]].download(filepath='temp', quiet=True, callback=yt_dl_callback)
		downloadList[0][0].getbestaudio().download(filepath='temp', quiet=True, callback=yt_dl_callback)
		video_name = None
		audio_name = None
		for i in listdir('temp'):
			if '.mp4' in i:
				video_name = i
			else:
				audio_name = i
		
		videoclip = VideoFileClip('./temp/'+video_name)
		audioclip = AudioFileClip('./temp/'+audio_name)
		videoclip.audio = audioclip
		videoclip.write_videofile(downloadList[0][2]+'\\'+video_name)
	else:
		downloadListWidget.insert(parent='', index=END, iid=downloadListCounter, values=(yt.title, yt_quality_choises[index], str(bytesto(yt.allstreams[yt_streams_index[index]].get_filesize(), 'm'))+'mb', 0, 0, 0))
		downloadListCounter += 1
		downloadList[0][0].allstreams[downloadList[0][1]].download(filepath=path, quiet=True, callback=yt_dl_callback)

def dl_button_callback():
	if (len(path) > 3):
		choosed = yt_quality_choises.count(qualitySelector.get())
		if (choosed == 1):
			Thread(target=Download).start()
		else:
			messagebox.showerror(title="Quality Error!", message="Please Choose a Quality.")
	else:
		messagebox.showerror(title="Location Error!", message="Please Choose a Location For Saving Downloaded Videos.")

# Make Tabs
# https://www.youtube.com/watch?v=5Xx5AwhsJmw
tabControl = ttk.Notebook(win)
mainTab = ttk.Frame(tabControl)
downloadListTab = ttk.Frame(tabControl)
tabControl.add(mainTab, text='Main')
tabControl.add(downloadListTab, text='Downloads')
tabControl.pack(expand=1, fill="both")

""" mainTab Widgets """
# YouTube Label
youtubeLabel = Label(mainTab, text="Enter Video Url:", font=("monospace", 15, "bold"))
youtubeLabel.place(relx=0.5, anchor=CENTER, y=20)

# YouTube Url Input
youtubeInputVar = StringVar()
youtubeInputVar.trace("w", lambda name, index, mode, youtubeInputVar=youtubeInputVar: input_callback())
youtubeInput = Entry(mainTab, width=50, textvariable=youtubeInputVar)
youtubeInput.place(relx=0.5, anchor=CENTER, y=50)

# Error Message Label
errMsgLabel = Label(mainTab, font=("monospace", 11))
errMsgLabel.place(relx=0.5, anchor=CENTER, y=75)

# Video Overview
overviewFrame = Frame(mainTab, bg="white", width=450, height=150)
overviewFrame.place(relx=0.5, anchor=CENTER, y=170)
overviewImageLabel = Label(overviewFrame, bg="lightgray", width=190, height=140, image=None)
overviewImageLabel.place(rely=0.5, anchor=CENTER, x=100, width=190, height=140)
overviewTitleLabel = Label(overviewFrame, wraplength=240, anchor=W, justify=LEFT)
overviewTitleLabel.place(width=240, x=200, y=10)
overviewTimeLabel = Label(overviewFrame, anchor=W, justify=LEFT, font=('monospace', 9, 'bold'))
overviewTimeLabel.place(x=200, y=120)

# Chosing Saving Path Label
savePathLabel = Label(mainTab, text="Save Location", font=("monospace", 15, "bold"))
savePathLabel.place(relx=0.5, anchor=CENTER, y=275)

# Choosing Saving Path Button
savePathButton = Button(mainTab, text="Choose Location", bg="red", fg="white", font=("monospace", 9, "bold"), command=chooseLoaction)
savePathButton.place(relx=0.5, anchor=CENTER, y=310)

# Error Saving Path Message Label
errSavePathMsgLabel = Label(mainTab, font=("monospace", 11))
errSavePathMsgLabel.place(relx=0.5, anchor=CENTER, y=338)

# Quality Label
qualityLabel = Label(mainTab, text="Select Quality", font=("monospace", 15, "bold"))
qualityLabel.place(relx=0.5, anchor=CENTER, y=370)

# Quality Selector
qualitySelector = ttk.Combobox(mainTab, font=("monospace", 10), state=DISABLED)
qualitySelector.place(relx=0.5, anchor=CENTER, y=400)

# Download Button
downloadButton = Button(mainTab, text="Download", bg="red", fg="white", font=("monospace", 13, "bold"), state=DISABLED, command=dl_button_callback)
downloadButton.place(relx=0.5, anchor=CENTER, y=445)

""" downloadListTab Tab Widgets """
# Download List Vertical Scrollbar
downloadListVerticalScrollbar = Scrollbar(downloadListTab)
downloadListVerticalScrollbar.place(width=20, height=400, x=480, y=0)

# Download List Horizontal Scrollbar
downloadListHorizontalScrollbar = Scrollbar(downloadListTab, orient='horizontal')
downloadListHorizontalScrollbar.place(width=500, height=20, x=0, y=400)

# Download List Widget
downloadListWidget = ttk.Treeview(downloadListTab, yscrollcommand=downloadListVerticalScrollbar.set, xscrollcommand=downloadListHorizontalScrollbar.set)

# Set Download List Scrollbars
downloadListVerticalScrollbar.config(command=downloadListWidget.yview)
downloadListHorizontalScrollbar.config(command=downloadListWidget.xview)

# Set Download List Columns
downloadListWidget['show'] = 'headings'
downloadListWidget['columns'] = ('Name', 'Quality', 'Size', 'Status', 'LeftTime', 'Speed')
downloadListWidget.column('Name', minwidth=25, width=110)
downloadListWidget.column('Quality', minwidth=25, width=80)
downloadListWidget.column('Size', minwidth=10, width=30)
downloadListWidget.column('Status', minwidth=10, width=30)
downloadListWidget.column('LeftTime', minwidth=10, width=30)
downloadListWidget.column('Speed', minwidth=10, width=30)
downloadListWidget.heading('Name', text='Name')
downloadListWidget.heading('Quality', text='Quality')
downloadListWidget.heading('Size', text='Size')
downloadListWidget.heading('Status', text='Status')
downloadListWidget.heading('LeftTime', text='Left Time')
downloadListWidget.heading('Speed', text='Speed')
downloadListWidget.place(width=480, height=400, x=0, y=0)


win.mainloop()