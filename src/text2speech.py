import pyttsx3

class Speak:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.setvoice()
        
    def setvoice(self):
        id = 0
        voices = self.engine.getProperty("voices")
        for voice in voices:
            if "an" in voice.name.lower():
                break
            else:
                id += 1

        self.engine.setProperty("voice", voices[id].id)
        self.engine.setProperty('rate', 100)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()