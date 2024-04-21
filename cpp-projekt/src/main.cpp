#include <QApplication>
#include "shopsystem.h"

int main(int argc, char **argv)
{
    QApplication *app = new QApplication(argc, argv);


    ShopSystem *s = new ShopSystem(new QWidget);

    s->show();

    return app->exec();
}