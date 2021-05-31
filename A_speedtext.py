import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import time
import keyboard
import multiprocessing
#from pydub import AudioSegment


class speedtext:

    language = 'vi'

    def countdown(self, t):    
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
        print("Tôi: ")


    def speak(self, text):
        print("Bot nhân viên: {}".format(text))
        tts = gTTS(text=text, lang= self.language, slow=False)
        tts.save("sound.mp3")
        playsound.playsound("sound.mp3", False)

        #sound = AudioSegment.from_file(file="sound.mp3",format="mp3")
        #fast_sound = self.speed_change(sound, 2.0)
        os.remove("sound.mp3")

    def get_audio(self):
        r = sr.Recognizer()
        with sr.Microphone() as mic:
            r.adjust_for_ambient_noise(mic)
            audio = r.record(mic, duration= 3)
            try:
                text = r.recognize_google(audio, language="vi-VN")
                print(text)
                return text
            except:
                print("...")
                return 0

    def stop(self):
        self.speak("Hẹn gặp lại quý khách!")
        time.sleep(2)

    def get_text(self):
        for i in range(3):
            print("Nhấn Space để bắt đầu nói: ")
            keyboard.wait('Space')
            self.countdown(int(2))
            text = self.get_audio()
            if text:
                #self.speak(text)
                return text.lower()
            elif i < 2:
                self.speak("Mình không nghe rõ. Bạn nói lại đi!")
                time.sleep(2)
        self.stop()
        return 0

