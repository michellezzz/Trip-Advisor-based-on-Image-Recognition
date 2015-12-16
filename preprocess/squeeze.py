from PIL import Image
import os

num = 0

for infile in os.listdir('./input'):
    print infile
    #outfile = './output/%d.jpg' % num
    outfile = './output/' + infile
    im = Image.open('./input' + '/' + infile)
    im.thumbnail((200, 200))
    im.save(outfile, im.format)
    num += 1
