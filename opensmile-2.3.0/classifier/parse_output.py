import csv
import os
import numpy as np
import pandas

output_directory = "/afs/andrew.cmu.edu/usr23/npmurali/private/18500/YungSpaceRanger/opensmile-2.3.0/soccerfield/output"
coefficient_names = []

def create_average_file(filename):
    avg_dict = dict()
    global coefficient_names
    with open(filename, 'rb') as csvfile:
        filereader = csv.DictReader(csvfile, delimiter=';')
        coefficient_names = filereader.fieldnames
        for row in filereader:
            for coeff in coefficient_names:
                if "pcm" not in coeff:
                    continue
                if coeff not in avg_dict:
                    avg_dict[coeff] = [float(row[coeff])]
                else:
                    avg_dict[coeff].append(float(row[coeff]))
    return avg_dict

def avg_values_across_dict(avg_dict):
    for key in avg_dict:
        value_array = avg_dict[key]
        avg_dict[key] = sum(value_array)/len(value_array)
    return avg_dict

def dict_to_value_array(mydict):
    result = []
    keylist = mydict.keys()
    keylist.sort()
    for key in keylist:
        result.append(mydict[key])
    return result


def parsefiles():
    header_added = False
    with open('all_output.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for filename in os.listdir(output_directory):
            print "file looking at"+str(os.path.join(output_directory, filename))
            full_path = os.path.join(output_directory, filename)
            avg_dict = create_average_file(full_path)
            avg_dict = avg_values_across_dict(avg_dict)
            avg_dict['name'] = filename
            if (not(header_added)):
                coefficient_names.remove('frameTime')
                writer.writerow(coefficient_names)
                header_added = True
            writer.writerow(dict_to_value_array(avg_dict))
    return csv_file

def classify():
    output_csv = parsefiles()
    df = pandas.read_csv('all_output.csv')
    print df

if __name__ == "__main__":
    classify()
