import os
import sys
import subprocess
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import matplotlib.pyplot as plt

def extractAudioFeatures(audioPath):
    # Extract features from audio file
    [Fs, x] = audioBasicIO.readAudioFile(audioPath)
    x = audioBasicIO.stereo2mono(x)
    mF, sF = audioFeatureExtraction.mtFeatureExtraction(x, Fs, len(x), len(x), Fs, Fs)
    res = list()
    for item in mF:
        res.append(item[0])
    return res

if __name__ == "__main__":
    if '--help' in sys.argv:
        print "Usage:\tpython %s AUDIO_PATH" % sys.argv[0]
        sys.exit(0)

    AUDIO_PATH = "videos/We-Dont-Talk-Anymore.wav"
    audio = AUDIO_PATH if len(sys.argv) < 2 else sys.argv[1]
    mF = extractAudioFeatures(audio)
    print "Mid-term features:"
    print mF
