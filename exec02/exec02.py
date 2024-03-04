# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
from math import sqrt
import tkinter.font

class myApp:

    def prevod(self, event=None):
        try:
            v = float(self.ent_in.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")


        print(self.var.get())
        if self.var.get() == 0:
            if v < -20 or v > 50:
                messagebox.showerror("Invalid Input", "Please enter a valid number.💩")
                return

            result = v * 9/5 + 32
        else:
            if v < 0 or v > 120:
                messagebox.showerror("Invalid Input", "Please enter a valid number.💩")
                return
            result = (v - 32) * 5/9
        self.ent_out.delete(0, END)
        self.ent_out.insert(0, str(round(result, 2)))
        self.update_thermometer(result)

    def update_thermometer(self,value):
        min_y = 80
        max_y = 292
        y_coord = 0
        if self.var.get() == 1:
            #Min_Max for Celsius
            min_temp = -20
            max_temp = 50

            temp_range = max_temp - min_temp
            thermometer_range = max_y - min_y
            temp_height = (value - min_temp) / temp_range * thermometer_range
            

            y_coord = max_y - temp_height
        else:
            #Min_Max for fahrenheit
            min_temp = 0
            max_temp = 120

            temp_range = max_temp - min_temp
            thermometer_range = max_y - min_y
            temp_height = (value - min_temp) / temp_range * thermometer_range
            # 4 because of the offset in the temperature
            y_coord = max_y - temp_height - 4

        self.ca.coords(self.r,146,292,152,y_coord)
        

    def __init__(self, root):

        root.title('Temperature Converter')
        root.resizable(False, False)
        root.bind('<Return>', self.prevod)

        def_font = tkinter.font.nametofont("TkDefaultFont")
        def_font.config(size=16)

        self.left_frame = Frame(root)
        self.right_frame = Frame(root)

        # Adding a label to the right frame
        self.var = IntVar(value=0)
        self.dir_frame = LabelFrame(self.left_frame,text="Direction")
        self.rbtn1 = Radiobutton(self.dir_frame,text="C->F", value=0, variable=self.var,command=self.prevod)
        self.rbtn2 = Radiobutton(self.dir_frame,text="F->C" ,value=1, variable=self.var,command=self.prevod)


        self.dir = IntVar()
        self.dir.set(1)
        #Input Output Frame
        self.ent_frame = LabelFrame(self.left_frame)
        #Input textfield
        self.lbl_in = Label(self.ent_frame, text="Input")
        self.ent_in = Entry(self.ent_frame, width=10, font = def_font)
        self.ent_in.insert(0, '0')
        #Output textfield
        self.lbl_out = Label(self.ent_frame, text="Output")
        self.ent_out = Entry(self.ent_frame,width=10,font = def_font,)


        self.btn_cnvrt = Button(self.ent_frame,text="Convert",command=self.prevod)


        self.ca = Canvas(self.right_frame, width=300, height=400)
        self.photo = PhotoImage(file="th_empty.png")
        self.ca.create_image(150, 200, image=self.photo)
        self.r = self.ca.create_rectangle(146, 292, 152, 80, fill="blue")
        self.ca.coords(self.r,146,292,152,292)


        self.signature = Label(self.right_frame,text="KUD0132")



        self.left_frame.pack(side="left",fill=BOTH,expand=True, anchor=CENTER)
        self.right_frame.pack(side="right",fill=BOTH,expand=True,anchor = CENTER)
        self.dir_frame.pack(side = TOP,padx=5,pady=5,fill=X)
        self.ent_frame.pack(padx=5,pady=5,fill=BOTH, expand=True)
        self.rbtn1.pack(side=LEFT)
        self.rbtn2.pack(side=LEFT)
        self.lbl_in.pack()
        self.ent_in.pack(fill=X,expand=True)
        self.lbl_out.pack()
        self.ent_out.pack(fill=X,expand=True)
        self.btn_cnvrt.pack(side="bottom")
        self.ca.pack()
        self.signature.pack(anchor=SE,side=BOTTOM)

        self.ent_in.focus_force()


root = Tk()
app = myApp(root)
root.mainloop()

