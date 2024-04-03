from tkinter import *
from tkinter import ttk

class App:

    def __init__(self, root):
        self.root = root
        self.root.title("My Tkinter App")
        self.tree_values = []
        self.createTable()
        self.createForm()
        self.createButtons()       

    def createTable(self):
        self.tree = ttk.Treeview(self.root, columns=('first name', 'last name', 'birth number'), show='headings')
        self.tree.heading('first name', text='First Name')  # Corrected column name
        self.tree.heading('last name', text='Last Name')  # Corrected column name
        self.tree.heading('birth number', text='Birth Number')  # Corrected column name
        self.tree.insert("", END, values=("John", "Roe", "045216/1512"))
        self.tree.insert("", END, values=("Jane", "Doe", "901121/7238"))
        self.tree.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)
        self.tree.bind("<<TreeviewSelect>>", self.itemSelected)


    def createForm(self):
        self.form_frame = ttk.Frame(self.root)
        self.form_frame.grid(row=1, column=0, columnspan=2, pady=(5, 0))
        # Name   
        name_label = ttk.Label(self.form_frame, text="Name:")
        name_label.grid(row=0, column=0, sticky="e")
        self.name_entry = ttk.Entry(self.form_frame)
        self.name_entry.grid(row=0, column=1, sticky="ew")

        # Surname
        surname_label = ttk.Label(self.form_frame, text="Surname:")
        surname_label.grid(row=1, column=0, sticky="e")  # Change row to 1
        self.surname_entry = ttk.Entry(self.form_frame)
        self.surname_entry.grid(row=1, column=1, sticky="ew")  # Change row to 1

        # Birth Number
        birth_number_label = ttk.Label(self.form_frame, text="Birth Number:")
        birth_number_label.grid(row=2, column=0, sticky="e")  # Change row to 2
        self.birth_number_entry = ttk.Entry(self.form_frame)
        self.birth_number_entry.grid(row=2, column=1, sticky="ew")  # Change row to 2

        # Address Notebook
        address_notebook_frame = Frame(self.root)
        address_notebook_frame.grid(row=2, column=0, columnspan=2,sticky='nsew', pady=(0, 5))

        address_notebook = ttk.Notebook(address_notebook_frame)
        address_notebook.pack(fill='both',expand=True)
        # Address Frame
        address_frame = ttk.Frame(address_notebook)
        address_notebook.add(address_frame, text="Address")

        address_frame_cont = LabelFrame(address_frame,text="Address")
        address_frame_cont.pack(pady=10)



        # Street
        street_label = ttk.Label(address_frame_cont, text="Street:")
        street_label.grid(row=0, column=0, sticky="e")
        self.street_entry = ttk.Entry(address_frame_cont)
        self.street_entry.grid(row=0, column=1, sticky="ew")

        # House Number
        house_number_label = ttk.Label(address_frame_cont, text="House Number:")
        house_number_label.grid(row=0, column=2, sticky="e")
        self.house_number_entry = ttk.Entry(address_frame_cont,width=6)
        self.house_number_entry.grid(row=0, column=3, sticky="w")

        # City
        city_label = ttk.Label(address_frame_cont, text="City:")
        city_label.grid(row=1, column=0, sticky="e")
        self.city_entry = ttk.Entry(address_frame_cont)
        self.city_entry.grid(row=1, column=1,columnspan=3, sticky="ew")

        # Zip Code
        zip_code_label = ttk.Label(address_frame_cont, text="Zip Code:")
        zip_code_label.grid(row=2, column=0, sticky="e")
        self.zip_code_entry = ttk.Entry(address_frame_cont,width=10)
        self.zip_code_entry.grid(row=2, column=1, sticky="w")

        # Note Frame
        note_frame = ttk.Frame(address_notebook)
        address_notebook.add(note_frame, text="Note")

        # Note
        note_frame_inner = ttk.Frame(note_frame)
        note_frame_inner.grid(row=0, column=0, sticky="w")
        note_label = ttk.Label(note_frame_inner, text="Note:")
        note_label.grid(row=0, column=0, sticky="w")
        self.note_entry = Text(note_frame_inner,height=3)
        self.note_entry.grid(row=1, column=0, sticky="e")

    def createButtons(self):  # New method to create buttons
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.grid(row=3, column=0, columnspan=2, pady=(0,5))
        
        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.clearInputs)
        self.cancel_button.grid(row=0, column=0,padx=5 )
        
        self.add_button = ttk.Button(self.button_frame, text="Add new record", command=self.addRecord)
        self.add_button.grid(row=0, column=1,padx=5 )
        
        self.save_button = ttk.Button(self.button_frame, text="Save new record", command=self.saveRecord)
        self.save_button.grid(row=0, column=2,padx=5 )


    def clearInputs(self):
        self.name_entry.delete(0, END)
        self.surname_entry.delete(0, END)
        self.birth_number_entry.delete(0, END)
        self.street_entry.delete(0, END)
        self.birth_number_entry.delete(0, END)
        self.city_entry.delete(0, END)
        self.zip_code_entry.delete(0, END)

    def clearSelect(self):
        self.tree.selection_remove(*self.tree.selection())
        root.update_idletasks()

    def addRecord(self):
        # Add new record to the tree
        self.clearInputs()
        self.clearSelect()

    def saveRecord(self):
        # Save the new record
        first_name = self.name_entry.get()
        last_name = self.surname_entry.get()
        birth_number = self.birth_number_entry.get()
        street = self.street_entry.get()
        num = self.house_number_entry.get()
        city = self.city_entry.get()
        psc = self.zip_code_entry.get()
        # Insert the values into the tree
        selected_items = self.tree.selection()
        if selected_items:
            # Update the selected item
            for item in selected_items:
                self.tree.item(item, values=(first_name, last_name, birth_number,street,num,city,psc))
        else:
            self.tree.insert('', END, values=(first_name, last_name, birth_number,street,num,city,psc))
        self.clear_text_boxes()


    def itemSelected(self, event):
        selected_item = self.tree.focus()
        item_values = self.tree.item(selected_item)['values']
        if item_values:
            self.name_entry.delete(0, END)
            self.surname_entry.delete(0, END)
            self.birth_number_entry.delete(0, END)

            self.name_entry.insert(0, item_values[0])
            self.surname_entry.insert(0, item_values[1])
            self.birth_number_entry.insert(0, item_values[2])

    def run(self):
        self.root.mainloop()

root = Tk()
app = App(root)
app.run()
