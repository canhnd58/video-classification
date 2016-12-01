import os
import sys
import subprocess
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import matplotlib.pyplot as plt

def extractAudioFeatures(videoPath):
    # Extract audio from video
    AUDIO_PATH = "videos/audio.wav"
    command = "ffmpeg -i %s %s -y" % (videoPath, AUDIO_PATH)
    FNULL = open(os.devnull, 'w')
    subprocess.call(command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)

    # Extract features from audio file
    [Fs, x] = audioBasicIO.readAudioFile(AUDIO_PATH)
    x = audioBasicIO.stereo2mono(x)
    # print "Total size:", len(x)
    # print "Frame size:", Fs
    mF, sF = audioFeatureExtraction.mtFeatureExtraction(x, Fs, len(x), len(x), Fs, Fs)
    return mF

if __name__ == "__main__":
    if '--help' in sys.argv:
        print "Usage:\tpython %s VIDEO_PATH" % sys.argv[0]
        sys.exit(0)

    VIDEO_PATH = "videos/We-Dont-Talk-Anymore.mp4"
    video = VIDEO_PATH if len(sys.argv) < 2 else sys.argv[1]
    mF = extractAudioFeatures(video)
    print "Mid-term features:"
    print mF
