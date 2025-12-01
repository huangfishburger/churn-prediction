"""
This script executes a comprehensive data processing pipeline for cleaning, filtering, and standardizing raw dataset inputs based on business-specific logic.
"""

import time
import pandas as pd
import numpy as np
from utils import *
import warnings
warnings.filterwarnings('ignore')

start_time = time.time()

# Load data
plan = pd.read_csv('./data/會員方案_20240123.csv')
info = pd.read_csv('./data/會員基本資料_20240123.csv')
payment = pd.read_csv('./data/會員付費歷程_20240123.csv')
history = pd.read_csv('./data/會員遊玩歷程_20240123.csv')
gamelist = pd.read_csv('./data/gamelist_genres_encoded.csv')

# Convert column names to English
plan = to_eng_column_names(plan)
info = to_eng_column_names(info)
payment = to_eng_column_names(payment)
history = to_eng_column_names(history)
gamelist = to_eng_column_names(gamelist)

# Remove exclusive data
plan = remove_excluded_id(plan)
info = remove_excluded_id(info)
payment = remove_excluded_id(payment)
history = remove_excluded_id(history)
plan = remove_non_cgp(plan)
plan = remove_basic_plans(plan)
plan = remove_daily_plans(plan)
plan = remove_test_plans(plan)
plan, payment = remove_remark_plans(plan, payment)
history = remove_extreme_values(history, 'ping')

# Process game names
history = clean_game_names(history)

# Convert date formats
plan = convert_datetime(plan)
payment = convert_datetime(payment)
history = convert_datetime(history)
plan = remove_opposite_datetime(plan)

# Convert labels
info = convert_gender(info)
info = convert_twm_number(info)
history = convert_connect(history)
history = convert_platform(history)

# Additional mark
plan = mark_promo(plan)
history = mark_high_ping(history)

# Remove brackets
info = remove_brackets(info, 'current_plan')
plan = remove_brackets(plan, 'plan')

# Fill NaN values
gamelist = gamelist.replace('', np.nan)
gamelist = gamelist[~gamelist['game'].isnull()]

# Export
plan.to_csv('./data/plan.csv', index=False)
info.to_csv('./data/info.csv', index=False)
payment.to_csv('./data/payment.csv', index=False)
history.to_csv('./data/history.csv', index=False)
gamelist.to_csv('./data/gamelist.csv', index=False)

end_time = time.time()

execution_seconds = end_time - start_time
print(f'Total execution time is {int(execution_seconds // 60)} min {int(execution_seconds % 60)} sec')
