import audio as au
import motion as mo
import extract_image_feature as im
import process_image_csv as pic
import download as dl
import os
import sys
import subprocess

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
		data_file = data[5:-4]
		audio_file = open("csv/%s_audio.csv" % data_file, "w")
		image_file = open("csv/%s_image.csv" % data_file, "w")
		image_file.close() # Close immediately to clear contents in file; file will be write in subprocess
		motion_file = open("csv/%s_motion.csv" % data_file, "w")
		contents = file.readlines()

		for content in contents:
			try:
				content = content[:-1]
				print_process('\r#%s %-30s:\tDownloading' %(count, content))
				path = dl.download(content)
				if path is None:
					print '#%s %-30s:\tDOWNLOAD FAIL' % (count, content)
					continue
				print_process('\r#%s %-30s:\tNormalizing' %(count, content))
				audio_path, video_path = dl.normalize(path)
				print_process('\r#%s %-30s:\tExtracting audio feature  ' %(count, content))
				audio_features = au.extractAudioFeatures(audio_path)

				print_process('\r#%s %-30s:\tExtracting motion feature ' %(count, content))
				motion_features = mo.motion(video_path)

				print_process('\r#%s %-30s:\tExtracting image feature  ' %(count, content))
				print_process('\r')
				# No longer use extract_image_feature
				# image_features = im.extract_image_feature(video_path)
				# Use subprocess to extracting image features
				command = "python src/process_image_csv.py videos/%s.avi csv/%s_image.csv" % (content, data_file)
				process_image_log = open("process_image.log", 'w')
				subprocess.call(command, shell=True, stdout=process_image_log, stderr=subprocess.STDOUT)

				print_process('\r#%s %-30s:\tExporting csv file' %(count, content))
				export_csv(audio_features,content,audio_file)
				export_csv(motion_features,content,motion_file)
				# export_csv(image_features,content,image_file)

				print_process('\r#%s %-30s:\tRemoving files' %(count, content))
				os.remove(video_path)
				os.remove(audio_path)

			except Exception:
				print '#%s %-30s:\tEXPORT FAIL' % (content, count)

			else:
				print '\r#%s %-30s:\tSUCCESS                               ' %(count, content)
				count +=1
				if str(count) == num:
					break

	finally:
		print_process('\rClosing file')
		file.close()
		# image_file.close()
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
