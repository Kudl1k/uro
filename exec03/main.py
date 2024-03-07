from tkinter import *
from tkinter import ttk

class App:

    def __init__(self, root):
        self.root = root
        self.root.title("My Tkinter App")
        self.createTable()
        self.createForm()        
        
    def createTable(self):
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.pack(side=TOP,expand=True,fill=BOTH)
        self.tree = ttk.Treeview(self.table_frame, columns=('first name', 'last name', 'birth number'), show=' headings ' )
        self.tree.heading('first name', text='First Name')
        self.tree.heading('last name', text='Last Name')
        self.tree.heading ( 'birth number' , text='Birth Number' )
        self.tree.insert ( "", END, values=("John" , "Roe" , "045216/1512"))
        self.tree.insert ( "" , END, values=("Jane" , "Doe" , "901121/7238"))
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar = ttk.Scrollbar(self.table_frame, orient=VERTICAL, command=self.tree.yview) 
        self.tree.configure ( yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.tree.bind('<<TreeviewSelect>>', self.itemSelected)

    def createForm(self):
        self.form_frame = ttk.Frame(self.root)
        self.form_frame.pack(expand=True)

        # Name
        name_label = ttk.Label(self.form_frame, text="Name:")
        name_label.grid(row=0, column=0, sticky=W)
        self.name_entry = ttk.Entry(self.form_frame)
        self.name_entry.grid(row=0, column=1, sticky=W)

        # Birth Number
        birth_number_label = Label(self.form_frame, text="Birth Number:")
        birth_number_label.grid(row=1, column=0, sticky=W)
        self.birth_number_entry = ttk.Entry(self.form_frame)
        self.birth_number_entry.grid(row=1, column=1, sticky=W)

        # Address
        address_notebook = ttk.Notebook(self.form_frame)
        address_notebook.grid(row=2, column=0, columnspan=2, sticky='nsew')

        address_frame = Frame(address_notebook)
        address_notebook.add(address_frame, text="Address")

        # Street
        street_label = Label(address_frame, text="Street:")
        street_label.grid(row=0, column=0, sticky=W)
        self.street_entry = ttk.Entry(address_frame)
        self.street_entry.grid(row=0, column=1, sticky=W)

        # House Number
        house_number_label = Label(address_frame, text="House Number:")
        house_number_label.grid(row=0, column=2, sticky=W)
        self.house_number_entry = ttk.Entry(address_frame)
        self.house_number_entry.grid(row=0, column=3, sticky=W)

        # City
        city_label = Label(address_frame, text="City:")
        city_label.grid(row=1, column=0, sticky=W)
        self.city_entry = ttk.Entry(address_frame)
        self.city_entry.grid(row=1, column=1, sticky=W)

        # Zip Code
        zip_code_label = Label(address_frame, text="Zip Code:")
        zip_code_label.grid(row=1, column=2, sticky=W)
        self.zip_code_entry = ttk.Entry(address_frame)
        self.zip_code_entry.grid(row=1, column=3, sticky=W)


        note_frame = Frame(address_notebook)
        address_notebook.add(note_frame, text="Note")

        note_label = Label(note_frame, text="Note:")
        note_label.grid(row=0, column=0, sticky=W)
        self.note_entry = ttk.Entry(note_frame)
        self.note_entry.grid(row=0, column=1, sticky=W)

        # Configure the form_frame's row and column weights
        self.form_frame.grid_rowconfigure(0, weight=1)
        self.form_frame.grid_rowconfigure(1, weight=1)
        self.form_frame.grid_rowconfigure(2, weight=1)
        self.form_frame.grid_rowconfigure(3, weight=1)

    def itemSelected(self, event):
        for selected_item in self.tree.selection():
            print(self.tree.item(selected_item)['values'])



    def run(self):
        self.root.mainloop()



root = Tk()
app = App(root)
app.run()