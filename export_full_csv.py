import os
import csv
def export_csv(features,name,files):
	features = features[1:]
	line = ','.join([str(x) for x in features])
	line = line + ',' + name
	line += '\n'
	files.write(line)
def process():
	files = open("csv/test.csv" , "wb")

	for file in os.listdir("csv"):
		pre_name = str(file).split('_')[0]
		
		if file.endswith(".csv") and pre_name == 'id2games':
			with open('csv/%s' %file, 'rb') as f:
				reader = csv.reader(f)
				your_list = list(reader)
			if 'game' not in locals():
				game = your_list
			else:
				for num, value in enumerate(your_list):
					game[num] = game[num] + value[1:]
					# print l[num]
		if file.endswith(".csv") and pre_name == 'id2musics':
			with open('csv/%s' %file, 'rb') as f:
				reader = csv.reader(f)
				your_list = list(reader)
			if 'music' not in locals():
				music = your_list
			else:
				for num, value in enumerate(your_list):
					music[num] = music[num] + value[1:]
					# print l[num]
		if file.endswith(".csv") and pre_name == 'id2news':
			with open('csv/%s' %file, 'rb') as f:
				reader = csv.reader(f)
				your_list = list(reader)
			if 'new' not in locals():
				new = your_list
			else:
				for num, value in enumerate(your_list):
					new[num] = new[num] + value[1:]
					# print l[num]
		if file.endswith(".csv") and pre_name == 'id2sports':
			with open('csv/%s' %file, 'rb') as f:
				reader = csv.reader(f)
				your_list = list(reader)
			if 'sport' not in locals():
				sport = your_list
			else:
				for num, value in enumerate(your_list):
					sport[num] = sport[num] + value[1:]
					# print l[num]
	arr = []
	for num, value in enumerate(game[0]):
		arr.append(str(num))
	export_csv(arr,'label',files)
	for num, value in enumerate(game):
		export_csv(value,'game',files)
	for num, value in enumerate(music):
		export_csv(value,'music',files)
	for num, value in enumerate(sport):
		export_csv(value,'sport',files)
	for num, value in enumerate(new):
		export_csv(value,'new',files)


if __name__ == "__main__":
	process()

			



