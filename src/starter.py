import tensorflow as tf
import os

# current_path = os.getcwd()
current_path = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(current_path, "example-data/train-N.tfrecord")

for i, serialized_example in enumerate(tf.python_io.tf_record_iterator(input_file)):
    example = tf.train.Example()
    example.ParseFromString(serialized_example)
    feature = example.features.feature["video_id"].bytes_list.value
    labels = example.features.feature["labels"].int64_list.value
    print("#{} Feature = {}, Labels = {}".format(i, feature, labels))
