# -*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
import pandas as py
import numpy as np

class Repository:
    def __init__(self):
        self.connection = []
        self.cursor = self.establish_db_connection()
        self.create_salesInfo_table()

    def establish_db_connection(self):
        try:
            self.connection = sqlite3.connect("Product_sales.db")
            cursor = self.connection.cursor()
            return cursor
        except Error as error:
            print(error)

    def create_salesInfo_table(self):
        create_query = """ CREATE TABLE IF NOT EXISTS SALES_INFO(
            id integer PRIMARY KEY,
            product_name text NOT NULL,
            quantity_sold integer,
            price integer,
            date_of_sale TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount integer
            );"""
        self.cursor.execute(create_query)

    def load_data_into_sales_db(self, filePath):
        dataframe = py.read_csv(filePath, usecols=['product_name','quantity_sold', 'price', 'date_of_sale'])
        dataframe = self.sanitize_data(dataframe)
        dataframe.to_sql('SALES_INFO', self.connection, if_exists = 'replace')
        self.connection.commit()
        self.cursor.execute(''' SELECT * FROM SALES_INFO''')
        return self.cursor.fetchall()
    
    def sanitize_data(self, dataframe):
        dataframe.dropna(subset = ['date_of_sale'], inplace = True)
        dataframe = dataframe.replace(np.nan, 0)
        dataframe['total_amount'] = dataframe['quantity_sold'] * dataframe['price']        
        return dataframe
