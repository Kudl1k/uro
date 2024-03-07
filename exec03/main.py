from tkinter import *


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("My Tkinter App")
        
        # Add your widgets and layout here
        
    def run(self):
        self.root.mainloop()



root = Tk()
app = App(root)
app.run()