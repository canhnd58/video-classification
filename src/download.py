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
CODEC = 'XVID'
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
        os.system('rm %s' % (filepath, ))
    return filepath

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
    cv2_version = cv2.__version__[0]

    if cv2_version == '3':
        fourcc = cv2.VideoWriter_fourcc(*codec)
    elif cv2_version == '2':
        fourcc = cv2.cv.CV_FOURCC(*codec)
    else:
        raise Exception('Unsupported opencv version!')

    out_path = path[0:-4] + '.avi'
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
    os.unlink(path)
    return (audio_path, out_path)

if __name__ == "__main__":
    if len(sys.argv) < 2 or '--help' in sys.argv:
        print "Usage:\tpython %s YOUTUBE_ID" % sys.argv[0]
        sys.exit(0)

    path = download(sys.argv[1])
    if path is not None:
        normalize(path)
        print '%-30s:\tDONE' % (path, )
    else:
        print '%-30s:\tSKIPPED' % (path, )
