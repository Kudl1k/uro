# -*- coding: utf-8 -*-

from tkinter import *
from math import sqrt
import tkinter.font

class myApp:

    def prevod(self, event=None):
        v = float(self.ent_in.get())
        print(self.var.get())
        if self.var.get() == 0:
            result = v * 9/5 + 32
        else:
            result = (v - 32) * 5/9
        self.ent_out.delete(0, END)
        self.ent_out.insert(0, str(round(result, 2)))
        self.update_thermometer(result)

    def update_thermometer(self,value):
        pass

    def __init__(self, root):

        root.title('Převodník teplot')
        root.resizable(False, False)
        root.bind('<Return>', self.prevod)

        def_font = tkinter.font.nametofont("TkDefaultFont")
        def_font.config(size=16)

        self.left_frame = Frame(root)
        self.right_frame = Frame(root)

        # Adding a label to the right frame
        self.var = IntVar(value=0)
        self.dir_frame = Frame(self.left_frame)
        self.rbtn1 = Radiobutton(self.dir_frame,text="C->F", value=0, variable=self.var,command=self.prevod)
        self.rbtn2 = Radiobutton(self.dir_frame,text="F->C" ,value=1, variable=self.var,command=self.prevod)


        self.dir = IntVar()
        self.dir.set(1)
        #Input Output Frame
        self.ent_frame = Frame(self.left_frame)
        #Input textfield
        self.lbl_in = Label(self.ent_frame, text="Input")
        self.ent_in = Entry(self.ent_frame, width=10, font = def_font)
        self.ent_in.insert(0, '0')
        #Output textfield
        self.lbl_out = Label(self.ent_frame, text="Output")
        self.ent_out = Entry(self.ent_frame,width=10,font = def_font,)


        self.btn_cnvrt = Button(self.ent_frame,text="Convert",command=self.prevod)


        self.ca = Canvas(self.right_frame, width=300, height=400)
        self.photo = PhotoImage(file="th.png")
        self.ca.create_image(150, 200, image=self.photo)
        self.ca.create_rectangle(146, 292, 152, 80, fill="blue")

        self.left_frame.pack(side="left",fill=BOTH,expand=True, anchor=CENTER)
        self.right_frame.pack(side="right",fill=BOTH,expand=True,anchor = CENTER)
        self.dir_frame.pack(padx=10,pady=10,fill=BOTH,expand=True,anchor=CENTER)
        self.ent_frame.pack(fill=BOTH, expand=True)
        self.rbtn1.pack(side=LEFT)
        self.rbtn2.pack(side=LEFT)
        self.lbl_in.pack()
        self.ent_in.pack()
        self.lbl_out.pack()
        self.ent_out.pack()
        self.btn_cnvrt.pack(side="bottom")
        self.ca.pack()

        self.ent_in.focus_force()


root = Tk()
app = myApp(root)
root.mainloop()

