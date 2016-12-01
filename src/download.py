import cv2
import os
import sys
import subprocess
from pytube import YouTube
from pytube.exceptions import DoesNotExist

URL = "https://youtu.be/"
ID = "wCkerYMffMo"
FILE_TYPE = 'mp4'
RESOLUTION = '360p'
SECONDS = 30
VIDEO_DIR = 'videos/'
FPS = 24
CODEC = 'x264'
WIDTH = 640
HEIGHT = 360

def download(ytid=ID, **kwargs):
    ftype = kwargs.pop('ftype', FILE_TYPE)
    reso = kwargs.pop('reso', RESOLUTION)
    vdir = kwargs.pop('vdir', VIDEO_DIR)

    yt = YouTube(URL+ytid)
    try:
        video = yt.get(ftype, reso)
    except DoesNotExist:
        return None

    yt.set_filename(ytid)
    video.download(vdir)
    return "%s%s.%s" % (vdir, ytid, ftype)

def normalize(path, **kwargs):
    fps = kwargs.pop('fps', FPS)
    reso = kwargs.pop('reso', (WIDTH, HEIGHT))
    seconds = kwargs.pop('sec', SECONDS)
    codec = kwargs.pop('codec', CODEC)

    audio_path = path[0:-4] + '.wav'
    command = "ffmpeg -i %s %s -y" % (path, audio_path)
    FNULL = open(os.devnull, 'w')
    subprocess.call(command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)

    cap = cv2.VideoCapture(path)
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out_path = path[0:-4] + '.30sec.mp4'
    out = cv2.VideoWriter(out_path, fourcc, fps, reso, True)

    frame_count = fps * seconds
    while(cap.isOpened()):
        if frame_count == 0: break
        frame_count -= 1

        ret, frame = cap.read()
        if ret:
            out.write(frame)

    cap.release()
    out.release()
    os.system('mv %s %s' % (out_path, path))

if __name__ == "__main__":
    if len(sys.argv) < 2 or '--help' in sys.argv:
        print "Usage:\tpython %s YOUTUBE_ID" % sys.argv[0]
        sys.exit(0)

    path = download(sys.argv[1])
    if path is not None:
        normalize(path)
        print '%100s:\tDONE' % (path, )
    else:
        print '%100s:\tSKIPPED' % (path, )

