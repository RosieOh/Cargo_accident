from functools import lru_cache
import pandas as pd
import os
from datetime import datetime, timedelta

class DataCache:
    def __init__(self, cache_dir='.cache'):
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def get_cache_path(self, data_type):
        return os.path.join(self.cache_dir, f'{data_type}_data.parquet')
    
    def is_cache_valid(self, cache_path, max_age_hours=24):
        if not os.path.exists(cache_path):
            return False
        
        cache_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
        return datetime.now() - cache_time < timedelta(hours=max_age_hours)
    
    def save_to_cache(self, df, data_type):
        cache_path = self.get_cache_path(data_type)
        df.to_parquet(cache_path)
    
    def load_from_cache(self, data_type):
        cache_path = self.get_cache_path(data_type)
        if self.is_cache_valid(cache_path):
            return pd.read_parquet(cache_path)
        return None

# Create global cache instance
data_cache = DataCache()

@lru_cache(maxsize=32)
def get_cached_data(data_type):
    """Get cached data with LRU cache."""
    return data_cache.load_from_cache(data_type)

@lru_cache(maxsize=32)
def get_cached_visualization(data_type, viz_type, **kwargs):
    """Get cached visualization with LRU cache."""
    cache_key = f"{data_type}_{viz_type}_{str(kwargs)}"
    return None  # Implement actual caching logic

def clear_cache():
    """Clear all cached data."""
    data_cache = DataCache()
    for file in os.listdir(data_cache.cache_dir):
        os.remove(os.path.join(data_cache.cache_dir, file))
    get_cached_data.cache_clear()
    get_cached_visualization.cache_clear() 