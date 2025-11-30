# print('導入套件...')
import time
import pandas as pd
import numpy as np
from utils import *
import warnings
warnings.filterwarnings('ignore')

# 你的代码逻辑
# ...

# 恢复警告显示（可选）
# warnings.resetwarnings()


start_time = time.time()

# print('載入資料...')
plan = pd.read_csv('./data/會員方案_20240123.csv')
info = pd.read_csv('./data/會員基本資料_20240123.csv')
payment = pd.read_csv('./data/會員付費歷程_20240123.csv')
history = pd.read_csv('./data/會員遊玩歷程_20240123.csv')
gamelist = pd.read_csv('./data/gamelist_genres_encoded.csv')

# print('英文欄位名稱轉換...')
plan = to_eng_column_names(plan)
info = to_eng_column_names(info)
payment = to_eng_column_names(payment)
history = to_eng_column_names(history)
gamelist = to_eng_column_names(gamelist)

# print('處理排除名單...')
plan = remove_excluded_id(plan)
info = remove_excluded_id(info)
payment = remove_excluded_id(payment)
history = remove_excluded_id(history)

# print('移除非 CGP 通路...')
plan = remove_non_cgp(plan)

# print('移除基本方案...')
plan = remove_basic_plans(plan)

# print('移除日訂方案...')
plan = remove_daily_plans(plan)

# print('移除測試方案...')
plan = remove_test_plans(plan)

# print('移除特定優惠碼方案...')
plan, payment = remove_remark_plans(plan, payment)

# print('移除極端 ping 值...')
history = remove_extreme_values(history, 'ping')

# print('處理遊戲名稱...')
history = clean_game_names(history)

# print('轉換日期格式...')
plan = convert_datetime(plan)
payment = convert_datetime(payment)
history = convert_datetime(history)

# print('移除方案結束日早於方案起始日資料...')
plan = remove_opposite_datetime(plan)

# print('轉換性別標籤...')
info = convert_gender(info)

# print('轉換台灣大哥大會員標籤...')
info = convert_twm_number(info)

# print('轉換連線方式標籤...')
history = convert_connect(history)

# print('轉換平台標籤...')
history = convert_platform(history)

# print('標記使用優惠碼與否...')
plan = mark_promo(plan)

# print('標記高 ping 值...')
history = mark_high_ping(history)

# print('移除方案名稱之數字與小括號...')
info = remove_brackets(info, 'current_plan')
plan = remove_brackets(plan, 'plan')

# print('遊戲清單所有欄位之空值補 NA 並去除無遊戲名稱者...')
gamelist = gamelist.replace('', np.nan)
gamelist = gamelist[~gamelist['game'].isnull()]

# print('輸出資料...')
plan.to_csv('./data/plan.csv', index=False)
info.to_csv('./data/info.csv', index=False)
payment.to_csv('./data/payment.csv', index=False)
history.to_csv('./data/history.csv', index=False)
gamelist.to_csv('./data/gamelist.csv', index=False)

end_time = time.time()

execution_seconds = end_time - start_time
print(f'總執行時間為 {int(execution_seconds // 60)} 分 {int(execution_seconds % 60)} 秒')