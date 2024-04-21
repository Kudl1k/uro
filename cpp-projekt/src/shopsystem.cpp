#include "shopsystem.h"

ShopSystem::ShopSystem(QWidget *parent) : QMainWindow(parent)
{
    this->setWindowTitle("Shop System - KUD0132");
    this->setMinimumSize(1280, 720);
    this->move(100, 100);
    QWidget *centralWidget = new QWidget(this);
    mainlayout = new QVBoxLayout(centralWidget);
    setup_menubar();
    setup_header();
    setup_table();
    this->setCentralWidget(centralWidget);
}

void ShopSystem::showAlert(const QString &message)
{
    QMessageBox::information(this, "Alert", message);
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
}

void ShopSystem::setup_search()
{
    QHBoxLayout *searchlayout = new QHBoxLayout();

    QComboBox *searchComboBox = new QComboBox();
    searchComboBox->addItem("All");
    searchComboBox->addItem("id");
    searchComboBox->addItem("title");
    searchComboBox->addItem("price");
    searchComboBox->addItem("stock");
    searchComboBox->addItem("brand");
    searchComboBox->addItem("category");
    searchComboBox->addItem("placement");
    searchComboBox->setMaximumWidth(100);
    searchlayout->addWidget(searchComboBox);

    QLineEdit *searchbox = new QLineEdit();
    searchbox->setPlaceholderText("Search...");
    searchbox->setMinimumWidth(200);
    searchbox->setMaximumWidth(300);
    searchlayout->addWidget(searchbox);

    QToolButton *searchButton = new QToolButton();
    searchButton->setText("Search");
    searchlayout->addWidget(searchButton);

    headerlayout->addLayout(searchlayout);
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

    QStandardItemModel *model = new QStandardItemModel(0, 7, this);
    model->setHeaderData(0, Qt::Horizontal, tr("id"));
    model->setHeaderData(1, Qt::Horizontal, tr("title"));
    model->setHeaderData(2, Qt::Horizontal, tr("price"));
    model->setHeaderData(3, Qt::Horizontal, tr("stock"));
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

    mainlayout->addWidget(tableView);
}