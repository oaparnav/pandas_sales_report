import sqlite3

def set_data_to_db(data):
    with sqlite3.connect('sales.db') as connection:
        print("Database connection successful")
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS salestable (
                product_name TEXT,
                quantity_sold REAL,
                price REAL,
                date_of_sale TEXT
            )
        ''')
        cursor.execute("DELETE FROM salestable")
        cursor.executemany('''
            INSERT INTO salestable (product_name, quantity_sold, price, date_of_sale)
            VALUES (?, ?, ?, ?)
        ''', [(item['product_name'], item['quantity_sold'], item['price'], item['date_of_sale']) for item in data])
        connection.commit()

def set_processed_data_to_db(dbname, table_name, data):
    with sqlite3.connect(f'{dbname}.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (key REAL, value REAL)")
        cursor.execute(f"DELETE FROM {table_name}")
        cursor.executemany(f"INSERT INTO {table_name} VALUES (?, ?)", data.items())
        connection.commit()

def retrieve_info_from_table(dbname, table_name):
    with sqlite3.connect(f'{dbname}.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        total_sales_data = cursor.fetchall()
        print(f"{table_name}: ", total_sales_data)
        return total_sales_data
