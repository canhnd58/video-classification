import os
import sys
import subprocess

if __name__ == '__main__':
    if '--help' in sys.argv:
        print "Usage:\tpython %s ID_TEXT_PATH NUMBER_TO_RUN" % sys.argv[0]
        sys.exit(0)

    id_path = sys.argv[1]
    num = sys.argv[2]

    count = 0
    # Remove old image.csv file
    fo = open("csv/image.csv", 'w')
    fo.close()

    fi = open(id_path, 'r')
    contents = fi.readlines()

    for content in contents:
        if str(count) == num:
            break
        count += 1
        content = content[:-1]
        if not os.path.exists("videos/%s.avi" % content):
            print "videos/%s.avi not found! Continue... " % content
            continue
        command = "python src/process_image_csv.py videos/%s.avi" % content
        FNULL = open(os.devnull, 'w')
        print "%s: Processing %s" % (count, content)
        subprocess.call(command, shell=True, stdout=FNULL)
