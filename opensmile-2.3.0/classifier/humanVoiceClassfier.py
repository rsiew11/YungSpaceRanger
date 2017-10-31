import argparse
import os
import pandas
import csv
from sklearn import svm
import numpy as np

# The absolute path of the wav file we wnat to predict if a human voice or not
predict_file = ""
# The absolute path of the folder we store our csv mfcc files in
training_folder = ""
# Name of csv file containing every wav file and their corresponding coefficients
total_data = "total_data.csv"
# Name of the file containing every wav file mapped to its target
target_file = ""
# Header for csv file for all outputs
coefficient_names = []
coefficients = ["pcm_fftMag_mfcc[0]", "pcm_fftMag_mfcc[1]", "pcm_fftMag_mfcc[2]",
        "pcm_fftMag_mfcc[3]", "pcm_fftMag_mfcc[4]", "pcm_fftMag_mfcc[5]",
        "pcm_fftMag_mfcc[6]", "pcm_fftMag_mfcc[7]", "pcm_fftMag_mfcc[8]",
        "pcm_fftMag_mfcc[9]", "pcm_fftMag_mfcc[10]", "pcm_fftMag_mfcc[11]",
        "pcm_fftMag_mfcc[12]"]
""""pcm_fftMag_mfcc_de[0]"]
        "pcm_fftMag_mfcc_de[1]", "pcm_fftMag_mfcc_de[2]",
        "pcm_fftMag_mfcc_de[3]", "pcm_fftMag_mfcc_de[4]",
        "pcm_fftMag_mfcc_de[5]", "pcm_fftMag_mfcc_de[6]",
        "pcm_fftMag_mfcc_de[7]", "pcm_fftMag_mfcc_de[8]",
        "pcm_fftMag_mfcc_de[9]", "pcm_fftMag_mfcc_de[10]",
        "pcm_fftMag_mfcc_de[11]", "pcm_fftMag_mfcc_de[12]"]
pcm_fftMag_mfcc_de_de[0]", "pcm_fftMag_mfcc_de_de[1]",
        "pcm_fftMag_mfcc_de_de[2]", "pcm_fftMag_mfcc_de_de[3]",
        "pcm_fftMag_mfcc_de_de[4]", "pcm_fftMag_mfcc_de_de[5]",
        "pcm_fftMag_mfcc_de_de[6]", "pcm_fftMag_mfcc_de_de[7]",
        "pcm_fftMag_mfcc_de_de[8]", "pcm_fftMag_mfcc_de_de[9]",
        "pcm_fftMag_mfcc_de_de[10]", "pcm_fftMag_mfcc_de_de[11]",
        "pcm_fftMag_mfcc_de_de[12]"]"""

print coefficients

target = 0
def dummy_target():
    global target
    target = int(not(bool(target)))
    return target

# function that adds the target value to a given average dictionary
# based on the target file
def target_value( basename ):
    with open(target_file, 'rb') as csvfile:
        filereader = csv.DictReader(csvfile, delimiter=',')
        for row in filereader:
            file_name = row['filename']
            # extract the base name to insert into avg dictionary
            base_name, file_extension = os.path.splitext(os.path.basename(file_name))
            # insert the target value into the average dictionary
            if (base_name == basename):
                return int(row['target'])
    return 0

# function that uses all the frame data provided by a given csv file and
# computes the averages for each of the coefficients across all frames
# returns a dictionary mapping it's name and
# every coefficient
def compute_avg_coeffs( coeff_output_file ):
    # stores each coefficient mapped to the avg value of that coeff
    avg_dict = dict()
    with open(coeff_output_file, 'rb') as csvfile:
        # parse the csv file as a dict -- coeff -> value
        filereader = csv.DictReader(csvfile, delimiter=';')
        coeff_header = filereader.fieldnames
        for row in filereader:
            for coeff in coeff_header:
                # ignore the name and frameTime fields
                if "pcm" not in coeff:
                    continue
                # create an array mapping coeff -> list of values
                # at each frame time
                if coeff not in avg_dict:
                    avg_dict[coeff] = [float(row[coeff])]
                else:
                    avg_dict[coeff].append(float(row[coeff]))

    # now, take the average of all values in each array
    for key in avg_dict:
        value_array = avg_dict[key]
        avg_dict[key] = sum(value_array)/len(value_array)

    # add a parameter for the filename (minus the extension)
    base_name, file_extension = os.path.splitext(os.path.basename(coeff_output_file))
    avg_dict['file'] = base_name
    #avg_dict['human'] = dummy_target()
    avg_dict['human'] = target_value(base_name)
    return avg_dict, coeff_header

# function that takes in a dictionary
# and returns an array of its values
# sorted by its keys
def dict_to_value_array(mydict):
    result = []
    keylist = mydict.keys()
    keylist.sort()
    for key in keylist:
        if key == 'target':
            continue
        result.append(mydict[key])
    return result

# function that parses each output file and creates
# one large output file with all the averages
# returns the name of the file to output to
def create_single_output( ):
    # write the header
    header_added = False

    # create a target array
    targets = []

    with open(total_data, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        # for each in the output, create the dictionary and write to total data
        print training_folder

        for filename in os.listdir(training_folder):
            print filename


            full_path = os.path.join(training_folder, filename)
            print "file looking at"+full_path
            if "other_output" in full_path:
                continue

            avg_dict, coefficient_names = compute_avg_coeffs(full_path)

            if (not(header_added)):
                coefficient_names.remove('frameTime')
                coefficient_names.remove('name')
                coefficient_names.insert(0, 'file')
                writer.writerow(coefficient_names)
                header_added = True

            targets.append(avg_dict['human'])

            # write the array form of the dictionary to csv
            writer.writerow(dict_to_value_array(avg_dict))
    return total_data, targets

# return a matrix that can be passed into the classifier
def matrix_from_csv( single_output ):
    matrix = []
    avg_dict, coeff_header = compute_avg_coeffs(single_output)
    for coeff in coeff_header:
        if "pcm" not in coeff:
            continue
        matrix.append(float(avg_dict[coeff]))
    return [matrix[0:13]]

# function that creates a classifier and tests on a sample
def classify( single_output ):
    total_data, targets = create_single_output()
    df = pandas.read_csv(total_data, usecols=coefficients)
    clf = svm.SVC(gamma=0.001, C=100.)
    print targets
    clf.fit(df.values, targets)
    matrix = matrix_from_csv(single_output)
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
    parser.add_argument('--target_file', '-t', action="store",
                        dest="target_file", type=str,
                        help="File containing wav file mapped to target value")

    args = parser.parse_args()

    # need absolute paths to files and folders
    predict_file = os.path.abspath(args.predict_file)
    training_folder = os.path.abspath(args.training_folder)
    target_file = os.path.abspath(args.target_file)
    classify( predict_file )
