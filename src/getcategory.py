fi = open("data/id2label.txt", "rb")
fo_games = open("data/id2games.txt", "wb")
fo_musics = open("data/id2musics.txt", "wb")
fo_news = open("data/id2news.txt", "wb")
fo_sports = open("data/id2sports.txt", "wb")
contents = fi.readlines()
for content in contents:
    content = content[0:-1]
    video_id, category = content.split(',')
    if category == "/Games":
        fo_games.write("%s\n" % video_id)
    elif category == "/Musics":
        fo_musics.write("%s\n" % video_id)
    elif category == "/News":
        fo_news.write("%s\n" % video_id)
    elif category == "/Sports":
        fo_sports.write("%s\n" % video_id)
    else:
        continue
fo_games.close()
fo_musics.close()
fo_news.close()
fo_sports.close()
