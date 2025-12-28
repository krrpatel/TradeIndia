import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, search_nse_companies, format_market_cap
from datetime import datetime, time
import pytz
import yfinance as yf

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    rows = db.execute(
        "SELECT username, cash FROM users WHERE id = ?",
        session["user_id"]
    )
    username = rows[0]["username"]
    cash = float(rows[0]["cash"])

    data = db.execute(
        """
        SELECT
            quote,
            SUM(quantity) AS total_shares
        FROM purchases
        WHERE username = ?
        GROUP BY quote
        HAVING total_shares > 0
        """,
        username
    )

    total_portfolio_value = 0.0
    error = False

    for row in data:
        current = lookup(row["quote"])

        if current is None:
            error = True
            row["current_price"] = 0
            row["individual_total"] = 0
            continue

        price = float(current["price"])
        row["current_price"] = price
        row["individual_total"] = price * row["total_shares"]

        total_portfolio_value += row["individual_total"]

    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)

    is_weekday = now.weekday() < 5

    market_open = (
        is_weekday and
        time(9, 15) <= now.time() <= time(15, 30)
    )

    total = cash + total_portfolio_value

    return render_template(
        "index.html",
        data=data,
        cash=cash,
        total=total,
        error=error,
        market_open=market_open
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)

        if not shares:
            return apology("must provide shares", 400)

        if not shares.isdigit():
            return apology("shares must be a positive integer", 400)

        shares = int(shares)

        if shares <= 0:
            return apology("shares must be a positive integer", 400)

        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol", 400)

        price = float(stock["price"])
        total_cost = price * shares

        rows = db.execute(
            "SELECT username, cash FROM users WHERE id = ?",
            session["user_id"]
        )

        cash = rows[0]["cash"]

        if cash < total_cost:
            return apology("not enough cash", 400)

        db.execute(
            """
            INSERT INTO purchases (username, quote, quantity, buyingprice, ptime)
            VALUES (?, ?, ?, ?, ?)
            """,
            rows[0]["username"],
            symbol.upper(),
            shares,
            price,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )

        db.execute(
            "UPDATE users SET cash = cash - ? WHERE id = ?",
            total_cost,
            session["user_id"]
        )

        flash("Purchase successful!")
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    rows = db.execute(
        "SELECT username, cash FROM users WHERE id = ?",
        session["user_id"]
    )
    username = rows[0]["username"]
    data = db.execute(
        """
            SELECT
                quote,
                quantity,
                buyingprice,
                ptime
            FROM purchases
            WHERE username = ?
            """,
        username
    )
    return render_template("history.html", data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        flash(f"Welcome, {request.form.get("username")}!")
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol", 400)

        quoteDetails = lookup(symbol)

        if quoteDetails is None:
            return apology("invalid symbol", 400)

        return render_template(
            "quote.html",
            quoted=True,
            quoteDetails=quoteDetails
        )

    return render_template("quote.html", quoted=False)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)

        if not password or not confirmation:
            return apology("must provide password/confirm password", 400)
        elif password != confirmation:
            return apology("password and confirm password is not same", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 1:
            return apology("username already exists", 400)
        else:
            db.execute(
                "INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)",
                username,
                generate_password_hash(password, method="scrypt", salt_length=16),
                100000
            )

            flash(f"Register Done : now login!")
            return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must select symbol", 400)

        if not shares:
            return apology("must enter shares", 400)

        if not shares.isdigit():
            return apology("shares must be a positive integer", 400)

        shares = int(shares)

        if shares <= 0:
            return apology("shares must be a positive integer", 400)

        rows = db.execute(
            "SELECT username, cash FROM users WHERE id = ?",
            session["user_id"]
        )
        username = rows[0]["username"]

        data = db.execute(
            """
            SELECT
                COALESCE(SUM(quantity), 0) AS total_shares
            FROM purchases
            WHERE username = ? AND quote = ?
            """,
            username,
            symbol.upper()
        )

        owned_shares = data[0]["total_shares"]

        if owned_shares < shares:
            return apology("not enough shares", 400)

        current = lookup(symbol)
        if current is None:
            return apology("invalid symbol", 400)

        price = float(current["price"])
        total_gain = price * shares

        db.execute(
            """
            INSERT INTO purchases (username, quote, quantity, buyingprice, ptime)
            VALUES (?, ?, ?, ?, ?)
            """,
            username,
            symbol.upper(),
            -shares,
            price,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )

        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            total_gain,
            session["user_id"]
        )

        flash("Sell completed successfully!")
        return redirect("/")

    rows = db.execute(
        """
        SELECT DISTINCT quote
        FROM purchases
        WHERE username = ?
        """,
        db.execute(
            "SELECT username FROM users WHERE id = ?",
            session["user_id"]
        )[0]["username"]
    )

    return render_template("sell.html", list=rows)


@app.route("/changepass", methods=["GET", "POST"])
@login_required
def changepass():
    if request.method == "POST":
        old = request.form.get("old")
        new = request.form.get("new")
        confirm = request.form.get("confirm")

        if not old:
            return apology("must provide old password", 400)

        if not new:
            return apology("must provide new password", 400)

        if new != confirm:
            return apology("passwords do not match", 400)

        rows = db.execute(
            "SELECT hash FROM users WHERE id = ?",
            session["user_id"]
        )

        if not check_password_hash(rows[0]["hash"], old):
            return apology("incorrect password", 400)

        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            generate_password_hash(new),
            session["user_id"]
        )

        flash("Password changed successfully")
        return redirect("/")

    return render_template("changepass.html")

@app.route("/research", methods=["GET", "POST"])
@login_required
def research():
    results = []

    if request.method == "POST":
        query = request.form.get("query")

        if not query:
            return apology("must provide company name", 400)

        results = search_nse_companies(query)

        if not results:
            flash("No matching NSE companies found")

    return render_template("research.html", results=results)


@app.route("/research/<symbol>")
@login_required
def research_detail(symbol):
    import yfinance as yf

    ticker = yf.Ticker(symbol + ".NS")
    info = ticker.info

    if not info or "longName" not in info:
        return apology("invalid symbol", 400)

    return render_template(
        "research_detail.html",
        symbol=symbol,
        info=info,
        market_cap=format_market_cap(info.get("marketCap"))
    )
