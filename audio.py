import pyaudio
import wave,os

"""
This class creates a recording session.

INPUT : N/A

OUTPUT : recorded file path

@author: asriva20
"""

DIRECTORY = ""


class RecordAudio:

    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.CHUNK = 1024
        self.RECORD_SECONDS = 5
        self.WAVE_OUTPUT_FILENAME = "file.wav"
        self._lock = 0

    @property
    def lock(self):
        return self._lock

    @lock.setter
    def lock(self, state):
        assert state is 0 or 1
        self._lock = state

    def record(self):
        audio = pyaudio.PyAudio()
        self._lock = 1
        # start Recording
        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS,
                            rate=self.RATE, input=True,
                            frames_per_buffer=self.CHUNK)
        print("recording...")
        frames = []

        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)
        print("finished recording")

        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()
        self._lock = 0

        waveFile = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

        return os.path.join(self.WAVE_OUTPUT_FILENAME)
