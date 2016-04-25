import speech_recognition as sr
import webbrowser
from subprocess import *
import os
import pythonwifi
from pygame import *

file = 'file.wav'


class SpeechRecognition:

    def __init__(self):
        self.sphinx_test = None
        self.google_test = None
        self.wit_text = None
        self.api_text = None
        self.music = None

    def translate_from_voice(self):
        # obtain audio from the microphone
        r = sr.Recognizer()
        r.energy_threshold = 10

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(r.energy_threshold))

        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
        # recognize speech using Sphinx
        try:
            self.sphinx_text = r.recognize_sphinx(audio)
            print("Sphinx thinks you said " + self.sphinx_text)
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

        # recognize speech using Google Speech Recognition
        try:
            self.google_text = r.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + self.google_text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        WIT_AI_KEY = "UED7X6TWU4HRDVF3DAKYFPEK7JJIFRBO" # Wit.ai keys are 32-character uppercase alphanumeric strings
        try:
            self.wit_text = r.recognize_wit(audio, key=WIT_AI_KEY)
            print("Wit.ai thinks you said " + self.wit_text)
        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))

        # recognize speech using api.ai
        API_AI_CLIENT_ACCESS_TOKEN = "2486a77cb10e400c900856e77539647d " # api.ai keys are 32-character lowercase hexadecimal strings
        try:
            self.api_text = r.recognize_api(audio, client_access_token=API_AI_CLIENT_ACCESS_TOKEN)
            print("api.ai thinks you said " + self.api_text)
        except sr.UnknownValueError:
            print("api.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from api.ai service; {0}".format(e))

        return_text = self.sphinx_text
        if self.analyze_text(return_text) is False:
            return_text = self.google_text
            if self.analyze_text(return_text) is False:
                return_text = self.wit_text
                if self.analyze_text(return_text) is False:
                    return_text = self.api_text
                    self.analyze_text(return_text)

    def analyze_text(self,text):
        if 'music' in text:
            if 'on' in text:
                print('music on')
                # turnMusicOn()
                return True
            elif 'off' in text:
                print('music off')
                # turnMusicOff()
                return True

        if 'volume' in text:
            if 'up' in text:
                self.volume_up()
                return True
            elif 'down' in text:
                self.volume_down()
                return True

        if 'bluetooth' in text:
            if 'on' in text:
                print('bluetooth on')
                # turnBluetoothOn()
                return True
            elif 'off' in text:
                print('bluetooth off')
                # turnBluetoothOff()
                return True

        return False

    def playMuisc(self):
        self.music = Popen("vlc file", shell=True)

    def stopMusic(self):
        self.music.terminate()

    # volume up done
    def volume_up(self):
        call(["amixer", "-D", "pulse", "sset", "Master", "10%+"])
        return "vol_up" + getstatusoutput('amixer')[1].split(' ')[30]

    # volume down done
    def volume_down(self):
        call(["amixer", "-D", "pulse", "sset", "Master", "10%-"])
        return "vol_down" + getstatusoutput('amixer')[1].split(' ')[30]

    # open maps done
    def open_google_map(self):
        url = 'https://www.google.com/maps'
        print('start open:' + url)
        # Windows
        chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
        webbrowser.get(chrome_path).open(url)

    # close maps done
    def close_chrome(self):
        os.system('taskkill /im chrome.exe')

    # open browser done
    def open_browser(self):
        webbrowser.open("https://www.google.com")

    # search queries
    def search_browser(self, text):
        url = 'https://www.google.com//#q=' + text
        webbrowser.open_new_tab(url)

    # search
    def search_map(self, text):
        url = 'https://www.google.com/maps/search/' + text
        chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
        webbrowser.get(chrome_path).open(url)

    def bluetooth_on(self):
        pass

    def bluetooth_off(self):
        pass

    def wifi_on(self):
        pythonwifi

s = SpeechRecognition()
s.translate_from_voice()
    # open_google_map()
    # close_chrome()