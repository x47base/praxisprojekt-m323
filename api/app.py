"""Docstring"""
from datetime import date
from flask import Flask, jsonify, request
from classes.expense import Category, Expense, Expenses

app = Flask(__name__)

expense_data = [
    Expense(title="Grocery", amount=50.0, expense_date=date.today(), expense_category=Category("Food")),
    Expense(title="Utilities", amount=150.0, expense_date=date.today(), expense_category=Category("Bills")),
]

expenses = Expenses(expense_data)

@app.route('/expenses', methods=['GET'])
def get_expenses():
    """API Endpoint"""
    return jsonify([exp.__dict__ for exp in expenses.expenses])

@app.route('/expenses/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    """API Endpoint"""
    if expense_id < len(expenses.expenses):
        return jsonify(expenses.expenses[expense_id].__dict__)
    return jsonify({"error": "Expense not found"}), 404

@app.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    """API Endpoint"""
    if 0 <= expense_id < len(expenses.expenses):
        data = request.get_json()
        expense = expenses.expenses[expense_id]
        expense.title = data.get('title')
        expense.amount = data.get('amount')
        expense.expense_date = date.fromisoformat(data.get('expense_date', expense.expense_date.isoformat()))
        expense.expense_category = Category(data.get('expense_category'))
        return jsonify(expense.__dict__), 200
    else:
        return jsonify({"error": "Expense not found"}), 404

@app.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """API Endpoint"""
    if 0 <= expense_id < len(expenses.expenses):
        deleted_expense = expenses.expenses.pop(expense_id)
        return jsonify({"message": "Expense deleted", "deleted_expense": deleted_expense.__dict__}), 200
    else:
        return jsonify({"error": "Expense not found"}), 404

@app.route('/expenses', methods=['POST'])
def add_expense():
    """API Endpoint"""
    data = request.get_json()
    new_expense = Expense(
        title=data['title'],
        amount=data['amount'],
        expense_date=date.fromisoformat(data['expense_date']),
        expense_category=Category(data['expense_category'])
    )
    expenses.expenses.append(new_expense)
    return jsonify(new_expense.__dict__), 201

@app.route('/expenses/total', methods=['GET'])
def get_total_expenses():
    """API Endpoint"""
    return jsonify({"total_expenses": expenses.total_expenses()})

@app.route('/expenses/statistics', methods=['GET'])
def get_statistics():
    """API Endpoint"""
    stats = expenses.total_and_average_expenses()
    return jsonify(stats)

@app.route('/expenses/high-expense-summary', methods=['GET'])
def high_expense_summary():
    """API Endpoint"""
    min_amount = float(request.args.get('min_amount', 0))
    summary = expenses.high_expense_summary(min_amount)
    return jsonify(summary)

if __name__ == '__main__':
    app.run(debug=True)
