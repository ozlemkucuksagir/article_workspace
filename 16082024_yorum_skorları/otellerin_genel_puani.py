# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 19:05:54 2024

@author: usnis
"""

import pandas as pd

# Load the previously processed CSV with hotel_score
file_path = 'D:/makaleİçin/article_workspace/16082024_yorum_skorları/analiz_sonuclari_new_with_hotel_score.csv'
df = pd.read_csv(file_path)

# Calculate the average hotel_score for each hotel using the correct column name 'otel_ad'
hotel_score_avg = df.groupby('otel_ad')['hotel_score'].mean().reset_index()
hotel_score_avg.columns = ['otel_ad', 'hotel_score_avg']

# Load the oteller.csv file
oteller_df = pd.read_csv('D:/makaleİçin/article_workspace-kozi/article_workspace-kozi/svr/oteller.csv')

# Merge the average hotel_score with the oteller.csv data
oteller_df = pd.merge(oteller_df, hotel_score_avg, on='otel_ad', how='left')

# Replace NaN values in 'hotel_score_avg' column with 'null'
oteller_df['hotel_score_avg'] = oteller_df['hotel_score_avg'].fillna('null')

# Save the updated dataframe to a new CSV file
output_file_path_oteller = 'D:/makaleİçin/article_workspace/16082024_yorum_skorları/oteller_with_hotel_score_avg.csv'
oteller_df.to_csv(output_file_path_oteller, index=False)
