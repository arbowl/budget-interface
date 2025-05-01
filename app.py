"""App"""

from datetime import datetime
from os.path import exists
from sqlite3 import Connection, Row, connect

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.wrappers.response import Response

from assets.cards import cards


app = Flask(__name__)
DATABASE = "budget.db"
MONTHLY_SPENDING_BUDGET = 2415


def get_db_connection() -> Connection:
    """Get a connection to the database"""
    conn = connect(DATABASE)
    conn.row_factory = Row
    return conn


def init_db() -> None:
    """Initialize the database"""
    if exists(DATABASE):
        return
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT DEFAULT CURRENT_DATE,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            method TEXT NOT NULL,
            is_input INTEGER DEFAULT 0,
            is_business INTEGER DEFAULT 0,
            note TEXT
        );
    """
    )
    conn.commit()
    conn.close()


def calculate_rewards(transactions: list[dict]) -> float:
    """Calculate rewards for a given method and category"""
    total_rewards: float = 0.0
    for tx in transactions:
        if tx["is_input"]:
            continue
        rate = cards[tx["method"]][tx["category"]]
        tx["reward_rate"] = rate
        tx["reward_amount"] = round(tx["amount"] / 100 * rate, 2)
        total_rewards += tx["reward_amount"]
    return total_rewards


def post_transaction() -> Response:
    """Submit transaction data from the form"""
    amount = float(request.form["amount"])
    category = request.form["category"]
    method = request.form["method"]
    is_input = 1 if request.form.get("is_input") == "on" else 0
    is_business = 1 if request.form.get("is_business") == "on" else 0
    note = request.form.get("note", "")
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO transactions (amount, category, method, is_input, "
        "is_business, note) VALUES (?, ?, ?, ?, ?, ?)",
        (amount, category, method, is_input, is_business, note),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/", methods=["GET", "POST"])
def index() -> Response | str:
    """Main page"""
    if request.method == "POST":
        return post_transaction()
    conn = get_db_connection()
    selected_month = request.args.get(
        "month",
        datetime.now().strftime("%Y-%m")
    )
    month_rows = conn.execute(
        "SELECT DISTINCT strftime('%Y-%m', date) AS month "
        "FROM transactions "
        "ORDER BY month DESC"
    ).fetchall()
    avail_months = [row["month"] for row in month_rows]
    avail_months = [
       {"key": m, "label": datetime.strptime(m, "%Y-%m").strftime("%B %Y")}
       for m in avail_months
    ]
    cur = conn.execute(
        "SELECT * FROM transactions "
        "WHERE strftime('%Y-%m', date)=? "
        "ORDER BY date DESC",
        (selected_month,)
    )
    rows = cur.fetchall()
    transactions = [dict(tx) for tx in rows]
    total_out = sum(
        tx["amount"]
        for tx in transactions
        if not tx["is_input"] and not tx["is_business"]
    )
    total_in = sum(tx["amount"] for tx in transactions if tx["is_input"])
    net_spend = total_out - total_in
    remaining = MONTHLY_SPENDING_BUDGET - net_spend
    total_rewards = calculate_rewards(transactions)
    conn.close()
    return render_template(
        "index.html",
        transactions=transactions,
        remaining=remaining,
        budget=MONTHLY_SPENDING_BUDGET,
        spent=net_spend,
        total_rewards=round(total_rewards, 2),
        avail_months=avail_months,
        selected_month=selected_month
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=8001, ssl_context="adhoc")
