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

        # Create an "Info" menu
        info_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Info", menu=info_menu)

        # Add items to the "Info" menu
        info_menu.add_command(label="About", command=self.showAbout)
        info_menu.add_command(label="Help", command=self.showHelp)

        self.main_frame.pack(fill=BOTH, expand=True)
        self.filters_frame.pack(fill=X, anchor=NW, padx=5)
        self.product_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.category_filter.pack(side=LEFT)
        self.category_filter_frame.pack(side=LEFT, padx=5)

        self.add_product_frame.pack(side=LEFT)
        self.add_product_button.pack(side=LEFT,padx=5)
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

        self.add_product_frame = Frame(self.filters_frame)
        self.add_product_button = Button(self.add_product_frame,text="Add Product",command=self.openAddWindow)

        # Create a new LabelFrame for the search controls
        search_frame = LabelFrame(self.filters_frame, text="Search")
        search_frame.pack(side=RIGHT, padx=10)

        # Define the categories
        categories = ['All', 'Title', 'Price', 'Stock', 'Brand', 'Category', 'Placement']

        # Create a StringVar for the selected category
        self.selected_category = StringVar()
        self.selected_category.set(categories[0])  # Set the default category to 'All'

        # Create an OptionMenu for category selection
        category_menu = OptionMenu(search_frame, self.selected_category, *categories)
        category_menu.pack(side=LEFT, padx=10)

        # Create an Entry widget for the search query
        self.search_query = Entry(search_frame)
        self.search_query.pack(side=LEFT, padx=10)

        # Create a search button
        search_button = Button(search_frame, text="Search", command=self.setCategory)
        search_button.pack(side=LEFT, padx=10)


    def setCategory(self, event = None):
        self.category = self.category_filter.get()
        print(self.category)
        self.getProducts()

    def sort_column(self, col, reverse):
        l = [(int(self.tree.item(k, 'text')), k) if col == "#0" else (self.tree.set(k, col), k) for k in self.tree.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)

        # reverse sort next time
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse) if col != "#0" else self.sort_column("#0", not reverse))
    def setupTreeView(self, root):
        self.tree = ttk.Treeview(self.product_frame,
                                columns=("Title", "Price", "Stock", "Brand", "Category", "Placement"))
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
        self.tree.column("Placement", minwidth=50, width=100, stretch=False)  # Placement column moved to the end

        # Add horizontal scrollbar to the Treeview widget
        self.hsb = ttk.Scrollbar(self.product_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.hsb.set)
        self.tree.bind("<Double-1>", self.openProductWindow)

    def getProducts(self):
        self.tree.delete(*self.tree.get_children())
        self.formatted_products = []  # Define a new list to store the formatted products
        for product in products:
            # Check if the search query is in any of the product fields
            if (self.category == "" or product["category"] == self.category) and (self.search_query is None or any(self.search_query.get().lower() in str(value).lower() for value in product.values())):
                # Generate random placement
                formatted_product = (
                    product["title"],
                    product["price"],
                    product["stock"],
                    product["brand"],
                    product["category"],
                    product["placement"],
                    product['images']
                )
                self.formatted_products.append(formatted_product)  # Append the formatted product to the list
                self.tree.insert('', 'end', text=int(product["id"]), values=(product["title"], product["price"], product["stock"], product["brand"], product["category"], product["placement"],product['images']))
        return self.formatted_products  # Return the list of formatted products


    def openProductWindow(self, event):
        item_id = self.tree.focus()
        if item_id:
            # Retrieve the actual index of the item in the list
            item_index = self.tree.index(item_id)
            # Retrieve the item data
            product = self.formatted_products[item_index]
            if product:
                print(product)
                self.new_window = Toplevel()
                self.new_window.title("Add product")  # Assuming the first value is the title
                self.new_window.geometry('400x480')
                self.new_window.resizable(False, False)  # Make the window non-resizable

                info_frame = LabelFrame(self.new_window, text="Info")
                info_frame.pack(side=TOP, anchor=NW, fill=X, padx=10, pady=10)
                info_frame.grid_columnconfigure(1, weight=1)  # Add this line

                labels = ['Title', 'Price', 'Stock', 'Brand', 'Category' , 'Placement']

                # Initialize the dictionary to store the Entry widgets
                self.entries = {}

                for i, label_text in enumerate(labels):
                    label = Label(info_frame, text=f"{label_text}:")
                    label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
                    entry = Entry(info_frame)
                    entry.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
                    entry.insert(0, self.formatted_products[item_index][i])
                    self.entries[label_text.lower()] = entry
                image_frame = LabelFrame(self.new_window, text="Images")
                image_frame.pack(side= TOP, fill=BOTH, padx=10, pady=10, expand=True)
                image_frame.grid_rowconfigure(0, weight=1)  # Set the weight of the row containing the images to 1

                scrollbar = Scrollbar(image_frame, orient=HORIZONTAL)
                scrollbar.pack(side=BOTTOM, fill=X)

                # Create a canvas and a frame inside the canvas
                canvas = Canvas(image_frame, width=380, height=100, xscrollcommand=scrollbar.set)
                frame = Frame(canvas)
                scrollbar.config(command=canvas.xview)
                canvas.create_window((0, 0), window=frame, anchor="nw")
                save_button = Button(self.new_window, text="Save", command=self.saveProduct)
                save_button.pack(side=BOTTOM,pady=10)



                # Add image labels to the frame
                img_labels = []
                img_width = 0
                img_height = 0
                for i, image_url in enumerate(self.formatted_products[item_index][6]):
                    response = requests.get(image_url)
                    img_data = response.content
                    img = Image.open(io.BytesIO(img_data))
                    img.thumbnail((100, 200))  # Resize the image to fit the frame
                    img = ImageTk.PhotoImage(img)
                    img_label = Label(frame, image=img)
                    img_label.image = img  # Keep a reference to the image object
                    img_label.grid(row=0, column=i, padx=5, pady=5)  # Use grid for the image labels
                    img_labels.append(img_label)
                    img_width += img.width()  # Add the width of the image to the total width
                    img_height = max(img_height, img.height())  # Update the maximum height

                # Update the scroll region of the canvas
                canvas.config(scrollregion=(0, 0, img_width + 100, img_height))
                # Update the width of the canvas
                canvas.config(width=img_width)
                canvas.pack(side=LEFT, fill=BOTH, expand=True)


    def openAddWindow(self):
        self.new_window = Toplevel()
        self.new_window.title("Add product")
        self.new_window.geometry('400x480')
        self.new_window.resizable(False, False)

        info_frame = LabelFrame(self.new_window, text="Info")
        info_frame.pack(side=TOP, anchor=NW, fill=X, padx=10, pady=10)

        info_frame.grid_columnconfigure(1, weight=1)  # Add this line

        labels = ['Title', 'Price', 'Stock', 'Brand', 'Category' , 'Placement']

        # Initialize the dictionary to store the Entry widgets
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = Label(info_frame, text=f"{label_text}:")
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = Entry(info_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
            self.entries[label_text.lower()] = entry

        image_frame = LabelFrame(self.new_window, text="Images")
        image_frame.pack(side=TOP, fill=BOTH, padx=10, pady=10, expand=True)
        image_frame.grid_rowconfigure(0, weight=1)  # Set the weight of the row containing the images to 1
        canvas = Canvas(image_frame, width=380, height=100)
        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.config(scrollregion=(0, 0, 380, 100))
        # Update the width of the canvas
        canvas.config(width=380)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        buttons_frame = Frame(self.new_window)
        buttons_frame.pack(side=BOTTOM,anchor=S,fill=X,padx=10,pady=10)
        add_photos_button = Button(buttons_frame,text="Add Photos",command=self.loadPhotos)
        add_photos_button.pack()
        add_button = Button(buttons_frame,text="Add product", command=self.addProduct)
        add_button.pack()
        

    def addProduct(self):
        title = self.entries['title'].get()
        price = self.entries['price'].get()
        stock = self.entries['stock'].get()
        brand = self.entries['brand'].get()
        category = self.entries['category'].get()
        placement = self.entries['placement'].get()

        # Create a new product
        new_product = {
            "id": len(products) + 1,  # Add this line
            "title": title,
            "price": price,
            "stock": stock,
            "brand": brand,
            "category": category,
            "placement": placement,
            "images": []  # You can add functionality to add images later
        }

        # Add the new product to the products list
        products.append(new_product)

        # Refresh the product list
        self.getProducts()

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
