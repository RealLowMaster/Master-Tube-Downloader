from tkinter import Tk, Label, Entry, StringVar, Button, Frame, filedialog, ttk
from tkinter.constants import CENTER, DISABLED, W, LEFT
from PIL import ImageTk, Image
import requests
from io import BytesIO
import pafy

win = Tk()
win.title("Master Tube Downloader v1.0.0")
win.iconbitmap('./icon.ico')

win_width = 500
win_height = 600
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
win.geometry(f"{win_width}x{win_height}+{int((screen_width/2)-(win_width/2))}+{int((screen_height/2)-(win_height/2))}")
win.resizable(False, False)

# Global Values
path = ""
yt = None
yt_streams = None
dl_enable = False

""" functions """
def url_callback(value):
	global dl_enable
	global yt
	global yt_streams
	dl_enable = False
	yt = None
	yt_streams = None
	url = value.get()
	errMsgLabel.config(text="Video Not Found", fg='red')
	overviewImageLabel.configure(image=None)
	overviewImageLabel.image = None
	overviewTitleLabel.config(text="")
	overviewTimeLabel.config(text="")
	qualitySelector.config(values=None, state=DISABLED)
	if (len(url) > 10):
		yt = pafy.new(url)
		dl_enable = True
		errMsgLabel.config(text="Video Found", fg='green')
		overviewImage = ImageTk.PhotoImage(Image.open(requests.get(yt.thumb, stream=True).raw).resize((190, 140), Image.ANTIALIAS))
		overviewImageLabel.configure(image=overviewImage)
		overviewImageLabel.image = overviewImage
		overviewTitleLabel.config(text=yt.title)
		overviewTimeLabel.config(text=yt.duration)

		videos = []
		audios = []
		print(yt.allstreams)
		for i in range(0, len(yt.allstreams)):
			if (yt.allstreams[i].extension == 'mp4' and videos.count(yt.allstreams[i].quality) == 0):
				videos.append(yt.allstreams[i].quality)
			elif (yt.allstreams[i].extension == 'mp3' or yt.allstreams[i].extension == 'm4a'):
				if (audios.count(yt.allstreams[i].quality) == 0):
					audios.append(yt.allstreams[i].quality)
		
		print("=================================")
		print(videos)
		print("=================================")
		print(audios)
		print("=================================")
		for i in audios:
			videos.append(i)
		print("=================================")
		qualitySelector.config(values=videos, state='readonly')
	else:
		errMsgLabel.config(text="Please Enter a Url", fg='red')

# Make Tabs
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
youtubeInputVar.trace("w", lambda name, index, mode, youtubeInputVar=youtubeInputVar: url_callback(youtubeInputVar))
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
savePathButton = Button(mainTab, text="Choose Location", bg="red", fg="white", font=("monospace", 9, "bold"))
savePathButton.place(relx=0.5, anchor=CENTER, y=310)

# Error Saving Path Message Label
errSavePathMsgLabel = Label(mainTab, text="", font=("monospace", 11))
errSavePathMsgLabel.place(relx=0.5, anchor=CENTER, y=338)

# Quality Label
qualityLabel = Label(mainTab, text="Select Quality", font=("monospace", 15, "bold"))
qualityLabel.place(relx=0.5, anchor=CENTER, y=370)

# Quality Selector
qualitySelector = ttk.Combobox(mainTab, font=("monospace", 10), state=DISABLED)
qualitySelector.place(relx=0.5, anchor=CENTER, y=400)

# Download Button
downloadButton = Button(mainTab, text="Download", bg="red", fg="white", font=("monospace", 13, "bold"))
downloadButton.place(relx=0.5, anchor=CENTER, y=445)


win.mainloop()