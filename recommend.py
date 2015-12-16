#from PIL import Image
import os
import lsh
import numpy
import cv2

orb = cv2.ORB()

def recommend_place(infile_list):
    extract_query(infile_list)
    os.system('''cp query.csv pig/''')
    os.system('''rm query.csv''')
    os.chdir("pig")
    print "path"
    os.system('''pwd''')
    os.system('''rm -rf *.out''')
    os.system('''rm -rf pig.result''')
    os.system('''pig -x local match.py''')

    good_pic = dict()

    weight = [3,2,1]
    for i in range(20):
        file_name = "part-m-%05d"%i
        file = open("pig.result/" + file_name, 'r')
        row = 0
        for each_line in file:
            each_line = each_line[0:-1].split()
            pic_num = int(each_line[0])
            pic_score = int(each_line[1]) * weight[row]
            if pic_num in good_pic:
                good_pic[pic_num] += pic_score
            else:
                good_pic[pic_num] = pic_score
            row += 1

    sorted_good_pic = sorted(good_pic.iteritems(), key=lambda d:d[1], reverse = True)

    outfile = './static/'+str(sorted_good_pic[0][0]) + ".jpg"
    message = "from server"
    print outfile
    os.system('''rm -f query.csv''')
    os.chdir("..")
    return outfile, message


def extract_query(infile_list):
    featureID = 0
    imageID = 0
    NUMBER_OF_TABLES = 20
    totalDescriptors = 0
    f = open('query.csv', 'w')
    for file_name in infile_list:

        img = cv2.imread(file_name, 0)
        kp = orb.detect(img, None)
        kp, des = orb.compute(img, kp)

        numDescriptors = des.shape[0]
        totalDescriptors = totalDescriptors + numDescriptors
        contig = numpy.ascontiguousarray(des, dtype=numpy.uint8)
        hashes = lsh.hash(contig)

        # for each descriptor, get the 20 hash values
        cnt = 0
        for descriptor in xrange(0, numDescriptors):
            f.write("%u, %u, " % (featureID, imageID))
            for hash in xrange(0, NUMBER_OF_TABLES):
                f.write("%u, " % (hashes[cnt]))
                cnt = cnt + 1
            f.write("\n")
            featureID = featureID + 1
        imageID = imageID + 1
    print "Wrote %u descriptor records\n" % (totalDescriptors)
    f.close()


if __name__ == "__main__":
    #extract_query()
    (a,b)=recommend_place(['input/10.jpg', 'input/16.jpg'])
    print b
