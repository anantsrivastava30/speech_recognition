import speech_recognition as sr


m = None
for microphone_name in sr.Microphone.list_microphone_names():
    print(microphone_name)


with sr.AudioFile("file.wav") as source:    # open the audio file for reading
    pass