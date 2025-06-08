import pandas as pd

def process_cargo_data(df: pd.DataFrame) -> pd.DataFrame:
    # Check if the dataframe is empty
    if df.empty:
        return df
    
    # 날짜 컬럼이 문자열이면 datetime으로 변환
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
    # 결측치 처리
    if 'accident_count' in df.columns:
        df['accident_count'] = pd.to_numeric(df['accident_count'], errors='coerce').fillna(0)
    if 'region' in df.columns:
        df['region'] = df['region'].fillna('미상')
    if 'accident_type' in df.columns:
        df['accident_type'] = df['accident_type'].fillna('기타')
    if 'accident_severity' in df.columns:
        df['accident_severity'] = pd.to_numeric(df['accident_severity'], errors='coerce').fillna(0)
    return df

def process_vehicle_data(df: pd.DataFrame) -> pd.DataFrame:
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
    for col in ['car_accidents', 'truck_accidents']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    if 'region' in df.columns:
        df['region'] = df['region'].fillna('미상')
    if 'accident_type' in df.columns:
        df['accident_type'] = df['accident_type'].fillna('기타')
    df['total_accidents'] = df.get('car_accidents', 0) + df.get('truck_accidents', 0)
    return df

def process_fatal_data(df: pd.DataFrame) -> pd.DataFrame:
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
    if 'fatal_accidents' in df.columns:
        df['fatal_accidents'] = pd.to_numeric(df['fatal_accidents'], errors='coerce').fillna(0)
    if 'region' in df.columns:
        df['region'] = df['region'].fillna('미상')
    if 'accident_type' in df.columns:
        df['accident_type'] = df['accident_type'].fillna('기타')
    if 'rest_area_count' in df.columns:
        df['rest_area_count'] = pd.to_numeric(df['rest_area_count'], errors='coerce').fillna(0)
    if 'weather' in df.columns:
        df['weather'] = pd.to_numeric(df['weather'], errors='coerce').fillna(0)
    return df 