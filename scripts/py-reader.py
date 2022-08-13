import tkinter as tk # Python-3
#import Tkinter as tk # Python-2
from tkinter import filedialog
import pyttsx3
import time
import threading
from tts_class import TTS_Engine
import multiprocessing
from multiprocessing import Value
import os.path


''' global variables	'''
rawTxt = " "
preppedTxt = " "
maxLoops = 0
lineTracker = Value('i', 0)
proc = None


'''		GUI helper functions	'''
def findLine(v):
	global proc
	if proc.is_alive():
		if captionstr.get() != preppedTxt[lineTracker.value-1]:

			captionstr.set(preppedTxt[lineTracker.value-1])
			curLine.set(lineTracker.value)

		time.sleep(v)
		findLine(v)

def changeLine(b):
	# print next line
	if b==True and lineTracker.value < maxLoops:
		lineTracker.value+=1

	# print previous line
	if b==False and lineTracker.value > 0:
		lineTracker.value-=1	
	
	# update visuals
	if lineTracker.value < maxLoops:
		captionstr.set(preppedTxt[lineTracker.value])
		curLine.set(lineTracker.value)

	#print(lineTracker.value)
	stopAudio()

# tts engine callback
def onStart(name):
	lineTracker.value += 1

# stop audio (does NOT interrupt current line)
def stopAudio():
	global proc
	if proc != None and proc.is_alive():
		proc.terminate()


def triggerThread(action):
	global proc

	# play text from the beginning
	if action == "start":
		lineTracker.value=0 

	# play or resume audio
	if proc == None or proc.is_alive() == False:
		proc = multiprocessing.Process(target=playAudio, args=(preppedTxt, maxLoops, lineTracker.value))
		proc.start()

		captions_thread = threading.Thread(target=findLine, args=(1.0,))
		captions_thread.start()


def playAudio(t, maxL, pos):
	tempVal = tts.fetchSettings()
	
	eng = pyttsx3.init()
	eng.setProperty('voice', tempVal[3])
	eng.setProperty('rate', tempVal[0])
	#eng.setProperty('volume', tempVal[1])
	eng.connect('started-utterance', onStart)
	
	# speak
	if pos <= maxL:
		
		for line in range(pos, maxL):
			if(line != ""):
				#print(t[line])
				eng.say(t[line], t[line])

	eng.runAndWait()


def exitApp():
	stopAudio()
	rm_children()
	window.destroy()
	quit()


def rm_children():
	for child in window.winfo_children():
		child.destroy()


'''		application visuals		'''

# draw the main menu
def drawMM(): 
	# prep the window
	rm_children();
	stopAudio()

	# Intro page/ start menu
	mm = window#tk.Frame(window)

	# Show image using label
	bgImg = tk.Label( mm, image = bg , bg="#ffffff").place(x = 0,y = 0)

	title = tk.Label(mm, text=" PY-Reader ", font=("Times",35,"bold italic underline"), bg="#ffffff")
	title.place(relx = 0.5, rely=0.1, anchor="center")

	subtitle = tk.Label(mm, text=" powered by tkinter & pyttsx3 ", font=("Times",12,"italic"), bg="#ffffff")
	subtitle.place(relx = 0.5, rely=0.175, anchor="center")

	start = tk.Button(mm, text="Begin", command = drawFileMenu, width = 10 )
	start.place(relx = 0.25, rely=0.775, anchor="center")

	settings = tk.Button(mm, text="Settings", command = drawSettingsMenu, width = 10 )
	settings.place(relx = 0.75, rely=0.775, anchor="center")

	exit = tk.Button(mm, text="Exit Application", command = drawExitPage, width = 10)
	exit.place(relx = 0.5, rely=0.925, anchor="center")

# Prompt to confirm before exiting application
def drawExitPage():
	response = tk.messagebox.askquestion("Exit application", "Are you sure?")
	if(response == "yes"):
		exitApp()

