import csv
import os
import numpy as np

output_directory = "/afs/andrew.cmu.edu/usr23/npmurali/private/18500/YungSpaceRanger/opensmile-2.3.0/soccerfield/output"
coefficient_names = []
format_values = ['f8']*39

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

def create_classifier(avg_dict):
    names = ['coefficient', 'value']
    format_values = ['U25', 'f8']
    dtype = dict(names = names, formats=format_values)
    array = np.array(list(avg_dict.items()), dtype=dtype)
    print repr(array)

              

                
def parsefiles():
    for filename in os.listdir(output_directory):
        print "file looking at"+str(os.path.join(output_directory, filename))
        full_path = os.path.join(output_directory, filename)
        avg_dict = create_average_file(full_path)
        avg_dict = avg_values_across_dict(avg_dict)
        create_classifier(avg_dict)



if __name__ == "__main__":
    parsefiles()

