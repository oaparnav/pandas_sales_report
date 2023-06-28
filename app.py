# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from access_database import set_data_to_db, retrieve_info_from_table, set_processed_data_to_db

class Sales:

    # intialization of variables
    def __init__(self):
        self.sales_data = []
        self.total_prices = {}
        self.total_prices_per_year = {}
        self.average_prices = {}
        self.sales_distribution = {}

    # get sales data
    def get_sales_data(self, use_cols=["product_name", "quantity_sold", "price", "date_of_sale"]):
        self.sales_data = pd.read_csv('sales_data.csv', usecols=use_cols)
        self.sales_data = self.sales_data.dropna()
        self.data_dict = self.sales_data.to_dict(orient='records')
        set_data_to_db(self.data_dict)

    # draw plot charts for each data
    def drawPlotChart(self):
        pdf_file = 'combined_graphs.pdf'
        pdf_pages = PdfPages(pdf_file)

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        plots = [
            (list(self.total_prices.keys()), list(self.total_prices.values()),
             'Product', 'Total sales', 'Total Sales per Product', 'blue'),
            (list(self.total_prices_per_year.keys()), list(self.total_prices_per_year.values(
            )), 'Year', 'Total sales', 'Total Sales per Year', 'green'),
            (list(self.average_prices.keys()), list(self.average_prices.values()),
             'Product', 'Total Average Prices', 'Average Price per Product', 'red'),
            (list(self.sales_distribution.keys()), list(self.sales_distribution.values(
            )), 'Product', 'Quantity', 'Sales Distribution by Quantity', 'orange')
        ]

        for i, (x, y, x_label, y_label, title, color) in enumerate(plots):
            ax = axes[i // 2, i % 2]
            plot_data = pd.DataFrame({x_label: x, y_label: y})
            plot_data.plot.line(x=x_label, y=y_label,
                                rot=90, color=color, ax=ax)
            ax.set_ylabel(y_label)
            ax.set_xlabel(x_label)
            ax.set_title(title)

        plt.tight_layout()
        pdf_pages.savefig(fig)
        pdf_pages.close()
        print("Combined graphs saved as PDF:", pdf_file)

    # create a data set for different graphs
    def generic_product_set(self):
        product_set = retrieve_info_from_table('sales', 'salestable')
        for name, price, quantity, year in [(item[0], item[1], item[2], pd.to_datetime(str(item[3])).year) for item in product_set]:
            total = price * quantity
            self.total_prices[name] = self.total_prices.get(name, 0) + total
            self.total_prices_per_year[year] = self.total_prices_per_year.get(
                year, 0) + total
            self.sales_distribution[name] = self.sales_distribution.get(
                name, []) + [quantity]
        self.sales_distribution = {
            name: sum(quantities) for name, quantities in self.sales_distribution.items()}
        self.average_prices = {
            name: self.total_prices[name] / self.sales_distribution[name] for name in self.total_prices}
        self.drawPlotChart()

    # store processd information to db by creating tables
    def set_processed_data_to_db(self):
        data_to_store = {
            'products': self.total_prices,
            'years': self.total_prices_per_year,
            'average': self.average_prices,
            'quantity': self.sales_distribution
        }

        for table_name, data in data_to_store.items():
            set_processed_data_to_db('total_sales', table_name, data)

    # reteieve the processed info from table if required(testing purpose)
    def retrieve_info_from_table_data(self):
        tables_to_retrieve = ['products', 'years', 'average', 'quantity']

        for table_name in tables_to_retrieve:
            retrieve_info_from_table('total_sales', table_name)


sales_info = Sales()
sales_info.get_sales_data()
sales_info.generic_product_set()
sales_info.set_processed_data_to_db()
sales_info.retrieve_info_from_table_data()
