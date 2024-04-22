#include <QMainWindow>
#include <QMessageBox>
#include <QMenuBar>
#include <QMenu>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QFormLayout>
#include <QGridLayout>
#include <QToolButton>
#include <QComboBox>
#include <QLineEdit>
#include <QLabel>
#include <QPushButton>
#include <QTableView>
#include <QStandardItemModel>
#include <QHeaderView>
#include <QDialog>
#include <QDesktopServices>
#include <QScrollArea>
#include <vector>
#include <product.h>

class AddProductDialog;
class EditProductDialog;

class ShopSystem : public QMainWindow
{
public:
    ShopSystem(QWidget *parent = nullptr);
    void showAlert(const QString &message);
    int getNextId();
    void fillTableWithProducts();
    void fillTableWithProducts(const QString &query);
    void addProduct(Product *product);
    void editProduct(Product *product, std::string title, double price, int stock, std::string brand, std::string category, std::string placement);

private:
    std::vector<Product> allproducts;
    std::vector<Product> products;

    void generateProducts();
    void performSearch();
    QVBoxLayout *mainlayout;
    QHBoxLayout *headerlayout;
    AddProductDialog *addProductDialog;
    QStandardItemModel *model;
    QLineEdit *searchbox;
    QComboBox *searchComboBox;
    void setup_menubar();
    void setup_header();
    void setup_search();
    void setup_category();
    void setup_table();
    void openAddProductWindow();
    void openEditProductWindow(const QModelIndex &index);
};

class AddProductDialog : public QDialog
{
public:
    AddProductDialog(QWidget *parent = nullptr, ShopSystem *s = nullptr);
    ~AddProductDialog() {}

protected:
private:
    ShopSystem *s;
};

class EditProductDialog : public QDialog
{
public:
    EditProductDialog(Product *product, QWidget *parent, ShopSystem *s);
    ~EditProductDialog() {}

protected:
private:
    Product *product;
    ShopSystem *s;
};