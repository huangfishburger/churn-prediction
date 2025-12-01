# Taiwan Mobile x NTU DAC G3 Project

## Introduction
This project is the fifth-semester (spring term) initiative of the NTU Data Analytics and Consulting (DAC) club. It focuses on developing an LSTM predictive model to analyze user features and behavioral records, aiming to help Taiwan Mobile (TWM) predict paying subscribers at high risk of churn for its GeForce NOW service.

**(Note on Authorship): This repository is a derivative copy of the original team project. The code represents the combined efforts of the development team listed below. My primary contributions focused on feature engineering and model tuning.**

## Table of Contents
- Introduction
- Project Structure
- Environment and Packages
- main.py
- 01_data_cleaning.py
- 02_get_dataset.ipynb
- 03_feature_engineering.ipynb
- 04_LSTM.ipynb
- Authors
- Last Updated

## Project Structure
```
├── main.py  
├── 01_data_cleaning.py  
├── 02_get_dataset.ipynb  
├── 03_feature_engineering.ipynb  
├── 04_LSTM.ipynb  
├── requirements.txt  
└── data(Proprietary data - Not included in this repository)
    ├── 會員方案_20240123.csv  
    ├── 會員基本資料_20240123.csv  
    ├── 會員付費歷程_20240123.csv  
    ├── 會員遊玩歷程_20240123.csv  
    ├── 方案對照表_cleaned.csv  
    ├── 排除名單_20240123.csv  
    ├── 優惠碼對照表.csv  
    └── gamelist_genres_encoded.csv  
```

## Environment and Packages
- Python 3.11.6.
- Required packages and versions are saved in `requirements.txt` and can be installed using the following command:
  - `$ pip install -r requirements.txt`

## main.py
- **Purpose**
  - Executes files 01 through 04 sequentially in a single run.
- **Usage**
  - Set the working directory to this project folder, and execute the file directly.
  - `$ python3 main.py`

## 01_data_cleaning.py
- **Purpose**
  - Takes raw input data and cleans it for subsequent model dataset creation, analysis, and visualization.
- **Steps**
  - Load all raw data files.
  - Convert column names to English.
  - Remove data for specific IDs based on the exclusion list.
  - Remove data for non-CGP channels, as they are outside the scope of analysis.
  - Remove records related to basic plans, as they are outside the scope of analysis.
  - Remove records related to daily subscription plans.
  - Remove internal testing data.
  - Remove data associated with specific promo codes.
  - Remove extreme ping values due to identified data anomalies.
  - Perform game name reconciliation and processing based on the `gamelist_genres_encoded.csv` file.
  - Convert date formats.
  - Remove records where the "Plan End Date is earlier than Plan Start Date" due to data errors.
  - Binary conversion of gender labels.
  - Binary conversion of TWM membership status.
  - Convert connection type labels.
  - Convert platform labels.
  - Binary conversion for promo code usage.
  - Binary conversion for high ping values.
  - Remove numbers and parentheses from plan names, as they are irrelevant to the analysis.
  - Output processed data.
- **Input Files**
  - `member_plans_20240123.csv`: Raw member plan data
  - `member_basic_info_20240123.csv`: Raw member basic information
  - `member_payment_history_20240123.csv`: Raw payment history data
  - `member_play_history_20240123.csv`: Raw member play history data
  - `gamelist_genres_encoded.csv`: Manually processed game names and category mapping table
- **Output Files**
  - `plan.csv`: Cleaned member plan data
  - `info.csv`: Cleaned member basic information
  - `payment.csv`: Cleaned payment history data
  - `history.csv`: Cleaned member play history data
  - `gamelist.csv`: Cleaned game names and category mapping table

## 02_get_dataset.ipynb
- **Purpose**
  - Creates features related to connection method, playing platform, game categories, subscription/churn timing relative to holidays, and determines the subscription plan type.
  - Constructs the main subscription period table.
- **Steps**
  - Define data processing functions:
    - `make_adj_end_date`: Adjusts the plan end date.
    - `make_subscription`: Creates consolidated subscription periods.
    - `plan_type`: Assigns the dominant plan type to each subscription period.
    - `process_data_connect_platform_game_category`: Processes features related to connection, platform, game category, and holiday timing.
  - Load all necessary CSV files.
  - Execute `make_adj_end_date` to calculate the adjusted end date for each plan.
  - Execute `make_subscription` to create the main subscription period table.
  - Execute `process_data_connect_platform_game_category` to add behavioral and seasonal features.
  - Execute `plan_type` to assign the plan type to each subscription.
  - Output the processed data.
- **Input Files**
  - `plan.csv`: Subscription plan data
  - `history.csv`: Service usage history data
  - `info.csv`: User information data
  - `plan_reconciliation_cleaned.csv`: Plan reconciliation table
  - `gamelist_genres_encoded.csv`: Game list and category data
- **Output Files**
  - `subscription.csv`: Processed main subscription period table

## 03_feature_engineering.ipynb
- **Purpose**
  - Combines the main subscription table with player historical usage records, splitting the data into weekly features starting from the churn/non-churn date back to the subscription start date or half a year (26 weeks).
- **Steps**
  - Split the date range into weekly intervals.
  - Calculate the weekly average playing minutes (`avg_play_minute`) (week 1–12).
  - Calculate the weekly average play count per day (`avg_row_count_by_day`) (week 1–12).
  - Impute missing values (e.g., fill NaNs).
  - Output data.
- **Input Files**
  - `subscription.csv`: Processed main subscription period table
  - `history.csv`: Service usage history data
- **Output Files**
  - `feature_week.csv`: Contains weekly usage features across the subscription periods.

## 04_LSTM.ipynb
- **Purpose**
  - Utilizes the extracted features to predict high-risk churn paying subscribers for GeForce NOW.
- **Steps**
  - Normalize numerical variables.
  - One-hot encode categorical variables.
  - Handle class imbalance using SMOTE.
  - Reshape the data into a three-dimensional format for LSTM.
  - Input data into the LSTM model.
  - Output prediction results.
- **Input Files**
  - `feature_week.csv`: Weekly usage features.
- **Output Files**
  - `feature_week_pred.csv`: `feature_week` data including the predicted churn results.

## Authors
This project was developed by Dien-Shiou Ding, Yu-Ting Huang, I-Hsi Cheng, Gao-Tian Chen, Min-Tzu Chou, Hung-Kai Huang, Ching-Hsun Lin, and Yu-Ting Huang.
For any inquiries, please contact: sophia.ythuang@gmail.com

## Last Updated
This document was last updated on December 1, 2025.
