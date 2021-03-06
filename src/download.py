import cv2
import sys
import os
import os.path
import subprocess
from sys import platform
from pytube import YouTube
from pytube.exceptions import DoesNotExist

URL = "https://youtu.be/"
ID = "wCkerYMffMo"
FILE_TYPE = 'mp4'
RESOLUTION = '360p'
SECONDS = 30
FPS = 24
VIDEO_DIR = 'videos/'
LINUX_CODEC = 'XVID'
MAC_CODEC = 'mp4v'
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
    filepath = "%s%s.%s" % (vdir, ytid, ftype)
    try:
        video.download(vdir)
    except OSError:
        os.unlink(filepath)
        video.download(vdir)
    return filepath

def normalize(path, **kwargs):
    reso = kwargs.pop('reso', (WIDTH, HEIGHT))
    seconds = kwargs.pop('sec', SECONDS)
    fps = kwargs.pop('fps', FPS)
    remove = kwargs.pop('remove', True)
    log = kwargs.pop('log', True)

    if platform == "linux" or platform == "linux2":
        codec = LINUX_CODEC
    elif platform == "darwin":
        codec = MAC_CODEC
    else:
        raise Exception("Unsupported Platform")

    codec = kwargs.pop('codec', codec)

    if not os.path.isfile(path):
        raise Exception('%s not found!' % (path, ))

    audio_path = path[0:-4] + '.tmp.wav'
    command = "ffmpeg -i %s %s -y" % (path, audio_path)
    download_log = open("download.log", 'w') if log else None
    subprocess.call(command, shell=True, stdout=download_log, stderr=subprocess.STDOUT)

    cap = cv2.VideoCapture(path)
    cv2_version = cv2.__version__[0]

    if cv2_version == '3':
        fourcc = cv2.VideoWriter_fourcc(*codec)
    elif cv2_version == '2':
        fourcc = cv2.cv.CV_FOURCC(*codec)
    else:
        raise Exception('Unsupported OpenCV version!')

    out_path = path[0:-4] + '.tmp.avi'
    out = cv2.VideoWriter(out_path, fourcc, fps, reso, True)

    frame_count = fps * seconds
    while(cap.isOpened()):
        if frame_count <= 0: break
        frame_count -= 1
        ret, frame = cap.read()

        if not ret: continue
        resized = cv2.resize(frame, reso)
        out.write(resized)

    cap.release()
    out.release()
    if remove: os.unlink(path)

    return (audio_path, out_path)

if __name__ == "__main__":
    if len(sys.argv) < 2 or '--help' in sys.argv:
        print "Usage:\tpython %s YOUTUBE_ID" % sys.argv[0]
        sys.exit(0)

    ytid = sys.argv[1]
    remove = '--keep-origin' not in sys.argv

    path = VIDEO_DIR + ytid + '.mp4'
    if '--only-normalize' not in sys.argv:
        path = download(ytid)

    if path is None:
        print '%-30s:\tSKIPPED' % (ytid, )

    if '--only-download' not in sys.argv:
        normalize(path, remove=remove)

    print '%-30s:\tDONE' % (ytid, )
