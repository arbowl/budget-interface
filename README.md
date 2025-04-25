# Budget Tracker

A Flask-based web application for tracking monthly expenses, calculating rewards from credit card transactions, and monitoring your budget.

## Features

- **Manual Transaction Input**: Add transactions with details like amount, category, payment method, and notes.
- **Rewards Calculation**: Automatically calculates rewards based on the card and category.
- **Budget Monitoring**: Tracks spending against a predefined monthly budget.
- **Web Interface**: User-friendly interface built with Flask and TailwindCSS.

## Project Structure
```
 ├── app.py            # Main Flask application
 ├── assets/
 │ └── cards.py        # Credit card rewards logic
 ├── templates/
 │ └── index.html      # HTML template for the web interface
 ├── budget.db         # SQLite database for storing transactions
 └── requirements.txt  # Python dependencies
 ```

## Setup Instructions

1. **Clone the Repository**:
```bash
   git clone https://github.com/arbowl/budget-interface
   cd budget-interface
```

2. **Install Dependencies:**

`pip install -r requirements.txt`

3. **Run the Application:**
`python app.py`

4. **Access the Web Interface:**
Open your browser and navigate to https://localhost:8001.

## Database Schema
The app uses an SQLite database (budget.db) with the following schema:

```sql
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
```

## Configuration
- **Monthly Budget:** Update the MONTHLY_SPENDING_BUDGET variable in app.py to set your monthly budget.
- **Rewards Rates:** Modify the cards dictionary in assets/cards.py to customize reward rates for different cards and categories.
