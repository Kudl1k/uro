#include "shopsystem.h"

ShopSystem::ShopSystem(QWidget *parent) : QMainWindow(parent)
{
    this->setWindowTitle("Shop System - KUD0132");
    this->setMinimumSize(1280, 720);
    this->move(100, 100);
    generateProducts();
    QWidget *centralWidget = new QWidget(this);
    mainlayout = new QVBoxLayout(centralWidget);
    setup_menubar();
    setup_header();
    setup_table();
    fillTableWithProducts();
    this->setCentralWidget(centralWidget);
}

void ShopSystem::showAlert(const QString &message)
{
    QMessageBox::information(this, "Alert", message);
}

int ShopSystem::getNextId()
{
    return products.size() + 1;
}

void ShopSystem::generateProducts()
{
    this->products.push_back(Product(1, "iPhone 9", 549, 94, "Apple", "smartphones", "A1"));
    this->products.push_back(Product(2, "iPhone X", 899, 34, "Apple", "smartphones", "A2"));
    this->products.push_back(Product(3, "Samsung Universe 9", 1249, 36, "Samsung", "smartphones", "A3"));
    this->products.push_back(Product(4, "OPPOF19", 280, 123, "OPPO", "smartphones", "A4"));
    this->products.push_back(Product(5, "Huawei P30", 499, 32, "Huawei", "smartphones", "B1"));
    this->products.push_back(Product(6, "MacBook Pro", 1749, 83, "Apple", "laptops", "B2"));
    this->products.push_back(Product(7, "Samsung Galaxy Book", 1499, 50, "Samsung", "laptops", "B3"));
    this->products.push_back(Product(8, "Microsoft Surface Laptop 4", 1499, 68, "Microsoft Surface", "laptops", "B4"));
    this->products.push_back(Product(9, "Infinix INBOOK", 1099, 96, "Infinix", "laptops", "C1"));
    this->products.push_back(Product(10, "HP Pavilion 15-DK1056WM", 1099, 89, "HP Pavilion", "laptops", "C2"));
}

void ShopSystem::setup_menubar()
{
    QMenuBar *menu = this->menuBar();
    QMenu *navigation = menu->addMenu("Info");
    QAction *alertAction = new QAction("Alert", this);
    connect(alertAction, &QAction::triggered, this, [=]()
            { this->showAlert("This project was created by KUD0132"); });
    navigation->addAction(alertAction);
}

void ShopSystem::setup_header()
{
    headerlayout = new QHBoxLayout();
    setup_search();
    headerlayout->addItem(new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum));
    setup_category();
    headerlayout->addStretch(1);
    QPushButton *addProduct = new QPushButton("Add Product");
    headerlayout->addWidget(addProduct);
    mainlayout->addLayout(headerlayout);

    connect(addProduct, &QPushButton::clicked, this, &ShopSystem::openAddProductWindow);
}

void ShopSystem::setup_search()
{
    QHBoxLayout *searchlayout = new QHBoxLayout();

    searchComboBox = new QComboBox();
    searchComboBox->addItem("title");
    searchComboBox->addItem("price");
    searchComboBox->addItem("stock");
    searchComboBox->addItem("brand");
    searchComboBox->addItem("category");
    searchComboBox->addItem("placement");
    searchComboBox->addItem("id");
    searchComboBox->setMaximumWidth(100);
    searchlayout->addWidget(searchComboBox);

    searchbox = new QLineEdit();
    searchbox->setPlaceholderText("Search...");
    searchbox->setMinimumWidth(200);
    searchbox->setMaximumWidth(300);
    searchlayout->addWidget(searchbox);

    QToolButton *searchButton = new QToolButton();
    searchButton->setText("Search");
    searchlayout->addWidget(searchButton);

    headerlayout->addLayout(searchlayout);

    connect(searchButton, &QPushButton::clicked, this, &ShopSystem::performSearch);
}

void ShopSystem::setup_category()
{
    QHBoxLayout *categorylayout = new QHBoxLayout();

    QLabel *categorylabel = new QLabel("Category: ");
    categorylayout->addWidget(categorylabel);
    QComboBox *categoryComboBox = new QComboBox();
    categoryComboBox->addItem("");
    categoryComboBox->addItem("id");
    categoryComboBox->addItem("title");
    categoryComboBox->addItem("price");
    categoryComboBox->addItem("stock");
    categoryComboBox->addItem("brand");
    categoryComboBox->addItem("category");
    categoryComboBox->addItem("placement");
    categorylayout->addWidget(categoryComboBox);

    headerlayout->addLayout(categorylayout);
}

