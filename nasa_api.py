"""
NASA API Integration Module
Handles connections to NASA Earth observation data services
"""

import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
from config import NASA_CONFIG, DATA_SOURCES, VARIABLE_MAPPINGS

class NASADataClient:
    """
    Client for accessing NASA Earth observation data.
    """
    
    def __init__(self):
        self.username = NASA_CONFIG['earthdata_username']
        self.password = NASA_CONFIG['earthdata_password']
        self.api_key = NASA_CONFIG['api_key']
        self.session = requests.Session()
        
        if self.username and self.password:
            self.session.auth = (self.username, self.password)
    
    def fetch_merra2_data(self, lat: float, lon: float, 
                          start_date: str, end_date: str,
                          variable: str) -> np.ndarray:
        """
        Fetch MERRA-2 reanalysis data.
        
        Example URL structure:
        https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/
        M2T1NXSLV.5.12.4/2020/01/MERRA2_400.tavg1_2d_slv_Nx.20200101.nc4
        """
        
        try:
            # In production, construct proper OPeNDAP URL
            base_url = DATA_SOURCES['MERRA2']['url']
            
            # This would use xarray or pydap to access the data
            # Example with xarray:
            # import xarray as xr
            # ds = xr.open_dataset(opendap_url, decode_times=True)
            # data = ds[variable].sel(lat=lat, lon=lon, method='nearest')
            # data = data.sel(time=slice(start_date, end_date))
            
            # For demo purposes, return simulated data
            print(f"Fetching MERRA-2 {variable} data for ({lat}, {lon})")
            return self._simulate_data(variable, start_date, end_date)
            
        except Exception as e:
            print(f"Error fetching MERRA-2 data: {e}")
            return self._simulate_data(variable, start_date, end_date)
    
    def fetch_gpm_imerg_data(self, lat: float, lon: float,
                             start_date: str, end_date: str) -> np.ndarray:
        """
        Fetch GPM IMERG precipitation data.
        
        Example URL:
        https://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L3/
        GPM_3IMERGDF.06/2020/01/3B-DAY.MS.MRG.3IMERG.20200101-S000000-E235959.V06.nc4
        """
        
        try:
            base_url = DATA_SOURCES['GPM_IMERG']['url']
            
            # In production:
            # ds = xr.open_dataset(opendap_url)
            # precip = ds['precipitation'].sel(lat=lat, lon=lon, method='nearest')
            # precip = precip.sel(time=slice(start_date, end_date))
            
            print(f"Fetching GPM IMERG precipitation data for ({lat}, {lon})")
            return self._simulate_data('precipitation', start_date, end_date)
            
        except Exception as e:
            print(f"Error fetching GPM IMERG data: {e}")
            return self._simulate_data('precipitation', start_date, end_date)
    
    def fetch_giovanni_data(self, variable: str, bbox: Tuple[float, float, float, float],
                           start_date: str, end_date: str) -> Dict:
        """
        Fetch data using NASA Giovanni interface.
        
        Giovanni provides time-averaged data and statistics.
        """
        
        try:
            giovanni_url = DATA_SOURCES['GIOVANNI']['url'] + 'daac-bin/service_manager.pl'
            
            params = {
                'service': 'ArAvTs',  # Area-Averaged Time Series
                'starttime': start_date,
                'endtime': end_date,
                'bbox': f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
                'data': variable,
                'format': 'json'
            }
            
            # In production:
            # response = self.session.get(giovanni_url, params=params)
            # data = response.json()
            
            print(f"Fetching Giovanni data for {variable}")
            return {'status': 'simulated', 'data': []}
            
        except Exception as e:
            print(f"Error fetching Giovanni data: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def fetch_hydrology_data(self, lat: float, lon: float,
                            start_date: str, end_date: str,
                            variables: List[str]) -> pd.DataFrame:
        """
        Fetch point-based data from Hydrology Data Rods.
        
        Good for precipitation and temperature point data.
        URL: https://hydro1.gesdisc.eosdis.nasa.gov/data/
        """
        
        try:
            # Construct API request
            hydro_url = "https://hydro1.gesdisc.eosdis.nasa.gov/daac-bin/access/timeseries.cgi"
            
            params = {
                'variable': ','.join(variables),
                'location': f"GEOM:POINT({lon},{lat})",
                'startDate': start_date,
                'endDate': end_date,
                'type': 'asc2'
            }
            
            # In production:
            # response = self.session.get(hydro_url, params=params)
            # df = pd.read_csv(io.StringIO(response.text))
            
            print(f"Fetching Hydrology Data Rods for ({lat}, {lon})")
            return pd.DataFrame()
            
        except Exception as e:
            print(f"Error fetching Hydrology data: {e}")
            return pd.DataFrame()
    
    def fetch_modis_data(self, lat: float, lon: float,
                        start_date: str, end_date: str,
                        product: str = 'MOD11A1') -> np.ndarray:
        """
        Fetch MODIS data (temperature, aerosols).
        
        Products:
        - MOD11A1: Land Surface Temperature
        - MOD04_L2: Aerosol Optical Depth
        """
        
        try:
            # MODIS data requires different access method
            # Usually through LAADS DAAC or AppEEARS
            
            print(f"Fetching MODIS {product} data for ({lat}, {lon})")
            return self._simulate_data('modis', start_date, end_date)
            
        except Exception as e:
            print(f"Error fetching MODIS data: {e}")
            return self._simulate_data('modis', start_date, end_date)
    
    def _simulate_data(self, variable: str, start_date: str, 
                      end_date: str) -> np.ndarray:
        """
        Generate simulated data for demonstration.
        Replace with actual API calls in production.
        """
        
        # Calculate number of years
        if isinstance(start_date, str):
            years = 20
        else:
            years = 20
        
        # Generate realistic simulated data
        np.random.seed(42)
        
        if variable in ['T2M', 'temperature']:
            # Temperature in Kelvin (convert to Fahrenheit later)
            data = 288 + np.random.normal(0, 3, years)  # ~59°F average
        elif variable in ['precipitation', 'PRECTOT']:
            # Precipitation in mm
            data = np.random.gamma(2, 25, years)
        elif variable in ['U10M', 'V10M', 'wind']:
            # Wind speed in m/s
            data = np.random.gamma(3, 2, years)
        elif variable in ['QV2M', 'humidity']:
            # Specific humidity
            data = np.random.normal(0.01, 0.003, years)
        elif variable in ['AOD', 'modis']:
            # Aerosol Optical Depth
            data = np.random.gamma(2, 0.15, years)
        else:
            data = np.random.normal(50, 10, years)
        
        return data
    
    def authenticate_earthdata(self) -> bool:
        """
        Authenticate with NASA Earthdata Login.
        """
        
        try:
            auth_url = "https://urs.earthdata.nasa.gov/api/users/tokens"
            
            if self.username and self.password:
                response = self.session.post(
                    auth_url,
                    auth=(self.username, self.password)
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    self.api_key = token_data.get('access_token', '')
                    return True
            
            return False
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    def get_data_availability(self, dataset: str, lat: float, 
                             lon: float) -> Dict:
        """
        Check data availability for a specific location and dataset.
        """
        
        availability = {
            'dataset': dataset,
            'location': (lat, lon),
            'available': True,
            'temporal_coverage': {
                'start': '1980-01-01',
                'end': datetime.now().strftime('%Y-%m-%d')
            },
            'spatial_resolution': '0.5° x 0.625°',
            'temporal_resolution': 'Daily',
            'variables': []
        }
        
        if dataset == 'MERRA2':
            availability['variables'] = ['T2M', 'PRECTOT', 'U10M', 'V10M', 'QV2M']
            availability['temporal_coverage']['start'] = '1980-01-01'
        elif dataset == 'GPM_IMERG':
            availability['variables'] = ['precipitation']
            availability['temporal_coverage']['start'] = '2000-06-01'
        elif dataset == 'MODIS':
            availability['variables'] = ['LST', 'AOD']
            availability['temporal_coverage']['start'] = '2000-02-24'
        
        return availability


class DataCache:
    """
    Simple caching mechanism for NASA data requests.
    """
    
    def __init__(self, cache_dir: str = './cache'):
        self.cache_dir = cache_dir
        self.cache = {}
        
        import os
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def get(self, key: str) -> Optional[any]:
        """
        Retrieve data from cache.
        """
        
        if key in self.cache:
            cached_item = self.cache[key]
            
            # Check if cache is still valid (1 hour TTL)
            if datetime.now() - cached_item['timestamp'] < timedelta(hours=1):
                return cached_item['data']
        
        return None
    
    def set(self, key: str, data: any):
        """
        Store data in cache.
        """
        
        self.cache[key] = {
            'data': data,
            'timestamp': datetime.now()
        }
    
    def generate_key(self, lat: float, lon: float, date: str, 
                    variable: str) -> str:
        """
        Generate cache key from parameters.
        """
        
        return f"{lat}_{lon}_{date}_{variable}"
    
    def clear_expired(self):
        """
        Remove expired cache entries.
        """
        
        current_time = datetime.now()
        expired_keys = []
        
        for key, item in self.cache.items():
            if current_time - item['timestamp'] > timedelta(hours=1):
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]


