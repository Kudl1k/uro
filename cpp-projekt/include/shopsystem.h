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

class ShopSystem : public QMainWindow
{
public:
    ShopSystem(QWidget *parent = nullptr);
    void showAlert(const QString &message);
    int getNextId();
    void fillTableWithProducts();
    void addProduct(Product *product);

private:
    std::vector<Product> products;

    void generateProducts();

    QVBoxLayout *mainlayout;
    QHBoxLayout *headerlayout;
    AddProductDialog *addProductDialog;
    QStandardItemModel *model;
    void setup_menubar();
    void setup_header();
    void setup_search();
    void setup_category();
    void setup_table();
    void openAddProductWindow();
};

class AddProductDialog : public QDialog
{
public:
    explicit AddProductDialog(QWidget *parent = nullptr, ShopSystem *s = nullptr);
    ~AddProductDialog() {}

protected:
private:
    ShopSystem *s;
};