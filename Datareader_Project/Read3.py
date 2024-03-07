import pandas as pd
import matplotlib.pyplot as plt

csv_file = 'Randomdata.csv'
data = pd.read_csv(csv_file, delimiter=';')

country_column = 'Country'

# Count the occurrences of each country
country_counts = data[country_column].value_counts()

# Plot the pie chart
plt.figure(figsize=(8, 8))
plt.pie(country_counts, labels=country_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Country Distribution')
plt.show()
