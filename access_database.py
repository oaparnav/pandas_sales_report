import sqlite3

def set_data_to_db(data):
    connection = sqlite3.connect('sales.db')
    if connection:
        print("Database connection successful")
        # Connect to the database
        cursor = connection.cursor()
        # Create the table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS salestable (
                product_name TEXT,
                quantity_sold REAL,
                price REAL,
                date_of_sale TEXT
            )
        ''')
        
        # Clear existing data from the table
        cursor.execute("DELETE FROM salestable")
        
        for item in data:
            cursor.execute('''
                INSERT INTO salestable (product_name, quantity_sold, price, date_of_sale)
                VALUES (?, ?, ?, ?)
            ''', (item['product_name'], item['quantity_sold'], item['price'], item['date_of_sale']))

        # Commit the changes and close the connection
        connection.commit()
        connection.close()
    else:
        print('Error!!')

def set_processed_data_to_db(dbname, table_name, data, key1, key2):
    connection = sqlite3.connect('total_sales.db')
    if connection:
        cursor = connection.cursor()
        # Create the table
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({key1} REAL, {key2} REAL)")
        
        # Clear existing data from the table
        cursor.execute(f"DELETE FROM {table_name}")
        
        # Insert data into the table
        for key1, key2 in data.items():
            cursor.execute(
                f"INSERT INTO {table_name} VALUES (?, ?)", (key1, key2))
        # Commit the changes and close the connection
        connection.commit()
        connection.close()
    else:
        print('Error setting individual data!!')
    
def retrieve_info_from_table(dbname, table_name):
    connection = sqlite3.connect(f'{dbname}.db')
    if connection:
        # Connect to the database
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        total_sales_data = cursor.fetchall()
        print(f"{table_name}: ", total_sales_data)
        return total_sales_data
    else:
        print("Unable to receive info at this moment")
