import numpy as np
import cv2
import sys

VIDEO = 'videos/video1.mp4'
DURATION = 10
THRESHOLD = 32
MC_MAX = 10

def motion(video=VIDEO, **kwargs):
    duration = kwargs.pop('duration', DURATION)
    threshold = kwargs.pop('threshold', THRESHOLD)
    debug = kwargs.pop('debug', False)

    cap = cv2.VideoCapture(video)
    prev = None
    timestamp = 0

    # fgbg = cv2.createBackgroundSubtractorMOG2()

    # Initialize motion coefficient array
    mc_array = np.array([])
    large_mc_array = np.array([])
    zero_mc = 0

    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret: break

        # Convert to grayscale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Skip the first frame
        if prev is None:
            prev = frame
            mhi = np.zeros(frame.shape, np.float32)
            continue

        # Update motion history
        diff = cv2.absdiff(frame, prev)
        # diff = fgbg.apply(frame)
        ret, fg = cv2.threshold(diff, threshold, 1, cv2.THRESH_BINARY)
        timestamp += 1
        mhi[fg!=0] = timestamp
        mhi[np.all([fg==0, mhi<(timestamp-duration)], axis=0)] = 0

        # Normalize motion history
        n_mhi = np.clip((mhi - (timestamp - duration)) / duration, 0, 1)
        mc = 0 if (np.all(fg==0)) else (np.sum(n_mhi) / np.sum(fg))

        if mc > MC_MAX:
            large_mc_array = np.append(large_mc_array, mc)
        elif mc == 0:
            zero_mc += 1
        else:
            mc_array = np.append(mc_array, mc)

        prev = frame
        if debug:
            cv2.imshow('frame', frame)
            cv2.imshow('foreground', fg*255)
            cv2.imshow('mhi', np.uint8(n_mhi*255))
            print mc
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

    if len(mc_array) == 0:
        return (0, 0, zero_mc, len(large_mc_array))
    # (MC Mean, MC Standard Deviation, Num of Zero MC, Num of Large MC)
    return (np.mean(mc_array), np.std(mc_array), zero_mc, len(large_mc_array))

if __name__ == '__main__':
    if len(sys.argv) < 2 or '--help' in sys.argv:
        print "Usage:\tpython %s VIDEO_PATH [--debug]" % sys.argv[0]
        sys.exit(0)

    video = sys.argv[1]
    debug = '--debug' in sys.argv

    mean, std, zero, large = motion(video, debug=debug)
    print "Motion Coefficient"
    print "Mean\tStd\t=0\t>%d" % MC_MAX
    print "%.2f\t%.2f\t%d\t%d" % (mean, std, zero, large)
