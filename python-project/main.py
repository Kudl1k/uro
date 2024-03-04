import io
from tkinter import *
import tkinter.font
from tkinter import messagebox
from tkinter import ttk
from data import *
from PIL import Image, ImageTk


class myApp:
    category = ""

    def __init__(self, root):
        root.title('Shop system')
        root.resizable(True, True)
        root.geometry('640x480')
        root.minsize(640, 480)
        self.main_frame = Frame(root)
        self.filters_frame = Frame(self.main_frame)
        self.setup_filters(root)
        self.product_frame = LabelFrame(self.main_frame, text="Products")
        self.setupTreeView(root)

        self.main_frame.pack(fill=BOTH, expand=True)
        self.filters_frame.pack(fill=X, anchor=NW, padx=5)
        self.product_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.category_filter.pack(side=LEFT)
        self.category_filter_frame.pack(side=LEFT, padx=5)
        self.sort_type_filter.pack(side=LEFT)
        self.sort_type_filter_frame.pack(side=LEFT, padx=5)
        self.tree.pack(fill=BOTH, expand=True)
        self.hsb.pack(side="bottom", fill="x")

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

        self.sort_type = ["Ascending", "Descending"]
        self.sort_type.insert(0, "")

        self.sort_type_filter_frame = LabelFrame(self.filters_frame, text="Sort type")
        self.sort_type_filter = ttk.Combobox(
            self.sort_type_filter_frame,
            state="readonly",
            values=self.sort_type,
        )
        self.category_filter.bind("<<ComboboxSelected>>", self.setCategory)

    def setCategory(self, event):
        self.category = self.category_filter.get()
        print(self.category)
        self.getProducts()

    def setupTreeView(self, root):
        self.tree = ttk.Treeview(self.product_frame,
                                 columns=("Title", "Description", "Price", "Rating", "Stock", "Brand", "Category"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Rating", text="Rating")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Brand", text="Brand")
        self.tree.heading("Category", text="Category")

        self.getProducts()

        self.tree.column("#0", minwidth=50, width=50, stretch=False)
        self.tree.column("Title", minwidth=100, width=100)
        self.tree.column("Description", minwidth=100, width=100)
        self.tree.column("Price", minwidth=50, width=50, stretch=False)
        self.tree.column("Rating", minwidth=50, width=50, stretch=False)
        self.tree.column("Stock", minwidth=50, width=50, stretch=False)
        self.tree.column("Brand", minwidth=50, width=50)
        self.tree.column("Category", minwidth=50, width=100)

        # Add horizontal scrollbar to the Treeview widget
        self.hsb = ttk.Scrollbar(self.product_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.hsb.set)
        self.tree.bind("<Double-1>", self.openProductWindow)

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
        item_id = self.tree.focus()
        if item_id:
            # Retrieve the actual index of the item in the list
            item_index = self.tree.index(item_id)
            # Retrieve the item data
            product = products[item_index]
            if product:
                print(product)
                new_window = Toplevel()
                new_window.title(f"Product: {product['title']}")  # Assuming the first value is the title
                new_window.geometry('400x480')
                new_window.resizable(False, False)  # Make the window non-resizable

                info_frame = LabelFrame(new_window, text="Info")
                info_frame.pack(side=TOP, anchor=NW, fill=X, padx=10, pady=10)

                # Define the labels for the product details
                labels = ['Title', 'Description', 'Price', 'Rating', 'Stock', 'Brand', 'Category']

                # Add labels and entry widgets for the product details
                for i, label_text in enumerate(labels):
                    label = Label(info_frame, text=f"{label_text}:")
                    label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
                    # Use StringVar for the Entry widget
                    value_var = StringVar()
                    value_var.set(product[label_text.lower()])
                    entry = Entry(info_frame, textvariable=value_var, state="readonly")
                    entry.grid(row=i, column=1, sticky="w", padx=10, pady=5)

                image_frame = LabelFrame(new_window, text="Images")
                image_frame.pack(side=BOTTOM, fill=BOTH, padx=10, pady=10, expand=True)
                image_frame.grid_rowconfigure(0, weight=1)  # Set the weight of the row containing the images to 1

                scrollbar = Scrollbar(image_frame, orient=HORIZONTAL)
                scrollbar.pack(side=BOTTOM, fill=X)

                # Create a canvas and a frame inside the canvas
                canvas = Canvas(image_frame, width=380, height=100, xscrollcommand=scrollbar.set)
                frame = Frame(canvas)
                scrollbar.config(command=canvas.xview)
                canvas.create_window((0, 0), window=frame, anchor="nw")



                # Add image labels to the frame
                img_labels = []
                img_width = 0
                img_height = 0
                for i, image_url in enumerate(product['images']):
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
                canvas.config(scrollregion=(0, 0, img_width, img_height))
                canvas.pack(side=LEFT, fill=BOTH, expand=True)
root = Tk()
app = myApp(root)
root.mainloop()
