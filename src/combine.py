import audio as au
import motion as mo
import extract_image_feature as im
import download as dl
import os
import sys

NUM_VIDEO = 5

def export_csv(features,videoId,file):
	line = ','.join([str(x) for x in features])
	line = videoId + ',' + line
	line += '\n'
	file.write(line)

def print_process(text):
	print text,
	sys.stdout.flush()

def extract_feature(data, **kwargs):
	try:
		num = kwargs.pop('num_video', NUM_VIDEO)
		count = 0
		file = open(data,"r")
		audio_file = open("csv/audio.csv" , "w")
		image_file = open("csv/image.csv" , "w")
		motion_file = open("csv/motion.csv" , "w")
		contents = file.readlines()
	
		for content in contents:
			try:
				content = content[:-1]
				print_process('\r%-30s:\tDownloading' %(content,))
				path = dl.download(content)
				if path is None:
					print '%-30s:\tDOWNLOAD FAIL' % (content, )
					continue
				print_process('\r%-30s:\tNormalizing' %(content,))
				audio_path, video_path = dl.normalize(path)

				print_process('\r%-30s:\tExtracting audio feature  ' %(content,))
				audio_features = au.extractAudioFeatures(audio_path)

				print_process('\r%-30s:\tExtracting motion feature ' %(content,))
				motion_features = mo.motion(video_path)

				print_process('\r%-30s:\tExtracting image feature  ' %(content,))
				print_process('\r')
				image_features = im.extract_image_feature(video_path)

				print_process('\r%-30s:\tExporting csv file' %(content,))
				export_csv(audio_features,content,audio_file)
				export_csv(motion_features,content,motion_file)
				export_csv(image_features,content,image_file)
				
			except Exception:
				print '%-30s:\tEXPORT FAIL' % (content, )
			
			else:
				print '\r%-30s:\tSUCCESS                               ' % (content, )
				count +=1
				if str(count) == num:
					break
				
	finally:
		print_process('\rClosing file')
		file.close()
		image_file.close()
		motion_file.close()
		audio_file.close()

if __name__ == "__main__":
	if len(sys.argv) < 2:
		extract_feature('data/id2games.txt')
	elif len(sys.argv) == 2:
		video = sys.argv[1]
		extract_feature(video)
	else:
		video = sys.argv[1]
		num = sys.argv[2]
		extract_feature(video, num_video = num)
	





