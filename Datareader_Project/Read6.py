import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Assuming you have a GeoDataFrame containing country geometries, for example, using 'naturalearth_lowres' dataset
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

csv_file = 'RandomData.csv'
data = pd.read_csv(csv_file, delimiter=';')

country_column = 'Country'

# Count the occurrences of each country
country_counts = data[country_column].value_counts().reset_index()
country_counts.columns = ['name', 'count']

# Merge the user counts with the geometries
world = world.merge(country_counts, how='left', left_on='name', right_on='name')

# Plot the choropleth map
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world.boundary.plot(ax=ax)
world.plot(column='count', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
plt.title('User Distribution by Country')
plt.show()