# draw the settings menu
def drawSettingsMenu(): 
	# prep the window
	rm_children();

	sm = window

	# Show image using label
	tk.Label( sm, image = settings_bg, bg="#ffffff").place(x = 0,y = 0)

	title = tk.Label(sm, text=" Settings ", font=("Times",25,"bold italic"), bg="#ffffff")
	title.place(relx = 0.5, rely=0.1, anchor="center")

	# Speech rate
	sr = tk.Label(sm, text="Speech Rate:", font=("Times", 18), bg="#ffffff")
	sr.place(relx = 0.15, rely=0.25, anchor="center")

	sScale = tk.Scale(sm, activebackground="blue", orient="horizontal", from_=75, to=225, width=20, length=300)
	sScale.place(relx = 0.3, rely=0.2)#, anchor="center")

	# Volume
	volTxt = tk.Label(sm, text="Volume:", font=("Times", 18), bg="#ffffff")
	volTxt.place(relx = 0.15, rely=0.4, anchor="center")

	vol = tk.Scale(sm, activebackground="blue", orient="horizontal", from_=0, to=100, width=20, length=300)
	vol.place(relx = 0.3, rely=0.35)

	# ------------------------------------------
	# Voices
	voiceTxt = tk.Label(sm, text="Voices:", font=("Times", 18), bg="#ffffff").place(relx = 0.15, rely=0.55, anchor="center")

	vFrame = tk.Frame(sm)
	vFrame.place(relx = 0.5, rely=0.6, anchor="center" )

	scrollbar = tk.Scrollbar(vFrame)
	scrollbar.pack( side = "right", fill = "y" )

	voiceOptions = tk.Listbox(vFrame, yscrollcommand=scrollbar.set, height = 5, font=("Times", 14))

	tv = tts.voicesList
	for v in tv:
   		voiceOptions.insert("end", v)

	voiceOptions.pack()#place(relx = 0.15, rely=0.5)
	scrollbar.config( command = voiceOptions.yview )
	# ------------------------------------------

	# Info button
	info = tk.Button(sm, image=infoIcon, text="Begin", command = drawInfoPage )
	info.place(relx = 0.925, rely=0.1, anchor="center")

	# Save Changes
	save = tk.Button(sm, text="Save Changes", command = lambda : saveSettings(sScale, vol, voiceOptions), width = 10)
	save.place(relx = 0.25, rely=0.9, anchor="center")

	# Return to main menu
	exit = tk.Button(sm, text="Main Menu", command = drawMM, width = 10)
	exit.place(relx = 0.75, rely=0.9, anchor="center")

	# update elements to match current settings
	tempVal = tts.fetchSettings()
	
	# set UI elements to match save data
	sScale.set(tempVal[0])
	vol.set(tempVal[1])
	voiceOptions.see(tempVal[2])
	voiceOptions.selection_set(tempVal[2])#activate(tempVal[2])


def drawInfoPage():
	ph = " Speech Rate: Control how fast words are spoken. (75-225).\n\n Volume: Set how loud the audio output should be. (0-100)\n\n Voices: Shows all currently available voices the application can use."
	tk.messagebox.showinfo("Info", ph)


def saveSettings(sr, vol, vo):
	# Change settings all at once
	if vo.curselection() != ():
		tts.updateSettings(int( sr.get()), vol.get(), vo.get(vo.curselection()), vo.curselection()[0] )
		tk.messagebox.showinfo("Saved", "A current settings have been saved.")
	else:
		tk.messagebox.showwarning("Missing Value", "A voice must be selected before changes can be saved.")
	

