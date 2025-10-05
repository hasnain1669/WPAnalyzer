# Quick Start Guide

Get the NASA Weather Probability Analyzer running in 5 minutes!

## 📦 Step 1: Setup (2 minutes)

### Create project folder and files

1. Create a new folder called `nasa-weather-analyzer`

2. Save these files in the folder:
   - `app.py` - Main application
   - `data_processor.py` - Data processing
   - `visualizations.py` - Charts
   - `export_handler.py` - Export functions
   - `utils.py` - Utilities
   - `config.py` - Configuration
   - `nasa_api.py` - NASA integration
   - `requirements.txt` - Dependencies
   - `.env.example` - Environment template

### Install dependencies

Open terminal/command prompt in the folder:

```bash
pip install -r requirements.txt
```

This installs:
- Streamlit (web framework)
- Plotly (visualizations)
- Pandas & NumPy (data processing)
- Other required packages

## 🚀 Step 2: Run the App (30 seconds)

In your terminal, run:

```bash
streamlit run app.py
```

You should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

## 🎯 Step 3: Use the App (2 minutes)

### Your first analysis:

1. **Left sidebar** - Configure analysis:
   - Keep default coordinates (Seattle: 47.6062, -122.3321)
   - Keep default date (October 15)
   - Select variables: Temperature, Precipitation
   - Set thresholds: Temp > 90°F, Precip > 2 inches
   - Keep 20 years of data

2. **Click "Analyze Weather Probability"**

3. **View results**:
   - Summary cards show probability percentages
   - Charts display historical patterns
   - Interpretation explains the findings

4. **Export data** (optional):
   - Click "Download CSV" for spreadsheet
   - Click "Download JSON" for structured data

## 💡 Quick Examples

### Example 1: Wedding Planning
```
Location: Seattle, WA (47.6062, -122.3321)
Date: October 15
Variables: Temperature, Precipitation
Question: Will it rain on my October wedding?

Result: See historical rain probability!
```

### Example 2: Summer Vacation
```
Location: Phoenix, AZ (33.4484, -112.0740)
Date: July 15
Variables: Temperature
Threshold: 105°F
Question: How hot does it get in July?

Result: See extreme heat probability!
```

### Example 3: Hiking Trip
```
Location: Denver, CO (39.7392, -104.9903)
Date: June 1-7 (range)
Variables: Temperature, Precipitation, Wind
Question: What's the weather like for hiking?

Result: See complete weather profile!
```

## 🔧 Common Locations

Copy-paste these coordinates:

| Location | Latitude | Longitude |
|----------|----------|-----------|
| New York, NY | 40.7128 | -74.0060 |
| Los Angeles, CA | 34.0522 | -118.2437 |
| Chicago, IL | 41.8781 | -87.6298 |
| Miami, FL | 25.7617 | -80.1918 |
| Seattle, WA | 47.6062 | -122.3321 |
| Denver, CO | 39.7392 | -104.9903 |
| Phoenix, AZ | 33.4484 | -112.0740 |
| Boston, MA | 42.3601 | -71.0589 |

## ⚙️ Optional: Production Setup

For real NASA data (not simulated):

1. **Register for NASA Earthdata**:
   - Visit: https://urs.earthdata.nasa.gov/users/new
   - Create free account

2. **Configure credentials**:
   ```bash
   # Copy template
   cp .env.example .env
   
   # Edit .env and add your credentials
   NASA_EARTHDATA_USERNAME=your_username
   NASA_EARTHDATA_PASSWORD=your_password
   ```

3. **Enable real data** in `nasa_api.py`:
   - Uncomment actual API calls
   - Comment out simulated data returns

4. **Install additional packages**:
   ```bash
   pip install pydap xarray netCDF4
   ```

## 🎨 Customization Tips

### Change default location
Edit `app.py`:
```python
latitude = st.number_input("Latitude", value=YOUR_LAT)
longitude = st.number_input("Longitude", value=YOUR_LON)
```

### Adjust thresholds
Edit `config.py`:
```python
VARIABLE_MAPPINGS = {
    'Temperature': {
        'default_threshold': 85  # Change from 90
    }
}
```

### Change years of data
Edit `config.py`:
```python
ANALYSIS_CONFIG = {
    'default_years': 25  # Change from 20
}
```

## 🐛 Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### "Port already in use"
```bash
streamlit run app.py --server.port 8502
```

### App won't start
1. Check Python version: `python --version` (need 3.8+)
2. Update pip: `pip install --upgrade pip`
3. Reinstall: `pip uninstall streamlit && pip install streamlit`

### Blank visualizations
- Refresh browser (Ctrl+R or Cmd+R)
- Check browser console for errors (F12)
- Try different browser (Chrome recommended)

## 📚 Next Steps

1. **Read full documentation**: See `README.md`
2. **Try different locations**: Test various cities
3. **Experiment with variables**: Mix and match weather factors
4. **Export data**: Download for Excel or Python analysis
5. **Share findings**: Use screenshots or export PDFs

## 💬 Understanding Results

### Probability Interpretation
- **< 30%**: Low risk, conditions unlikely
- **30-60%**: Moderate risk, plan contingencies
- **> 60%**: High risk, strongly consider alternatives

### Trend Interpretation
- **Positive trend**: Values increasing over time
- **Negative trend**: Values decreasing over time
- **Flat trend**: Relatively stable conditions

### Statistical Confidence
- **20+ years**: Highly reliable statistics
- **10-20 years**: Moderately reliable
- **< 10 years**: Limited confidence

## 🎓 Learning Resources

Watch these to understand the data:
- NASA Earthdata overview
- Introduction to MERRA-2
- Understanding climate data

Read about:
- Percentiles and probability
- Statistical significance
- Climate vs weather

## ✅ Verification

Make sure everything works:

- [ ] App starts without errors
- [ ] Sidebar inputs respond
- [ ] Analysis button works
- [ ] Charts display
- [ ] Export buttons work
- [ ] No console errors

## 🎉 You're Ready!

You now have a working weather probability analyzer!

**What to try**:
1. Analyze your own location
2. Check weather for upcoming events
3. Compare different seasons
4. Export and share findings
5. Customize for your needs

**Need help?**
- Check `README.md` for detailed docs
- Review code comments
- Check NASA Earthdata documentation

---

**Happy Analyzing! 📊🌦️**