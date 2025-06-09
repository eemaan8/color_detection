import pandas as pd

df = pd.read_csv('color.csv')

def get_color_name(R, G, B):
    min_diff = float('inf')
    color_name = ""

    for i in range(len(df)):
        csv_r = int(df.loc[i, 'R'])
        csv_g = int(df.loc[i, 'G'])
        csv_b = int(df.loc[i, 'B'])

        # Calculate Euclidean distance
        diff = ((R - csv_r) ** 2 + (G - csv_g) ** 2 + (B - csv_b) ** 2) ** 0.5

        if diff < min_diff:
            min_diff = diff
            color_name = df.loc[i, 'ColorName']

    return color_name
