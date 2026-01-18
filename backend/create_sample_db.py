"""
Sample database creation script for testing.
Creates a SQLite database with sample sales data.
"""

import sqlite3
import random
from datetime import datetime, timedelta

def create_sample_database():
    """Create a sample SQLite database with sales data."""
    
    # Connect to database
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    # Drop existing tables
    cursor.execute('DROP TABLE IF EXISTS sales')
    cursor.execute('DROP TABLE IF EXISTS customers')
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('DROP TABLE IF EXISTS regions')
    
    # Create regions table
    cursor.execute('''
        CREATE TABLE regions (
            region_id INTEGER PRIMARY KEY,
            region_name TEXT NOT NULL
        )
    ''')
    
    regions = [
        (1, 'North'),
        (2, 'South'),
        (3, 'East'),
        (4, 'West')
    ]
    cursor.executemany('INSERT INTO regions VALUES (?, ?)', regions)
    
    # Create products table
    cursor.execute('''
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    
    products = [
        (1, 'Laptop Pro', 'Electronics', 1299.99),
        (2, 'Wireless Mouse', 'Electronics', 29.99),
        (3, 'Office Chair', 'Furniture', 299.99),
        (4, 'Standing Desk', 'Furniture', 599.99),
        (5, 'Monitor 27"', 'Electronics', 399.99),
        (6, 'Keyboard Mechanical', 'Electronics', 149.99),
        (7, 'Desk Lamp', 'Furniture', 49.99),
        (8, 'USB Hub', 'Electronics', 39.99),
    ]
    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?)', products)
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            region_id INTEGER NOT NULL,
            FOREIGN KEY (region_id) REFERENCES regions (region_id)
        )
    ''')
    
    customers = [
        (1, 'Acme Corp', 1),
        (2, 'TechStart Inc', 2),
        (3, 'Global Solutions', 3),
        (4, 'Innovate LLC', 4),
        (5, 'Enterprise Co', 1),
        (6, 'SmallBiz Ltd', 2),
        (7, 'MegaCorp', 3),
        (8, 'Startup Hub', 4),
    ]
    cursor.executemany('INSERT INTO customers VALUES (?, ?, ?)', customers)
    
    # Create sales table
    cursor.execute('''
        CREATE TABLE sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date TEXT NOT NULL,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    ''')
    
    # Generate sample sales data for the last 6 months
    sales_data = []
    start_date = datetime.now() - timedelta(days=180)
    
    for i in range(500):
        sale_date = start_date + timedelta(days=random.randint(0, 180))
        customer_id = random.randint(1, 8)
        product_id = random.randint(1, 8)
        quantity = random.randint(1, 10)
        
        # Get product price
        cursor.execute('SELECT price FROM products WHERE product_id = ?', (product_id,))
        price = cursor.fetchone()[0]
        total_amount = price * quantity
        
        sales_data.append((
            sale_date.strftime('%Y-%m-%d'),
            customer_id,
            product_id,
            quantity,
            total_amount
        ))
    
    cursor.executemany(
        'INSERT INTO sales (sale_date, customer_id, product_id, quantity, total_amount) VALUES (?, ?, ?, ?, ?)',
        sales_data
    )
    
    conn.commit()
    conn.close()
    
    print("Sample database created successfully!")
    print(f"Created {len(sales_data)} sales records")
    print("Database: test.db")
    print("\nTables:")
    print("- regions (4 records)")
    print("- products (8 records)")
    print("- customers (8 records)")
    print(f"- sales ({len(sales_data)} records)")


if __name__ == '__main__':
    create_sample_database()