void ShopSystem::setup_table()
{
    QTableView *tableView = new QTableView(this);

    model = new QStandardItemModel(0, 7, this);
    model->setHeaderData(0, Qt::Horizontal, tr("id"));
    model->setHeaderData(1, Qt::Horizontal, tr("title"));
    model->setHeaderData(4, Qt::Horizontal, tr("brand"));
    model->setHeaderData(5, Qt::Horizontal, tr("category"));
    model->setHeaderData(6, Qt::Horizontal, tr("placement"));

    tableView->setModel(model);

    tableView->setColumnWidth(0, 75);
    tableView->horizontalHeader()->setSectionResizeMode(1, QHeaderView::Stretch);
    tableView->setColumnWidth(2, 75);
    tableView->setColumnWidth(3, 75);
    tableView->horizontalHeader()->setSectionResizeMode(4, QHeaderView::Stretch);
    tableView->horizontalHeader()->setSectionResizeMode(5, QHeaderView::Stretch);
    tableView->setColumnWidth(6, 75);
    connect(tableView, &QTableView::doubleClicked, this, &ShopSystem::openEditProductWindow);
    mainlayout->addWidget(tableView);
}

void ShopSystem::fillTableWithProducts()
{
    model->removeRows(0, model->rowCount());

    for (const auto &product : products)
    {
        QStandardItem *idItem = new QStandardItem(QString::number(product.getId()));
        QStandardItem *titleItem = new QStandardItem(QString::fromStdString(product.getTitle()));
        QStandardItem *priceItem = new QStandardItem(QString::number(product.getPrice()));
        QStandardItem *stockItem = new QStandardItem(QString::number(product.getStock()));
        QStandardItem *brandItem = new QStandardItem(QString::fromStdString(product.getBrand()));
        QStandardItem *categoryItem = new QStandardItem(QString::fromStdString(product.getCategory()));
        QStandardItem *placementItem = new QStandardItem(QString::fromStdString(product.getPlacement()));

        QList<QStandardItem *> items = {idItem, titleItem, priceItem, stockItem, brandItem, categoryItem, placementItem};
        model->appendRow(items);
    }
}

void ShopSystem::fillTableWithProducts(const QString &query)
{
    model->removeRows(0, model->rowCount());
    QString selectedColumn = searchComboBox->currentText();

    for (const Product &product : products)
    {
        QString productAttribute;

        if (selectedColumn == "title")
        {
            productAttribute = QString::fromStdString(product.getTitle());
        }
        else if (selectedColumn == "brand")
        {
            productAttribute = QString::fromStdString(product.getBrand());
        }
        else if (selectedColumn == "category")
        {
            productAttribute = QString::fromStdString(product.getCategory());
        }
        else if (selectedColumn == "placement")
        {
            productAttribute = QString::fromStdString(product.getPlacement());
        }
        else if (selectedColumn == "id")
        {
            productAttribute = QString::fromStdString(std::to_string(product.getId()));
        }
        if (productAttribute.toLower().contains(query.toLower()))
        {
            QStandardItem *idItem = new QStandardItem(QString::number(product.getId()));
            QStandardItem *titleItem = new QStandardItem(QString::fromStdString(product.getTitle()));
            QStandardItem *priceItem = new QStandardItem(QString::number(product.getPrice()));
            QStandardItem *stockItem = new QStandardItem(QString::number(product.getStock()));
            QStandardItem *brandItem = new QStandardItem(QString::fromStdString(product.getBrand()));
            QStandardItem *categoryItem = new QStandardItem(QString::fromStdString(product.getCategory()));
            QStandardItem *placementItem = new QStandardItem(QString::fromStdString(product.getPlacement()));

            QList<QStandardItem *> items = {idItem, titleItem, priceItem, stockItem, brandItem, categoryItem, placementItem};
            model->appendRow(items);
        }
    }
}

void ShopSystem::addProduct(Product *product)
{
    products.push_back(*product);
}

void ShopSystem::editProduct(Product *product, std::string title, double price, int stock, std::string brand, std::string category, std::string placement)
{
    product->setTitle(title);
    product->setPrice(price);
    product->setStock(stock);
    product->setBrand(brand);
    product->setCategory(category);
    product->setPlacement(placement);
}

void ShopSystem::openAddProductWindow()
{
    addProductDialog = new AddProductDialog(this, this);
    addProductDialog->setAttribute(Qt::WA_DeleteOnClose, true);
    connect(addProductDialog, &QDialog::finished, addProductDialog, &QObject::deleteLater);
    addProductDialog->show();
}

void ShopSystem::openEditProductWindow(const QModelIndex &index)
{
    Product *product = &products[index.row()];
    EditProductDialog *editProductDialog = new EditProductDialog(product, this, this);
    editProductDialog->show();
}

