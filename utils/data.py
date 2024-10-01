import pandas as pd

def save_data(data, filename):
    df = pd.json_normalize(data)
    df.to_csv(f'./data/{filename}.csv', index=False, sep=';')