class DataValidator:
    """
    Validate NASA data for quality and completeness.
    """
    
    @staticmethod
    def validate_coordinates(lat: float, lon: float) -> bool:
        """
        Validate latitude and longitude.
        """
        return -90 <= lat <= 90 and -180 <= lon <= 180
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> bool:
        """
        Validate date range.
        """
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            return start <= end and end <= datetime.now()
        except:
            return False
    
    @staticmethod
    def validate_data_quality(data: np.ndarray) -> Dict:
        """
        Assess data quality metrics.
        """
        
        quality = {
            'completeness': 1.0 - (np.sum(np.isnan(data)) / len(data)),
            'has_outliers': False,
            'valid': True
        }
        
        # Check for outliers (values beyond 3 standard deviations)
        if len(data) > 0:
            mean = np.nanmean(data)
            std = np.nanstd(data)
            outliers = np.abs(data - mean) > 3 * std
            quality['has_outliers'] = np.any(outliers)
        
        quality['valid'] = quality['completeness'] > 0.8
        
        return quality


# Utility functions for data conversion

def kelvin_to_fahrenheit(temp_k: float) -> float:
    """Convert Kelvin to Fahrenheit."""
    return (temp_k - 273.15) * 9/5 + 32

def kelvin_to_celsius(temp_k: float) -> float:
    """Convert Kelvin to Celsius."""
    return temp_k - 273.15

def mm_to_inches(mm: float) -> float:
    """Convert millimeters to inches."""
    return mm / 25.4

def ms_to_mph(ms: float) -> float:
    """Convert meters per second to miles per hour."""
    return ms * 2.23694

def calculate_wind_speed(u: float, v: float) -> float:
    """Calculate wind speed from u and v components."""
    return np.sqrt(u**2 + v**2)

def specific_humidity_to_relative(q: float, temp_k: float, 
                                  pressure: float = 101325) -> float:
    """
    Convert specific humidity to relative humidity (approximate).
    """
    # Simplified conversion
    e_s = 611.2 * np.exp(17.67 * (temp_k - 273.15) / (temp_k - 29.65))
    e = q * pressure / (0.622 + 0.378 * q)
    rh = (e / e_s) * 100
    return min(100, max(0, rh))

def aod_to_aqi_estimate(aod: float) -> float:
    """
    Rough estimate of AQI from Aerosol Optical Depth.
    This is a simplified conversion for demonstration.
    """
    # Very rough approximation
    if aod < 0.1:
        return 50
    elif aod < 0.3:
        return 100
    elif aod < 0.5:
        return 150
    else:
        return 200