import os
import csv
def export_csv(features,name,files):
	line = ','.join([str(x) for x in features])
	line = line + ',' + name
	line += '\n'
	files.write(line)
def del_id(file):
	with open(file, 'rb') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	l = your_list
	for num, value in enumerate(your_list):
		l[num] = value[1:]
	return l
def concat(a,b,c):
	for num, value in enumerate(a):
		a[num] = value + b[num] + c[num]
	return a
def process():
	files = open("csv/test.csv" , "wb")
	game_motion = del_id('csv/id2games_motion.csv')
	game_image = del_id('csv/id2games_image.csv')
	game_audio = del_id('csv/id2games_audio.csv')
	news_motion = del_id('csv/id2news_motion.csv')
	news_image = del_id('csv/id2news_image.csv')
	news_audio = del_id('csv/id2news_audio.csv')
	sport_motion = del_id('csv/id2sports_motion.csv')
	sport_image = del_id('csv/id2sports_image.csv')
	sport_audio = del_id('csv/id2sports_audio.csv')
	music_motion = del_id('csv/id2musics_motion.csv')
	music_image = del_id('csv/id2musics_image.csv')
	music_audio = del_id('csv/id2musics_audio.csv')
	
	l = game_motion
	l = concat(game_motion,game_audio,game_image)
	for num, value in enumerate(l):
		export_csv(l[num],'Game',files)
	
	l = game_motion
	l = concat(news_motion,news_audio,news_image)
	for num, value in enumerate(l):
		export_csv(l[num],'News',files)

	l = game_motion
	l = concat(sport_motion,sport_audio,sport_image)
	for num, value in enumerate(l):
		export_csv(l[num],'Sport',files)

	l = game_motion
	l = concat(music_motion,music_audio,music_image)
	for num, value in enumerate(l):
		export_csv(l[num],'Music',files)


	# for file in os.listdir("csv"):
	# 	pre_name = str(file).split('_')[0]
	# 	pos = str(file).split('_')[-1]
		
	# 	if file.endswith(".csv") and pre_name == 'id2games':
	# 		print pos
	# 		with open('csv/%s' %file, 'rb') as f:
	# 			reader = csv.reader(f)
	# 			your_list = list(reader)
	# 		if 'game' not in locals():
	# 			game = your_list
	# 		else:
	# 			for num, value in enumerate(your_list):
	# 				game[num] = game[num] + value[1:]
	# 				# print l[num]
	# 	if file.endswith(".csv") and pre_name == 'id2musics':
	# 		print file 
	# 		with open('csv/%s' %file, 'rb') as f:
	# 			reader = csv.reader(f)
	# 			your_list = list(reader)
	# 		if 'music' not in locals():
	# 			music = your_list
	# 		else:
	# 			for num, value in enumerate(your_list):
	# 				music[num] = music[num] + value[1:]
	# 				# print l[num]
	# 	if file.endswith(".csv") and pre_name == 'id2news':
	# 		# print file 
	# 		with open('csv/%s' %file, 'rb') as f:
	# 			reader = csv.reader(f)
	# 			your_list = list(reader)
	# 		if 'new' not in locals():
	# 			new = your_list
	# 		else:
	# 			for num, value in enumerate(your_list):
	# 				new[num] = new[num] + value[1:]
	# 				# print l[num]
	# 	if file.endswith(".csv") and pre_name == 'id2sports':
	# 		# print file 
	# 		with open('csv/%s' %file, 'rb') as f:
	# 			reader = csv.reader(f)
	# 			your_list = list(reader)
	# 		if 'sport' not in locals():
	# 			sport = your_list
	# 		else:
	# 			for num, value in enumerate(your_list):
	# 				sport[num] = sport[num] + value[1:]
	# 				# print l[num]
	# arr = []
	# for num, value in enumerate(game[0]):
	# 	arr.append(str(num))
	# export_csv(arr,'label',files)
	# for num, value in enumerate(game):
	# 	export_csv(value,'game',files)
	# for num, value in enumerate(music):
	# 	export_csv(value,'music',files)
	# for num, value in enumerate(sport):
	# 	export_csv(value,'sport',files)
	# for num, value in enumerate(new):
	# 	export_csv(value,'new',files)


if __name__ == "__main__":
	process()

			



