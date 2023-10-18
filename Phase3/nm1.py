import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Read the data from the csv file
data = pd.read_csv("statsfinal.csv")
print("Info of the data:\n")
print(data.info())
print()

#Data cleaning
#1) identifying missing values
missing_values = data.isnull().sum()
print(missing_values)
print("There is no missing values")

#2)Drop rows with missing values
data.dropna(inplace=True)

#3)Remove duplicates
data.drop_duplicates(inplace=True)
#drop the column unnamed because it resembles the index
data = data.drop(columns=['Unnamed: 0'])

#data formatting
# Instead of formatting , Separate the date into separate columns
data['Day'] = data['Date'].apply(lambda x: x.split('-')[0])
data['Month'] = data['Date'].apply(lambda x: x.split('-')[1])
data['Year'] = data['Date'].apply(lambda x: x.split('-')[2])


#Data Reduction
#We remove 2010 and 2023 because it has insufficient data
data_reduced = data.query("Year != '2010' and Year != '2023'")

remove_date = []

for i in range(11,23):
    remove_date.append('31-9-20'+str(i))
    remove_date.append('31-11-20'+str(i))

#print(remove_date)

#These are incorrect dates so we remove them
data_reduced = data_reduced[~data_reduced['Date'].isin(remove_date)]

print("\nDataset after cleaning and processing\n")
print(data_reduced)

#Create a function that allows us to plot a bar chart for the 4 products
def plot_bar_chart(df, columns, stri, str1, val):
    # Aggregate sales for each product by year, by sum or mean
    if val == 'sum':
        sales_by_year = df.groupby('Year')[columns].sum().reset_index()
    elif val == 'mean':
        sales_by_year = df.groupby('Year')[columns].mean().reset_index()

    # Melt the data to make it easier to plot
    sales_by_year_melted = pd.melt(sales_by_year, id_vars='Year', value_vars=columns, var_name='Product', value_name='Sales')

    # Create a bar chart
    plt.figure(figsize=(20,4))
    sns.barplot(data=sales_by_year_melted, x='Year', y='Sales', hue='Product') #,palette="cividis")
    plt.xlabel('Year')
    plt.ylabel(stri)
    plt.title(f'{stri} by {str1}')
    plt.xticks(rotation=45)
    plt.show()

plot_bar_chart(data_reduced, ['Q-P1', 'Q-P2', 'Q-P3', 'Q-P4'],'Total Unit Sales', 'Year', 'sum')

plot_bar_chart(data_reduced, ['Q-P1', 'Q-P2', 'Q-P3', 'Q-P4'],'Mean Unit Sales', 'Year', 'mean')

plot_bar_chart(data_reduced, ['S-P1', 'S-P2', 'S-P3', 'S-P4'], 'Total Revenue', 'Year', 'sum')

plot_bar_chart(data_reduced, ['S-P1', 'S-P2', 'S-P3', 'S-P4'], 'Mean Revenue', 'Year', 'mean')

