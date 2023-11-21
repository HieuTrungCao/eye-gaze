import os
import playsound
import wikipedia
from webdriver_manager.chrome import ChromeDriverManager
from gtts import gTTS

wikipedia.set_lang('vi')
language = 'vi'
path = ChromeDriverManager().install()

def speak(text):
    print("Bot: {}".format(text))
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("sound.mp3")
    playsound.playsound("sound.mp3", False)
    os.remove("sound.mp3")

# speak("Tôi là cao trung hiếu")