AddProductDialog::AddProductDialog(QWidget *parent, ShopSystem *s) : QDialog(parent)
{
    setWindowTitle("Add Product");
    this->setMinimumSize(400, 480);
    this->move(100, 100);
    QVBoxLayout *mainlayout = new QVBoxLayout;

    QFormLayout *formLayout = new QFormLayout;

    QLineEdit *titleEdit = new QLineEdit;
    QLineEdit *priceEdit = new QLineEdit;
    QLineEdit *stockEdit = new QLineEdit;
    QLineEdit *brandEdit = new QLineEdit;
    QLineEdit *categoryEdit = new QLineEdit;
    QLineEdit *placementEdit = new QLineEdit;

    QDoubleValidator *doubleValidator = new QDoubleValidator(0, 1000000, 2, this);
    priceEdit->setValidator(doubleValidator);

    QIntValidator *intValidator = new QIntValidator(0, 1000000, this);
    stockEdit->setValidator(intValidator);

    formLayout->addRow("Title:", titleEdit);
    formLayout->addRow("Price:", priceEdit);
    formLayout->addRow("Stock:", stockEdit);
    formLayout->addRow("Brand:", brandEdit);
    formLayout->addRow("Category:", categoryEdit);
    formLayout->addRow("Placement:", placementEdit);

    mainlayout->addLayout(formLayout);

    QPushButton *addphotos = new QPushButton();
    addphotos->setMaximumWidth(200);
    addphotos->setText("Add Photos");
    QHBoxLayout *buttonLayout1 = new QHBoxLayout();
    buttonLayout1->addStretch(1);
    buttonLayout1->addWidget(addphotos);
    buttonLayout1->addStretch(1);
    mainlayout->addLayout(buttonLayout1);

    QScrollArea *scrollArea = new QScrollArea(this);
    QWidget *scrollWidget = new QWidget(scrollArea);
    QHBoxLayout *imageLayout = new QHBoxLayout(scrollWidget);

    QPixmap image1("../images/logo.jpg");
    QPixmap image2("../images/logo.jpg");
    QPixmap image3("../images/logo.jpg");
    QPixmap image4("../images/logo.jpg");
    QPixmap image5("../images/logo.jpg");

    QLabel *imageLabel1 = new QLabel();
    QLabel *imageLabel2 = new QLabel();
    QLabel *imageLabel3 = new QLabel();
    QLabel *imageLabel4 = new QLabel();
    QLabel *imageLabel5 = new QLabel();

    imageLabel1->setPixmap(image1.scaledToHeight(200, Qt::SmoothTransformation));
    imageLabel2->setPixmap(image2.scaledToHeight(200, Qt::SmoothTransformation));
    imageLabel3->setPixmap(image3.scaledToHeight(200, Qt::SmoothTransformation));
    imageLabel4->setPixmap(image4.scaledToHeight(200, Qt::SmoothTransformation));
    imageLabel5->setPixmap(image5.scaledToHeight(200, Qt::SmoothTransformation));

    imageLayout->addWidget(imageLabel1);
    imageLayout->addWidget(imageLabel2);
    imageLayout->addWidget(imageLabel3);
    imageLayout->addWidget(imageLabel4);
    imageLayout->addWidget(imageLabel5);

    scrollWidget->setLayout(imageLayout);
    scrollArea->setWidget(scrollWidget);

    mainlayout->addWidget(scrollArea);

    QPushButton *addProduct = new QPushButton("Add Product");
    addProduct->setMaximumWidth(200);

    QHBoxLayout *buttonLayout2 = new QHBoxLayout();
    buttonLayout2->addStretch(1);
    buttonLayout2->addWidget(addProduct);
    buttonLayout2->addStretch(1);

    mainlayout->addLayout(buttonLayout2);

    this->setLayout(mainlayout);

    connect(addphotos, &QPushButton::clicked, this, [=]()
            { s->showAlert("Pick photos"); });

    connect(addProduct, &QPushButton::clicked, this, [=]()
            {
        QString title = titleEdit->text();
        double price = priceEdit->text().toDouble();
        int stock = stockEdit->text().toInt();
        QString brand = brandEdit->text();
        QString category = categoryEdit->text();
        QString placement = placementEdit->text();
        Product *newproduct = new Product(s->getNextId(),title.toStdString(),price,stock,brand.toStdString(),category.toStdString(),placement.toStdString());
        s->addProduct(newproduct);
        s->fillTableWithProducts();
        this->close(); });
}

