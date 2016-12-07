import os
import subprocess

count = 0
for filename in os.listdir("videos"):
    if filename.endswith(".avi"):
        count += 1
        command = "python src/process_image_csv.py videos/%s" % filename
        FNULL = open(os.devnull, 'w')
        print "%s: Processing %s" % (count, filename)
        subprocess.call(command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
