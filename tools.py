import codecs
def writeToFile(filename, arrayOfData):
    file = codecs.open(filename, 'w',encoding= "UTF-8")
    for d in arrayOfData:
        file.write(d+'\n')
    file.close()