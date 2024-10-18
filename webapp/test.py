import pandas as pd
import numpy as np

# Simulate loading data
print("Loading data...")
df = pd.read_csv(r"D:\01A-TRABAJO\PYTHON\DATASCIENCE\EJERCICIOS\final_project_space\Final_Project\df_clean.csv")
nombres_proveedores = pd.read_csv(r"D:\01A-TRABAJO\PYTHON\DATASCIENCE\EJERCICIOS\final_project_space\Final_Project\nombres_proveedores.csv", sep=';')
euros_proveedor = pd.read_csv(r"D:\01A-TRABAJO\PYTHON\DATASCIENCE\EJERCICIOS\final_project_space\Final_Project\euros_proveedor.csv", sep=',')

print("\nInitial data types:")
print(df.dtypes)
print(nombres_proveedores.dtypes)
print(euros_proveedor.dtypes)

# Convert columns to string
df['CLIENTE'] = df['CLIENTE'].astype(str)
nombres_proveedores['codigo'] = nombres_proveedores['codigo'].astype(str)
euros_proveedor['CLIENTE'] = euros_proveedor['CLIENTE'].astype(str)

print("\nData types after conversion:")
print(df.dtypes)
print(nombres_proveedores.dtypes)
print(euros_proveedor.dtypes)

# Convert numerical columns in euros_proveedor
for col in euros_proveedor.columns:
    if col != 'CLIENTE':
        euros_proveedor[col] = pd.to_numeric(euros_proveedor[col], errors='coerce')

print("\nData types in euros_proveedor after numeric conversion:")
print(euros_proveedor.dtypes)

# Simulate customer selection
customer_code = df['CLIENTE'].iloc[0]  # Take the first customer as an example
print(f"\nAnalysis for customer: {customer_code}")

customer_data = df[df["CLIENTE"] == str(customer_code)]
customer_euros = euros_proveedor[euros_proveedor["CLIENTE"] == str(customer_code)]

print("\nCustomer data:")
print(customer_data)
print("\nCustomer euro data:")
print(customer_euros)

# Obtain percentage of units sold by manufacturer
all_manufacturers = customer_data.iloc[:, 1:].T
all_manufacturers.index = all_manufacturers.index.astype(str)

print("\nAll manufacturers:")
print(all_manufacturers)
print(all_manufacturers.dtypes)

# Get total sales by manufacturer
sales_data = customer_euros.iloc[:, 1:].T
sales_data.index = sales_data.index.astype(str)

print("\nSales data:")
print(sales_data)
print(sales_data.dtypes)

# Remove the 'CLIENTE' row before attempting to sort sales data
sales_data_filtered = sales_data.drop(index='CLIENTE')

# Ensure all values are numeric
sales_data_filtered = sales_data_filtered.apply(pd.to_numeric, errors='coerce')

# Attempt to sort the sales data after filtering
try:
    print("\nAttempting to sort the sales data...")
    top_sales = sales_data_filtered.sort_values(by=sales_data_filtered.columns[0], ascending=False).head(10)
    print("Sorting successful:")
    print(top_sales)
except Exception as e:
    print(f"Error sorting: {str(e)}")
    print("Values in the first column:")
    print(sales_data_filtered[sales_data_filtered.columns[0]])
    print("Data types in the first column:")
    print(sales_data_filtered[sales_data_filtered.columns[0]].apply(type))

print("\nDebugging script completed.")
