import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings

warnings.filterwarnings("ignore")

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

# Create a figure and axis
def month_plot():
    fig, ax = plt.subplots()

    # Plot the sales data for each product by month
    data_reduced.groupby('Month')[['Q-P1', 'Q-P2', 'Q-P3', 'Q-P4']].sum().plot(ax=ax)

    # Set the x-axis limits to only show up to December
    ax.set_xlim(left=0, right=13)

    # Set the axis labels and title
    ax.set_xlabel('Month')
    ax.set_ylabel('Total unit sales')
    ax.set_title('Trend in sales of all four products by month')

    # Show the plot
    plt.show()

#month_plot()

data_reduced['Month'] = data['Month'].replace('9', '09')

#month_plot()

def month_31_data(df, months):
    m31_data = df[df['Month'].isin(months) & (df['Day'] == '31')]
    return m31_data

_31_months = month_31_data(data_reduced, ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'])
#print(_31_months)

plot_bar_chart(_31_months, ['Q-P1', 'Q-P2', 'Q-P3', 'Q-P4'], 'Average Units', 'each Month, for 31st', 'mean')

plot_bar_chart(_31_months, ['S-P1', 'S-P2', 'S-P3', 'S-P4'], 'Average Revenue', 'each Month, for 31st', 'mean')

# gives us the average for all the 31st days across all years for each product
def avg_on_31st(df, product):
    df_31 = df[df['Day'] == '31']
    avg_sales = df_31[product].mean()
    return avg_sales

avg_on_31st(data_reduced, ['Q-P1', 'Q-P2', 'Q-P3', 'Q-P4']).round(2)

#print(avg_on_31st(data_reduced, ['S-P1', 'S-P2', 'S-P3', 'S-P4']).round(2))


#Top selling Products
def plot_top_selling_products(df, columns, stri, val):
    # Aggregate sales for each product by sum or mean
    if val == 'sum':
        product_sales = df[columns].sum()
    elif val == 'mean':
        product_sales = df[columns].mean()

    # Sort the products by sales in descending order
    product_sales = product_sales.sort_values(ascending=False)

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    sns.barplot(x=product_sales.index, y=product_sales.values, palette="viridis")
    plt.xlabel('Product')
    plt.ylabel(stri)
    plt.title(f'Top-Selling Products by {stri}')
    plt.xticks(rotation=45)

    # Add annotations to label the top-selling products
    for i, value in enumerate(product_sales):
        plt.text(i, value, f'{value:.2f}', ha='center', va='bottom')

    plt.show()

plot_top_selling_products(data_reduced, ['Q-P1', 'Q-P2', 'Q-P3', 'Q-P4'], 'Total Unit Sales', 'sum')
plot_top_selling_products(data_reduced, ['S-P1', 'S-P2', 'S-P3', 'S-P4'], 'Total Revenue', 'sum')

#Product with the highest sales

def top_selling_products_by_total_sales(df):
    # Calculate the total unit sales for each product
    total_sales = df[['Q-P1', 'Q-P2', 'Q-P3', 'Q-P4']].sum()

    # Get the product with the maximum total sales
    max_sales_product = total_sales.idxmax()
    max_sales_value = total_sales.max()

    return max_sales_product, max_sales_value

def top_selling_products_by_total_revenue(df):
    # Calculate the total revenue for each product
    total_revenue = df[['S-P1', 'S-P2', 'S-P3', 'S-P4']].sum()

    # Get the product with the maximum total revenue
    max_revenue_product = total_revenue.idxmax()
    max_revenue_value = total_revenue.max()

    return max_revenue_product, max_revenue_value

max_sales_product, max_sales_value = top_selling_products_by_total_sales(data_reduced)
max_revenue_product, max_revenue_value = top_selling_products_by_total_revenue(data_reduced)

print(f"The product with the highest total unit sales is {max_sales_product} with {max_sales_value} units.")
print(f"The product with the highest total revenue is {max_revenue_product} with ${max_revenue_value:.2f}.")


#Peak Sales Periods

def peak_sales_period(df, stri):
    if stri == 'Total Unit Sales':
        sales_column = 'Q-P'
    elif stri == 'Total Revenue':
        sales_column = 'S-P'

    # Create a list of columns to sum
    columns_to_sum = [f'{sales_column}1', f'{sales_column}2', f'{sales_column}3', f'{sales_column}4']

    max_sales_value = 0
    max_sales_month = None
    max_sales_year = None

    for year in df['Year'].unique():
        for month in df['Month'].unique():
            total_sales = df[(df['Year'] == year) & (df['Month'] == month)][columns_to_sum].sum().sum()
            if total_sales > max_sales_value:
                max_sales_value = total_sales
                max_sales_month = month
                max_sales_year = year

    if max_sales_month is not None and max_sales_year is not None:
        return max_sales_month, max_sales_year, max_sales_value
    else:
        return None, None, None

# Call the peak_sales_period function to calculate the peak unit sales and revenue
max_unit_sales_month, max_unit_sales_year, max_unit_sales_value = peak_sales_period(data_reduced, 'Total Unit Sales')
max_revenue_month, max_revenue_year, max_revenue_value = peak_sales_period(data_reduced, 'Total Revenue')

if max_unit_sales_month is not None and max_revenue_month is not None:
    print(f"The peak month for total unit sales is {max_unit_sales_month}-{max_unit_sales_year} with {max_unit_sales_value} units.")
    print(f"The peak month for total revenue is {max_revenue_month}-{max_revenue_year} with ${max_revenue_value:.2f}.")
else:
    print("Error: Unable to determine the peak sales period.")


# Create a function to plot sales trends by year
def sales_trends_by_year(df, columns, stri, val):
    # Aggregate sales for each product by year, by sum or mean
    if val == 'sum':
        sales_by_year = df.groupby('Year')[columns].sum().reset_index()
    elif val == 'mean':
        sales_by_year = df.groupby('Year')[columns].mean().reset_index()

    # Melt the data to make it easier to plot
    sales_by_year_melted = pd.melt(sales_by_year, id_vars='Year', value_vars=columns, var_name='Product', value_name='Sales')

    # Create a bar chart
    plt.figure(figsize=(20, 4))
    sns.barplot(data=sales_by_year_melted, x='Year', y='Sales', hue='Product')
    plt.xlabel('Year')
    plt.ylabel(stri)
    plt.title(f'{stri} by Year')
    plt.xticks(rotation=45)
    plt.show()

# Example of calling the function for sales trends by year
sales_trends_by_year(data_reduced, ['Q-P1', 'Q-P2', 'Q-P3', 'Q-P4'], 'Total Unit Sales', 'sum')
sales_trends_by_year(data_reduced, ['S-P1', 'S-P2', 'S-P3', 'S-P4'], 'Total Revenue', 'sum')
