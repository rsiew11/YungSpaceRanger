import argparse
import os
import pandas
import csv
from sklearn import svm

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


# function that adds the target value to a given average dictionary
# based on the target file
def target_value( basename ):
    with open(target_file, 'rb') as csvfile:
        filereader = csv.DictReader(csvfile, delimiter=',')
        # parse the csv file as a dict
        for row in filereader:
            file_name = row['filename']
            # extract the base name to insert into avg dictionary
            base_name = os.path.basename(file_name)
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
        coefficient_header = filereader.fieldnames
        for row in filereader:
            for coeff in coefficient_names:
                # ignore the name and frameTime fields
                if "pcm" not in coeff:
                    continue
                # create an array mapping coeff -> list of values
                # at each frame time
                if coeff not in avg_dict:
                    avg_dict[coeff] = [float(row[coeff])]
                else:
                    avg_dict[coeff].append(float(row[coeff]))

    close(coeff_output_file)
    # now, take the average of all values in each array
    for key in avg_dict:
        value_array = avg_dict[key]
        avg_dict[key] = sum(value_array)/len(value_array)

    # add a parameter for the filename (minus the extension)
    base_name = os.path.basename(coeff_output_file)
    avg_dict['file'] = base_name
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
        result.append(mydict[key])
    return result

# function that parses each output file and creates
# one large output file with all the averages
# returns the name of the file to output to
def create_single_output( ):
    # write the header
    header_added = True

    # create a target array
    targets = []

    with open(total_data, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        # for each in the output, create the dictionary and write to total data
        for filename in os.listdir(training_folder):

            print "file looking at"+str(os.path.join(output_directory, filename))

            full_path = os.path.abspath(filename)

            avg_dict, coefficient_names = comput_avg_coeffs(full_path)

            if (not(header_added)):
                coefficient_names.remove('frameTime')
                coeffiecient_names.remove('name')
                coefficient_names.insert(0, 'file')
                writer.writerow(coefficient_names)
                header_added = True

            targets.append(avg_dict['target'])

            # write the array form of the dictionary to csv
            writer.writerow(dict_to_value_array(avg_dict))
    return total_data, targets

# return a matrix that can be passed into the classifier
def matrix_from_csv( single_output ):
    matrix = []
    with open(single_output, 'rb') as csvfile:
        reader = csv.reader(csv_file, delimiter=';')
        coeff_names = reader.fieldnames
        for row in reader:
            # skip the first row
            for coeff in coeff_names:
                if "pcm" not in coeff:
                    continue
                matrix.append(float(str(row[coeff])))
    return [matrix]

# function that creates a classifier and tests on a sample
def classify( single_output ):
    total_data, targets = create_single_output()
    df = pandas.read_csv(total_data)
    clf = svm.SVC(gamma=0.001, C=100.)
    clf.fit(df.values, targets)
    print df.values
    print clf.predict(matrix_from_csv(single_output))


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

