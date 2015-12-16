__author__ = 'Michelle'

import web
import os
import search

urls = ('/upload', 'Upload')
render = web.template.render('templates/',)


num_of_input = 3
infile_list = []


def get_file_index():
    index_file = open("file_index.csv")
    index_file.readline()
    index_file.readline()
    file_index = dict()
    for each_line in index_file:
        each_line = each_line[0:-1].split('|')
        file_index[each_line[0].strip()] = each_line[1]
    return file_index


def get_history():
    history = list()
    for infile in os.listdir('./input'):
        history.append(infile)
    if len(history) > 12:
        return history[0:12]
    return history


class Upload:

    def GET(self):
        web.header("Content-Type", "text/html; charset=GB18030")
        return render.upload([], [], get_history(), -1)

    def POST(self):
        x = web.input(myfile={})
        history = get_history()
        filedir = 'input'  # change this to the directory you want to store the file in.
        if 'myfile' in x:  # to check if the file-object is created
            filepath = x.myfile.filename.replace('\\', '/')  # replaces the windows-style slashes with linux ones.
            filename = filepath.split('/')[-1]  # splits the and chooses the last part (the filename with extension)
            fout = open(filedir + '/' + filename, 'wb')  # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read())  # writes the uploaded file to the newly created file.
            fout.close()  # closes the file, upload complete.

            infile_list.append(filedir + '/' + filename)
            if len(infile_list) >= 3:
                os.system('''rm -f ./input/.DS_Store''')
                outfile_list = search.search_place(infile_list, get_file_index(), 3)
                #outfile_list = ["./static/foluolunsa.jpg", "./static/hude.jpg", "./static/zoo.jpg"]
                del infile_list[:]
                return render.upload(outfile_list, infile_list, get_history(), 1)
            else:
                return render.upload(['./static/more.jpg'], infile_list, get_history(), 0)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
