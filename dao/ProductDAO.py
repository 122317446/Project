import sqlite3
from model.Product import Product

class ProductDAO:
    def __init__(self, db_name="website.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Product (
                prodID INTEGER PRIMARY KEY AUTOINCREMENT,
                prodName TEXT NOT NULL,
                prodDesc TEXT,
                prodPrice REAL NOT NULL,
                prodStock INTEGER NOT NULL,
                prodUsage TEXT NOT NULL,
                uniqeAttribute TEXT NOT NULL,
                prodImage TEXT
            )
        ''')
        self.connection.commit()

    def add_product(self, product):
        self.cursor.execute(
            '''
            INSERT INTO Product (prodName, prodDesc, prodPrice, prodStock, prodUsage, uniqeAttribute, prodImage)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                product.prodName,
                product.prodDesc,
                product.prodPrice,
                product.prodStock,
                product.prodUsage,
                ",".join(product.uniqeAttribute),
                product.prodImage
            )
        )
        self.connection.commit()
        
        product.prodID = self.cursor.lastrowid

    def get_all_products(self):
        self.cursor.execute("SELECT * FROM Product")
        rows = self.cursor.fetchall()
        return [Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6].split(","), row[7]) for row in rows]

    def get_product_by_id(self, prodID):
        self.cursor.execute("SELECT * FROM Product WHERE prodID = ?", (prodID,))
        row = self.cursor.fetchone()
        if row:
            return Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6].split(","), row[7])
        return None

    def update_product(self, product):
        self.cursor.execute('''
            UPDATE Product
            SET prodName = ?, prodDesc = ?, prodPrice = ?, prodStock = ?, prodUsage = ?, uniqeAttribute = ?, prodImage = ?
            WHERE prodID = ?
        ''', (product.prodName, product.prodDesc, product.prodPrice, product.prodStock, product.prodUsage,
              ",".join(product.uniqeAttribute), product.prodImage, product.prodID))
        self.connection.commit()

    def delete_product(self, prodID):
        self.cursor.execute("DELETE FROM Product WHERE prodID = ?", (prodID,))
        self.connection.commit()

    def close_connection(self):
        self.connection.close()
