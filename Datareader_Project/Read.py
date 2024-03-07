import pandas as pd
import matplotlib.pyplot as plt

csv_file = 'RandomData.csv'

# Specify the delimiter as semicolon
data = pd.read_csv(csv_file, delimiter=';')

country_column = 'Country'

# Count the occurrences of each country
country_counts = data[country_column].value_counts()

# Select the top 10 countries
top_countries = country_counts.head(10)

# Plot the bar chart
plt.figure(figsize=(10, 6))
plt.bar(top_countries.index, top_countries.values, color='blue')
plt.xlabel('Country')
plt.ylabel('Number of Users')
plt.title('Top 10 Countries by Number of Users')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

plt.show()
