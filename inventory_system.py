import csv
import os
from datetime import datetime

class Product:
    # inventory products
    def __init__(self, id, name, qty, price, category):
        self.id = id
        self.name = name
        self.qty = int(qty)
        self.price = float(price)
        self.category = category

    def List(self):
        # Convert product object to List format
        return [self.id, self.name, self.qty, self.price, self.category]

class Inventory:
    # Manages inventory operations
    def __init__(self, filename="inventory.csv"):
        self.filename = filename
        self.products = self.load()

    # Load products from file into memory
    def load(self):
        items = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        items.append(Product(*row))
        return items

     # Save the entire product list back to CSV
    def saveInventory(self):
        with open(self.filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for p in self.products:
                writer.writerow(p.List())

     # Log every change made to the inventory into a log file
    def logUpdate(self, product, action):
        with open("stock_update_log.csv", 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                product.id,
                action,
                product.qty,
                product.price,
                product.category,
                product.name
            ])

    # Add a new product to the inventory
    def addProduct(self):
        id = input("ID:- ")
        name = input("Name:- ")
        qty = input("Quantity:- ")
        price = input("Price:- ")
        category = input("Category:- ")
        product = Product(id, name, qty, price, category)
        self.products.append(product)
        self.saveInventory()
        self.logUpdate(product, "Added")
        print("Product added")

     # Display all products
    def view(self):
        if not self.products:
            print("No products found")
        else:
            for p in self.products:
                print(f"{p.id} | {p.name} | Qty: {p.qty} | ₹{p.price} | {p.category}")

    # Delete a product using its ID
    def deleteProduct(self, id):
        for p in self.products:
            if p.id == id:
                self.products.remove(p)
                self.saveInventory()
                self.logUpdate(p, "Deleted")
                print("Product deleted.")
                return
        print("Product ID not found.")

    # Search product by name or ID
    def search(self, key):
        key = key.lower()
        found = False
        for p in self.products:
            if key in p.id.lower() or key in p.name.lower():
                print(f"{p.id} | {p.name} | Qty: {p.qty} | ₹{p.price} | {p.category}")
                found = True
        if not found:
            print("No match found.")

    # Update product details
    def updateProduct(self, id, updatedData):
        for p in self.products:
            if p.id == id:
                if "Name" in updatedData:
                    p.name = updatedData["Name"]
                if "Quantity" in updatedData:
                    p.qty = updatedData["Quantity"]
                if "Price" in updatedData:
                    p.price = updatedData["Price"]
                if "Category" in updatedData:
                    p.category = updatedData["Category"]
                self.saveInventory()
                self.logUpdate(p, "Updated")
                print("Product updated")
                return
        print("Product ID not found.")

    # Generate inventory report
    def report(self):
        total = sum(p.qty * p.price for p in self.products)
        print(f"Total inventory value:- ₹{total:.2f}")
        print("Low Stock(Qty<10):")
        for p in self.products:
            if p.qty < 10:
                print(f"{p.name} (ID: {p.id}) - Qty: {p.qty}")

# Main menu loop
def main():
    inventory = Inventory()

    while True:
        print("""
1. Add product
2. View product
3. Search product
4. Update product
5. Delete product
6. Generate product
7. Exit
""")
        choice = input("Enter your choice:- ")
        match choice:
            case "1":
                inventory.addProduct()

            case "2":
                inventory.view()

            case "3":
                searchTerm = input("Enter product name or ID to search:- ")
                inventory.search(searchTerm)

            case "4":
                productId = input("Enter product ID to update:- ")
                updatedData = {}
                if input("Update name? (y/n):- ") == "y":
                    updatedData["Name"] = input("Enter new name:- ")
                if input("Update quantity? (y/n):- ") == "y":
                    updatedData["Quantity"] = int(input("Enter new quantity:- "))
                if input("Update price? (y/n):- ") == "y":
                    updatedData["Price"] = float(input("Enter new price:- "))
                if input("Update category? (y/n):- ") == "y":
                    updatedData["Category"] = input("Enter new category:- ")
                inventory.updateProduct(productId, updatedData)

            case "5":
                productId = input("Enter product ID to delete:- ")
                inventory.deleteProduct(productId)

            case "6":
                inventory.report()

            case "7":
                print("Exiting inventory system.")
                break

            case _:
                print("Invalid choice!")

# Entry point of the program
if __name__ == "__main__":
    main()
