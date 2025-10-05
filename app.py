import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
from data_processor import WeatherDataProcessor
from visualizations import create_probability_cards, create_time_series, create_box_plot, create_trend_chart
from export_handler import export_to_csv, export_to_json, generate_pdf_report

# Page configuration
st.set_page_config(
    page_title="NASA Weather Probability Analyzer",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #00008B;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 1px solid #90caf9;
    }
    .metric-card {
        background-color: #f5f5f5;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = WeatherDataProcessor()
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# Header
st.markdown('<h1 class="main-header">🌦️ NASA Weather Probability Analyzer</h1>', unsafe_allow_html=True)
st.markdown("### Plan your outdoor activities with confidence using historical weather data")

# Sidebar - Input Panel
with st.sidebar:
    st.header("📍 Location & Date Selection")
    
    # Location input methods
    location_method = st.radio(
        "Select location method:",
        ["Coordinates", "Location Search", "Map Pin-drop"]
    )
    
    if location_method == "Coordinates":
        col1, col2 = st.columns(2)
        with col1:
            latitude = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=47.6062, format="%.4f")
        with col2:
            longitude = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=-122.3321, format="%.4f")
        location_name = st.text_input("Location Name (optional)", "Seattle, WA")
    
    elif location_method == "Location Search":
        location_name = st.text_input("Search location", "Seattle, WA")
        # Simplified: In production, use geocoding API
        latitude = 47.6062
        longitude = -122.3321
        st.info(f"📍 Coordinates: {latitude}, {longitude}")
    
    else:  # Map Pin-drop
        st.info("Map integration placeholder - Use coordinates method for now")
        latitude = 47.6062
        longitude = -122.3321
        location_name = "Seattle, WA"
    
    st.markdown("---")
    
    # Date Selection
    st.header("📅 Date Selection")
    date_type = st.radio("Select date type:", ["Specific Date", "Date Range"])
    
    if date_type == "Specific Date":
        selected_date = st.date_input("Select date", datetime(2024, 10, 15))
        start_date = selected_date
        end_date = selected_date
    else:
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start date", datetime(2024, 10, 10))
        with col2:
            end_date = st.date_input("End date", datetime(2024, 10, 20))
    
    st.markdown("---")
    
    # Weather Variables
    st.header("🌡️ Weather Variables")
    variables = st.multiselect(
        "Select variables to analyze:",
        ["Temperature", "Precipitation", "Wind Speed", "Humidity", "Air Quality"],
        default=["Temperature", "Precipitation"]
    )
    
    st.markdown("---")
    
    # Threshold Customization
    st.header("⚠️ Threshold Settings")
    thresholds = {}
    
    if "Temperature" in variables:
        thresholds['temp'] = st.slider("Temperature threshold (°F)", 50, 110, 90)
    if "Precipitation" in variables:
        thresholds['precip'] = st.slider("Precipitation threshold (inches)", 0.0, 5.0, 2.0, 0.1)
    if "Wind Speed" in variables:
        thresholds['wind'] = st.slider("Wind speed threshold (mph)", 0, 50, 25)
    if "Humidity" in variables:
        thresholds['humidity'] = st.slider("Humidity threshold (%)", 0, 100, 80)
    if "Air Quality" in variables:
        thresholds['aqi'] = st.slider("Air Quality Index threshold", 0, 300, 100)
    
    st.markdown("---")
    
    # Historical Data Range
    st.header("📊 Historical Data")
    year_range = st.slider("Years of historical data", 10, 30, 20)
    
    # Analysis Button
    analyze_button = st.button("🔍 Analyze Weather Probability", type="primary", use_container_width=True)

# Main Content Area
if analyze_button:
    with st.spinner("Analyzing historical weather data..."):
        try:
            # Process data
            results = st.session_state.data_processor.analyze_weather(
                latitude=latitude,
                longitude=longitude,
                location_name=location_name,
                start_date=start_date,
                end_date=end_date,
                variables=variables,
                thresholds=thresholds,
                years=year_range
            )
            
            st.session_state.analysis_results = results
            st.success("✅ Analysis complete!")
            
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
            st.info("This demo uses simulated data. In production, it would connect to NASA APIs.")

