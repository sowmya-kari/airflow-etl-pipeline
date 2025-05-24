import pandas as pd

def transform():
    df = pd.read_json('data/raw_data.json')
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df = df[['date', 'positive', 'death']]
    df.to_csv('data/cleaned_data.csv', index=False)
