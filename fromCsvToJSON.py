import pandas as pd

csv_file = 'data.csv'
json_file = 'output.json'

df = pd.read_csv(csv_file)
df.to_json(json_file, orient='records')

print(json_file)