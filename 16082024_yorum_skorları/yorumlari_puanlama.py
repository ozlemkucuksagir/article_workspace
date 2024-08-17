# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 18:56:32 2024

@author: usnis
"""

import pandas as pd

# Load the CSV file
file_path = 'D:/makaleİçin/article_workspace/16082024_yorum_skorları/analiz_sonuclari_new.csv'
df = pd.read_csv(file_path)

# Define a function to calculate the hotel_score
def calculate_hotel_score(row):
    if row['opion'] == 'olumlu':
        if 0.75 <= row['score'] <= 1.0:
            return 10
        elif 0.50 <= row['score'] < 0.75:
            return 9
        else:
            return 8
    elif row['opion'] == 'olumsuz':
        if row['score'] < 0.50:
            return 8
        elif 0.50 <= row['score'] < 0.75:
            return 7
        elif 0.75 <= row['score'] <= 1.0:
            return 6
    return None

# Apply the function to the dataframe to create the hotel_score column
df['hotel_score'] = df.apply(calculate_hotel_score, axis=1)

# Save the updated dataframe to a new CSV file
output_file_path = 'D:/makaleİçin/article_workspace/16082024_yorum_skorları/analiz_sonuclari_new_with_hotel_score.csv'
df.to_csv(output_file_path, index=False)
