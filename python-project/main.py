import io
from tkinter import *
import tkinter.font
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from data import *
from PIL import Image, ImageTk
import random
import string
import re


class myApp:
    category = ""

    def __init__(self, root):
        root.title('Shop system')
        root.resizable(True, True)
        root.geometry('800x480')
        root.minsize(800, 480)
        self.main_frame = Frame(root)
        self.filters_frame = Frame(self.main_frame)
        self.setup_filters(root)
        self.product_frame = LabelFrame(self.main_frame, text="Products")
        self.setupTreeView(root)
        menu_bar = Menu(root)
        root.config(menu=menu_bar)
        self.highest_id = len(products) + 1

        info_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Info", menu=info_menu)

        info_menu.add_command(label="About", command=self.showAbout)
        info_menu.add_command(label="Help", command=self.showHelp)

        self.main_frame.pack(fill=BOTH, expand=True)
        self.filters_frame.pack(fill=X, anchor=NW, padx=5)
        self.product_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.category_filter.pack(side=LEFT)
        self.category_filter_frame.pack(side=LEFT, padx=5)

        self.add_product_button_label.pack(side=RIGHT,fill=Y)
        self.add_product_button.pack(side=RIGHT,padx=10)

        self.tree.pack(fill=BOTH, expand=True)
        self.hsb.pack(side="bottom", fill="x")

    def showAbout(self):
        messagebox.showinfo("About", "Creator of this app is KUD0132")

    def showHelp(self):
        messagebox.showinfo("Help", "No help for you :)")


    def setup_filters(self, root):
        self.categories = sorted(set([x["category"] for x in products]), key=lambda x: x.lower())
        self.categories.insert(0, "")

        self.category_filter_frame = LabelFrame(self.filters_frame, text="Category")
        self.category_filter = ttk.Combobox(
            self.category_filter_frame,
            state="readonly",
            values=self.categories,
        )
        self.category_filter.bind("<<ComboboxSelected>>", self.setCategory)
        self.add_product_button_label = Label(self.filters_frame)
        self.add_product_button = Button(self.add_product_button_label,text="Add Product",command=self.openAddWindow)

        search_frame = LabelFrame(self.filters_frame, text="Search")
        search_frame.pack(side=LEFT, padx=10)

        categories = ['All', 'Title', 'Price', 'Stock', 'Brand', 'Category', 'Placement']

        self.selected_category = StringVar()
        self.selected_category.set(categories[0])

   
        category_menu = OptionMenu(search_frame, self.selected_category, *categories)
        category_menu.pack(side=LEFT, padx=10)

        self.search_query = Entry(search_frame)
        self.search_query.pack(side=LEFT, padx=10)

        search_button = Button(search_frame, text="Search", command=self.setCategory)
        search_button.pack(side=LEFT, padx=10)


    def setCategory(self, event = None):
        self.category = self.category_filter.get()
        print(self.category)
        self.getProducts()

    def sort_column(self, col, reverse):
        l = [(int(self.tree.item(k, 'text')), k) if col == "#0" else (self.tree.set(k, col), k) for k in self.tree.get_children('')]
        l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)

        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse) if col != "#0" else self.sort_column("#0", not reverse))
    def setupTreeView(self, root):
        self.tree = ttk.Treeview(self.product_frame, columns=("Title", "Price", "Stock", "Brand", "Category", "Placement"))
        self.tree.heading("#0", text="ID", command=lambda: self.sort_column("#0", False))
        self.tree.heading("Title", text="Title", command=lambda: self.sort_column("Title", False))
        self.tree.heading("Price", text="Price", command=lambda: self.sort_column("Price", False))
        self.tree.heading("Stock", text="Stock", command=lambda: self.sort_column("Stock", False))
        self.tree.heading("Brand", text="Brand", command=lambda: self.sort_column("Brand", False))
        self.tree.heading("Category", text="Category", command=lambda: self.sort_column("Category", False))
        self.tree.heading("Placement", text="Placement", command=lambda: self.sort_column("Placement", False))

        self.getProducts()

        self.tree.column("#0", minwidth=50, width=50, stretch=False)
        self.tree.column("Title", minwidth=100, width=100)
        self.tree.column("Price", minwidth=50, width=50, stretch=False)
        self.tree.column("Stock", minwidth=50, width=50, stretch=False)
        self.tree.column("Brand", minwidth=50, width=50)
        self.tree.column("Category", minwidth=100, width=100,stretch=False)
        self.tree.column("Placement", minwidth=50, width=100, stretch=False) 

        self.hsb = ttk.Scrollbar(self.product_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.hsb.set)
        self.tree.bind("<Double-1>", self.openProductWindow)

    def getProducts(self):
        self.tree.delete(*self.tree.get_children())
        self.formatted_products = [] 
        for product in products:
            if (self.category == "" or product["category"] == self.category) and (self.search_query is None or any(self.search_query.get().lower() in str(value).lower() for value in product.values())):
                formatted_product = (
                    product['index'],
                    product['id'],
                    product["title"],
                    product["price"],
                    product["stock"],
                    product["brand"],
                    product["category"],
                    product["placement"],
                    product['images']
                )
                self.formatted_products.append(formatted_product) 
                self.tree.insert('', 'end', text=int(product["id"]), values=(product["title"], product["price"], product["stock"], product["brand"], product["category"], product["placement"],product['images'],int(product['index'])))
        return self.formatted_products 


    def openProductWindow(self, event):
        item_id = self.tree.focus()
        print(item_id)
        if item_id:
            item = self.tree.item(item_id)
            print(item)
            item_index = item['values'][7]
            product = products[item_index]
            if product:
                print(product)
                self.selected_product = product
                self.new_window = Toplevel()
                self.new_window.title("Edit product")
                self.new_window.geometry('400x480')
                self.new_window.resizable(False, False)

                info_frame = LabelFrame(self.new_window, text="Info")
                info_frame.pack(side=TOP, anchor=NW, fill=X, padx=10, pady=10)
                info_frame.grid_columnconfigure(1, weight=1)

                labels = ['Title', 'Price', 'Stock', 'Brand', 'Category' , 'Placement']
                self.entries = {}

                for i, label_text in enumerate(labels):
                    label = Label(info_frame, text=f"{label_text}:")
                    label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
                    entry = Entry(info_frame)
                    entry.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
                    entry.insert(0, products[item_index][label_text.lower()])
                    self.entries[label_text.lower()] = entry

                add_photos_button = Button(self.new_window,text="Edit Photos",command=self.loadPhotos)
                add_photos_button.pack(side=TOP)
                image_frame = LabelFrame(self.new_window, text="Images")
                image_frame.pack(side= TOP, fill=BOTH, padx=10, pady=10, expand=True)
                image_frame.grid_rowconfigure(0, weight=1) 

                scrollbar = Scrollbar(image_frame, orient=HORIZONTAL)
                scrollbar.pack(side=BOTTOM, fill=X)
                
                canvas = Canvas(image_frame, width=380, height=100, xscrollcommand=scrollbar.set)
                frame = Frame(canvas)
                scrollbar.config(command=canvas.xview)
                canvas.create_window((0, 0), window=frame, anchor="nw")
                buttons_frame = Frame(self.new_window)
                buttons_frame.pack(side=BOTTOM)
                save_button = Button(buttons_frame, text="Save", command=self.saveProduct,width=10)
                save_button.pack(side=LEFT,pady=10,padx=5)
                remove_button = Button(buttons_frame, text="Remove", command=self.removeProduct,width=10)
                remove_button.pack(side=RIGHT, pady=10,padx=5)



                img_labels = []
                img_width = 0
                img_height = 0
                for i, image_url in enumerate(products[item_index]['images']):
                    response = requests.get(image_url)
                    img_data = response.content
                    img = Image.open(io.BytesIO(img_data))
                    img.thumbnail((100, 200)) 
                    img = ImageTk.PhotoImage(img)
                    img_label = Label(frame, image=img)
                    img_label.image = img 
                    img_label.grid(row=0, column=i, padx=5, pady=5)
                    img_labels.append(img_label)
                    img_width += img.width()
                    img_height = max(img_height, img.height())

                canvas.config(scrollregion=(0, 0, img_width + 100, img_height))
                canvas.config(width=img_width)
                canvas.pack(side=LEFT, fill=BOTH, expand=True)
    def removeProduct(self):
        if self.selected_product:
            confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete this product?")
            if confirm:
                products.remove(self.selected_product)
                self.getProducts()
                messagebox.showinfo("Success", "Product successfully deleted")
                self.new_window.destroy()


    def openAddWindow(self):
        self.new_window = Toplevel()
        self.new_window.title("Add product")
        self.new_window.geometry('400x480')
        self.new_window.resizable(False, False)

        info_frame = LabelFrame(self.new_window, text="Info")
        info_frame.pack(side=TOP, anchor=NW, fill=X, padx=10, pady=10)

        info_frame.grid_columnconfigure(1, weight=1)

        labels = ['Title', 'Price', 'Stock', 'Brand', 'Category' , 'Placement']

        self.entries = {}

        for i, label_text in enumerate(labels):
            label = Label(info_frame, text=f"{label_text}:")
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = Entry(info_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
            self.entries[label_text.lower()] = entry

        self.entries['title'].insert(0,'New Product')
        self.entries['price'].insert(0,'100')
        self.entries['stock'].insert(0,'100')
        self.entries['brand'].insert(0,'Apple')
        self.entries['category'].insert(0,'smartphones')
        self.entries['placement'].insert(0,'A1')

        add_photos_button = Button(self.new_window,text="Add Photos",command=self.loadPhotos)
        add_photos_button.pack(side=TOP)
        image_frame = LabelFrame(self.new_window, text="Images")
        image_frame.pack(side=TOP, fill=BOTH, padx=10, pady=10, expand=True)
        image_frame.grid_rowconfigure(0, weight=1)
        canvas = Canvas(image_frame, width=380, height=100)
        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.config(scrollregion=(0, 0, 380, 100))

        canvas.config(width=380)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        buttons_frame = Frame(self.new_window)
        buttons_frame.pack(side=BOTTOM,anchor=S,fill=X,padx=10,pady=10)
        add_button = Button(buttons_frame,text="Add product", command=self.addProduct)
        add_button.pack()
        

    def addProduct(self):
        title = self.entries['title'].get()
        if title == "":
            messagebox.showerror("Error", "Title should not be empty")
            return
        price = self.entries['price'].get()
        try:
            float(price)
        except ValueError:
            messagebox.showerror("Invalid Price", "Please enter a valid number for price.")
        
        stock = self.entries['stock'].get()
        try:
            float(stock)
        except ValueError:
            messagebox.showerror("Invalid Stock", "Please enter a valid number for stock.")
        brand = self.entries['brand'].get()
        if brand == "":
            messagebox.showerror("Error", "Brand should not be empty")
            return
        category = self.entries['category'].get()
        if category == "":
            messagebox.showerror("Error", "Category should not be empty")
            return
        placement = self.entries['placement'].get()
        if not re.match("^[A-D][1-5]$", placement):
            messagebox.showerror("Error", "Placement shoudl start with letter from A-D and end with number from 1-5")
            return


        new_product = {
            "index": len(products),
            "id": self.highest_id,
            "title": title,
            "price": price,
            "stock": stock,
            "brand": brand,
            "category": category,
            "placement": placement,
            "images": []
        }
        
        self.highest_id += 1


        products.append(new_product)

        self.getProducts()
        self.new_window.destroy()

    def saveProduct(self):
        item_id = self.tree.focus()
        if item_id:
            item_index = self.tree.index(item_id)
            product = products[item_index]
            if product:
                product["title"] = self.entries['title'].get()
                product["price"] = self.entries['price'].get()
                product["stock"] = self.entries['stock'].get()
                product["brand"] = self.entries['brand'].get()
                product["category"] = self.entries['category'].get()
                product["placement"] = self.entries['placement'].get()
                self.getProducts()
                self.new_window.destroy()

    def loadPhotos(self):
        file_paths = filedialog.askopenfilenames(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg')])
        messagebox.showerror("Error", "Could not load the files")


root = Tk()
app = myApp(root)
root.mainloop()
