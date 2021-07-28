from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pafy

win = Tk()
win.title("Master Tube Downloader v1.0.0")
win.geometry("400x400")
win.columnconfigure(0, weight=1)

# Global Values
path = ""

# Choosing Path Functions
def openPathDialog():
	global path
	path = filedialog.askdirectory()
	if (len(path) > 1):
		errSavePathMsgLabel.config(text=path, fg="green")
	else:
		errSavePathMsgLabel.config(text="Please Choose Location", fg="red")

# Download
def Download():
	choise = qualitySelector.get()
	url = youtubeInput.get()
	if (len(url) > 1):
		errMsgLabel.config(text="")
		""""
		yt = pafy.new("https://www.youtube.com/watch?v=eYpL-YMHjWw")
		if (choise == qualityChoices[3]):
			select = yt.streams.filter(progressive=True).first()
		elif (choise == qualityChoices[0]):
			select = yt.streams.filter(progressive=True, file_extension="mp4").last()
		elif (choise == qualityChoices[4]):
			select = yt.streams.filter(only_audio=True).first()
		else:
			errMsgLabel.config(text="Paste Link again!", fg="red")
		
		select.download(path)
		errMsgLabel.config(text="Download Completed!", fg="greed")"""


# YouTube Label
youtubeLabel = Label(win, text="Enter Video Url:", font=("monospace", 15))
youtubeLabel.grid()

# YouTube Url Input
youtubeInputVar = StringVar()
youtubeInput = Entry(win, width=50, textvariable=youtubeInputVar)
youtubeInput.grid()

# Error Message Label
errMsgLabel = Label(win, text="", font=("monospace", 11))
errMsgLabel.grid()

# Chosing Saving Path Label
savePathLabel = Label(win, text="Save Location", font=("monospace", 15, "bold"))
savePathLabel.grid()

# Choosing Saving Path Button
savePathButton = Button(win, text="Choose Location", width=10, bg="red", fg="white", command=openPathDialog)
savePathButton.grid()

# Error Saving Path Message Label
errSavePathMsgLabel = Label(win, text="", font=("monospace", 11))
errSavePathMsgLabel.grid()

# Quality Label
qualityLabel = Label(win, text="Select Quality", font=("monospace", 15))
qualityLabel.grid()

# Quality Selector
qualityChoices = ["144p", "360p", "480p", "720p", "Audio Only"]
qualitySelector = ttk.Combobox(win, values=qualityChoices)
qualitySelector.grid()

# Download Button
downloadButton = Button(win, text="Download", width=10, bg="red", fg="white", command=Download)
downloadButton.grid()

# Developer Label
developerLabel = Label(win, text="Developer Label", font=("monospace", 15))
developerLabel.grid()


win.mainloop()