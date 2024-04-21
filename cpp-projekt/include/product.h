#include <iostream>
#include <string>

class Product
{
public:
    Product(int id, std::string title, double price, int stock, std::string brand, std::string category, std::string placement) : id(id), title(title), price(price), stock(stock), brand(brand), category(category), placement(placement){};
    int getId() const { return id; };
    std::string getTitle() const { return title; };
    double getPrice() const { return price; };
    int getStock() const { return stock; };
    std::string getBrand() const { return brand; };
    std::string getCategory() const { return category; };
    std::string getPlacement() const { return placement; };

private:
    int id;
    std::string title;
    double price;
    int stock;
    std::string brand;
    std::string category;
    std::string placement;
};
