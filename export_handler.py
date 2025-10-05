import pandas as pd
import json
from datetime import datetime
from typing import Dict
import io

def export_to_csv(results: Dict) -> str:
    """
    Export analysis results to CSV format.
    Follows the specification: Location, Latitude, Longitude, Date, Variable, 
    Mean, StdDev, Threshold, Probability_Exceeding, Trend, Data_Source, Units
    """
    
    rows = []
    
    for variable, stats in results['statistics'].items():
        row = {
            'Location': results['location'],
            'Latitude': results['latitude'],
            'Longitude': results['longitude'],
            'Date': results['date'],
            'Variable': variable,
            'Mean': stats['mean'],
            'Median': stats['median'],
            'StdDev': stats['std'],
            'Min': stats['min'],
            'Max': stats['max'],
            'Threshold': stats.get('threshold', 'N/A'),
            'Probability_Exceeding': f"{stats['probability']:.2f}%",
            'Trend': f"{stats['trend']:.2f}",
            'Data_Source': stats['data_source'],
            'Units': stats['units'],
            'Percentile_10th': stats['percentiles']['10th'],
            'Percentile_25th': stats['percentiles']['25th'],
            'Percentile_50th': stats['percentiles']['50th'],
            'Percentile_75th': stats['percentiles']['75th'],
            'Percentile_90th': stats['percentiles']['90th']
        }
        rows.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(rows)
    
    # Add metadata as comments at the top
    metadata_text = f"# Weather Probability Analysis Report\n"
    metadata_text += f"# Generated: {results['metadata']['analysis_date']}\n"
    metadata_text += f"# Years Analyzed: {results['years_analyzed']}\n"
    metadata_text += f"# Data Sources: {', '.join(set(results['metadata']['data_sources'].values()))}\n"
    metadata_text += "#\n"
    
    # Convert to CSV
    csv_buffer = io.StringIO()
    csv_buffer.write(metadata_text)
    df.to_csv(csv_buffer, index=False)
    
    return csv_buffer.getvalue()

def export_to_json(results: Dict) -> str:
    """
    Export analysis results to JSON format with full metadata.
    """
    
    export_data = {
        'analysis_info': {
            'location': results['location'],
            'coordinates': {
                'latitude': results['latitude'],
                'longitude': results['longitude']
            },
            'date_range': results['date'],
            'years_analyzed': results['years_analyzed'],
            'generated_at': results['metadata']['analysis_date']
        },
        'statistics': {},
        'probabilities': results.get('probabilities', {}),
        'trends': {},
        'data_sources': results['metadata']['data_sources']
    }
    
    # Format statistics for each variable
    for variable, stats in results['statistics'].items():
        export_data['statistics'][variable] = {
            'summary': {
                'mean': round(stats['mean'], 2),
                'median': round(stats['median'], 2),
                'std_dev': round(stats['std'], 2),
                'min': round(stats['min'], 2),
                'max': round(stats['max'], 2)
            },
            'percentiles': {k: round(v, 2) for k, v in stats['percentiles'].items()},
            'threshold_analysis': {
                'threshold': stats.get('threshold', None),
                'probability_exceeding': round(stats['probability'], 2),
                'units': stats['units']
            },
            'trend': {
                'value': round(stats['trend'], 2),
                'units_per_decade': stats['units']
            },
            'data_source': stats['data_source']
        }
    
    # Add trend details
    for variable, trend in results.get('trends', {}).items():
        export_data['trends'][variable] = {
            'direction': trend['direction'],
            'slope': round(trend['slope'], 4),
            'r_squared': round(trend['r_squared'], 4),
            'significance': trend['significance']
        }
    
    return json.dumps(export_data, indent=2)

def export_time_series_csv(results: Dict) -> str:
    """
    Export detailed time series data to CSV.
    """
    
    all_data = []
    
    for variable, df in results.get('time_series', {}).items():
        for _, row in df.iterrows():
            all_data.append({
                'Location': results['location'],
                'Latitude': results['latitude'],
                'Longitude': results['longitude'],
                'Variable': variable,
                'Year': row['year'],
                'Value': row['value'],
                'Units': results['statistics'][variable]['units'],
                'Data_Source': results['statistics'][variable]['data_source']
            })
    
    df = pd.DataFrame(all_data)
    return df.to_csv(index=False)

def generate_pdf_report(results: Dict) -> bytes:
    """
    Generate a comprehensive PDF report.
    This is a placeholder - in production, would use reportlab or weasyprint.
    """
    
    # This would generate a full PDF report with:
    # - Executive summary
    # - Location details
    # - Statistical analysis for each variable
    # - Visualizations
    # - Recommendations
    # - Methodology notes
    
    report_text = f"""
    WEATHER PROBABILITY ANALYSIS REPORT
    ===================================
    
    Location: {results['location']}
    Coordinates: {results['latitude']}, {results['longitude']}
    Analysis Date: {results['date']}
    Years Analyzed: {results['years_analyzed']}
    
    SUMMARY OF FINDINGS
    -------------------
    """
    
    for variable, stats in results['statistics'].items():
        report_text += f"""
    {variable}:
        Mean: {stats['mean']:.2f} {stats['units']}
        Range: {stats['min']:.2f} - {stats['max']:.2f} {stats['units']}
        Probability of Exceeding Threshold: {stats['probability']:.1f}%
        Long-term Trend: {stats['trend']:.2f} {stats['units']}/decade
        Data Source: {stats['data_source']}
    """
    
    report_text += """
    
    METHODOLOGY
    -----------
    This analysis is based on historical NASA Earth observation data spanning
    multiple decades. Statistical methods include percentile analysis, trend
    detection using linear regression, and probability calculations based on
    historical frequency.
    
    DISCLAIMER
    ----------
    This report provides historical probability analysis and should not be
    interpreted as a weather forecast. Past weather patterns do not guarantee
    future conditions.
    """
    
    return report_text.encode('utf-8')

def create_summary_table(results: Dict) -> pd.DataFrame:
    """
    Create a summary table suitable for display or export.
    """
    
    summary_data = []
    
    for variable, stats in results['statistics'].items():
        summary_data.append({
            'Variable': variable,
            'Mean': f"{stats['mean']:.2f} {stats['units']}",
            'Range': f"{stats['min']:.2f} - {stats['max']:.2f}",
            'Exceeds Threshold': f"{stats['probability']:.1f}%",
            'Trend': f"{stats['trend']:.2f} {stats['units']}/decade",
            'Data Quality': 'High' if results['years_analyzed'] >= 20 else 'Moderate'
        })
    
    return pd.DataFrame(summary_data)

def export_metadata(results: Dict) -> Dict:
    """
    Extract and format metadata for export.
    """
    
    metadata = {
        'analysis': {
            'timestamp': results['metadata']['analysis_date'],
            'location': {
                'name': results['location'],
                'latitude': results['latitude'],
                'longitude': results['longitude']
            },
            'temporal_coverage': {
                'date_range': results['date'],
                'years_analyzed': results['years_analyzed']
            }
        },
        'data_sources': results['metadata']['data_sources'],
        'variables_analyzed': list(results['statistics'].keys()),
        'processing_info': {
            'statistical_methods': [
                'Percentile analysis',
                'Linear trend detection',
                'Probability calculation',
                'Distribution analysis'
            ],
            'quality_indicators': {
                'temporal_resolution': 'Daily',
                'spatial_resolution': 'Point-based',
                'data_completeness': 'High'
            }
        }
    }
    
    return metadata