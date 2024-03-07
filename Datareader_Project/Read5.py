import pandas as pd
import matplotlib.pyplot as plt

csv_file = 'RandomData.csv'
data = pd.read_csv(csv_file, delimiter=';')

firstname_column = 'firstname'

# Count the occurrences of each first name
firstname_counts = data[firstname_column].value_counts()

# Select the top 10 most common first names
top_firstnames = firstname_counts.head(10)

# Plot the bar chart
plt.figure(figsize=(10, 6))
plt.bar(top_firstnames.index, top_firstnames.values, color='purple')
plt.xlabel('First Name')
plt.ylabel('Frequency')
plt.title('Top 10 Most Common First Names')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
