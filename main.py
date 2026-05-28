from fastapi import FastAPI
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     
    allow_credentials=True,
    allow_methods=["*"],     
    allow_headers=["*"]
)
conn_obj = mysql.connector.connect(
    host=os.getenv("db_host"),
    user=os.getenv("db_user"),
    password=os.getenv("db_password"),
    database=os.getenv("db_name"),
    port=int(os.getenv("db_port"))
)
cursor_obj = conn_obj.cursor(dictionary=True)
cursor_obj.execute("""
CREATE TABLE IF NOT EXISTS expenses(
    expense_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100),
    amount FLOAT,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn_obj.commit()
@app.get("/")
def home():

    return {
        "message": "API Running Successfully"
    }
@app.post("/add_expense")
def add_expense(expense: dict):
    title=expense.get("title")
    amount=expense.get("amount")
    category=expense.get("category")
    query="insert into expenses(title,amount,category)values(%s,%s,%s)"
    data=(title,amount,category)
    cursor_obj.execute(query,data)
    conn_obj.commit()
    return{
        "AddExpense":"expense added successfully..."
    }
@app.get("/ViewExpenses")
def view_expenses():
    query="select * from expenses"
    cursor_obj.execute(query)
    all_expenses=cursor_obj.fetchall()
    return all_expenses
@app.put("/update_expense/{expense_id}")
def update_expense(expense_id: int, expense: dict):
    title=expense.get("title")
    amount=expense.get("amount")
    category=expense.get("category")
    query="update expenses set title =%s,amount=%s,category=%s where expense_id=%s"
    values=(title,amount,category,expense_id)
    cursor_obj.execute(query,values)
    conn_obj.commit()
    return{
        "updated_msg":"expenses updated successfully.."
    }
@app.delete("/delete_expenses/{expense_id}")
def delete_expense(expense_id: int):
    query = "DELETE FROM expenses WHERE expense_id=%s"
    cursor_obj.execute(query, (expense_id,))
    conn_obj.commit()
    return {
        "delete_msg": "Expense Deleted Successfully"
    }

@app.get("/search_expenses")
def search_expenses(category:str):
    query="select * from expenses where category=%s"
    cursor_obj.execute(query,(category,))
    searched_data=cursor_obj.fetchall()
    return searched_data

@app.get("/sort_expenses")
def sort_expenses(order:str):
    if order=="low_to_high":
        query="select * from expenses order by amount asc"
    else:
        query="select * from expenses order by amount desc"
    cursor_obj.execute(query)
    sorted_data=cursor_obj.fetchall()
    return sorted_data
@app.get("/filter_expenses")
def filter_expenses(amount:float):
    query="select * from expenses where amount >=%s"
    cursor_obj.execute(query,(amount,))
    filtered_data=cursor_obj.fetchall()
    return filtered_data