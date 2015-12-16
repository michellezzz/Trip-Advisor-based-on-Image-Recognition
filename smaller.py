__author__ = 'Michelle'

import web
import os
#from PIL import Image
import recommend

urls = ('/upload', 'Upload')
render = web.template.render('templates/',)

num_of_input = 3
infile_list = []

def fileCountIn(dir):
    return sum([len(files) for root, dirs, files in os.walk(dir)])


class Upload:

    def GET(self):
        web.header("Content-Type", "text/html; charset=utf-8")
        return render.upload('', '')

    def POST(self):
        x = web.input(myfile={})
        filedir = 'input'  # change this to the directory you want to store the file in.
        if 'myfile' in x:  # to check if the file-object is created
            filepath = x.myfile.filename.replace('\\', '/')  # replaces the windows-style slashes with linux ones.
            filename = filepath.split('/')[-1]  # splits the and chooses the last part (the filename with extension)
            fout = open(filedir + '/' + filename, 'wb')  # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read())  # writes the uploaded file to the newly created file.
            fout.close()  # closes the file, upload complete.

            os.system('''rm -f ./input/.DS_Store''')

            infile_list.append(filedir + '/' + filename)
            if len(infile_list) >= 3:
                outfile, message = recommend.recommend_place(infile_list)
                del infile_list[:]
                return render.upload(outfile, message)
            else:
                return render.upload('./static/more.jpg', 'more picture please'+str(infile_list))


if __name__ == "__main__":
   app = web.application(urls, globals())
   app.run()
