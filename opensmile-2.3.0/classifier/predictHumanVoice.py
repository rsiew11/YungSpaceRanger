import argparse
import os
import humanVoiceClassifier

global human_voice_clf
human_voice_clf = humanVoiceClassifier.human_voice_clf

# return a matrix that can be passed into the classifier
def matrix_from_csv( single_output ):
    matrix = []
    avg_dict, coeff_header = humanVoiceClassifier.compute_avg_coeffs(single_output)
    for coeff in coeff_header:
        if "pcm" not in coeff:
            continue
        matrix.append(float(avg_dict[coeff]))
    return [matrix[0:26]]



# function that creates a classifier and tests on a sample
def classify( single_output ):
    global human_voice_clf
    if (human_voice_clf is None):
        print "Classifier has not been trained! Please run the trainHumanVoiceClassifier script on training data to train"
        human_voice_clf = humanVoiceClassifier.create_classifier(training_folder, target_file)
    clf = human_voice_clf

    matrix = matrix_from_csv(single_output)
    #print clf.score(matrix)
    #x_test=vectorizer.fit_transform(matrix)
    print matrix
    print clf.predict(matrix)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
            'Detect if a given 1 second WAV file contains a human voice.')
    parser.add_argument('--wav_file', '-w', action="store",
                        dest="predict_file", type=str,
                        help="Wave file to predict as human voice or not")

    parser.add_argument('--training_data', '-d', action="store",
                        dest="training_folder", type=str,
                        help="Folder containing data to train classifier")
    parser.add_argument('--target_values', '-t', action="store",
                        dest="target_file", type=str,
                        help="CSV file containing wav file mapped to target value")

    args = parser.parse_args()

    # need absolute paths to files and folders
    training_folder = os.path.abspath(args.training_folder)
    target_file = os.path.abspath(args.target_file)
    predict_file = os.path.abspath(args.predict_file)
    classify( predict_file )
