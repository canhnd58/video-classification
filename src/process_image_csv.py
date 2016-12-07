import sys
import extract_image_feature as im

if __name__ == '__main__':
    video_path = sys.argv[1]
    fo = open("csv/image.csv", "a")
    image_features = im.extract_image_feature(video_path)
    line = ','.join([str(x) for x in image_features])
    line = video_path[7:-4] + ',' + line + '\n'
    fo.write(line)
    fo.close()
