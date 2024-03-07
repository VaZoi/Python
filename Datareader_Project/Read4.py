import pandas as pd
import matplotlib.pyplot as plt

csv_file = 'RandomData.csv'
data = pd.read_csv(csv_file, delimiter=';')

zip_code_column = 'Zip Code'

# Convert 'Zip Code' to numeric values
data[zip_code_column] = pd.to_numeric(data[zip_code_column], errors='coerce')

# Plot the histogram
plt.figure(figsize=(10, 6))
plt.hist(data[zip_code_column].dropna(), bins=20, color='orange', edgecolor='black')
plt.xlabel('Zip Code')
plt.ylabel('Frequency')
plt.title('Distribution of Zip Codes')
plt.show()
