
def classify(csv,wav):
    fd = open(str(csv),"r+")
    data = fd.readlines()
    fd.close()
    
    numFiles = len(data)

    findyDict = {}
    for i in xrange(numFiles):
        comma = data[i].find(',')
        key = data[i][0:comma]
        val = int(data[i][comma+1])
        findyDict[key] = val

    return findyDict[str(wav)]













