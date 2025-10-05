import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import random

class WeatherDataProcessor:
    """
    Handles weather data retrieval, processing, and statistical analysis.
    In production, this would connect to NASA APIs (MERRA-2, GPM IMERG, etc.)
    """
    
    def __init__(self):
        self.data_sources = {
            'Temperature': 'MERRA-2',
            'Precipitation': 'GPM IMERG',
            'Wind Speed': 'MERRA-2',
            'Humidity': 'MERRA-2',
            'Air Quality': 'MODIS'
        }
        
        self.units = {
            'Temperature': '°F',
            'Precipitation': 'inches',
            'Wind Speed': 'mph',
            'Humidity': '%',
            'Air Quality': 'AQI'
        }
    
    def analyze_weather(self, latitude: float, longitude: float, location_name: str,
                       start_date, end_date, variables: List[str], 
                       thresholds: Dict, years: int) -> Dict:
        """
        Main analysis function that orchestrates data retrieval and processing.
        """
        
        # Convert dates
        if hasattr(start_date, 'strftime'):
            start_date_str = start_date.strftime('%m-%d')
            end_date_str = end_date.strftime('%m-%d')
        else:
            start_date_str = start_date
            end_date_str = end_date
        
        results = {
            'location': location_name,
            'latitude': latitude,
            'longitude': longitude,
            'date': f"{start_date_str} to {end_date_str}",
            'years_analyzed': years,
            'statistics': {},
            'time_series': {},
            'distributions': {},
            'trends': {},
            'probabilities': {},
            'metadata': {
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data_sources': {}
            }
        }
        
        # Process each variable
        for variable in variables:
            # Fetch historical data (simulated for demo)
            historical_data = self._fetch_historical_data(
                latitude, longitude, start_date, end_date, 
                variable, years
            )
            
            # Calculate statistics
            stats = self._calculate_statistics(
                historical_data, 
                variable, 
                thresholds.get(variable.lower().split()[0])
            )
            results['statistics'][variable] = stats
            
            # Generate time series
            results['time_series'][variable] = self._generate_time_series(historical_data)
            
            # Generate distribution data
            results['distributions'][variable] = historical_data
            
            # Calculate trends
            results['trends'][variable] = self._calculate_trends(historical_data)
            
            # Calculate probabilities
            results['probabilities'][variable] = self._calculate_probabilities(
                historical_data,
                thresholds.get(variable.lower().split()[0])
            )
            
            # Add metadata
            results['metadata']['data_sources'][variable] = self.data_sources[variable]
        
        return results
    
    def _fetch_historical_data(self, lat: float, lon: float, start_date, 
                               end_date, variable: str, years: int) -> np.ndarray:
        """
        Simulate fetching historical data from NASA APIs.
        In production, this would use OPeNDAP, Giovanni, or direct API access.
        """
        
        # Simulate realistic data based on variable type
        np.random.seed(int(lat * 100 + lon * 100))
        
        if variable == "Temperature":
            # Simulate temperature data (°F)
            base_temp = 60 + lat * 0.5
            seasonal_variation = 15
            trend = 0.2  # warming trend
            
            data = []
            for year in range(years):
                year_temp = base_temp + np.random.normal(0, 8) + trend * year
                data.append(year_temp)
            
            return np.array(data)
        
        elif variable == "Precipitation":
            # Simulate precipitation data (inches)
            base_precip = 1.5
            data = np.random.gamma(2, base_precip, years)
            return data
        
        elif variable == "Wind Speed":
            # Simulate wind speed (mph)
            data = np.random.gamma(3, 5, years)
            return data
        
        elif variable == "Humidity":
            # Simulate humidity (%)
            base_humidity = 65
            data = base_humidity + np.random.normal(0, 15, years)
            return np.clip(data, 0, 100)
        
        elif variable == "Air Quality":
            # Simulate AQI
            data = np.random.gamma(2, 30, years)
            return np.clip(data, 0, 300)
        
        return np.random.normal(50, 10, years)
    
    def _calculate_statistics(self, data: np.ndarray, variable: str, 
                             threshold: float = None) -> Dict:
        """
        Calculate comprehensive statistics for the data.
        """
        
        stats = {
            'mean': float(np.mean(data)),
            'median': float(np.median(data)),
            'std': float(np.std(data)),
            'min': float(np.min(data)),
            'max': float(np.max(data)),
            'percentiles': {
                '10th': float(np.percentile(data, 10)),
                '25th': float(np.percentile(data, 25)),
                '50th': float(np.percentile(data, 50)),
                '75th': float(np.percentile(data, 75)),
                '90th': float(np.percentile(data, 90))
            },
            'units': self.units[variable],
            'data_source': self.data_sources[variable]
        }
        
        # Calculate probability of exceeding threshold
        if threshold is not None:
            probability = (np.sum(data > threshold) / len(data)) * 100
            stats['probability'] = float(probability)
            stats['threshold'] = threshold
        else:
            stats['probability'] = 0.0
            stats['threshold'] = None
        
        # Calculate trend
        years = np.arange(len(data))
        if len(data) > 1:
            coefficients = np.polyfit(years, data, 1)
            trend_per_year = coefficients[0]
            stats['trend'] = float(trend_per_year * 10)  # per decade
        else:
            stats['trend'] = 0.0
        
        return stats
    
    def _generate_time_series(self, data: np.ndarray) -> pd.DataFrame:
        """
        Generate time series dataframe for visualization.
        """
        
        current_year = datetime.now().year
        years = list(range(current_year - len(data), current_year))
        
        df = pd.DataFrame({
            'year': years,
            'value': data
        })
        
        return df
    
    def _calculate_trends(self, data: np.ndarray) -> Dict:
        """
        Calculate detailed trend information.
        """
        
        years = np.arange(len(data))
        
        # Linear regression
        if len(data) > 1:
            coefficients = np.polyfit(years, data, 1)
            trend_line = coefficients[0] * years + coefficients[1]
            
            # Calculate R-squared
            ss_res = np.sum((data - trend_line) ** 2)
            ss_tot = np.sum((data - np.mean(data)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        else:
            coefficients = [0, np.mean(data)]
            trend_line = data
            r_squared = 0
        
        return {
            'slope': float(coefficients[0]),
            'intercept': float(coefficients[1]),
            'trend_line': trend_line.tolist(),
            'r_squared': float(r_squared),
            'direction': 'increasing' if coefficients[0] > 0 else 'decreasing',
            'significance': 'strong' if abs(r_squared) > 0.7 else 'moderate' if abs(r_squared) > 0.4 else 'weak'
        }
    
    def _calculate_probabilities(self, data: np.ndarray, threshold: float = None) -> Dict:
        """
        Calculate various probability metrics.
        """
        
        if threshold is None:
            threshold = np.percentile(data, 75)
        
        exceed_count = np.sum(data > threshold)
        total_count = len(data)
        
        probabilities = {
            'exceed_probability': float((exceed_count / total_count) * 100),
            'normal_probability': float(((total_count - exceed_count) / total_count) * 100),
            'threshold_used': float(threshold),
            'exceed_count': int(exceed_count),
            'total_count': int(total_count)
        }
        
        # Calculate probability distribution
        hist, bin_edges = np.histogram(data, bins=20)
        probabilities['distribution'] = {
            'counts': hist.tolist(),
            'bin_edges': bin_edges.tolist()
        }
        
        return probabilities
    
    def fetch_nasa_data_opendap(self, dataset: str, variable: str, 
                                lat: float, lon: float, 
                                start_date: str, end_date: str):
        """
        Template for actual NASA OPeNDAP data access.
        This would be implemented in production with pydap or xarray.
        """
        
        # Example structure for real implementation:
        # from pydap.client import open_url
        # dataset_url = f"https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/{dataset}"
        # dataset = open_url(dataset_url)
        # data = dataset[variable][time_slice, lat_index, lon_index]
        
        pass
    
    def fetch_nasa_data_giovanni(self, service: str, dataset: str, 
                                 variable: str, bbox: Tuple, 
                                 start_date: str, end_date: str):
        """
        Template for NASA Giovanni API access.
        This would be implemented in production with requests.
        """
        
        # Example structure for real implementation:
        # import requests
        # giovanni_url = "https://giovanni.gsfc.nasa.gov/giovanni/daac-bin/service_manager.pl"
        # params = {
        #     'service': service,
        #     'dataset': dataset,
        #     'variable': variable,
        #     'bbox': f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
        #     'starttime': start_date,
        #     'endtime': end_date
        # }
        # response = requests.get(giovanni_url, params=params)
        
        pass
    
    def cache_data(self, key: str, data: any):
        """
        Cache frequently requested data for performance.
        In production, use Redis or file-based caching.
        """
        pass
    
    def get_cached_data(self, key: str):
        """
        Retrieve cached data if available.
        """
        pass