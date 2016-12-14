from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from contextlib import contextmanager
import sys
import os
import numpy as np
import extract_image_feature as im
import motion as mo
import audio as au
import download as dl
import model as md

MODEL = 'model/video_classification.pkl'
CSV = 'csv/combine_all.csv'

def print_error(text):
    print >> sys.stderr, '[ERROR] %s' % text
    sys.exit(1)

def print_info(text):
    print '[INFO] %s' % text

def print_help():
    print 'Usage:'
    print '\tpython %s [OPTIONS...] VIDEO_PATH' % sys.argv[0]
    print '\tpython %s [OPTIONS...] -y YOUTUBE_ID' % sys.argv[0]
    print 'Options:'
    template = "\t{0:5}{1:20}{2:20}"
    print template.format('-h', '--help', 'Show this help')
    print template.format('-y', '--youtube', 'Download video from youtube')
    print template.format('-v', '--verbose', 'Print more processing information')
    print template.format('-l', '--log', 'Store some debug information in log file')
    print template.format('-m', '--model [MODEL]', 'Predict using custom model')
    sys.exit(0)

def parse_argument(symbols, default=None):
    for symbol in symbols:
        try:
            index = sys.argv.index(symbol)
            value = True if default == False else sys.argv.pop(index + 1)
            del sys.argv[index]
            return value
        except:
            pass

    return default

@contextmanager
def stderr_redirector(stream):
    stderr = sys.stderr
    stderr_fd = stderr.fileno()
    with os.fdopen(os.dup(stderr_fd), 'wb') as copied:
        stderr.flush()
        os.dup2(stream.fileno(), stderr_fd)
        try:
            yield stderr
        finally:
            stderr.flush()
            os.dup2(copied.fileno(), stderr_fd)

def predict(arg, **kwargs):
    model_path = kwargs.pop('model', MODEL)
    csv_path = kwargs.pop('csv', CSV)
    verbose = kwargs.pop('verbose', False)
    log = kwargs.pop('log', False)
    youtube = kwargs.pop('youtube', False)

    log_file = 'predict.log' if log else os.devnull

    if verbose: print_info("Loading model from '%s'..." % model_path)
    try:
        with open(log_file, 'w') as f, stderr_redirector(f):
            clf = joblib.load(model_path)
    except IOError:
        print_error("Unable to open file '%s'" % model_path)
    except KeyError:
        if verbose:
            print_info('The model is incompatible with the system sklearn library')
            print_info("Rebuilding model from '%s'..." % csv_path)
        try:
            md.csv_to_model(csv_path, model_path)
            clf = joblib.load(model_path)
        except:
            print_error("Unable to rebuild model from '%s'" % csv_path)

    if verbose: print_info('Downloading...')
    if youtube:
        try:
            video_path = dl.download(arg)
        except Exception, e:
            print_error(str(e))
        if video_path is None:
            print_error('Cannot download video from YouTube')
    else:
        video_path = arg

    try:
        with open(log_file, 'a') as f, stderr_redirector(f):
            if verbose: print_info('Normalizing video...')
            audio, video = dl.normalize(video_path, remove=False, log=False)

            if verbose: print_info('Extracting motion features...')
            motion_f = mo.motion(video)

            if verbose: print_info('Extracting audio features...')
            audio_f = au.extractAudioFeatures(audio)

            if verbose: print_info('Extracting image features...')
            image_f = im.extract_image_feature(video)

        features = [np.array(list(motion_f) + list(audio_f) + list(image_f))]
        label = clf.predict(features)[0]

        if verbose: print_info('Removing temporary files...')
        os.unlink(video)
        os.unlink(audio)

        return label

    except Exception, e:
        print_error(str(e))


if __name__ == '__main__':
    need_help = parse_argument(['-h', '--help'], False)
    if need_help: print_help()

    model_path = parse_argument(['-m', '--model'], MODEL)
    verbose = parse_argument(['-v', '--verbose'], False)
    log = parse_argument(['-l', '--log'], False)
    youtube = parse_argument(['-y', '--youtube'], False)

    if len(sys.argv) != 2: print_help()

    video = sys.argv[1]
    print predict(video, model=model_path, verbose=verbose, log=log, youtube=youtube)

