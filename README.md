# 💸 Nix's Expense Tracker

A clean, pastel-themed expense tracker web app built using Python and Flask.  
Track your income and expenses, get monthly insights, and receive gentle financial tips — all inside an elegant and beginner-friendly interface.

---

## 🧁 Features

- ➕ **Add Transactions**: Log income and expenses with custom categories and notes
- 📋 **View All Transactions**: Organized, styled table showing every entry
- 🧠 **Insights Section**: Get total income, total expenses, most-used category, and average expense
- 🌼 **Daily Money Tips**: See a rotating financial tip each time you visit Insights
- 🖼️ **Minimal UI**: Styled with soft colors and gentle cards, for a relaxing experience
- 💾 **Data Persistence**: Stored locally in `data.csv`
- 🧠 **Beginner Friendly**: Fully readable code, no complex setups

---

## 🗂️ Project Structure

## 🗂️ Project Structure

```text
nix-expense-tracker/
├── app.py                 # Main Flask application
├── data.csv               # Stores transaction data
│
├── static/                # Static assets (e.g. generated chart)
│   └── bar_chart.png
│
├── templates/             # All HTML templates
│   ├── index.html
│   ├── add.html
│   ├── confirmation.html
│   ├── transactions.html
│   ├── insights.html
│   └── report.html

```
Then open your browser at:
👉 http://127.0.0.1:5000/
