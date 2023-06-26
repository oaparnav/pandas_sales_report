# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from access_database import set_data_to_db, retrieve_info_from_table, set_processed_data_to_db

class Sales:

    ## intialization of variables
    def __init__(self):
        self.sales_data = []
        self.total_prices = {}
        self.total_prices_per_year = {}
        self.average_prices = {}
        self.sales_distribution = {}
    
    ## get sales data
    def get_sales_data(self, use_cols=["product_name", "quantity_sold", "price", "date_of_sale"]):
        self.sales_data = pd.read_csv('sales_data.csv', usecols=use_cols)
        self.sales_data = self.sales_data.dropna()
        self.data_dict = self.sales_data.to_dict(orient='records')
        set_data_to_db(self.data_dict)
    
    ## draw plot charts for each data
    def drawPlotChart(self):
        # Create a PDF file
        pdf_file = 'combined_graphs.pdf'
        pdf_pages = PdfPages(pdf_file)

        # Create a figure and subplots
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        # Total Sales per Product
        if self.total_prices:
            total_prices = pd.DataFrame({'Product': list(
                self.total_prices.keys()), 'Sales': list(self.total_prices.values())})
            ax1 = axes[0, 0]
            total_prices.plot.barh(
                x='Product', y='Sales', rot=0, color='blue', ax=ax1)
            ax1.set_ylabel('Products')
            ax1.set_xlabel('Total sales')
            ax1.set_title('Total Sales per Product')

        # Total Sales per Year
        if self.total_prices_per_year:
            plotLine = pd.DataFrame({'Year': list(self.total_prices_per_year.keys(
            )), 'Sales': list(self.total_prices_per_year.values())})
            ax2 = axes[0, 1]
            plotLine.plot.line(x='Year', y='Sales', rot=0,
                               color='green', ax=ax2)
            ax2.set_ylabel('Total sales')
            ax2.set_xlabel('Year')
            ax2.set_title('Total Sales per Year')

        # Average Price per Product
        if self.average_prices:
            plotLine = pd.DataFrame({'Product': list(
                self.average_prices.keys()), 'Sales': list(self.average_prices.values())})
            ax3 = axes[1, 0]
            plotLine.plot.line(x='Product', y='Sales',
                               rot=90, color='red', ax=ax3)
            ax3.set_ylabel('Total Average Prices')
            ax3.set_xlabel('Products')
            ax3.set_title('Average Price per Product')

        # Sales Distribution by Quantity
        if self.sales_distribution:
            plotLine = pd.DataFrame({'Product': list(
                self.sales_distribution.keys()), 'Sales': list(self.sales_distribution.values())})
            ax4 = axes[1, 1]
            plotLine.plot.line(x='Product', y='Sales',
                               rot=90, color='orange', ax=ax4)
            ax4.set_ylabel('Quantity')
            ax4.set_xlabel('Products')
            ax4.set_title('Sales Distribution by Quantity')

        # Adjust the spacing between subplots
        plt.tight_layout()

        # Save the combined chart as PDF
        pdf_pages.savefig(fig)

        # Close the PDF file
        pdf_pages.close()

        # Display the file path
        print("Combined graphs saved as PDF:", pdf_file)

    ## create a data set for different graphs
    def generic_product_set(self):
        product_set = retrieve_info_from_table('sales', 'salestable')
        total_prices = {}
        total_quantities = {}
        for item in product_set:
            name = item[0]
            price = item[1]
            quantity = item[2]
            year = pd.to_datetime(str(item[3])).year
            total = price * quantity

            total_prices[name] = total_prices.get(name, 0) + total
            total_quantities[name] = total_quantities.get(name, 0) + quantity
            self.total_prices[name] = self.total_prices.get(name, 0) + total
            self.total_prices_per_year[year] = self.total_prices_per_year.get(
                year, 0) + total
            self.sales_distribution[name] = self.sales_distribution.get(
                name, []) + [quantity]
        for name, quantities in self.sales_distribution.items():
            self.sales_distribution[name] = sum(quantities)
        self.average_prices = {
            name: total_prices[name] / total_quantities[name] for name in total_prices}
        self.drawPlotChart()

    ## store processd information to db by creating tables
    def set_processed_data_to_db(self):
        set_processed_data_to_db('total_sales', 'products', self.total_prices, 'name', 'price')
        set_processed_data_to_db('total_sales', 'years', self.total_prices_per_year, 'year', 'price')
        set_processed_data_to_db('total_sales', 'average', self.average_prices, 'name', 'price')
        set_processed_data_to_db('total_sales', 'quantity', self.sales_distribution, 'name', 'quantity')
    
    ## reteieve the processed info from table if required(testing purpose)
    def retrieve_info_from_table_data(self):
        retrieve_info_from_table('total_sales', 'products')
        retrieve_info_from_table('total_sales', 'years')
        retrieve_info_from_table('total_sales', 'average')
        retrieve_info_from_table('total_sales', 'quantity')

sales_info = Sales()
sales_info.get_sales_data()
sales_info.generic_product_set()
sales_info.set_processed_data_to_db()
sales_info.retrieve_info_from_table_data()