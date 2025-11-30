import pandas as pd
import numpy as np
import re

EXCLUSION_ID = pd.read_csv('./data/排除名單_20240123.csv').iloc[:, 0].tolist()
PROMOCODE = pd.read_csv('./data/優惠碼對照表.csv')
REMARK_PATTERNS = (
    PROMOCODE[
        PROMOCODE.iloc[:, 0].isin(
            ["內部測試", "其他(無法歸類)", "廠商合作-3C通路", "其他(無法歸類)", "廠商合作-硬體"]
        )
    ]
    .iloc[:, 1]
    .unique()
)
ENG_COLUMN_NAMES = {
    '台灣大會員編號': 'id',
    '台灣大哥大會員編號': 'id',
    '會員性別': 'gender',
    '會員目前年齡': 'age',
    '會員出生年月': 'birthday',
    '是否為台哥大門號': 'twm_number',
    '用戶方案名稱': 'current_plan',
    '會員Email': 'email',
    '方案名稱': 'plan',
    '方案起始日': 'start_date',
    '方案終止日': 'end_date',
    '方案取消日': 'cancel_date',
    '備註': 'remark',
    '備註(群組)': 'remark_summary',
    '申請通路': 'channel',
    '交易日期': 'payment_date',
    '原價金額': 'original_price',
    '折扣金額': 'discount',
    '實際扣款金額': 'actual_amount',
    '遊玩日期': 'play_date',
    '遊戲名稱': 'game',
    '網路連線方式': 'connect',
    '遊玩平台': 'platform',
    '延遲狀況(毫秒)': 'ping',
    '遊玩時間(分鐘數)-維度': 'play_minute',
    '遊玩時間(分鐘)': 'play_minute',
    '排隊時間': 'queuing',
    '遊玩次數': 'play_count',
    '支援平台': 'supported_platform',
    '遊戲上市日期': 'launch_date',
    '休閒': 'casual',
    '免費': 'free',
    '冒險': 'adventure',
    '動作': 'action',
    '多人線上戰術競技': 'multiplayer_tactical_competition',
    '大型多人連線': 'massive_multiplayer_online',
    '平台': 'platformer',
    '格鬥': 'fighting',
    '模擬': 'simulation',
    '獨立': 'indie',
    '競速': 'racing',
    '第一人稱射擊': 'first_person_shooter',
    '策略': 'strategy',
    '街機': 'arcade',
    '角色扮演': 'role_playing',
    '解謎': 'puzzle',
    '運動': 'sports',
    '闔家': 'family'
}
BASIC_PLAN_PATTERNS = '基本|basic'
DAILY_PLAN_PATTERNS = '單日|日訂|Day Pass'
TEST_PLAN_PATTERNS = '內部|測試|體驗'
GAME_SUFFIXES_LIST = [
    "Epic Games Store", "Ubisoft Connect", "Steam", 
    "Demo", "Closed Beta", "Closed Beta", "DEMO", "Uplay",
    "WW", "release", "GFNPC", "Windows" , "Taiwan",
    "Xbox app", "EA App", "my.com", "NA/EU", "Epic Games",
    "GFN PC", "CCP Launcher", "Wargaming", "Ubisoft",
    "GOG.com", "prerelease", "NA and EU", "Standalone launcher",
    "Mihoyo Launcher", "Korea", "Korean version", "North America",
    "Japan", "Instant Play Demo", "Wizards.com", "Battle.net",
    "Albion Launcher", "Riot Games", "APAC & SA", "launcher",
    "ROW", "Asia", "Grinding Gear", "GOTY", "GOG"
]
GAME_SUFFIXES_PATTERNS = re.compile(
    r"\s*-\s*(?:" + "|".join(map(re.escape, GAME_SUFFIXES_LIST)) + r")\s*.*$",
    flags=re.IGNORECASE,
)

GAME_NAMES = {
    'Overcooked! 2': 'Overcooked 2'
}



def to_eng_column_names(data, mapping=ENG_COLUMN_NAMES):
    '''
    轉換英文欄位名稱。
    '''
    new_data = data.rename(columns=mapping)
    return new_data

def remove_na_row(data):
    '''
    移除包含 NA 值的資料。
    '''
    new_data = data.dropna()
    return new_data

def remove_excluded_id(data, exclusion=EXCLUSION_ID):
    '''
    將列於排除名單的 ID 資料移除。
    '''
    new_data = data.drop(data[data['id'].isin(exclusion)].index)
    return new_data

def remove_basic_plans(data, pattern=BASIC_PLAN_PATTERNS):
    '''
    移除基本免費方案之資料，該方案不在分析範圍內。
    '''
    new_data = data[~data['plan'].astype(str).str.contains(pattern, case=False)]
    return new_data

def remove_daily_plans(data, pattern=DAILY_PLAN_PATTERNS):
    '''
    移除日訂方案之資料，該方案不在分析範圍內。
    '''
    new_data = data[~data['plan'].astype(str).str.contains(pattern, case=False)]
    return new_data

def remove_test_plans(data, pattern=TEST_PLAN_PATTERNS):
    '''
    移除內部測試方案，該方案不在分析範圍內。
    '''
    new_data = data[~data['plan'].astype(str).str.contains(pattern, case=False)]
    return new_data