# Display Results
if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    
    # Summary Cards
    st.header("📊 Analysis Summary")
    
    cols = st.columns(len(variables))
    for idx, variable in enumerate(variables):
        with cols[idx]:
            if variable in results['statistics']:
                stats = results['statistics'][variable]
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{variable}</h3>
                    <p><strong>Mean:</strong> {stats['mean']:.2f} {stats['units']}</p>
                    <p><strong>Range:</strong> {stats['min']:.2f} - {stats['max']:.2f}</p>
                    <p style="font-size: 1.5rem; color: #1f77b4;">
                        <strong>{stats['probability']:.1f}%</strong> chance of exceeding threshold
                    </p>
                    <p><strong>Trend:</strong> {stats['trend']:.2f} {stats['units']}/decade</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Visualizations
    st.header("📈 Detailed Visualizations")
    
    # Tabs for different chart types
    tab1, tab2, tab3, tab4 = st.tabs(["Time Series", "Distribution", "Trends", "Probability"])
    
    with tab1:
        st.subheader("Historical Time Series")
        for variable in variables:
            if variable in results['time_series']:
                fig = create_time_series(
                    results['time_series'][variable],
                    variable,
                    thresholds.get(variable.lower().split()[0], None)
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Value Distribution")
        for variable in variables:
            if variable in results['distributions']:
                fig = create_box_plot(
                    results['distributions'][variable],
                    variable,
                    thresholds.get(variable.lower().split()[0], None)
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Long-term Trends")
        for variable in variables:
            if variable in results['trends']:
                fig = create_trend_chart(
                    results['trends'][variable],
                    variable
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Probability Analysis")
        for variable in variables:
            if variable in results['probabilities']:
                prob_data = results['probabilities'][variable]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        f"{variable} - Exceeding Threshold",
                        f"{prob_data['exceed_probability']:.1f}%"
                    )
                with col2:
                    st.metric(
                        f"{variable} - Within Normal Range",
                        f"{prob_data['normal_probability']:.1f}%"
                    )
    
    st.markdown("---")
    
    # Interpretation
    st.header("💡 Interpretation & Recommendations")
    
    def generate_interpretation(results, variables, thresholds):
        """Generate natural language interpretation of results"""
        interpretation = f"<h4>Analysis for {results['location']} on {results['date']}</h4>"
        
        high_risk = []
        low_risk = []
        
        for variable in variables:
            if variable in results['statistics']:
                stats = results['statistics'][variable]
                prob = stats['probability']
                
                if prob > 60:
                    high_risk.append(f"{variable} ({prob:.1f}% chance of exceeding threshold)")
                elif prob < 20:
                    low_risk.append(f"{variable} ({prob:.1f}% chance of exceeding threshold)")
        
        if high_risk:
            interpretation += "<p><strong>⚠️ High Risk Factors:</strong></p><ul>"
            for item in high_risk:
                interpretation += f"<li>{item}</li>"
            interpretation += "</ul>"
        
        if low_risk:
            interpretation += "<p><strong>✅ Favorable Conditions:</strong></p><ul>"
            for item in low_risk:
                interpretation += f"<li>{item}</li>"
            interpretation += "</ul>"
        
        interpretation += "<p><em>Note: This analysis is based on historical data and provides probability estimates, not forecasts.</em></p>"
        
        return interpretation

    interpretation = generate_interpretation(results, variables, thresholds)
    st.markdown(f"<div class='info-box'>{interpretation}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Export Options
    st.header("📥 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv_data = export_to_csv(results)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=f"weather_analysis_{location_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        json_data = export_to_json(results)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name=f"weather_analysis_{location_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    with col3:
        st.button("Generate PDF Report", help="PDF export functionality coming soon")

else:
    # Welcome message
    st.markdown("""
    **🌾 Agricultural Planning**
    - Assess growing season conditions
    - Plan irrigation needs
    - Monitor climate trends
    """)

def generate_interpretation(results, variables, thresholds):
    """Generate natural language interpretation of results"""
    interpretation = f"<h4>Analysis for {results['location']} on {results['date']}</h4>"
    
    high_risk = []
    low_risk = []
    
    for variable in variables:
        if variable in results['statistics']:
            stats = results['statistics'][variable]
            prob = stats['probability']
            
            if prob > 60:
                high_risk.append(f"{variable} ({prob:.1f}% chance of exceeding threshold)")
            elif prob < 20:
                low_risk.append(f"{variable} ({prob:.1f}% chance of exceeding threshold)")
    
    if high_risk:
        interpretation += "<p><strong>⚠️ High Risk Factors:</strong></p><ul>"
        for item in high_risk:
            interpretation += f"<li>{item}</li>"
        interpretation += "</ul>"
    
    if low_risk:
        interpretation += "<p><strong>✅ Favorable Conditions:</strong></p><ul>"
        for item in low_risk:
            interpretation += f"<li>{item}</li>"
        interpretation += "</ul>"
    
    interpretation += "<p><em>Note: This analysis is based on historical data and provides probability estimates, not forecasts.</em></p>"
    
    return interpretation

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Data sources: NASA MERRA-2, GPM IMERG, MODIS | Built with Streamlit & Plotly</p>
    <p>⚠️ This tool provides historical probability analysis, not weather forecasts</p>
</div>
""", unsafe_allow_html=True)