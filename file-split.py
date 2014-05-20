#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Splits large text files into manageable chunks
"""

import sys, tkFileDialog
from Tkinter import *
from math import ceil

class Application(Frame):
    #initialize menu and window settings
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.parent = parent
        self.pack(fill=BOTH, expand=1)

        self.parent.title("File Splitter")

        #menu
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu.add_command(label="Open", command=self.file_select)
        filemenu.add_command(label="Quit", command=self.on_exit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        #app window
        width = 600
        height = 250

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - width)/2
        y = (sh - height)/2

        self.parent.geometry('%dx%d+%d+%d' % (width, height, x, y))

        self.frame_current_loaded_file_info = Frame(self)
        self.frame_current_loaded_file_info.pack()

        self.current_loaded_filename = StringVar()
        Label(self.frame_current_loaded_file_info, width=250, textvariable=self.current_loaded_filename).pack()

        self.current_loaded_file_lines_label = StringVar()
        Label(self.frame_current_loaded_file_info, width=50, textvariable=self.current_loaded_file_lines_label).pack()

        Button(self, text="Load a file", command=self.file_select).pack()

        self.label_header = StringVar()
        Label(self, textvariable=self.label_header).pack(anchor=NW)

        self.output_header = BooleanVar()
        Checkbutton(self, text="repeat header on output files", variable=self.output_header).pack(padx=10)

        self.frame_split_point = Frame(self)
        self.frame_split_point.pack(pady=10)

        self.split_point = StringVar()
        Label(self.frame_split_point, text="lines per file").pack(side=LEFT, padx=10)

        self.entry_split_point = Entry(self.frame_split_point, textvariable=self.split_point, validate="focusout", vcmd=self.split_point_is_int)
        self.entry_split_point.pack(side=RIGHT, padx=10)
        
        Button(self, text="split", command=self.split).pack()

        self.progress = StringVar()
        Label(self, textvariable=self.progress).pack()

    #validate split point entry
    def split_point_is_int(self):
        try:
            sp = int(self.split_point.get())
            if sp > 0:
                return True
            else:
                return False
        except ValueError:
            return False

    #split input file into chunks
    def split(self):
        if self.output_header:
            header = self.line_list[0]
        sp = int(self.split_point.get())
        number_of_output_files = int(ceil(float(len(self.line_list))/sp))
        input_file_name = self.current_loaded_filename.get().split(".")
        for i in xrange(number_of_output_files):
            self.progress.set("Writing %d of %d files" % (i, number_of_output_files))
            o = open(input_file_name[0] + "-part" + str(i) + "." + input_file_name[1], "w")
            if self.output_header:
                o.writelines(header)
                o.writelines(self.line_list[(i*sp)+1:((i+1)*sp)+1])
            else:
                o.writelines(self.line_list[(i*sp):((i+1)*sp)])
            o.close()
        self.progress.set("Wrote %d of %d files" % (i+1, number_of_output_files))

    #select input file
    def file_select(self):
        file_types = [('Text Files', '*.csv'), ('Text Files', '*.tab'), ('Text Files', '*.tsv'), ('Text Files', '*.ttx'), ('Text Files', '*.txt'), ('All Files', '*')]
        dialog = tkFileDialog.Open(self, filetypes=file_types)
        selected_file = dialog.show()
        if selected_file != "":
            self.f = open(selected_file, "r")
            self.line_list = self.f.readlines()
            self.f.close()
            path = selected_file
            filename = path.split("/")[-1]
            self.current_loaded_filename.set(filename)
            self.current_loaded_file_lines_label.set(str(len(self.line_list)) + " lines")
            self.label_header.set("header = " + self.line_list[0])

    #close
    def on_exit(self):
        self.quit()

def main():
    root = Tk()
    app = Application(root)

    root.mainloop()

if __name__ == '__main__':
    main()  