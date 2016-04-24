import speech_recognition as sr
import webbrowser
import os


def translate_from_voice():

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
        sphinx_text = r.recognize_sphinx(audio)
        print("Sphinx thinks you said " + sphinx_text)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

    # recognize speech using Google Speech Recognition
    try:
        google_text = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + google_text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    WIT_AI_KEY = "UED7X6TWU4HRDVF3DAKYFPEK7JJIFRBO" # Wit.ai keys are 32-character uppercase alphanumeric strings
    try:
        wit_text = r.recognize_wit(audio, key=WIT_AI_KEY)
        print("Wit.ai thinks you said " + wit_text)
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))

    # recognize speech using api.ai
    API_AI_CLIENT_ACCESS_TOKEN = "2486a77cb10e400c900856e77539647d " # api.ai keys are 32-character lowercase hexadecimal strings
    try:
        api_text = r.recognize_api(audio, client_access_token=API_AI_CLIENT_ACCESS_TOKEN)
        print("api.ai thinks you said " + api_text)
    except sr.UnknownValueError:
        print("api.ai could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from api.ai service; {0}".format(e))

    return_text = sphinx_text
    if analyze_text(return_text) == False:
        return_text = google_text
        if analyze_text(return_text) == False:
            return_text = wit_text
            if analyze_text(return_text) == False:
                return_text = api_text
                analyze_text(return_text)


def analyze_text(text):
    if 'music' in text:
        if 'on' in text:
            print 'music on'
            # turnMusicOn()
            return True
        elif 'off' in text:
            print 'music off'
            # turnMusicOff()
            return True
    if 'volume' in text:
        if 'up' in text:
            print 'volume on'
            return True
            # turnVolumeUp()
            return True
        elif 'down' in text:
            print 'volume off'
            # turnVolumeDown()
            return True
    if 'bluetooth' in text:
        if 'on' in text:
            print 'bluetooth on'
            # turnBluetoothOn()
            return True
        elif 'off' in text:
            print 'bluetooth off'
            # turnBluetoothOff()
            return True
    if 'map' in text:
        open_google_map()
        return True

    if 'browser' in text:
        if 'close' in text:
            close_chrome()
            return True
    if 'search' in text:
        search_map(text[7:])
        return True

    return False


def open_google_map():
    url = 'https://www.google.com/maps'
    print 'start open:' + url
    # Windows
    chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    webbrowser.get(chrome_path).open(url)


def close_chrome():
    os.system('taskkill /im chrome.exe')


def search_map(text):
    url = 'https://www.google.com/maps/search/' + text
    chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    webbrowser.get(chrome_path).open(url)


translate_from_voice()
# open_google_map()
# close_chrome()
