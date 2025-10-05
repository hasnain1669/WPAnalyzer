"""
Utility functions for the Weather Probability Analyzer
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import hashlib
import json

def format_date(date_obj) -> str:
    """
    Format date object to string.
    """
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime('%Y-%m-%d')

def parse_date(date_str: str) -> datetime:
    """
    Parse date string to datetime object.
    """
    formats = ['%Y-%m-%d', '%m-%d-%Y', '%d/%m/%Y', '%m/%d/%Y']
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Unable to parse date: {date_str}")

def get_date_range(center_date, window_days: int = 7) -> Tuple[datetime, datetime]:
    """
    Get date range around a center date.
    """
    if isinstance(center_date, str):
        center_date = parse_date(center_date)
    
    start_date = center_date - timedelta(days=window_days)
    end_date = center_date + timedelta(days=window_days)
    
    return start_date, end_date

def generate_years_list(current_year: int, num_years: int) -> List[int]:
    """
    Generate list of years for historical analysis.
    """
    return list(range(current_year - num_years, current_year))

def calculate_day_of_year(date_obj) -> int:
    """
    Calculate day of year (1-366).
    """
    if isinstance(date_obj, str):
        date_obj = parse_date(date_obj)
    return date_obj.timetuple().tm_yday

def get_season(date_obj) -> str:
    """
    Determine season from date.
    """
    if isinstance(date_obj, str):
        date_obj = parse_date(date_obj)
    
    month = date_obj.month
    
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

def format_coordinates(lat: float, lon: float) -> str:
    """
    Format coordinates for display.
    """
    lat_dir = 'N' if lat >= 0 else 'S'
    lon_dir = 'E' if lon >= 0 else 'W'
    
    return f"{abs(lat):.4f}°{lat_dir}, {abs(lon):.4f}°{lon_dir}"

def calculate_distance(lat1: float, lon1: float, 
                      lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points using Haversine formula (in km).
    """
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = np.radians(lat1)
    lat2_rad = np.radians(lat2)
    delta_lat = np.radians(lat2 - lat1)
    delta_lon = np.radians(lon2 - lon1)
    
    a = np.sin(delta_lat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(delta_lon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    
    return R * c

def get_nearest_grid_point(lat: float, lon: float, 
                          resolution: float = 0.5) -> Tuple[float, float]:
    """
    Get nearest grid point for a given resolution.
    """
    grid_lat = round(lat / resolution) * resolution
    grid_lon = round(lon / resolution) * resolution
    
    return grid_lat, grid_lon

def create_bbox(lat: float, lon: float, 
                buffer: float = 0.5) -> Tuple[float, float, float, float]:
    """
    Create bounding box around a point.
    Returns (min_lon, min_lat, max_lon, max_lat)
    """
    return (
        lon - buffer,
        lat - buffer,
        lon + buffer,
        lat + buffer
    )

def interpolate_missing_values(data: np.ndarray, method: str = 'linear') -> np.ndarray:
    """
    Interpolate missing values in data.
    """
    if len(data) == 0:
        return data
    
    # Create pandas Series for easy interpolation
    series = pd.Series(data)
    
    if method == 'linear':
        series = series.interpolate(method='linear')
    elif method == 'nearest':
        series = series.fillna(method='ffill').fillna(method='bfill')
    
    return series.values

def smooth_data(data: np.ndarray, window: int = 3) -> np.ndarray:
    """
    Apply moving average smoothing.
    """
    if len(data) < window:
        return data
    
    return np.convolve(data, np.ones(window)/window, mode='valid')

def detect_outliers(data: np.ndarray, method: str = 'iqr', 
                   threshold: float = 1.5) -> np.ndarray:
    """
    Detect outliers in data.
    Returns boolean array where True indicates outlier.
    """
    if method == 'iqr':
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        
        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr
        
        return (data < lower_bound) | (data > upper_bound)
    
    elif method == 'zscore':
        mean = np.mean(data)
        std = np.std(data)
        z_scores = np.abs((data - mean) / std)
        
        return z_scores > threshold
    
    return np.zeros(len(data), dtype=bool)

def remove_outliers(data: np.ndarray, method: str = 'iqr') -> np.ndarray:
    """
    Remove outliers from data.
    """
    outliers = detect_outliers(data, method)
    return data[~outliers]

def calculate_percentile_range(data: np.ndarray, 
                               lower: int = 25, 
                               upper: int = 75) -> Tuple[float, float]:
    """
    Calculate percentile range.
    """
    return np.percentile(data, lower), np.percentile(data, upper)

def calculate_confidence_interval(data: np.ndarray, 
                                 confidence: float = 0.95) -> Tuple[float, float]:
    """
    Calculate confidence interval for mean.
    """
    mean = np.mean(data)
    std_err = np.std(data) / np.sqrt(len(data))
    
    # Use normal distribution approximation
    z_score = 1.96 if confidence == 0.95 else 2.576
    
    margin = z_score * std_err
    
    return mean - margin, mean + margin

def generate_cache_key(*args, **kwargs) -> str:
    """
    Generate a unique cache key from arguments.
    """
    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
    key_string = '_'.join(key_parts)
    
    return hashlib.md5(key_string.encode()).hexdigest()

def format_number(value: float, precision: int = 2) -> str:
    """
    Format number for display.
    """
    return f"{value:.{precision}f}"

def format_percentage(value: float, precision: int = 1) -> str:
    """
    Format percentage for display.
    """
    return f"{value:.{precision}f}%"

def create_summary_statistics(data: np.ndarray) -> Dict:
    """
    Create comprehensive summary statistics.
    """
    return {
        'count': len(data),
        'mean': float(np.mean(data)),
        'median': float(np.median(data)),
        'std': float(np.std(data)),
        'min': float(np.min(data)),
        'max': float(np.max(data)),
        'range': float(np.max(data) - np.min(data)),
        'q1': float(np.percentile(data, 25)),
        'q3': float(np.percentile(data, 75)),
        'iqr': float(np.percentile(data, 75) - np.percentile(data, 25)),
        'skewness': float(pd.Series(data).skew()),
        'kurtosis': float(pd.Series(data).kurtosis())
    }

def risk_level_from_probability(probability: float) -> str:
    """
    Determine risk level from probability.
    """
    if probability < 30:
        return 'Low'
    elif probability < 60:
        return 'Moderate'
    else:
        return 'High'

def risk_color_from_probability(probability: float) -> str:
    """
    Get color code for risk level.
    """
    if probability < 30:
        return '#2ca02c'  # Green
    elif probability < 60:
        return '#ff7f0e'  # Orange
    else:
        return '#d62728'  # Red

def create_interpretation_text(variable: str, statistics: Dict, 
                              threshold: float) -> str:
    """
    Generate natural language interpretation.
    """
    prob = statistics['probability']
    mean = statistics['mean']
    units = statistics['units']
    trend = statistics['trend']
    
    interpretation = f"For {variable}, "
    
    # Probability interpretation
    if prob > 60:
        interpretation += f"there is a <strong>high likelihood ({prob:.1f}%)</strong> "
    elif prob > 30:
        interpretation += f"there is a <strong>moderate chance ({prob:.1f}%)</strong> "
    else:
        interpretation += f"there is a <strong>low probability ({prob:.1f}%)</strong> "
    
    interpretation += f"of exceeding the threshold of {threshold} {units}. "
    
    # Historical average
    interpretation += f"The historical average is {mean:.2f} {units}. "
    
    # Trend interpretation
    if abs(trend) > 0.5:
        direction = "increasing" if trend > 0 else "decreasing"
        interpretation += f"There is a notable {direction} trend of {abs(trend):.2f} {units} per decade."
    else:
        interpretation += "The long-term trend is relatively stable."
    
    return interpretation

def validate_input_data(data: Dict) -> Tuple[bool, List[str]]:
    """
    Validate user input data.
    """
    errors = []
    
    # Check latitude
    if 'latitude' in data:
        if not -90 <= data['latitude'] <= 90:
            errors.append("Latitude must be between -90 and 90")
    
    # Check longitude
    if 'longitude' in data:
        if not -180 <= data['longitude'] <= 180:
            errors.append("Longitude must be between -180 and 180")
    
    # Check dates
    if 'start_date' in data and 'end_date' in data:
        try:
            start = parse_date(data['start_date'])
            end = parse_date(data['end_date'])
            if start > end:
                errors.append("Start date must be before end date")
        except ValueError as e:
            errors.append(f"Invalid date format: {str(e)}")
    
    return len(errors) == 0, errors

def export_summary_report(results: Dict) -> str:
    """
    Generate a text summary report.
    """
    report = f"""
WEATHER PROBABILITY ANALYSIS SUMMARY
=====================================

Location: {results['location']}
Coordinates: {results['latitude']}, {results['longitude']}
Analysis Date: {results['date']}
Historical Period: {results['years_analyzed']} years

"""
    
    for variable, stats in results['statistics'].items():
        report += f"\n{variable.upper()}\n"
        report += f"{'-' * len(variable)}\n"
        report += f"Mean: {stats['mean']:.2f} {stats['units']}\n"
        report += f"Range: {stats['min']:.2f} - {stats['max']:.2f} {stats['units']}\n"
        report += f"Probability of Exceeding Threshold: {stats['probability']:.1f}%\n"
        report += f"Long-term Trend: {stats['trend']:.2f} {stats['units']}/decade\n"
        report += f"Data Source: {stats['data_source']}\n"
    
    return report