from gtts import gTTS 

import os 

fh = open("test.txt", "r")
myText = fh.read().replace("\n", " ")

language = 'en'

myobj = gTTS(text=myText, lang=language, slow=False) 

myobj.save("welcome.mp3") 

os.system("mpg321 welcome.mp3")
