import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector
from datetime import datetime, timedelta

# Replace these variables with your MySQL database credentials
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'mypy'
}

# Connect to the MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Calculate the date 7 days ago from today
seven_days_ago = datetime.now() - timedelta(days=7)
seven_days_ago_str = seven_days_ago.strftime('%Y-%m-%d')

# Fetch data from the 'users' table for the last 7 days
query = f"SELECT DATE(created_at) as date, COUNT(*) as user_count FROM users WHERE created_at >= '{seven_days_ago_str}' GROUP BY DATE(created_at)"
cursor.execute(query)
result = cursor.fetchall()

# Close the database connection
cursor.close()
conn.close()

# Convert the result to a Pandas DataFrame
df = pd.DataFrame(result, columns=['Date', 'User Count'])

# Convert the 'Date' column to datetime type
df['Date'] = pd.to_datetime(df['Date'])

# Sort the DataFrame by the 'Date' column
df = df.sort_values(by='Date')

# Plot the line chart
plt.plot(df['Date'], df['User Count'], marker='o')
plt.title('User Registration Over the Last 7 Days')
plt.xlabel('Date')
plt.ylabel('User Count')
plt.grid(True)
plt.show()
