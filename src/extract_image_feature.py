import numpy as np
import tensorflow as tf
import copy
import cv2
import os
from classify_image import*

IMAGE_STEP = 30
TOTAL_IMAGE = 2

def split_video(video):
  vidcap = cv2.VideoCapture(video)
  count = 0
  while count < IMAGE_STEP*TOTAL_IMAGE:
    success,image = vidcap.read()
    if count%IMAGE_STEP == 0:
      temp = count/IMAGE_STEP
      cv2.imwrite("frame%d.jpg" % temp, image)     # save frame as JPEG file
    count += 1

def extract_image_feature(video):
  maybe_download_and_extract()
  split_video(video)

  image = ('frame0.jpg')
  feature = run_inference_on_image(image)
  
  for num in range(1,TOTAL_IMAGE):
    image = ('frame%d.jpg' %num)
    temp = run_inference_on_image(image)
    feature = np.vstack((feature, temp))
  node_lookup = NodeLookup()
  feature = np.mean(feature,axis=0)
  for num in range(0, TOTAL_IMAGE):
  	os.system("rm " + 'frame%d.jpg' %num)
  return feature


if __name__ == '__main__':
  video = sys.argv[1]
  feature = extract_image_feature(video)
  print feature
