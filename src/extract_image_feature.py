import numpy as np
import tensorflow as tf
import copy
import cv2
from classify_image import*

IMAGE_STEP = 30
TOTAL_IMAGE = 10

def split_video():
  vidcap = cv2.VideoCapture('../videos/Doit.mp4')
  count = 0
  while count < IMAGE_STEP*TOTAL_IMAGE:
    success,image = vidcap.read()
    if count%IMAGE_STEP == 0:
      temp = count/IMAGE_STEP + 1
      cv2.imwrite("frame%d.jpg" % temp, image)     # save frame as JPEG file
    count += 1

def extract_image_feature():
  maybe_download_and_extract()
  split_video()

  image = ('frame1.jpg')
  feature = run_inference_on_image(image)
  
  for num in range(2,TOTAL_IMAGE):
    image = ('frame%d.jpg' %num)
    temp = run_inference_on_image(image)
    feature = np.vstack((feature, temp))
  node_lookup = NodeLookup()
  feature = np.mean(feature,axis=0)
  return feature


def main():
  print(extract_image_feature())

if __name__ == '__main__':
  main()
