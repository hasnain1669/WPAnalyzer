"""
Configuration file for NASA Weather Probability Analyzer
"""

import os
from typing import Dict

# NASA API Configuration
NASA_CONFIG = {
    'earthdata_username': os.getenv('NASA_EARTHDATA_USERNAME', ''),
    'earthdata_password': os.getenv('NASA_EARTHDATA_PASSWORD', ''),
    'api_key': os.getenv('NASA_API_KEY', ''),
}

# Data Source URLs
DATA_SOURCES = {
    'MERRA2': {
        'url': 'https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/',
        'variables': ['T2M', 'PRECTOT', 'U10M', 'V10M', 'QV2M'],
        'description': 'Modern-Era Retrospective analysis for Research and Applications'
    },
    'GPM_IMERG': {
        'url': 'https://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L3/GPM_3IMERGDF.06/',
        'variables': ['precipitation'],
        'description': 'Global Precipitation Measurement IMERG'
    },
    'MODIS': {
        'url': 'https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/',
        'variables': ['LST', 'AOD'],
        'description': 'Moderate Resolution Imaging Spectroradiometer'
    },
    'GIOVANNI': {
        'url': 'https://giovanni.gsfc.nasa.gov/giovanni/',
        'description': 'GES DISC Interactive Online Visualization ANd aNalysis Infrastructure'
    }
}

# Variable Mappings
VARIABLE_MAPPINGS = {
    'Temperature': {
        'dataset': 'MERRA2',
        'variable_name': 'T2M',
        'units': '°F',
        'conversion': lambda k: (k - 273.15) * 9/5 + 32,  # Kelvin to Fahrenheit
        'default_threshold': 90
    },
    'Precipitation': {
        'dataset': 'GPM_IMERG',
        'variable_name': 'precipitation',
        'units': 'inches',
        'conversion': lambda mm: mm / 25.4,  # mm to inches
        'default_threshold': 2.0
    },
    'Wind Speed': {
        'dataset': 'MERRA2',
        'variable_name': ['U10M', 'V10M'],
        'units': 'mph',
        'conversion': lambda ms: ms * 2.23694,  # m/s to mph
        'default_threshold': 25
    },
    'Humidity': {
        'dataset': 'MERRA2',
        'variable_name': 'QV2M',
        'units': '%',
        'conversion': lambda qv: qv * 100,  # Convert to percentage
        'default_threshold': 80
    },
    'Air Quality': {
        'dataset': 'MODIS',
        'variable_name': 'AOD',
        'units': 'AQI',
        'conversion': lambda aod: aod * 100,  # Simplified AQI conversion
        'default_threshold': 100
    }
}

# Analysis Configuration
ANALYSIS_CONFIG = {
    'default_years': 20,
    'min_years': 10,
    'max_years': 30,
    'date_window': 7,  # ±7 days around target date
    'cache_duration': 3600,  # 1 hour in seconds
    'max_concurrent_requests': 5
}

# Statistical Thresholds
PROBABILITY_THRESHOLDS = {
    'low': 0.30,      # < 30% probability
    'moderate': 0.60,  # 30-60% probability
    'high': 0.60       # > 60% probability
}

# Visualization Settings
VIZ_CONFIG = {
    'color_scheme': {
        'primary': '#1f77b4',
        'secondary': '#ff7f0e',
        'warning': '#d62728',
        'success': '#2ca02c'
    },
    'chart_height': 400,
    'chart_template': 'plotly_white'
}

# Export Settings
EXPORT_CONFIG = {
    'csv_encoding': 'utf-8',
    'json_indent': 2,
    'include_metadata': True,
    'decimal_places': 2
}

# Cache Configuration
CACHE_CONFIG = {
    'enabled': True,
    'backend': 'file',  # Options: 'file', 'redis', 'memory'
    'directory': './cache',
    'ttl': 3600
}

# Geocoding Configuration
GEOCODING_CONFIG = {
    'provider': 'nominatim',
    'user_agent': 'nasa_weather_analyzer',
    'timeout': 10
}

# Map Configuration
MAP_CONFIG = {
    'default_zoom': 10,
    'default_center': [39.8283, -98.5795],  # Center of USA
    'tile_layer': 'OpenStreetMap',
    'mapbox_token': os.getenv('MAPBOX_TOKEN', '')
}

# API Rate Limiting
RATE_LIMIT = {
    'requests_per_minute': 60,
    'requests_per_hour': 1000,
    'burst_size': 10
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'weather_analyzer.log'
}

# Error Messages
ERROR_MESSAGES = {
    'no_data': 'No data available for the specified location and date range.',
    'api_error': 'Error connecting to NASA data services. Please try again later.',
    'invalid_coordinates': 'Invalid coordinates. Latitude must be between -90 and 90, longitude between -180 and 180.',
    'invalid_date': 'Invalid date range. Please ensure dates are in the correct format.',
    'threshold_error': 'Invalid threshold value. Please enter a numeric value.'
}

# Success Messages
SUCCESS_MESSAGES = {
    'analysis_complete': 'Weather probability analysis completed successfully!',
    'export_complete': 'Data exported successfully!',
    'cache_hit': 'Data retrieved from cache.'
}

# Feature Flags
FEATURES = {
    'enable_map_selection': True,
    'enable_pdf_export': False,  # Not yet implemented
    'enable_multiple_locations': False,  # Future feature
    'enable_forecast_comparison': False,  # Future feature
    'enable_user_accounts': False,  # Future feature
    'enable_social_sharing': False  # Future feature
}

def get_config(key: str) -> Dict:
    """
    Retrieve configuration by key.
    """
    configs = {
        'nasa': NASA_CONFIG,
        'data_sources': DATA_SOURCES,
        'variables': VARIABLE_MAPPINGS,
        'analysis': ANALYSIS_CONFIG,
        'viz': VIZ_CONFIG,
        'export': EXPORT_CONFIG,
        'cache': CACHE_CONFIG,
        'map': MAP_CONFIG,
        'features': FEATURES
    }
    return configs.get(key, {})

def validate_config():
    """
    Validate that required configuration is present.
    """
    warnings = []
    
    if not NASA_CONFIG['api_key']:
        warnings.append("NASA API key not configured. Using simulated data.")
    
    if not MAP_CONFIG['mapbox_token']:
        warnings.append("Mapbox token not configured. Map features will be limited.")
    
    return warnings