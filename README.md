# 台灣大哥大 x NTU DAC G3 專案

## 介紹
此為台大資料分析與決策社第五屆下學期專案，透過建立 LSTM 預測模型，分析用戶特徵和行為記錄，幫助台灣大哥大預測 GeForce NOW 高風險流失的付費訂閱戶。

## 目錄
- 介紹
- 專案結構
- 環境與套件
- main.py
- 01_data_cleaning.py
- 02_get_dataset.ipynb
- 03_feature_split.ipynb
- 04_LSTM.ipynb
- 作者
- 更新時間

## 專案結構

├── main.py  
├── 01_data_cleaning.py  
├── 02_get_dataset.ipynb  
├── 03_feature_split.ipynb  
├── 04_LSTM.ipynb  
├── requirements.txt  
└── data  
    ├── 會員方案_20240123.csv  
    ├── 會員基本資料_20240123.csv  
    ├── 會員付費歷程_20240123.csv  
    ├── 會員遊玩歷程_20240123.csv  
    ├── 方案對照表_cleaned.csv  
    ├── 排除名單_20240123.csv  
    ├── 優惠碼對照表.csv  
    └── gamelist_genres_encoded.csv  

## 環境與套件
- python 3.11.6。
- 使用套件與版本儲存於 `requirements.txt` 並透過以下指令安裝。
  - `$ pip install -r requirements.txt`

## main.py
- **用途**
  - 一次性執行 01 ~ 04 之檔案。
- **使用方式**
  - 僅需將工作目錄設定於本專案後，直接執行本檔案即可。
  - `$ python3 main.py`

## 01_data_cleaning.py
- **用途**
  - 輸入原始資料，並將其清理乾淨，已用於後續製作模型資料以及分析、視覺化等使用。
- **步驟**
  - 載入所有 raw data
  - 欄位名稱轉換為英文
  - 根據排除名單，自所有資料中移除特定 ID 之資料
  - 移除非 CGP 通路之資料，非 CGP 通路不在分析範圍內
  - 移除基本方案之資料，基本方案不在分析範圍內
  - 移除日訂方案之資料，日訂方案不在分析範圍內
  - 移除內部測試之資料，內部測試不在分析範圍內
  - 移除特定優惠碼之資料，特定優惠碼不在分析範圍內
  - 部分 ping 值異常，移除極端 ping 值
  - 根據 `gamelist_genres_encoded.csv` 檔案進行遊戲名稱對照與處理
  - 日期格式轉換
  - 少數資料有「方案結束日早於方案起始日」之異常情況，將其移除
  - 性別標籤二元轉換
  - 台灣大哥大會員與否二元轉換
  - 連線方式標籤轉換
  - 平台標籤轉換
  - 優惠碼使用與否二元轉換
  - 高 ping 值二元轉換
  - 方案名稱包含括號與數字，但與分析內容無關，將其移除
  - 輸出資料
- **輸入檔案**
  - `會員方案_20240123.csv`: 會員方案原始資料
  - `會員基本資料_20240123.csv`: 會員基本資料原始資料
  - `會員付費歷程_20240123.csv`: 付費歷程原始資料
  - `會員遊玩歷程_20240123.csv`: 會員遊玩歷程原始資料
  - `gamelist_genres_encoded.csv`: 經手動處理後之遊戲名稱與類別對照表
- **輸出檔案**
  - `plan.csv`: 清理後之會員方案資料
  - `info.csv`: 清理後之會員基本資料
  - `payment.csv`: 清理後之付費歷程資料
  - `history.csv`: 清理後之會員遊玩歷程資料
  - `gamelist.csv`: 清理後之遊戲名稱與類別對照表

## 02_get_dataset.ipynb
- **用途**
  - 新增連線方式、遊玩平台、遊戲類別及是否在假期前中後訂閱退訂與訂閱方案類型特徵。
  - 製作訂閱區間大表。
- **步驟**
  - 定義數據處理函數：
   - `make_adj_end_date`: 調整計劃結束日期
   - `make_subscription`: 創建訂閱期間
   - `plan_type`: 分配計劃類型
   - `process_data_connect_platform_game_category`: 處理連接、平台、遊戲類別及假期相關特徵
  - 載入所有必要的 CSV 文件
  - 執行 `make_adj_end_date` 函數賦予各訂閱結束日期
  - 執行 `make_subscription` 函數創建訂閱區間大表
  - 執行 `process_data_connect_platform_game_category` 函數新增相關特徵
  - 執行 `plan_type` 函數為訂閱分配訂閱方案類型
  - 輸出處理後的數據
- **輸入檔案**
  - `plan.csv`: 訂閱數據
  - `history.csv`: 使用服務歷史數據
  - `info.csv`: 用戶資訊數據
  - `方案對照表_cleaned.csv`: 計劃對照表
  - `gamelist_genres_encoded.csv`: 遊戲列表及類別數據
- **輸出檔案**
  - `subscription.csv`: 處理後的訂閱區間大表

## 03_feature_split.ipynb
- **用途**
  - 結合訂閱區間大表與玩家歷史遊玩紀錄，從流失/未流失日期開始，每七天切分成一個欄位，直到訂閱起始日或半年。
- **步驟**
  - 切分每週日期區間
  - 計算每週平均遊玩時間 `avg_play_minute`（week1-week12）
  - 計算每週平均遊玩次數 `avg_row_count_by_day`（week1-week12）
  - 補上空值
  - 輸出資料
- **輸入檔案**
  - `subscription.csv`: 處理後的訂閱區間大表
  - `history.csv`: 使用服務歷史數據
- **輸出檔案**
  - `feature_week.csv`: 包含訂閱期間各周遊玩特徵

## 04_LSTM.ipynb
- **用途**
  - 運用特徵預測 GeForce NOW 高風險流失的付費訂閱戶。
- **步驟**
  - 數值變項歸一化
  - 類別變項 one-hot encoding
  - SMOTE 不平衡處理
  - 資料轉換為三維資料
  - 輸入 LSTM 模型
  - 輸出預測結果
- **輸入檔案**
  - `feature_week.csv`: 包含訂閱期間各周遊玩特徵
- **輸出檔案**
  - `feature_week_pred.csv`: 包含預測流失與否結果的 `feature_week` 資料

## 作者
本項目由 丁典秀、黃榆婷、鄭以希、陳高田、周敏慈、黃泓愷、林敬勛、黃郁庭 開發。
如有任何問題，請聯繫：charlottecheng920307@gmail.com

## 更新時間
本文件最後更新於 2024 年 7 月 23 日。
