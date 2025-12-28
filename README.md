TradeIndia – NSE Stock Trading & Research Platform
Video Demo: [click here](https://youtu.be/CiC-NoIq1d0)
Description

TradeIndia is a web-based stock trading and research application inspired by CS50 Finance, but redesigned specifically for the Indian stock market (NSE). The project allows users to register, log in, and simulate buying and selling of NSE-listed stocks using real-time market data fetched from Yahoo Finance. In addition to trading functionality, the application also includes a Research section that enables users to search for companies by name and view detailed financial and business information.

The primary goal of this project was to apply the concepts learned throughout CS50x—such as Flask, SQL, authentication, APIs, and frontend templating—to build a realistic, user-friendly financial application that feels relevant to the Indian market. The project goes beyond the original Finance problem set by adding a dark-themed interface, NSE market timing logic, and a research module with company overviews.

Features
User Authentication

Users can register with a unique username and password, log in securely, change their password, and log out. Passwords are securely hashed using Werkzeug’s generate_password_hash with the scrypt algorithm. Session management ensures that only authenticated users can access trading and portfolio features.

Portfolio Management

After logging in, users are presented with a portfolio page that shows:

Stocks currently owned

Total number of shares per stock

Current market price

Total value per holding

Available cash balance

Overall portfolio value (cash + holdings)

The portfolio dynamically fetches live prices using Yahoo Finance and updates the total value accordingly. Stocks that have been fully sold are automatically excluded from the portfolio view.

Buy and Sell Stocks

Users can buy shares of NSE-listed companies by entering the stock symbol and quantity. The application validates input carefully, ensuring that only positive integers are accepted and that users cannot buy shares exceeding their available cash. Selling shares is implemented using negative quantities in the database, which simplifies portfolio calculations and mirrors real-world accounting practices. Users are also prevented from selling more shares than they own.

Transaction History

The History page displays a complete log of all buy and sell transactions, including:

Stock symbol

Quantity (positive for buy, negative for sell)

Price at transaction time

Date and time of the transaction

Buy transactions are visually distinguished from sell transactions using color coding, making the history easy to read and understand.

Research Module (Non-Hardcoded)

The Research feature allows users to search for NSE-listed companies by name or partial keyword. The application uses Yahoo Finance’s search API to retrieve real, non-hardcoded company data. Users can select a company from the results and view a detailed research page that includes:

Company name and symbol

Current stock price

Sector and industry

Market capitalization (formatted into billions or trillions)

52-week high and low

A full company business description (overview)

This module transforms the project from a basic trading simulator into a more complete investment research tool.

Market Status Indicator

The application determines whether the NSE market is currently open based on Indian Standard Time (IST). The market is considered open only on weekdays (Monday to Friday) between 9:15 AM and 3:30 PM IST. This status is displayed clearly on the portfolio page, adding realism to the platform.

File Structure and Responsibilities

app.py
Contains all Flask routes, including authentication, portfolio display, buying and selling logic, transaction history, and research functionality.

helpers.py
Includes helper functions such as lookup for fetching stock prices, formatting utilities (e.g., market cap formatting), and decorators like login_required.

templates/
Contains all Jinja2 HTML templates, including:

layout.html – Base layout with dark theme styling and navigation

index.html – Portfolio dashboard

buy.html / sell.html – Trading forms

history.html – Transaction history

research.html / research_detail.html – Research search and detail views

login.html, register.html, changepass.html, apology.html

static/styles.css
Custom CSS used to implement a consistent dark theme across the application, overriding default Bootstrap styles where necessary.

finance.db
SQLite database storing users, purchases, and transaction data.

Design Decisions

One important design choice was to represent sell transactions as negative quantities instead of deleting or modifying previous purchases. This approach simplifies portfolio calculations, preserves transaction history, and closely resembles real-world accounting practices.

Another deliberate decision was to format all currency values in Indian Rupees (₹) and avoid using USD formatting utilities from the original CS50 Finance project. Formatting is handled either in the backend or directly in Jinja templates to maintain clarity and consistency.

The dark theme was chosen to improve visual comfort and give the application a modern, professional appearance similar to real trading platforms.

Conclusion

TradeIndia is a complete, functional stock trading and research application that demonstrates my understanding of web development, APIs, databases, and user authentication. This project reflects my ability to extend a given problem into a more complex, region-specific solution while maintaining clean code, usability, and security. It represents a meaningful culmination of everything I learned in CS50x.
