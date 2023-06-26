# -*- coding: utf-8 -*-
import pandas as py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sqlite3

totalSalesGroup = []
monthlySalesGroup = []
averageSalesGroup = []
totalQuantity = []

def data_load_and_sanitize(path):
    dataframe = py.read_csv(path)
    dataframe.dropna(subset = ['date_of_sale'], inplace = True)
    dataframe = dataframe.replace(np.nan, 0)
    dataframe['Total'] = dataframe['quantity_sold'] * dataframe['price']
    dataframe['date_of_sale'] = py.to_datetime(dataframe.date_of_sale, format='%Y-%m-%d')
    return dataframe;

def plot_graph():
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    if len(totalSalesGroup) > 0:
        ax1 = axes[0,0]
        totalSalesGroup.plot.barh(x = 'Product', y= 'sales', rot =0, color = 'Blue', ax=ax1)
        ax1.set_ylabel("price")
        ax1.set_xlabel("Products")
        ax1.set_title("Total sales report")
    if len(monthlySalesGroup) > 0:
        ax2 = axes[0,1]
        monthlySalesGroup.plot.line(x = 'Product', y= 'sales', rot =0, color = 'Red', ax=ax2)
        ax2.set_ylabel("price")
        ax2.set_xlabel("Year and Month")
        ax2.set_title("Monthly sales report")
    if len(averageSalesGroup) > 0:
        ax3 = axes[1,0]
        averageSalesGroup.plot.line(x = 'Product', y= 'sales', rot =90, color = 'Orange', ax=ax3)
        ax3.set_ylabel("Average")
        ax3.set_xlabel("Product")
        ax3.set_title("Average Sales Report")
    if len(totalQuantity) > 0:
        ax4 = axes[1,1]
        totalQuantity.plot.hist(x = 'Product', y= 'sales', rot =90, color = 'Green', ax=ax4)
        ax4.set_ylabel("Quantity")
        ax4.set_xlabel("Products")
        ax4.set_title("Total sales")
    
    pdf_name = "Output_graph.pdf"
    pdf_pages = PdfPages(pdf_name)
    pdf_pages.savefig(fig)
    pdf_pages.close()


def total_sales_report_by_product(dataframe):
    global totalSalesGroup
    totalSalesGroup = dataframe.groupby('=product_name')['Total'].sum()

def monthly_sales_report(dataframe):
    global monthlySalesGroup
    monthlySalesGroup = dataframe.groupby([dataframe.date_of_sale.dt.year, dataframe.date_of_sale.dt.month])['Total'].sum()

def average_sales_by_product(dataframe):
    global averageSalesGroup
    averageSalesGroup = dataframe.groupby('product_name')['Total'].mean()

def total_quantity_of_sales(dataframe):
    global totalQuantity
    totalQuantity = dataframe.groupby('product_name')['quantity_sold'].mean()
     
def connect_To_db():
    connection = sqlite3.connect("Product_sales.db")
    cursor = connection.cursor()
    if connection:
        print("Connection sucessfull")
    connection.close()
    
    
file_path = "/Users/mn34jw/MyPython/pandas_sales_report/sales_data.csv" 
df = data_load_and_sanitize(file_path) 
total_sales_report_by_product(df)
monthly_sales_report(df)
average_sales_by_product(df)
total_quantity_of_sales(df)
plot_graph()
connect_To_db()



