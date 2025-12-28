import requests

from flask import redirect, render_template, session
from functools import wraps
import yfinance as yf



def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def lookup(symbol):
    """Look up quote for NSE-listed stock using Yahoo Finance."""
    try:
        ticker = yf.Ticker(symbol.upper() + ".NS")
        info = ticker.info

        price = info.get("regularMarketPrice")
        name = info.get("longName")

        if price is None or name is None:
            return None

        return {
            "symbol": symbol.upper(),
            "name": name,
            "price": float(price)
        }

    except Exception:
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def search_nse_companies(query):
    url = "https://query1.finance.yahoo.com/v1/finance/search"
    params = {
        "q": query,
        "quotesCount": 10,
        "newsCount": 0
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers, timeout=5)

    if response.status_code != 200:
        return []

    data = response.json()
    results = []

    for item in data.get("quotes", []):
        symbol = item.get("symbol", "")

        if symbol.endswith(".NS"):
            results.append({
                "symbol": symbol.replace(".NS", ""),
                "name": item.get("shortname", "N/A")
            })

    return results

def format_market_cap(value):
    if value is None:
        return "N/A"

    value = float(value)

    if value >= 1_000_000_000_000:
        return f"₹{value / 1_000_000_000_000:.2f} Trillion"
    elif value >= 1_000_000_000:
        return f"₹{value / 1_000_000_000:.2f} Billion"
    elif value >= 1_000_000:
        return f"₹{value / 1_000_000:.2f} Million"
    else:
        return f"₹{value:.2f}"
