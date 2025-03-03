import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, filedialog
import os

# Function to get real-time stock data
def get_stock_data(symbol):
    print(f"Fetching stock data for {symbol}")
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d", interval="1m")
    print(data.head())  # Print the first few rows to verify
    return data

# Function to get historical stock data
def get_historical_data(symbol, period='1mo'):
    print(f"Fetching historical data for {symbol} for {period}")
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    print(data.head())  # Print the first few rows to verify
    return data

# Function to get detailed stock information
def get_detailed_info(symbol):
    print(f"Fetching detailed information for {symbol}")
    stock = yf.Ticker(symbol)
    info = stock.info
    print(info)  # Print stock information to verify
    return info

# Function to add a stock to the portfolio
def add_stock(portfolio, symbol, quantity, price):
    print(f"Attempting to add stock: {symbol}, Quantity: {quantity}, Buy Price: {price}")
    stock_data = get_stock_data(symbol)
    if not stock_data.empty:
        portfolio[symbol] = {
            'data': stock_data,
            'quantity': quantity,
            'buy_price': price
        }
        print(f"Stock {symbol} added to the portfolio.")
        messagebox.showinfo("Success", f'Stock {symbol} added to the portfolio.')
    else:
        print(f"Failed to retrieve data for stock: {symbol}")
        messagebox.showerror("Error", f'Failed to retrieve data for stock {symbol}.')

# Function to remove a stock from the portfolio
def remove_stock(portfolio, symbol):
    if symbol in portfolio:
        del portfolio[symbol]
        print(f"Stock {symbol} removed from the portfolio.")
        messagebox.showinfo("Success", f'Stock {symbol} removed from the portfolio.')
    else:
        print(f"Stock {symbol} not found in the portfolio.")
        messagebox.showerror("Error", f'Stock {symbol} not found in the portfolio.')

# Function to display the portfolio
def display_portfolio(portfolio):
    if not portfolio:
        print('The portfolio is empty.')
        messagebox.showinfo("Info", 'The portfolio is empty.')
    else:
        result = ""
        for symbol, details in portfolio.items():
            result += f'Stock: {symbol}\n'
            result += f'Quantity: {details["quantity"]}\n'
            result += f'Buy Price: {details["buy_price"]}\n'
            result += str(details['data'].head()) + "\n\n"
        print(result)
        messagebox.showinfo("Portfolio", result)

# Function to display historical data
def display_historical_data(symbol, period='1mo'):
    data = get_historical_data(symbol, period)
    if not data.empty:
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data['Close'], label='Close Price')
        plt.title(f'Historical Close Price for {symbol}')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend()
        plt.show()
    else:
        print(f'Failed to retrieve historical data for {symbol}.')
        messagebox.showerror("Error", f'Failed to retrieve historical data for {symbol}.')

# Function to summarize the portfolio
def summarize_portfolio(portfolio):
    total_value = 0
    total_investment = 0
    result = 'Portfolio Summary:\n'
    for symbol, details in portfolio.items():
        latest_price = details['data']['Close'].iloc[-1]
        quantity = details['quantity']
        buy_price = details['buy_price']
        total_investment += quantity * buy_price
        total_value += quantity * latest_price
        result += f'{symbol}: Latest Price = {latest_price}, Quantity = {quantity}, Buy Price = {buy_price}\n'
    result += f'\nTotal Investment: {total_investment}\n'
    result += f'Total Portfolio Value: {total_value}\n'
    result += f'Unrealized Profit/Loss: {total_value - total_investment}\n'
    print(result)
    messagebox.showinfo("Summary", result)

# Function to export portfolio to CSV
def export_portfolio(portfolio):
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if filename:
        data = []
        for symbol, details in portfolio.items():
            latest_price = details['data']['Close'].iloc[-1]
            data.append([symbol, details['quantity'], details['buy_price'], latest_price])
        df = pd.DataFrame(data, columns=['Symbol', 'Quantity', 'Buy Price', 'Latest Price'])
        df.to_csv(filename, index=False)
        print(f'Portfolio exported to {filename}')
        messagebox.showinfo("Success", f'Portfolio exported to {filename}')

# GUI setup
def setup_gui():
    portfolio = {}
    root = tk.Tk()
    root.title("Stock Portfolio Manager")
    
    def add_stock_callback():
        symbol = stock_symbol_entry.get().upper()
        quantity = int(stock_quantity_entry.get())
        price = float(stock_price_entry.get())
        add_stock(portfolio, symbol, quantity, price)
    
    def remove_stock_callback():
        symbol = stock_symbol_entry.get().upper()
        remove_stock(portfolio, symbol)
    
    def display_portfolio_callback():
        display_portfolio(portfolio)
    
    def summarize_portfolio_callback():
        summarize_portfolio(portfolio)
    
    def export_portfolio_callback():
        export_portfolio(portfolio)
    
    def display_historical_data_callback():
        symbol = stock_symbol_entry.get().upper()
        period = historical_period_entry.get()
        display_historical_data(symbol, period)

    # GUI Elements
    tk.Label(root, text="Stock Symbol:").grid(row=0, column=0)
    stock_symbol_entry = tk.Entry(root)
    stock_symbol_entry.grid(row=0, column=1)
    
    tk.Label(root, text="Quantity:").grid(row=1, column=0)
    stock_quantity_entry = tk.Entry(root)
    stock_quantity_entry.grid(row=1, column=1)
    
    tk.Label(root, text="Buy Price:").grid(row=2, column=0)
    stock_price_entry = tk.Entry(root)
    stock_price_entry.grid(row=2, column=1)

    tk.Label(root, text="Historical Period (e.g., '1mo', '1y'):").grid(row=3, column=0)
    historical_period_entry = tk.Entry(root)
    historical_period_entry.grid(row=3, column=1)
    
    tk.Button(root, text="Add Stock", command=add_stock_callback).grid(row=4, column=0)
    tk.Button(root, text="Remove Stock", command=remove_stock_callback).grid(row=4, column=1)
    tk.Button(root, text="Display Portfolio", command=display_portfolio_callback).grid(row=5, column=0)
    tk.Button(root, text="Summarize Portfolio", command=summarize_portfolio_callback).grid(row=5, column=1)
    tk.Button(root, text="Export Portfolio", command=export_portfolio_callback).grid(row=6, column=0)
    tk.Button(root, text="Display Historical Data", command=display_historical_data_callback).grid(row=6, column=1)

    root.mainloop()

# Run the GUI setup
setup_gui()
