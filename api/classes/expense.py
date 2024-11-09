"""Docstring"""
from dataclasses import dataclass
from datetime import date
from typing import Callable
from functools import reduce

@dataclass
class Category:
    """Docstring"""
    title: str

@dataclass
class Expense:
    """Docstring"""
    title: str
    amount: float
    expense_date: date
    expense_category: Category

class Expenses:
    """Docstring"""

    def __init__(self, expenses: list[Expense]):
        self.expenses = expenses

    # B1G
    def total_expenses(self):
        """Docstring"""
        return sum(expense.amount for expense in self.expenses)

    # B1F
    def get_expense_amounts(self):
        """Docstring"""
        return [expense.amount for expense in self.expenses]

    def sum_expenses(self):
        """Docstring"""
        return sum(self.get_expense_amounts())

    # B1E
    def avg_expenses(self):
        """Docstring"""
        total = self.sum_expenses()
        return total / len(self.expenses) if self.expenses else 0.0

    def total_and_average_expenses(self):
        """Docstring"""
        total = self.sum_expenses()
        average = self.avg_expenses()
        return {"total": total, "average": average}

    # B2G
    def apply_tax(self, tax_rate: float):
        """Docstring"""
        tax = lambda amount: amount * (1 + tax_rate)
        return [tax(expense.amount) for expense in self.expenses]

    # B2F
    def apply_to_expenses(self, func: Callable[[Expense], float]):
        """Docstring"""
        return [func(expense) for expense in self.expenses]

    # B2E
    def multitply_expense(self, multiplier: float):
        """Docstring"""
        def multiplier_function(expense: Expense):
            return expense.amount * multiplier
        return multiplier_function

    # B3G
    def squared_expenses(self):
        """Docstring"""
        return [lambda amount: amount ** 2 for amount in self.get_expense_amounts()]

    # B3F
    def exceeded_budget_on_expenses(self, budget: float):
        """Calculates the total amount by which each expense exceeds the budget."""
        return sum([(lambda amount, budget: max(0, amount - budget))(expense.amount, budget) for expense in self.expenses])

    # B3E
    def sort_by_amount(self):
        """Docstring"""
        return sorted(self.expenses, key=lambda exp: exp.amount)

    # B4G
    def map_titles(self):
        """Docstring"""
        return list(map(lambda exp: exp.title, self.expenses))

    def filter_min_amount(self, min_amount: float):
        """Docstring"""
        return list(filter(lambda exp: exp.amount > min_amount, self.expenses))

    def reduce_total_expense(self):
        """Docstring"""
        return reduce(lambda acc, exp: acc + exp.amount, self.expenses, 0.0)

    # B4F
    def filter_min_amount_titles(self, min_amount: float):
        """Docstring"""
        filtered_expenses = filter(lambda exp: exp.amount > min_amount, self.expenses)
        return list(map(lambda exp: exp.title, filtered_expenses))

    # B4E
    def high_expense_summary(self, min_amount: float):
        """Docstring"""
        high_expenses = filter(lambda exp: exp.amount > min_amount, self.expenses)
        high_amounts = map(lambda exp: exp.amount, high_expenses)
        total_high = reduce(lambda acc, amount: acc + amount, high_amounts, 0.0)
        return {"total_high_expenses": total_high, "count": len(list(high_expenses))}