EditProductDialog::EditProductDialog(Product *product, QWidget *parent, ShopSystem *s) : QDialog(parent)
{
    setWindowTitle("Add Product");
    this->setMinimumSize(400, 480);
    this->move(100, 100);
    QVBoxLayout *mainlayout = new QVBoxLayout;

    QFormLayout *formLayout = new QFormLayout;

    QLineEdit *titleEdit = new QLineEdit;
    titleEdit->setText(QString::fromStdString(product->getTitle()));
    QLineEdit *priceEdit = new QLineEdit;
    priceEdit->setText(QString::fromStdString(std::to_string(product->getPrice())));
    QLineEdit *stockEdit = new QLineEdit;
    stockEdit->setText(QString::fromStdString(std::to_string(product->getStock())));
    QLineEdit *brandEdit = new QLineEdit;
    brandEdit->setText(QString::fromStdString(product->getBrand()));
    QLineEdit *categoryEdit = new QLineEdit;
    categoryEdit->setText(QString::fromStdString(product->getCategory()));
    QLineEdit *placementEdit = new QLineEdit;
    placementEdit->setText(QString::fromStdString(product->getPlacement()));

    QDoubleValidator *doubleValidator = new QDoubleValidator(0, 1000000, 2, this);
    priceEdit->setValidator(doubleValidator);

    QIntValidator *intValidator = new QIntValidator(0, 1000000, this);
    stockEdit->setValidator(intValidator);

    formLayout->addRow("Title:", titleEdit);
    formLayout->addRow("Price:", priceEdit);
    formLayout->addRow("Stock:", stockEdit);
    formLayout->addRow("Brand:", brandEdit);
    formLayout->addRow("Category:", categoryEdit);
    formLayout->addRow("Placement:", placementEdit);

    mainlayout->addLayout(formLayout);

    QPushButton *addphotos = new QPushButton();
    addphotos->setMaximumWidth(200);
    addphotos->setText("Edit Photos");
    QHBoxLayout *buttonLayout1 = new QHBoxLayout();
    buttonLayout1->addStretch(1);
    buttonLayout1->addWidget(addphotos);
    buttonLayout1->addStretch(1);
    mainlayout->addLayout(buttonLayout1);

    QScrollArea *scrollArea = new QScrollArea(this);
    QWidget *scrollWidget = new QWidget(scrollArea);
    QHBoxLayout *imageLayout = new QHBoxLayout(scrollWidget);

    QPixmap image1("../images/logo.jpg");
    QPixmap image2("../images/logo.jpg");
    QPixmap image3("../images/logo.jpg");
    QPixmap image4("../images/logo.jpg");
    QPixmap image5("../images/logo.jpg");

    QLabel *imageLabel1 = new QLabel();
    QLabel *imageLabel2 = new QLabel();
    QLabel *imageLabel3 = new QLabel();
    QLabel *imageLabel4 = new QLabel();
    QLabel *imageLabel5 = new QLabel();

    imageLabel1->setPixmap(image1.scaledToHeight(200, Qt::SmoothTransformation));
    imageLabel2->setPixmap(image2.scaledToHeight(200, Qt::SmoothTransformation));
    imageLabel3->setPixmap(image3.scaledToHeight(200, Qt::SmoothTransformation));
    imageLabel4->setPixmap(image4.scaledToHeight(200, Qt::SmoothTransformation));
    imageLabel5->setPixmap(image5.scaledToHeight(200, Qt::SmoothTransformation));

    imageLayout->addWidget(imageLabel1);
    imageLayout->addWidget(imageLabel2);
    imageLayout->addWidget(imageLabel3);
    imageLayout->addWidget(imageLabel4);
    imageLayout->addWidget(imageLabel5);

    scrollWidget->setLayout(imageLayout);
    scrollArea->setWidget(scrollWidget);

    mainlayout->addWidget(scrollArea);

    QPushButton *addProduct = new QPushButton("Save Product");
    addProduct->setMaximumWidth(200);

    QHBoxLayout *buttonLayout2 = new QHBoxLayout();
    buttonLayout2->addStretch(1);
    buttonLayout2->addWidget(addProduct);
    buttonLayout2->addStretch(1);

    mainlayout->addLayout(buttonLayout2);

    this->setLayout(mainlayout);

    connect(addphotos, &QPushButton::clicked, this, [=]()
            { s->showAlert("Pick photos"); });

    connect(addProduct, &QPushButton::clicked, this, [=]()
            {
        QString title = titleEdit->text();
        double price = priceEdit->text().toDouble();
        int stock = stockEdit->text().toInt();
        QString brand = brandEdit->text();
        QString category = categoryEdit->text();
        QString placement = placementEdit->text();
        s->editProduct(product,title.toStdString(),price,stock,brand.toStdString(),category.toStdString(),placement.toStdString());
        std::cout << "Edited" << std::endl;
        s->fillTableWithProducts();
        this->close(); });
}

void ShopSystem::performSearch()
{
    QString query = searchbox->text();
    if (query.isEmpty())
    {
        fillTableWithProducts();
    }
    else
    {
        fillTableWithProducts(query);
    }
}
