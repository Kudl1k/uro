#include <QApplication>
#include <QWidget>
#include <QLabel>

int main(int argc, char **argv)
{
    QApplication *app = new QApplication(argc, argv);

    QWidget *hello = new QWidget();

    QLabel *world = new QLabel("Hello World", hello);

    hello->show();

    return app->exec();
}