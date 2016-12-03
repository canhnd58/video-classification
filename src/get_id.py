import os
import csv
import sys
import numpy
import tensorflow as tf

GAMES_CATEGORY = "/Games"
MUSICS_CATEGORY = "/Musics"
NEWS_CATEGORY = "/News"
SPORTS_CATEGORY = "/Sports"
CATEGORIES = [GAMES_CATEGORY, MUSICS_CATEGORY, NEWS_CATEGORY, SPORTS_CATEGORY]

def id2label(train_tfrecord_path, csv_filename, output_filename):
    # Open output file
    fo = open("%s/%s" % (train_tfrecord_path, output_filename), "wb")
    # Loop in tfrecord file
    for filename in os.listdir(train_tfrecord_path):
        if filename.endswith(".tfrecord"):
            filepath = "%s/%s" % (train_tfrecord_path, filename)
            for serialized_record in tf.python_io.tf_record_iterator(filepath):
                record = tf.train.Example()
                record.ParseFromString(serialized_record)
                video_id = record.features.feature["video_id"].bytes_list.value[0]
                if video_id.endswith("!"): # Video has been deleted by user
                    continue
                labels = record.features.feature["labels"].int64_list.value
                count = 0
                isCheck = [0, 0, 0, 0]
                category = ""
                with open("%s/%s" % (train_tfrecord_path, csv_filename), "rb") as csvFile:
                    reader = csv.reader(csvFile)
                    for row in reader:
                        if count == 2:
                            break
                        label = int(row[2])
                        if label in labels:
                            index = CATEGORIES.index(row[4])
                            if not isCheck[index]:
                                if not count:
                                    count += 1
                                    isCheck[index] = True
                                    category += row[4]
                                else:
                                    continue
                if count == 1:
                    fo.write("%s,%s\n" % (video_id, category))
    # Close output file
    fo.close()

if __name__ == "__main__":
    if '--help' in sys.argv:
        print "Usage:\tpython %s TRAIN_TFRECORD_PATH CSV_FILENAME OUTPUT_FILENAME" % sys.argv[0]
        sys.exit(0)
    TRAIN_TFRECORD_PATH = "trainrecord"
    CSV_FILENAME = "labels-histogram.csv"
    OUTPUT_FILENAME = "id2label.txt"
    train_tfrecord_path = TRAIN_TFRECORD_PATH if len(sys.argv) < 2 else sys.argv[1]
    csv_filename = CSV_FILENAME if len(sys.argv) < 3 else sys.argv[2]
    output_filename = OUTPUT_FILENAME if len(sys.argv) < 4 else sys.argv[2]
    id2label(train_tfrecord_path, csv_filename, output_filename)
