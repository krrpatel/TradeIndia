# TradeIndia – NSE Stock Trading & Research Platform

#### Video Demo: https://youtu.be/CiC-NoIq1d0

---

## Description

TradeIndia is a web-based stock trading and research application inspired by CS50 Finance, but redesigned specifically for the Indian stock market (NSE). The project allows users to register, log in, and simulate buying and selling of NSE-listed stocks using real-time market data fetched from Yahoo Finance. In addition to trading functionality, the application also includes a Research section that enables users to search for companies by name and view detailed financial and business information.

The primary goal of this project was to apply the concepts learned throughout CS50x—such as Flask, SQL, authentication, APIs, and frontend templating—to build a realistic, user-friendly financial application that feels relevant to the Indian market. The project goes beyond the original Finance problem set by adding a dark-themed interface, NSE market timing logic, and a research module with company overviews.

---

## Features

### User Authentication
Users can register with a unique username and password, log in securely, change their password, and log out. Passwords are securely hashed using Werkzeug’s `generate_password_hash` with the `scrypt` algorithm. Session management ensures that only authenticated users can access trading and portfolio features.

### Portfolio Management
After logging in, users are presented with a portfolio dashboard that displays:
- Stocks currently owned
- Total number of shares per stock
- Current market price
- Total value per holding
- Available cash balance
- Overall portfolio value (cash + holdings)

The portfolio dynamically fetches live prices using Yahoo Finance and updates the total value accordingly. Stocks that have been fully sold are automatically excluded from the portfolio view.

### Buy and Sell Stocks
Users can buy shares of NSE-listed companies by entering the stock symbol and quantity. The application validates input carefully, ensuring that only positive integers are accepted and that users cannot buy shares exceeding their available cash. Selling shares is implemented using negative quantities in the database, which simplifies portfolio calculations and mirrors real-world accounting practices. Users are also prevented from selling more shares than they own.

### Transaction History
The History page displays a complete log of all buy and sell transactions, including:
- Stock symbol
- Quantity (positive for buy, negative for sell)
- Price at transaction time
- Date and time of the transaction

Buy and sell transactions are visually distinguished using color coding, making the history easy to read and understand.

### Research Module (Non-Hardcoded)
The Research feature allows users to search for NSE-listed companies by name or partial keyword. The application uses Yahoo Finance’s search API to retrieve real, non-hardcoded company data. Users can select a company from the results and view a detailed research page that includes:
- Company name and symbol
- Current stock price
- Sector and industry
- Market capitalization (formatted into billions or trillions)
- 52-week high and low
- A detailed business description (company overview)

This module transforms the project from a basic trading simulator into a more complete investment research tool.

### Market Status Indicator
The application determines whether the NSE market is currently open based on Indian Standard Time (IST). The market is considered open only on weekdays (Monday to Friday) between 9:15 AM and 3:30 PM IST. This status is clearly displayed on the portfolio page, adding realism to the platform.

---

## File Structure and Responsibilities

- **app.py**  
  Contains all Flask routes, including authentication, portfolio display, buying and selling logic, transaction history, and research functionality.

- **helpers.py**  
  Includes helper functions such as stock lookup, market capitalization formatting, market timing logic, and the `login_required` decorator.

- **templates/**  
  Contains all Jinja2 HTML templates:
  - `layout.html` – Base layout with navigation and dark theme
  - `index.html` – Portfolio dashboard
  - `buy.html` / `sell.html` – Trading pages
  - `history.html` – Transaction history
  - `research.html` / `research_detail.html` – Research search and company details
  - `login.html`, `register.html`, `changepass.html`, `apology.html`

- **static/styles.css**  
  Custom CSS file implementing a consistent dark theme and overriding Bootstrap defaults.

- **finance.db**  
  SQLite database storing users, transactions, and portfolio data.

---

## Design Decisions

One key design decision was to store sell transactions as negative quantities rather than modifying or deleting previous purchase records. This approach simplifies portfolio calculations, preserves full transaction history, and aligns with real-world accounting principles.

Another important decision was to format all monetary values in Indian Rupees (₹) instead of using USD formatting from the original CS50 Finance project. Formatting is handled either in the backend or directly in Jinja templates to ensure clarity and consistency.

The dark theme was chosen to improve visual comfort and to give the application a modern, professional appearance similar to real-world trading platforms.

---

## Conclusion

TradeIndia is a complete and functional stock trading and research application that demonstrates my understanding of web development, APIs, databases, authentication, and frontend design. This project represents a meaningful extension of CS50 Finance into a region-specific solution for the Indian stock market and serves as the final culmination of my learning in CS50x.


```bash
submit50 cs50/problems/2025/x/project
