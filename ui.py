import tkinter
#import cmu
import speech_recognition as sr
import webbrowser
import os
from subprocess import *

music = None
flag_music = False

root = tkinter.Tk()
commandText = tkinter.StringVar()
bluetoothText = tkinter.StringVar()
bluetoothText.set("Off")
airconditionText = tkinter.StringVar()
airconditionText.set("Off")
temperatureText = tkinter.IntVar()
temperatureText.set(22)
volumeText = tkinter.IntVar()
volumeText.set(getstatusoutput('amixer')[1].split(' ')[30])


def onclick():
    s = translate_from_voice()
    commandText.set(s)


def bluetooth_on():
    bluetoothText.set("On")


def bluetooth_off():
    bluetoothText.set("Off")


def aircondition_on():
    airconditionText.set("On")


def aircondition_off():
    airconditionText.set("Off")


# volume up done
def volume_up():
    call(["amixer", "-D", "pulse", "sset", "Master", "10%+"])
    volumeText.set(getstatusoutput('amixer')[1].split(' ')[30])
    return getstatusoutput('amixer')[1].split(' ')[30]


# volume down done
def volume_down():
    call(["amixer", "-D", "pulse", "sset", "Master", "10%-"])
    volumeText.set(getstatusoutput('amixer')[1].split(' ')[30])
    return getstatusoutput('amixer')[1].split(' ')[30]


def temperature_up():
    current = temperatureText.get()
    temperatureText.set(current + 1)


def temperature_down():
    current = temperatureText.get()
    temperatureText.set(current - 1)


def translate_from_voice():
    # obtain audio from the microphone
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))

    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        google_text = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + google_text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return_text = google_text
    analyze_text(return_text.lower())
    return return_text


def analyze_text(text):
    if 'music' in text:
        if 'on' in text:
            if not flag_music:
                flag_music = True
                playMuisc()
            else:
                return "Music already on"
            return True
        elif 'off' in text:
            if flag_music:
                flag_music = False
                stopMusic()
            else:
                return "Music already off"
            return True

    if 'volume' in text:
        if 'up' in text:
            volume_up()
            return True
        elif 'down' in text:
            volume_down()
            return True

    if 'temperature' in text:
        if 'up' in text:
            temperature_up()
            return True
        elif 'down' in text:
            temperature_down()
            return True

    if 'air' in text and 'condition' in text:
        if 'on' in text[-3:]:
            aircondition_on()
            return True
        elif 'off' in text[-3:]:
            aircondition_off()
            return True

    if 'bluetooth' in text:
        if 'on' in text:
            print('bluetooth on')
            bluetooth_on()
            return True
        elif 'off' in text:
            print('bluetooth off')
            bluetooth_off()
            return True
    if 'map' in text:
        open_google_map()
        return True

    if 'browser' in text:
        if 'open' in text:
            open_browser()
            return True
        if 'close' in text:
            close_chrome()
            return True

    if 'find' in text:
        search_map(text[5:])
        return True

    return False


def playMuisc():
    music = Popen("vlc file", shell=True)


def stopMusic():
    music.terminate()

    # open maps done
def open_google_map():
    url = 'https://www.google.com/maps'
    print('start open:' + url)
    chrome_path = "C/usr/bin/google-chrome-stable"
    webbrowser.get(chrome_path).open(url)


    # close maps done
def close_chrome():
    os.system('taskkill /im chrome.exe')


# open browser done
def open_browser():
    webbrowser.open("https://www.google.com")

    # search queries
def search_browser(text):
    url = 'https://www.google.com//#q=' + text
    webbrowser.open_new_tab(url)

    # search
def search_map(text):
    url = 'https://www.google.com/maps/search/' + text
    chrome_path = "/usr/bin/google-chrome-stable"
    webbrowser.open(url)


root.title("Speech Recognition")
ButtonInput = tkinter.Button(root, text="click to input command", command=onclick)
InputText = tkinter.Label(root, text="Command Input")

Commendhint = tkinter.Label(root, text="The Command is: ")
CommendShow = tkinter.Entry(root, textvariable=commandText)

VolumeShow = tkinter.Label(root, text="Current Volume is: ")
VolumeAmout = tkinter.Entry(root, textvariable=volumeText, width=5)

BlueToothText = tkinter.Label(root, text="BlueTooth")
BlueToothShow = tkinter.Entry(root, textvariable=bluetoothText, width=5)

AirConditionText = tkinter.Label(root, text="AirCondition")
AirConditionShow = tkinter.Entry(root, textvariable=airconditionText, width=5)

TemperatureText = tkinter.Label(root, text="Temperature")
TemperatureShow = tkinter.Entry(root, textvariable=temperatureText, width=5)


ButtonInput.grid(padx = 10, pady = 10, column = 0, row = 0)
InputText.grid(padx = 5, column = 1, row = 0)

Commendhint.grid(padx = 10, pady = 10, column = 0, row = 1)
CommendShow.grid(padx = 5, column = 1, row = 1)

VolumeShow.grid(padx = 5, pady = 5, column = 0, row = 2)
VolumeAmout.grid(column = 1, row = 2)

BlueToothText.grid(padx = 5, pady = 5, column = 0, row = 3)
BlueToothShow.grid(column = 1, row = 3)

AirConditionText.grid(padx = 5, pady = 5, column = 0, row = 4)
AirConditionShow.grid(column = 1, row = 4)

TemperatureText.grid(padx = 5, pady = 5, column = 0, row = 5)
TemperatureShow.grid(column = 1, row = 5)

root.mainloop()