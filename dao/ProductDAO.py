import sqlite3
from model.Product import Product

class ProductDAO:
    def __init__(self, db_name="website.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
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
            '''INSERT INTO Product (prodName, prodDesc, prodPrice, prodStock, prodUsage, uniqeAttribute, prodImage) 
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (product.prodName, product.prodDesc, product.prodPrice, product.prodStock, product.prodUsage, 
            ",".join(product.uniqeAttribute), product.prodImage)
        )
        self.connection.commit()
        
        
        product.prodID = self.cursor.lastrowid
        return product.prodID  

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
    
    def filter_products(self, usage, price_min, price_max, sort_order):
        # Construct the SQL query
        query = '''
            SELECT * FROM Product
            WHERE prodUsage LIKE ?
            AND prodPrice BETWEEN ? AND ?
            ORDER BY prodPrice {}
        '''.format('ASC' if sort_order == 'asc' else 'DESC')

        # Execute the query
        self.cursor.execute(query, (f"%{usage}%", price_min, price_max))
        rows = self.cursor.fetchall()

        # Convert rows to Product objects
        return [
            Product(row['prodID'], row['prodName'], row['prodDesc'], row['prodPrice'],
                    row['prodStock'], row['prodUsage'], row['uniqeAttribute'].split(','), row['prodImage'])
            for row in rows
        ]

    def close_connection(self):
        self.connection.close()
