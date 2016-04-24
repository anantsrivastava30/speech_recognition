#!/usr/bin/env python
from os import path
from audio import RecordAudio

from pocketsphinx.pocketsphinx import *


"""
This class is a speech to text kernel.

INPUT : N/A

OUTPUT : N/A

@author: asriva20
"""


MODELDIR = "pocketsphinx/model"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
decoder = Decoder(config)

# Read from microphone
recording = RecordAudio().record()
stream = open("out.wav", 'rb')

# Process audio chunk by chunk. On keyword detected perform action and restart search
decoder = Decoder(config)

# Decode streaming data.
decoder = Decoder(config)
decoder.start_utt()
while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
    else:
        break
decoder.end_utt()
hypothesis = decoder.hyp()
print ('Best hypothesis: ', hypothesis.hypstr, " model score: ", hypothesis.best_score, " confidence: ", hypothesis.prob)
print ('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])
