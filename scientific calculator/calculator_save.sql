import mysql.connector

# 1. Connect to your MySQL database (edit with your credentials)
conn = mysql.connector.connect(
    host="local instance",
    user="root",
    password="mahi@123",
    database="calculator_app"
)
cursor = conn.cursor()

# 2. Save a calculation to MySQL
def save_history_sql(expression, result):
    query = "INSERT INTO history (expression, result) VALUES (%s, %s)"
    values = (expression, result)
    cursor.execute(query, values)
    conn.commit()

# 3. Retrieve last 10 calculations
def get_last_10_sql():
    query = "SELECT expression, result, timestamp FROM history ORDER BY timestamp DESC LIMIT 10"
    cursor.execute(query)
    return cursor.fetchall()

# ... Call save_history_sql(expr, result) after each calculation
# ... Use get_last_10_sql() to show history

# 4. Close when done
# cursor.close()
# conn.close()
