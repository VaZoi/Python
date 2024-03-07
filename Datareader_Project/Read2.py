import pandas as pd
import matplotlib.pyplot as plt

csv_file = 'RandomData.csv'
data = pd.read_csv(csv_file, delimiter=';')

city_column = 'City'

# Count the occurrences of each city
city_counts = data[city_column].value_counts()

# Select the top 10 cities
top_cities = city_counts.head(10)

# Plot the bar chart
plt.figure(figsize=(10, 6))
plt.bar(top_cities.index, top_cities.values, color='green')
plt.xlabel('City')
plt.ylabel('Number of Users')
plt.title('Top 10 Cities by Number of Users')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
