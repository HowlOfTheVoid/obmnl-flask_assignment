# Import libraries
from flask import Flask, request, redirect, render_template, url_for
# Instantiate Flask functionality
app = Flask(__name__)
# Sample data
# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]
# Read operation
@app.route("/")
def get_transactions():
    return render_template('transactions.html', transactions = transactions, balance = total_balance())

# Search operation
@app.route("/search", methods = ["GET", "POST"])
def search_transactions():
    if(request.method == 'POST'):
        min = request.form['min_amount']
        max = request.form['max_amount']
        filtered_transactions = []
        for transaction in transactions:
            if(transaction['amount'] >= min & transaction['amount'] <= max):
                filtered_transactions.append(transaction)
        return render_template('transactions.html', transactions = filtered_transactions, balance = total_balance())
    return render_template("search.html")

# Total Balance Operation
@app.route("/balance")
def total_balance():
    balance = 0
    for transaction in transactions:
        balance += transaction['amount']
    return f"Total Balance: {balance}"

# Create operation
@app.route("/create", methods = ["GET", "POST"])
def add_transaction():
    if(request.method == 'POST'):
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        transactions.append(transaction)

        return redirect(url_for("get_transactions"))
    return render_template("form.html")
    

# Update operation
@app.route("/update/<int:transaction_id>", methods = ["GET", "POST"])
def edit_transaction(transaction_id):
    if(request.method == 'POST'):
        for transaction in transactions:
            if (transaction['id'] == transaction_id):
                transaction['date'] = request.form['date']
                transaction['amount'] = request.form['amount']
                break

        return redirect(url_for("get_transactions"))
    
    for transaction in transactions:
        if (transaction['id'] == transaction_id):
            return render_template('edit.html', transaction = transaction)
    
    return {"message": "Transaction not found"}, 404

# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if(transaction['id'] == transaction_id):
            transactions.remove(transaction)
            break
    return redirect(url_for("get_transactions"))

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)