import os

num = 0

for infile in os.listdir('./input'):
    os.system('''cp ./input/%s ./output/%d.jpg''' % (infile, num))
    num += 1
