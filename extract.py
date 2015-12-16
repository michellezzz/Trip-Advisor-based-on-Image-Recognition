import os
import lsh
import numpy
import cv2

rootdir = "./static/"
orb = cv2.ORB(100)

featureID = 0
imageID = 0
NUMBER_OF_TABLES = 20
totalDescriptors = 0

file_db = open('./pig/database.csv', 'w')
file_index = open('file_index.csv', 'w')
file_index.write("%-10s|%-10s\n" % ("ImageID", "Filename"))
file_index.write("-"*50+'\n')
os.system('''rm -f ./static/.DS_Store''')

for infile in os.listdir(rootdir):
    filename = rootdir + infile
    if infile == "more.jpg":
        continue
    print filename

    file_index.write("%-10s|%-10s\n" % (imageID, filename))

    img = cv2.imread(filename, 0)
    kp = orb.detect(img, None)
    kp, des = orb.compute(img, kp)
    numDescriptors = des.shape[0]
    totalDescriptors = totalDescriptors + numDescriptors
    contig = numpy.ascontiguousarray(des, dtype=numpy.uint8)
    hashes = lsh.hash(contig)
    cnt = 0
    for descriptor in xrange(0, numDescriptors):
        file_db.write("%u, %u, " % (featureID, imageID))
        for hash in xrange(0, NUMBER_OF_TABLES):
            file_db.write("%u, " % (hashes[cnt]))
            cnt = cnt + 1
        file_db.write("\n")
        featureID = featureID + 1
    imageID = imageID + 1

print "Wrote %u descriptor records\n" % (totalDescriptors)

file_db.close()
file_index.close()
