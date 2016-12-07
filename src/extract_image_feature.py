import numpy as np
import tensorflow as tf
import copy
import cv2
import os
from classify_image import *

# IMAGE_STEP = 360
TOTAL_IMAGE = 4

def split_video(video):
  vidcap = cv2.VideoCapture(video)
  total_frame = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
  fps = int(vidcap.get(cv2.CAP_PROP_FPS))

  for index in range(0, TOTAL_IMAGE):
    if index == 0:
      frame_no = fps * 2 - 1 # The frame in 2nd second
    else:
      frame_no = (total_frame / TOTAL_IMAGE) * index - 1
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    success, image = vidcap.read()
    cv2.imwrite("frame%d.jpg" % index, image)


def extract_image_feature(video):
  maybe_download_and_extract()
  split_video(video)

  image = ('frame0.jpg')
  feature = run_inference_on_image(image)

  for num in range(1,TOTAL_IMAGE):
    image = ('frame%d.jpg' %num)
    temp = run_inference_on_image(image)
    feature = np.vstack((feature, temp))

  feature = np.mean(feature,axis=0)
  for num in range(0, TOTAL_IMAGE):
  	os.system("rm " + 'frame%d.jpg' %num)
  return feature


if __name__ == '__main__':
  video = sys.argv[1]
  feature = extract_image_feature(video)
  print feature
