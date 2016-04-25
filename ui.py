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
gray88toothText = tkinter.StringVar()
gray88toothText.set("Off")
airconditionText = tkinter.StringVar()
airconditionText.set("Off")
temperatureText = tkinter.IntVar()
temperatureText.set(22)
volumeText = tkinter.IntVar()
volumeText.set(getstatusoutput('amixer')[1].split(' ')[30])


def onclick():
    s = translate_from_voice()
    commandText.set(s)


def gray88tooth_on():
    gray88toothText.set("On")


def gray88tooth_off():
    gray88toothText.set("Off")


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

    if 'gray88tooth' in text:
        if 'on' in text:
            print('gray88tooth on')
            gray88tooth_on()
            return True
        elif 'off' in text:
            print('gray88tooth off')
            gray88tooth_off()
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
root.focus_set()
root.configure(background='floralwhite')
root.geometry('750x750+750+750')
root.frame()
ButtonInput_Image = tkinter.PhotoImage(file = "microphone.gif")
ButtonInput = tkinter.Button(root, text=" Speak Now ", command=onclick, fg = "black", bg = "gray88", relief='raised', font=("Sans sarif", 16), image = ButtonInput_Image)
#InputText = tkinter.Label(root, text="Command Input", relief = 'raised', bg = 'gray88', fg = 'black', font=("Sans sarif", 16))

Commendhint = tkinter.Label(root, text=" You Said ", relief = 'raised', bg = 'gray88', fg = 'black', font=("Sans sarif", 16))
CommendShow = tkinter.Entry(root, textvariable=commandText, relief = 'raised', bg = 'gray88', fg = 'black', font=("Sans sarif", 16))

VolumeShow = tkinter.Label(root, text=" Volume ", relief = 'raised', bg = 'gray88', fg = 'black', font=("Sans sarif", 16))
VolumeAmout = tkinter.Entry(root, textvariable=volumeText, width=5, relief = 'raised', bg = 'gray88', fg = 'black', font=("Sans sarif", 16))

BlueToothText = tkinter.Label(root, text=" Bluetooth ", relief = 'raised', bg = 'gray88', fg = 'black', font=("Sans sarif", 16))
BlueToothShow = tkinter.Entry(root, textvariable=gray88toothText, width=5, relief = 'raised', bg = 'gray88', fg = 'black', font=("Sans sarif", 16))

AirConditionText = tkinter.Label(root, text=" Air Condition ", relief = 'raised', bg = 'gray88', fg = 'black', font=("Sans sarif", 16))
AirConditionShow = tkinter.Entry(root, textvariable=airconditionText, width=5, relief = 'raised', bg = 'gray88', fg = 'black', font=("Sans sarif", 16))

TemperatureText = tkinter.Label(root, text=" Temperature ", relief = 'raised', bg = 'gray88', fg = 'black', font=("Sans sarif", 16))
TemperatureShow = tkinter.Entry(root, textvariable=temperatureText, width=5, relief = 'raised', bg = 'gray88', fg = 'black', font=("Sans sarif", 16))

ButtonInput.place( x = 300, y = 100)
# ButtonInput.grid(padx = 10, pady = 10, column = 500, row = 200)
#InputText.grid(padx = 5, column = 1, row = 0)

Commendhint.place( x = 200, y = 300)
CommendShow.place( x = 350, y = 300)

VolumeShow.place( x = 100, y = 500)
VolumeAmout.place( x = 200, y = 500)

BlueToothText.place( x = 350, y = 500)
BlueToothShow.place(x = 500, y = 500)

AirConditionText.place( x = 50, y = 600)
AirConditionShow.place(x = 200, y = 600)

TemperatureText.place( x = 350, y = 600)
TemperatureShow.place(x = 500, y = 600)


root.mainloop()
