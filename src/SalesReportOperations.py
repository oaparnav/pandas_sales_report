# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from Repository import Repository
from itertools import groupby
from datetime import datetime


class DataManipulator:
    
    def __init__(self):
        self.totalSalesGroup = []
        self.monthlySalesGroup = []
        self.averageSalesGroup = []
        self.totalQuantity = []
    
    def process_data(self, sales_info):
        processed_sales_info = [(item[0], item[1], item[2], item[3], datetime.strptime(item[4], '%Y-%m-%d'), item[5]) for item in sales_info]
        sorted_tuple = sorted(processed_sales_info, key=lambda item: item[1]) 
        group_by_product = groupby(sorted_tuple, key = lambda item : item[1])
        
        for product, values in group_by_product:
            total_Amount = 0
            total_quantity = 0
            for quantity, total in [(field[2], field[5]) for field in values]:
                total_quantity = total_quantity + quantity
                total_Amount = total_Amount + total
            #calculate total sales amount of each product
            self.totalSalesGroup.append((product, total_Amount))
            
            #calculate mean on each product
            self.averageSalesGroup.append((product, total_Amount/total_quantity))
            
            #total quantity_sold
            self.totalQuantity.append((product, total_quantity))
            
        
        sort_tuple_by_date = sorted(processed_sales_info, key = lambda item : item[4])
        group_by_month = groupby(sort_tuple_by_date, key = lambda item : item[4].strftime('%b %Y'))
        
        for month, values in group_by_month:
            monthlyRevenue = sum([field[3] for field in values])

            #calculate monthly sales
            self.monthlySalesGroup.append((month, monthlyRevenue))

class PlotGraph:
        
    def plot_graph(self, totalSalesGroup, monthlySalesGroup, averageSalesGroup, totalQuantity):
        data_and_plots = [
            (totalSalesGroup, 'Product', 'sales', 'barh',
             'Blue', 'price', 'products', 'Total sales report'),
            (monthlySalesGroup, 'Product', 'sales', 'line', 'Red',
             'price', 'Year and Month', 'Monthly sales report'),
            (averageSalesGroup, 'Product', 'sales', 'line',
             'Orange', 'Average', 'Product', 'Average Sales Report'),
            (totalQuantity, 'Product', 'sales', 'hist', 'Green', 'Quantity', 'Products', 'Total sales')]

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        for i, (data, x_label, y_label, plot_type, color, axis_ylabel, axis_xlabel, title) in enumerate(data_and_plots):
            ax = axes[i//2, i % 2]
            
            x = [item[0] for item in data]
            y = [item[1] for item in data]
            
            ax.plot(x, y, marker='o')
            ax.set_ylabel(axis_ylabel)
            ax.set_xlabel(axis_xlabel)
            ax.set_title(title)

        pdf_name = "Output_graph.pdf"
        with PdfPages(pdf_name) as pdf_pages:
           pdf_pages.savefig(fig)    
            
            
repository = Repository()
filePath = "/Users/mn34jw/MyPython/pandas_sales_report/sales_data.csv"
sales_info = repository.load_data_into_sales_db(filePath)
repository.connection.close()

dataManipulator = DataManipulator()
dataManipulator.process_data(sales_info)

plotgraph = PlotGraph()
plotgraph.plot_graph(dataManipulator.totalSalesGroup, dataManipulator.monthlySalesGroup, dataManipulator.averageSalesGroup, dataManipulator.totalQuantity)

