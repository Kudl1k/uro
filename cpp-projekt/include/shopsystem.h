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

class ShopSystem : public QMainWindow
{
public:
    ShopSystem(QWidget *parent = nullptr);

private:
    QVBoxLayout *mainlayout;
    QHBoxLayout *headerlayout;

    void showAlert(const QString &message);
    void setup_menubar();
    void setup_header();
    void setup_search();
    void setup_category();
    void setup_table();
};