# draw the e-reader menu
def drawFileMenu():
	# prep the window
	rm_children();

	# Intro page/ start menu
	fm = window

	# Show image using label
	bgImg = tk.Label( fm, image = bg, bg = 'white')
	bgImg.place(x = 0,y = 0)


	title = tk.Label(fm, text="PY-Reader",font=("Times",25,"bold italic"),fg="black", bg="#ffffff" )
	title.place(relx = 0.5, rely=0.1, anchor="center")


	# browse button
	browseBut = tk.Button(fm, text="browse files", command = searchFiles)
	browseBut.place(relx = 0.15, rely=0.2, anchor="center")

	fileName = tk.Label(fm, textvariable = pathstr, width = 35, font=("Times",16), fg = "blue", bg="#ffffff")
	fileName.place(relx = 0.625, rely=0.2, anchor="center")
	
	# word count
	w = tk.Label(fm, textvariable=wordstr,font=("Times",16), bg="#ffffff" )
	w.place(relx = 0.15, rely=0.3, anchor="center")

	# line count
	l = tk.Label(fm, textvariable=linestr,font=("Times",16), bg="#ffffff" )
	l.place(relx = 0.45, rely=0.3, anchor="center")

	# previous line
	bwdBut = tk.Button(fm, text="<", command = lambda : changeLine(False), width=2)
	bwdBut.place(relx = 0.7, rely=0.3, anchor="center")

	# current line/sentence
	cl = tk.Label(fm, textvariable=curLine,font=("Times",16), bg="#ffffff")
	cl.place(relx = 0.775, rely=0.3, anchor="center")

	# next line
	fwdBut = tk.Button(fm, text=">", command = lambda : changeLine(True), width=2)
	fwdBut.place(relx = 0.85, rely=0.3, anchor="center")

	# subtitles 
	subtitles = tk.Message(fm, textvariable=captionstr,font=("Times",16," italic "), width=590, justify="left")
	subtitles.place(relx = 0.5, rely=0.5025, anchor="center")

	# buttons
	startBut = tk.Button(fm, text="Play", command = lambda : triggerThread("start"), width=10 )
	startBut.place(relx = 0.25, rely=0.825, anchor="center")	

	resumeBut = tk.Button(fm, text="Resume", command = lambda : triggerThread("resume"), width=10 )
	resumeBut.place(relx = 0.5, rely=0.825, anchor="center")	
	
	stopBut = tk.Button(fm, text="Stop", command = stopAudio, width=10 )
	stopBut.place(relx = 0.75, rely=0.825, anchor="center")	


	returnBut = tk.Button(fm, text="Return to menu", command = lambda: drawMM())
	returnBut.place(relx = 0.5, rely=0.925, anchor="center")


def searchFiles():
	global rawTxt, preppedTxt, maxLoops
	p = os.path.realpath("")

	filepath = filedialog.askopenfilename(initialdir = p,
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                          				("all files",
                                                        "*")))

	''' import text file here '''
	f = open(filepath, "r")
	
	pathstr.set(f.name.split("/")[-1])

	rawTxt = f.read()
	f.close()
	
	# update global values
	preppedTxt = rawTxt.split(".")

	#print( "pre-cleaning", len(preppedTxt))
	for l in preppedTxt:
		if l == '' or l=="":
			preppedTxt.remove(l)
	#print( "post-cleaning", len(preppedTxt))

	maxLoops = (len(preppedTxt)-1)
	if len(preppedTxt) == 1:
		maxLoops = 1
		#print("max loop: ", maxLoops)

	lineTracker.value = -1

	wordCount = "word count:  " + str(len(rawTxt.split()))
	lineCount = "line count:  " + str(maxLoops)

	wordstr.set(wordCount)
	linestr.set(lineCount)
	captionstr.set("A new text file has been loaded.")
	curLine.set(0)

	stopAudio()
	tts.prepAudio(rawTxt, pathstr.get().split(".")[0])




if __name__ == "__main__":
	#tts = TTS_Engine()

	#setup window
	window = tk.Tk()
	window.geometry("640x480")
	window.title("Py-Reader")
	window.configure(background = 'white')
	#window.resizable(False,False)
	window.protocol("WM_DELETE_WINDOW", drawExitPage)

	# Add image file
	icon = tk.PhotoImage(file = "img/background.png")
	window.iconphoto(False, icon )

	bg = tk.PhotoImage(file = "img/background.png")
	settings_bg = tk.PhotoImage(file = "img/settings.png")#gear-180.png")#settings.png")
	infoIcon = tk.PhotoImage(file = "img/info50x50.png")

	# Declaration of Tkinter variables
	pathstr = tk.StringVar()
	pathstr.set("___ File Explorer ___")

	wordstr = tk.StringVar()
	wordstr.set("word count: ??")

	linestr = tk.StringVar()
	linestr.set("line count: ??*")
	
	captionstr = tk.StringVar()
	captionstr.set("--- Select a text file to begin ---")

	curLine = tk.IntVar()

	drawMM()
	
	tts = TTS_Engine()

	window.mainloop()