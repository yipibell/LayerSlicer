# pyinstaller -w -F -i "E:\my_Pythone_Scripts\Tester\a1.ico" LeyarSlicer.pyw #

from Tkinter import *
from ttk import Progressbar
import tkFileDialog
import tkMessageBox

class Gcode_Slicer:
    def __init__(self):
        self.main=Tk()
        self.file_path=''
        self.calculate_frame_Open=True

        self.title_Label=Label(self.main,text='Welcome to gcode slicer').grid(row=0,column=0,sticky='EW',columnspan=4)

        self.gcode_File_Path_Label=Label(self.main,text='Select Target gcode file:').grid(row=1,column=0, padx=3,pady=3)
        self.gcode_File_Path_Entry=Entry(self.main, width=35)
        self.gcode_File_Path_Entry.grid(row=1,column=1,columnspan=2, padx=3,pady=3)
        self.gcode_File_Path_Button=Button(self.main, text='select',width=9, command=self.get_gcode_File)
        self.gcode_File_Path_Button.grid(row=1,column=3, padx=3,pady=3)

        self.start_Layer_Label=Label(self.main,text='Layer to start from:').grid(row=2,column=0, padx=3,pady=3)
        self.start_Layer_Entry = Entry(self.main, width=5)
        self.start_Layer_Entry.grid(row=2, column=1,sticky='EW', padx=3, pady=3)
        self.start_Layer_Entry.bind('<Return>', self.start_slice)
        self.start_Layer_Calculate_Button=Button(self.main, text='Calculate starting layer', command=self.open_canculate)
        self.start_Layer_Calculate_Button.grid(row=2,column=2,columnspan=2, padx=3,pady=3, sticky='EW')

        self.slice_Layers_Button=Button(self.main, text='slice',width=9, command=self.slice)
        self.slice_Layers_Button.grid(row=4,column=0,sticky='EW', columnspan=4, padx=3,pady=3)

        self.main.title('gcode layer skipper')
        self.main.resizable(False,False)
        self.main.mainloop()

    def validete_File_Type(self,PATH):
        if PATH.split('.')[-1]=='gcode':
            return True
        return False

    def get_gcode_File(self):
        self.file_path = tkFileDialog.askopenfilename()
        if self.validete_File_Type(self.file_path):
            self.gcode_File_Path_Entry.delete(0,END)
            self.gcode_File_Path_Entry.insert(0,self.file_path)
        elif self.file_path=='':
            tkMessageBox.showwarning("Warning!", "You didn't chose a file")
        else:
            self.gcode_File_Path_Entry.delete(0, END)
            self.gcode_File_Path_Entry.insert(0, 'Thats a bad file type')
            tkMessageBox.showerror("Bad file", "file must end with .gcode")

    def slice(self):
        progress = Progressbar(self.main, orient="horizontal", length=30, mode="determinate")
        progress.grid(row=5,column=0,columnspan=4,sticky='EW',padx=3,pady=2)
        progress["value"] = 0

        if self.validete_File_Type(self.file_path):
            slice=-True
            output_Path='{}_From_Layer_{}.gcode'.format(self.file_path.split(',')[0],self.start_Layer_Entry.get())
            try:
                start_Layer=int(self.start_Layer_Entry.get())
            except ValueError:
                slice=False
                tkMessageBox.showerror("Bad Value", "starting layer must be a number")

            if slice:
                origen_File = open(self.file_path, 'r')
                all_lines = origen_File.readlines()
                origen_File.close()

                progress["maximum"] = len(all_lines)

                output_File = open(output_Path, 'w')
                output_File.write('')
                output_File.close()

                output_File = open(output_Path, 'a')

                copy = True
                error=False
                try:
                    num_of_line=0
                    for line in all_lines:
                        if num_of_line%10000==0:
                            progress.configure(value=num_of_line)
                            progress.update()
                        if ';LAYER:' in line:
                            if int(line.split(':')[1])<start_Layer:
                                print int(line.split(':')[1])
                                copy = False
                            elif ';LAYER:{}'.format(start_Layer) in line:
                                copy = True

                        if copy:
                            output_File.write(line)
                        num_of_line+=1
                except ValueError:
                    tkMessageBox.showerror("Bad Value", "There is a problem with one of the Layers in the line:\n{}".format(line))
                    error=True
                output_File.close()
                progress.destroy()
                if not error:
                    tkMessageBox.showinfo("Success", "new gcode file is created successfully in the same folder.\n file name is:\n{}".format(output_Path.split('/')[-1]))

    def open_canculate(self):
        if self.calculate_frame_Open:
            self.calculate_Frame = Frame(self.main)
            self.calculate_Frame.grid(row=0, column=5, rowspan=5, sticky='NS')

            self.start_Layer_Calculate_Button.configure(text='Close Calculator')

            self.layer_height_Label=Label(self.calculate_Frame,text='Layer hight:').grid(row=0,column=0,columnspan=2)
            self.layer_height_Entry=Entry(self.calculate_Frame)
            self.layer_height_Entry.grid(row=1, column=0, sticky='EW', columnspan=2)

            self.print_height_Label=Label(self.calculate_Frame,text='print hight:').grid(row=2,column=0,columnspan=2)
            self.print_height_Entry=Entry(self.calculate_Frame)
            self.print_height_Entry.grid(row=3, column=0, sticky='EW', columnspan=2)
            self.print_height_Entry.bind('<Return>', self.start_calculate)

            self.calculate_layers_Button = Button(self.calculate_Frame, text='Calculate layers', width=9, command=self.calculate)
            self.calculate_layers_Button.grid(row=4, column=0, sticky='EW', columnspan=4, padx=3, pady=3)

            self.calculate_frame_Open=False
        else:
            for widght in self.calculate_Frame.winfo_children():
                widght.destroy()
            self.calculate_Frame.destroy()
            self.calculate_frame_Open = True
            self.start_Layer_Calculate_Button.configure(text='Calculate starting layer')


    def calculate(self):
        if self.layer_height_Entry.get().isdigit() and self.print_height_Entry.get().isdigit():
            self.start_Layer_Entry.delete(0,END)
            self.start_Layer_Entry.insert(0,'{}'.format(int(float(self.layer_height_Entry.get()) / float(self.print_height_Entry.get()) - 0.5)))
            self.calculate_frame_Open=False
            self.open_canculate()
        else:
            tkMessageBox.showerror("Bad Value",
                                   "There is a problem with the layer height or print height\nThey both must be numbers")

    def start_calculate(self,event):
        self.calculate()

    def start_slice(self,event):
        self.slice()


if __name__ == '__main__':
    Gcode_Slicer()