def remove_remark_plans(plan, payment, pattern=REMARK_PATTERNS):
    '''
    移除特定優惠碼類別註記之資料，該註記不在分析範圍內。
    '''
    new_plan, new_payment = plan.copy(), payment.copy()
    new_payment = new_payment.merge(
        new_plan[['id', 'start_date', 'remark']],
        left_on=['id', 'payment_date'],
        right_on=['id', 'start_date'],
        how='left'
    )
    new_payment = new_payment[~new_payment['remark'].isin(pattern)].drop(['start_date', 'remark'], axis=1)
    new_plan = new_plan[~new_plan['remark'].isin(pattern)]
    return new_plan, new_payment

def remove_non_cgp(data):
    '''
    移除非 CGP 通路之資料，其他通路不在分析範圍內。
    '''
    new_data = data[data['channel'] == 'CGP']
    return new_data

def clean_game_names(data, suffixes=GAME_SUFFIXES_PATTERNS, mapping=GAME_NAMES):
    '''
    處理遊戲名稱。包含透過 mapping 參數中的參照表進行遊戲名稱對照、以及將特定遊戲的後綴去除，保持一致性。
    '''
    new_data = data.copy()
    new_data['game'] = new_data['game'].fillna('').astype(str)
    new_data['game'] = new_data['game'].str.replace(suffixes.pattern, '', regex=True)
    new_data['game'] = new_data['game'].str.replace("\u2019", "'")
    new_data['game'] = new_data['game'].map(mapping).fillna(new_data['game']).str.replace('?', '')
    return new_data

def remove_extreme_values(data, column, n=2):
    '''
    移除極端值資料。主要用於移除極端 ping 值資料，預設移除正負 2 個標準差
    '''
    lower = data[column].mean() - n * data[column].std()
    upper = data[column].mean() + n * data[column].std()
    new_data = data[(data[column] > lower) & (data[column] < upper)]
    return new_data

def convert_datetime(data):
    '''
    轉換時間欄位格式。
    '''
    new_data = data.copy()
    for column in new_data.columns:
        if 'date' in column.lower():
            try:
                new_data[column] = pd.to_datetime(new_data[column], format='%Y-%m-%d')
            except:
                new_data[column] = pd.to_datetime(new_data[column], format='%Y/%m/%d')
    return new_data

def remove_opposite_datetime(data):
    '''
    極少部分資料有「方案終止日」早於「方案起始日」之狀況且原因不明，將相關資料移除，避免異常數據導致異常分析結果。
    '''
    data = data[~(data['start_date'] > data['end_date'])]
    return data

def convert_gender(data):
    '''
    性別二元轉換。
    1 = 男性
    0 = 女性
    '''
    new_data = data.copy()
    if 'gender' in new_data.columns:
        new_data['gender'] = new_data['gender'].map({'男': 1, '女': 0})
    return new_data

def convert_twm_number(data):
    '''
    「是否為台灣大哥大門號」二元轉換。
    1 = 是台哥大門號用戶
    0 = 非台哥大門號用戶
    '''
    new_data = data.copy()
    if 'twm_number' in new_data.columns:
        new_data['twm_number'] = new_data['twm_number'].map({'N': 0, 'Y': 1})
    return new_data

def convert_connect(data):
    '''
    將連線方式彙整並進行轉換。共分為 WiFi、Mobile (行動網路)、Ethernet (乙太網路)、其他 (無法辨識等)。
    '''
    new_data = data.copy()
    if 'connect' in new_data.columns:
        def converter(label):
            if 'wifi' in label.lower():
                return 'wifi'
            elif 'mobile' in label.lower():
                return 'mobile'
            elif 'ethernet' in label.lower():
                return 'ethernet'
            else:
                return np.nan
        new_data['connect'] = new_data['connect'].astype(str).apply(converter)
    return new_data

def convert_platform(data):
    '''
    將遊玩平台彙整並進行轉換。共分為 Web、macOS、Windows、Linux、iOS、iPad、Android。
    '''
    new_data = data.copy()
    if 'platform' in new_data.columns:
        def converter(label):
            if 'webrtc' in label.lower():
                return 'web'
            elif 'macos' in label.lower():
                return 'macos'
            elif 'windows' in label.lower():
                return 'windows'
            elif 'linux' in label.lower():
                return 'linux'
            elif 'ios' in label.lower() or 'iphone' in label.lower():
                return 'ios'
            elif 'ipad' in label.lower():
                return 'ipados'
            elif 'android' in label.lower():
                return 'android'
            else:
                return 'other'
        new_data['platform'] = new_data['platform'].astype(str).apply(converter)
    return new_data

def mark_promo(data):
    '''
    標記是否使用優惠碼。
    1 = 是
    0 = 否
    '''
    if 'remark' in data.columns:
        new_data = data.copy()
        new_data['promo'] = 0
        new_data.loc[~new_data['remark'].isna(), 'promo'] = 1 
    return new_data

def mark_high_ping(data):
    '''
    標記 ping 值是否高於 250
    1 = 是
    0 = 否
    '''
    if 'ping' in data.columns:
        data['high_ping'] = (data['ping'] > 250).astype(int)
    return data

def remove_brackets(data, column):
    '''
    去除小括號與其內的數字。主要用於會員基本資料的「目前方案名稱」以及方案資料的「方案名稱」。
    '''
    new_data = data.copy()
    new_data[column] = data[column].str.replace(r'\s*\([^()]*\)\s*', '', regex=True)
    return new_data
