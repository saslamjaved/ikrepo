import csv

# Define the data
data = [
    {'Year': 2023, 'Category': 'AI Tools', 'Market Share': 35.0},
    {'Year': 2023, 'Category': 'AI Trends', 'Market Share': 25.0},
    {'Year': 2022, 'Category': 'AI Tools', 'Market Share': 30.0},
    {'Year': 2022, 'Category': 'AI Trends', 'Market Share': 20.0},
    {'Year': 2021, 'Category': 'AI Tools', 'Market Share': 28.0},
    {'Year': 2021, 'Category': 'AI Trends', 'Market Share': 22.0},
    {'Year': 2020, 'Category': 'AI Tools', 'Market Share': 25.0},
    {'Year': 2020, 'Category': 'AI Trends', 'Market Share': 18.0},
    {'Year': 2019, 'Category': 'AI Tools', 'Market Share': 22.0},
    {'Year': 2019, 'Category': 'AI Trends', 'Market Share': 15.0}
]

# Define the CSV file path
csv_file_path = 'ai_market_trends.csv'

# Write data to CSV
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Year', 'Category', 'Market Share'])
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print(f'Data successfully written to {csv_file_path}')
