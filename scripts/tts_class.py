import pyttsx3
import threading
import multiprocessing
from multiprocessing import  Queue

class TTS_Engine:
	# engine variables
	sRate = 115
	volume = 1.0

	# tracking variables
	lineCount = 0
	rawText = ""
	rdyText = ""
	voicesList = []
	curVoiceName = "default"
	curVoiceIndex = 0

	isReading = False
	fileName = "null"

	

	def __init__(self):

		# load the list of available voices
		if self.voicesList == []:
			q = Queue()

			v_thread = multiprocessing.Process(target=self.listVoices, args=(q,) )
			v_thread.start()
			v_thread.join()

			self.voicesList = q.get()


		# load app settings (if available)
		file_found = False

		try:
			sf = open("app_settings.txt", "x")
		except:
			#print("file exists!")
			file_found = True
		else:
			#print("no file found, continue init process")
			pass	
	

		if(file_found):
			sf = open("app_settings.txt", "r")
			#fData=sf.readlines()
			fData = sf.read().split(",")
			sf.close()
			#print("file Data: --> ", fData)
			
			self.sRate = int(fData[0])
			self.volume = (float(fData[1]) * 0.01) # form 1-100 -> 0.0-1.0 
			self.curVoiceName = fData[2]
			self.curVoiceIndex = int(fData[3])

		else: # no file found, create one via update function
			self.updateSettings(self.sRate, 100, self.curVoiceName, self.curVoiceIndex)
	
		

	#[future builds should have the option to read by sentence or by line]
	def prepAudio(self, rawTxt, item):
		self.rawText = rawTxt
		self.fileName = item

		# split raw text into an array of sentences
		self.lineCount = 0
		self.rdyText = self.rawText.split(".")

	def initVals(self, captionVar):
		self.caption = captionVar

	def listVoices(self, q):
		if self.voicesList == []:
			tmpL = []

			v = pyttsx3.init().getProperty('voices')
			for x in v:
				tmpL.append(x.id)

			q.put(tmpL)
			del v

		return self.voicesList

	def updateSettings(self, sr, vol, voc, vocID):
		self.sRate = sr
		self.volume = (vol * 0.01)
		self.curVoiceName = voc
		self.curVoiceIndex = vocID
		
		# save settings to a txt file
		prepStr = str(sr) + "," + str(vol) + "," + voc + "," + str(vocID)
		savefile = open("app_settings.txt", "w")
		savefile.write(prepStr)
		savefile.close()


	def fetchSettings(self): 
		vals = []
		vals.append(self.sRate)
		vals.append( int(self.volume * 100) ) #scale from 0.0-1.0 --> 0-100
		vals.append(self.curVoiceIndex)
		vals.append(self.curVoiceName)
		return vals

		

if __name__ == '__main__':
	print("main process active...")
	# load and test the class
	#eng = TTS_Engine()