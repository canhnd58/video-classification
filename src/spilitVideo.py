import cv2
print(cv2.__version__)
vidcap = cv2.VideoCapture('Doit.mp4')
success,image = vidcap.read()
count = 0
success = True

while count < 300:
	success,image = vidcap.read()
	if count%30 == 0:
		temp = count/30 + 1
		cv2.imwrite("frame%d.jpg" % temp, image)     # save frame as JPEG file
	count += 1