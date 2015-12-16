#from PIL import Image
import os
import lsh
import numpy
import cv2

orb = cv2.ORB(100)

def get_file_index():
    index_file = open("file_index.csv")
    index_file.readline()
    index_file.readline()
    file_index = dict()
    for each_line in index_file:
        each_line = each_line[0:-1].split('|')
        file_index[each_line[0].strip()] = each_line[1]
    return file_index



def generate_vote():
    os.chdir("pig")
    os.system('''pwd''')
    os.system('''rm -rf *.out''')
    os.system('''rm -rf pig.result''')
    os.system('''pig -x local match.py''')


def count_vote():
    weight = [3, 2, 1]
    good_pic = dict()
    for i in range(20):
        file_name = "part-m-%05d" % i
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
    return sorted_good_pic  # list [(key1, value1),(key2, value2),...]


def search_place(infile_list, file_index, num_of_recommend):
    extract_query(infile_list)
    generate_vote()
    sorted_good_pic = count_vote()

    outfile_list = list()
    for i in range(num_of_recommend):
        outfile = file_index[str(sorted_good_pic[i][0])]
        outfile_list.append(outfile)

    os.system('''rm -f query.csv''')
    os.chdir("..")
    return outfile_list


def extract_query(infile_list):
    featureID = 0
    imageID = 0
    NUMBER_OF_TABLES = 20
    totalDescriptors = 0
    f = open('./pig/query.csv', 'w')
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
    # extract_query()
    (a, b) = recommend_place(['static/7.jpg', 'static/7.jpg'], get_file_index(), 3)
    print a
    print b
    #print get_file_index()
