import os
import subprocess
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import matplotlib.pyplot as plt

def extractAudioFeatures(videoPath):
    # Extract audio from video
    audioPath = "src/example-data/audio.wav"
    command = "ffmpeg -i %s %s -y" % (videoPath, audioPath)
    FNULL = open(os.devnull, 'w')
    subprocess.call(command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)

    # Extract features from audio file
    [Fs, x] = audioBasicIO.readAudioFile(audioPath)
    x = audioBasicIO.stereo2mono(x)
    print "Total size:", len(x)
    print "Frame size:", Fs
    mF, sF = audioFeatureExtraction.mtFeatureExtraction(x, Fs, len(x), len(x), Fs, Fs)
    print "Short-term features:"
    print "There're %s features can be extracted" % len(sF)
    print "There're %s number of frames that fit into the input audio" % len(sF[0])
    print "Mid-term features:"
    print mF
    return mF

VIDEO_PATH = "src/example-data/We-Dont-Talk-Anymore.mp4"
extractAudioFeatures(VIDEO_PATH)
