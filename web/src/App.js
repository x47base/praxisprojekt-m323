import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Pie, Bar, Line } from 'react-chartjs-2';
import 'chart.js/auto';
import './App.css';

function App() {
  const [expenses, setExpenses] = useState([]);
  const [totalExpenses, setTotalExpenses] = useState(0);
  const [statistics, setStatistics] = useState({});
  const [highExpenseSummary, setHighExpenseSummary] = useState({});

  useEffect(() => {
    fetchExpenses();
    fetchTotalExpenses();
    fetchStatistics();
    fetchHighExpenseSummary();
  }, []);

  const fetchExpenses = async () => {
    const response = await axios.get('/expenses');
    setExpenses(response.data);
  };

  const fetchTotalExpenses = async () => {
    const response = await axios.get('/expenses/total');
    setTotalExpenses(response.data.total_expenses);
  };

  const fetchStatistics = async () => {
    const response = await axios.get('/expenses/statistics');
    setStatistics(response.data);
  };

  const fetchHighExpenseSummary = async (minAmount = 50) => {
    const response = await axios.get(`/expenses/high-expense-summary?min_amount=${minAmount}`);
    setHighExpenseSummary(response.data);
  };

  const pieData = {
    labels: expenses.map(exp => exp.expense_category.title),
    datasets: [
      {
        label: 'Expenses by Category',
        data: expenses.map(exp => exp.amount),
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
      },
    ],
  };

  const barData = {
    labels: expenses.map(exp => exp.title),
    datasets: [
      {
        label: 'Expense Amounts',
        data: expenses.map(exp => exp.amount),
        backgroundColor: '#36A2EB',
      },
    ],
  };

  const lineData = {
    labels: expenses.map((_, index) => `Expense ${index + 1}`),
    datasets: [
      {
        label: 'Total Expenses Over Time',
        data: expenses.map((_, index) => expenses.slice(0, index + 1).reduce((acc, exp) => acc + exp.amount, 0)),
        borderColor: '#FF6384',
        fill: false,
      },
    ],
  };

  return (
    <div className="App">
      <h1>Expense Tracker</h1>
      <div className="charts-container">
        <div className="chart-item" key="lineChart">
          <h2>Total Expenses: ${totalExpenses}</h2>
          <Line data={lineData} />
        </div>
        <div className="chart-item" key="pieChart">
          <h2>Expenses by Category</h2>
          <Pie data={pieData} />
        </div>
        <div className="chart-item" key="barChart">
          <h2>Individual Expenses</h2>
          <Bar data={barData} />
        </div>
      </div>
      <div className="statistics-container">
        <p>Total: {statistics.total}</p>
        <p>Average: {statistics.average}</p>
        <p>High Expense Summary: {highExpenseSummary.total_high_expenses}</p>
      </div>
    </div>
  );
}

export default App;
