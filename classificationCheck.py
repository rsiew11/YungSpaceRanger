import sys


#use this file by running "python THISFILE.py SMTH.csv SMTH.wav"
#sys.argv[1] is the csv file with the classification
#sys.argv[2] is the wav file in question


fd = open(str(sys.argv[1]),r+)

data = fd.readlines()
numFiles = len(data)


findyDict = {}
for i in xrange(numFiles):
    comma = str.find(',')
    key = data[i][0:comma]
    val = int(data[i][comma+1])
    findyDict[key] = val

return findyDict[str(sys.argv[2])]






