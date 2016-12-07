import os
import sys
import extract_image_feature as im

if __name__ == '__main__':
    video_path = sys.argv[1]
    csv_path = sys.argv[2]
    if not os.path.exists(video_path):
        raise Exception('File not found!')
    fo = open(csv_path, "a")
    image_features = im.extract_image_feature(video_path)
    line = ','.join([str(x) for x in image_features])
    line = video_path[7:-4] + ',' + line + '\n'
    fo.write(line)
    fo.close()
