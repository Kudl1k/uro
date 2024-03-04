from tkinter import *
import tkinter.font
from tkinter import messagebox
from tkinter import ttk
import requests
import json


response_API = requests.get('https://dummyjson.com/products?limit=100')
print(response_API.status_code)
products = json.loads(response_API.text)['products']

class myApp:
    category = ""
    def __init__(self,root):
        root.title('Shop system')
        root.resizable(True, True)
        root.geometry('640x480')
        root.minsize(640,480)
        self.main_frame = Frame(root)
        self.filters_frame = Frame(self.main_frame)
        self.setupFilters(root)
        self.product_frame = LabelFrame(self.main_frame,text="Products")
        self.setupTreeView(root)

             

        self.main_frame.pack(fill=BOTH,expand=True)
        self.filters_frame.pack(fill=X,anchor=NW,padx=5)
        self.product_frame.pack(fill=BOTH,expand=True,padx=10,pady=10)
        self.category_filter.pack(side=LEFT)
        self.category_filter_frame.pack(side=LEFT,padx=5)
        self.sort_type_filter.pack(side=LEFT)
        self.sort_type_filter_frame.pack(side=LEFT,padx=5)
        self.tree.pack(fill=BOTH, expand=True)
        self.hsb.pack(side="bottom", fill="x")

    def setupFilters(self,root):
        self.categories = sorted(set([x["category"] for x in products]), key=lambda x: x.lower())
        self.categories.insert(0, "")

        self.category_filter_frame = LabelFrame(self.filters_frame,text="Category")
        self.category_filter = ttk.Combobox(
            self.category_filter_frame,
            state = "readonly",
            values= self.categories,
        )
        self.category_filter.bind("<<ComboboxSelected>>", self.setCategory)

        self.sort_type = ["Ascending","Descending"]
        self.sort_type.insert(0, "")

        self.sort_type_filter_frame = LabelFrame(self.filters_frame,text="Sort type")
        self.sort_type_filter = ttk.Combobox(
            self.sort_type_filter_frame,
            state = "readonly",
            values= self.sort_type,
        )
        self.category_filter.bind("<<ComboboxSelected>>", self.setCategory)

        

        
    def setCategory(self,event):
        self.category = self.category_filter.get()
        print(self.category)
        self.getProducts()

    def setupTreeView(self,root):
        self.tree = ttk.Treeview(self.product_frame, columns=("Title", "Description", "Price", "Rating", "Stock", "Brand", "Category"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Rating", text="Rating")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Brand", text="Brand")
        self.tree.heading("Category", text="Category")

        self.getProducts()

        self.tree.column("#0", minwidth=50, width=50,stretch=False)
        self.tree.column("Title", minwidth=100,width=100)
        self.tree.column("Description", minwidth=100,width=100)
        self.tree.column("Price", minwidth=50,width=50,stretch=False)
        self.tree.column("Rating", minwidth=50,width=50,stretch=False)
        self.tree.column("Stock", minwidth=50,width=50,stretch=False)
        self.tree.column("Brand", minwidth=50,width=50)
        self.tree.column("Category", minwidth=50,width=100)


        # Add horizontal scrollbar to the Treeview widget
        self.hsb = ttk.Scrollbar(self.product_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.hsb.set)
        self.tree.bind("<<TreeviewOpen>>", self.openProductWindow)


    def getProducts(self):
        self.tree.delete(*self.tree.get_children())
        for product in products:
            if self.category == "" or product["category"] == self.category:
                self.tree.insert("", END, text=product["id"], values=(
                    product["title"],
                    product["description"],
                    product["price"],
                    product["rating"],
                    product["stock"],
                    product["brand"],
                    product["category"]
                ))
    def openProductWindow(self, event):
        print("called")
        item = self.tree.selection()[0]
        product_id = self.tree.item(item, "text")
        product = next((p for p in products if p["id"] == product_id), None)
        if product:
            new_window = Toplevel()
            new_window.title(f"Product: {product['title']}")
            new_window.geometry('400x300')
            new_window.resizable(True, True)
            new_window.minsize(400, 300)
            
            # Add labels and entry widgets for the product details
            for i, (key, value) in enumerate(product.items()):
                label = Label(new_window, text=f"{key}:")
                label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
                entry = Entry(new_window, state="readonly")
                entry.insert(END, value)
                entry.grid(row=i, column=1, sticky="w", padx=10, pady=5)

root = Tk()
app = myApp(root)
root.mainloop()