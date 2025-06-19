from flask import Flask, render_template, request
import csv
from datetime import datetime

app = Flask(__name__)

# Route: Homepage
@app.route("/")
def home():
    return render_template("index.html")

# Route: Add Transaction
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # Get form data
        t_type = request.form["type"]
        amount = float(request.form["amount"])
        category = request.form["category"]
        note = request.form["note"]
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Write to CSV
        with open("data.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date, t_type, amount, category, note])

        return render_template("confirmation.html")

    
    # If GET method, show the form
    return render_template("add.html")

from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt


@app.route("/transactions")
def transactions():
    try:
        transactions = []
        total_income = 0
        total_expense = 0
        balance = 0
        monthly_data = defaultdict(lambda: {'Income': 0, 'Expense': 0})

        with open("data.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                # 🛡️ Safely skip incomplete/bad rows
                if len(row) != 5:
                    continue
                try:
                    date_str = row[0]
                    t_type = row[1]
                    amount = float(row[2])
                    category = row[3]
                    note = row[4]

                    # Parse and group by month
                    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                    month = date.strftime('%b %Y')

                    if t_type == "Income":
                        total_income += amount
                        monthly_data[month]["Income"] += amount
                    elif t_type == "Expense":
                        total_expense += amount
                        monthly_data[month]["Expense"] += amount

                    transactions.append(row)  # ✅ keep only good rows
                except:
                    continue

        balance = total_income - total_expense

        

        return render_template("transactions.html",
                               transactions=transactions,
                               total_income=total_income,
                               total_expense=total_expense,
                               balance=balance)

    except Exception as e:
        return f"<h2>🚨 Oops! Something broke:<br>{e}</h2>", 500



@app.route("/report")
def report():
    try:
        from collections import defaultdict
        from datetime import datetime

        monthly_data = defaultdict(lambda: {"Income": 0, "Expense": 0})

        with open("data.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) != 5:
                    continue
                try:
                    date_str, t_type, amount_str, category, note = row
                    amount = float(amount_str.strip())
                    date = datetime.strptime(date_str.strip(), '%Y-%m-%d %H:%M:%S')
                    month = date.strftime('%b %Y')

                    if t_type == "Income":
                        monthly_data[month]["Income"] += amount
                    elif t_type == "Expense":
                        monthly_data[month]["Expense"] += amount
                except:
                    continue

        # ✅ Protect against empty chart lists
        if not monthly_data:
            return render_template("report.html", chart=False)

        months = sorted(monthly_data.keys())
        income_vals = [monthly_data[m]["Income"] for m in months]
        expense_vals = [monthly_data[m]["Expense"] for m in months]

        # 🛡️ Extra safety: if both lists are empty, skip chart
        if all(val == 0 for val in income_vals + expense_vals):
            return render_template("report.html", chart=False)

        # ✅ Create the chart safely
        plt.figure(figsize=(8, 5))
        x = range(len(months))
        plt.bar(x, income_vals, width=0.4, label='Income', align='center', color='#88e0ef')
        plt.bar(x, expense_vals, width=0.4, label='Expense', align='edge', color='#ffb3c6')
        plt.xticks(x, months, rotation=45)
        plt.ylabel("Amount (₹)")
        plt.title("Monthly Income vs Expense")
        plt.legend()
        plt.tight_layout()
        plt.savefig("static/bar_chart.png")
        plt.close()

        return render_template("report.html", chart=True)

    except Exception as e:
        return f"<h2>🚨 Report Error:<br>{e}</h2>", 500


@app.route("/insights")
def insights():
    try:
        import random
        from collections import Counter
        from datetime import datetime

        total_transactions = 0
        total_income = 0
        total_expense = 0
        categories = []

        with open("data.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) != 5:
                    continue
                try:
                    date_str, t_type, amount_str, category, note = row
                    amount = float(amount_str.strip())
                    total_transactions += 1
                    categories.append(category)

                    if t_type == "Income":
                        total_income += amount
                    elif t_type == "Expense":
                        total_expense += amount
                except:
                    continue

        most_common_category = Counter(categories).most_common(1)[0][0] if categories else "N/A"
        avg_expense = round(total_expense / total_transactions, 2) if total_transactions else 0

        tips_list = [
            "💸 Save first, spend later.",
            "📦 Avoid impulse purchases. Sleep on it.",
            "☕ Make coffee at home 5x a week = ₹1000 saved.",
            "🧠 Track your spending to control it.",
            "💳 Don't spend money to feel better. Feel better, then spend money.",
            "🧁 Needs > Wants. Always.",
            "📊 Invest in learning — it pays lifelong interest.",
        ]
        selected_tip = random.choice(tips_list)

        return render_template("insights.html",
                               total=total_transactions,
                               income=total_income,
                               expense=total_expense,
                               top_category=most_common_category,
                               avg_expense=avg_expense,
                               tip=selected_tip)
    except Exception as e:
        return f"<h2>⚠️ Insights error: {e}</h2>", 500








# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True)
