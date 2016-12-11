from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
import numpy as np

def csv_to_model(csv_path = 'csv/combine_all.csv', model_path = 'model/video_classification.pkl'):
    fi = open(csv_path, 'r')

    samples = fi.readlines()
    n_samples = list()
    n_features = list()
    for index, sample in enumerate(samples):
        if index == 0:
            continue
        sample = sample[:-1]
        # Order of features in csv: Motion[4] -> Audio[68] -> Image[1008] -> Label[1] (1080 features + 1 label)
        sample = sample.split(',')
        n_samples.append(sample[0:-1])
        n_features.append(sample[-1])

    clf = RandomForestClassifier()
    clf = clf.fit(n_samples, n_features)

    joblib.dump(clf, model_path)

if __name__ == '__main__':
    csv_to_model()
