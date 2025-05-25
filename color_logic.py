# color_logic.py
import pandas as pd

# Load color data (CSV should be in same folder)
df = pd.read_csv('color.csv')

def get_color_name(R, G, B):
    min_diff = float('inf')
    color_name = ""
    for i in range(len(df)):
        csv_r = int(df.loc[i, 'R'])
        csv_g = int(df.loc[i, 'G'])
        csv_b = int(df.loc[i, 'B'])
        diff = abs(R - csv_r) + abs(G - csv_g) + abs(B - csv_b)
        if diff < min_diff:
            min_diff = diff
            color_name = df.loc[i, 'ColorName']
    return color_name
