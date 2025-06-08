import pandas as pd
import os
import re

def load_data(data_type):
    """Load data based on the selected type."""
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    if data_type == 'cargo':
        return load_cargo_data(base_path)
    elif data_type == 'vehicle':
        return load_vehicle_data(base_path)
    else:  # fatal
        return load_fatal_data(base_path)

def extract_year_from_filename(filename):
    match = re.search(r'(20[0-9]{2})', filename)
    if match:
        return int(match.group(1))
    return None

def load_cargo_data(base_path):
    """Load and process cargo accident data from '화물차 사고 데이터 시각화' folder."""
    cargo_path = os.path.join(base_path, '화물차 사고 데이터 시각화')
    
    # Load all Excel files in the cargo directory
    dfs = []
    for file in os.listdir(cargo_path):
        if file.endswith('.xls'):
            file_path = os.path.join(cargo_path, file)
            try:
                # Read Excel file, skipping the first few rows if they contain metadata
                df = pd.read_excel(file_path)
                
                # Rename columns to match expected format
                rename_dict = {
                    '발생건수': 'accident_count',
                    '사망자수': 'fatal_count',
                    '치사율(%)': 'fatal_rate',
                    '시도': 'region',
                    '지자체': 'region',
                    '도로형태': 'accident_type',
                    '사고유형': 'accident_type',
                    '연령대': 'accident_type',
                    '기상상태': 'accident_type',
                    '위반유형': 'accident_type',
                }
                df = df.rename(columns=rename_dict)
                
                # Add date column if not present
                year = extract_year_from_filename(file)
                if year is not None:
                    df['date'] = pd.to_datetime(f'{year}-01-01')
                elif '연도' in df.columns:
                    df['date'] = pd.to_datetime(df['연도'].astype(str) + '-01-01')
                
                # Keep only necessary columns
                keep_cols = ['date', 'region', 'accident_type', 'accident_count', 'fatal_count', 'fatal_rate']
                for col in keep_cols:
                    if col not in df.columns:
                        df[col] = None
                dfs.append(df[keep_cols])
            except Exception as e:
                print(f"Error loading {file}: {str(e)}")
                continue
    
    # Combine all dataframes
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"Loaded cargo data with columns: {combined_df.columns.tolist()}")
        print(f"Sample data:\n{combined_df.head()}")
    else:
        print("No cargo data files found or loaded successfully")
        combined_df = pd.DataFrame(columns=['date', 'region', 'accident_type', 'accident_count', 'fatal_count', 'fatal_rate'])
    
    return combined_df

def load_vehicle_data(base_path):
    """Load and process vehicle accident data from '차종별 교통사고/data' folder."""
    vehicle_path = os.path.join(base_path, '차종별 교통사고', 'data')
    
    # Load all Excel files in the vehicle directory
    dfs = []
    for file in os.listdir(vehicle_path):
        if file.endswith('.xlsx'):
            file_path = os.path.join(vehicle_path, file)
            try:
                df = pd.read_excel(file_path)
                
                # Check the first column name and melt/unpivot if necessary
                if '가해운전자 차종별 ' in df.columns:
                    # Extract rows with accident counts
                    df = df[df.iloc[:,1] == '사고건수']
                    # Extract only rows with vehicle types
                    df = df[df.iloc[:,0].str.contains('화물차|승용차|버스|이륜차|기타', na=False)]
                    # melt
                    id_vars = [df.columns[0], df.columns[1]]
                    value_vars = [col for col in df.columns if col not in id_vars]
                    df_melt = df.melt(id_vars=id_vars, value_vars=value_vars, var_name='accident_type', value_name='accident_count')
                    df_melt = df_melt.rename(columns={df.columns[0]: 'vehicle_type', df.columns[1]: 'stat_type'})
                    # Add date column if not present
                    year = extract_year_from_filename(file)
                    if year is not None:
                        df_melt['date'] = pd.to_datetime(f'{year}-01-01')
                    elif '사고년도' in df_melt.columns:
                        df_melt['date'] = pd.to_datetime(df_melt['사고년도'].astype(str) + '-01-01')
                    # region is missing, use vehicle_type/accident_type instead
                    df_melt['region'] = None
                    # Keep only necessary columns
                    keep_cols = ['date', 'region', 'accident_type', 'accident_count', 'vehicle_type']
                    for col in keep_cols:
                        if col not in df_melt.columns:
                            df_melt[col] = None
                    dfs.append(df_melt[keep_cols])
                else:
                    # If it's a simple table structure, use it directly
                    dfs.append(df)
            except Exception as e:
                print(f"Error loading {file}: {str(e)}")
                continue
    
    # Combine all dataframes
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"Loaded vehicle data with columns: {combined_df.columns.tolist()}")
        print(f"Sample data:\n{combined_df.head()}")
    else:
        print("No vehicle data files found or loaded successfully")
        combined_df = pd.DataFrame(columns=['date', 'region', 'accident_type', 'accident_count', 'vehicle_type'])
    
    return combined_df

def load_fatal_data(base_path):
    """Load and process fatal accident data from '사망사고 및 휴게소' folder."""
    fatal_path = os.path.join(base_path, '사망사고 및 휴게소')
    
    # Load all files in the fatal directory
    dfs = []
    # Load fatal accident information.xlsb
    xlsb_file = os.path.join(fatal_path, '사망사고정보.xlsb')
    try:
        import pyxlsb
        df = pd.read_excel(xlsb_file, engine='pyxlsb')
        rename_dict = {
            '발생년': 'year',
            '발생년월일시': 'datetime',
            '사망자수': 'fatal_count',
            '사고유형_대분류': 'accident_type',
            '도로형태': 'road_type',
            '발생지시도': 'region',
            '위도': 'lat',
            '경도': 'lon',
        }
        df = df.rename(columns=rename_dict)
        # Date processing
        if 'datetime' in df.columns:
            df['date'] = pd.to_datetime(df['datetime'].astype(str).str[:8], errors='coerce')
        elif 'year' in df.columns:
            df['date'] = pd.to_datetime(df['year'].astype(str) + '-01-01')
        keep_cols = ['date', 'region', 'accident_type', 'fatal_count', 'road_type', 'lat', 'lon']
        for col in keep_cols:
            if col not in df.columns:
                df[col] = None
        dfs.append(df[keep_cols])
    except Exception as e:
        print(f"Error loading fatal xlsb: {e}")
    # Rest area information CSV
    for file in os.listdir(fatal_path):
        if file.endswith('.csv'):
            try:
                df = pd.read_csv(os.path.join(fatal_path, file))
                dfs.append(df)
            except Exception as e:
                print(f"Error loading {file}: {e}")
    
    # Combine all dataframes
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"Loaded fatal data with columns: {combined_df.columns.tolist()}")
        print(f"Sample data:\n{combined_df.head()}")
    else:
        print("No fatal data files found or loaded successfully")
        combined_df = pd.DataFrame(columns=['date', 'region', 'accident_type', 'fatal_count', 'road_type', 'lat', 'lon'])
    
    return combined_df 