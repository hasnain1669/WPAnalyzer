import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Optional

def create_probability_cards(statistics: dict, variable: str) -> dict:
    """
    Generate data structure for probability display cards.
    """
    return {
        'variable': variable,
        'mean': statistics['mean'],
        'range': f"{statistics['min']:.2f} - {statistics['max']:.2f}",
        'probability': statistics['probability'],
        'trend': statistics['trend'],
        'units': statistics['units']
    }

def create_time_series(df: pd.DataFrame, variable: str, threshold: Optional[float] = None) -> go.Figure:
    """
    Create an interactive time series plot with threshold line.
    """
    
    fig = go.Figure()
    
    # Add main time series line
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['value'],
        mode='lines+markers',
        name=variable,
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6),
        hovertemplate='<b>Year:</b> %{x}<br><b>Value:</b> %{y:.2f}<extra></extra>'
    ))
    
    # Add threshold line if provided
    if threshold is not None:
        fig.add_trace(go.Scatter(
            x=df['year'],
            y=[threshold] * len(df),
            mode='lines',
            name='Threshold',
            line=dict(color='red', width=2, dash='dash'),
            hovertemplate=f'<b>Threshold:</b> {threshold:.2f}<extra></extra>'
        ))
        
        # Shade areas exceeding threshold
        exceeds = df['value'] > threshold
        if exceeds.any():
            fig.add_trace(go.Scatter(
                x=df.loc[exceeds, 'year'],
                y=df.loc[exceeds, 'value'],
                mode='markers',
                name='Exceeds Threshold',
                marker=dict(color='red', size=8, symbol='x'),
                hovertemplate='<b>Year:</b> %{x}<br><b>Value:</b> %{y:.2f}<br><b>Status:</b> Exceeds<extra></extra>'
            ))
    
    # Update layout
    fig.update_layout(
        title=f'{variable} - Historical Time Series',
        xaxis_title='Year',
        yaxis_title=variable,
        hovermode='x unified',
        template='plotly_white',
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_box_plot(data: np.ndarray, variable: str, threshold: Optional[float] = None) -> go.Figure:
    """
    Create a box plot showing value distribution with threshold marker.
    """
    
    fig = go.Figure()
    
    # Add box plot
    fig.add_trace(go.Box(
        y=data,
        name=variable,
        boxmean='sd',
        marker_color='#1f77b4',
        hovertemplate='<b>Value:</b> %{y:.2f}<extra></extra>'
    ))
    
    # Add threshold line if provided
    if threshold is not None:
        fig.add_shape(
            type="line",
            x0=-0.5,
            x1=0.5,
            y0=threshold,
            y1=threshold,
            line=dict(color="red", width=3, dash="dash")
        )
        
        fig.add_annotation(
            x=0.5,
            y=threshold,
            text=f"Threshold: {threshold:.2f}",
            showarrow=True,
            arrowhead=2,
            arrowcolor="red",
            ax=50,
            ay=0,
            bgcolor="white",
            bordercolor="red"
        )
    
    # Update layout
    fig.update_layout(
        title=f'{variable} - Value Distribution',
        yaxis_title=variable,
        template='plotly_white',
        height=400,
        showlegend=False
    )
    
    return fig

def create_trend_chart(trend_data: dict, variable: str) -> go.Figure:
    """
    Create a scatter plot with trend line showing long-term changes.
    """
    
    # Get the original data points
    years = list(range(len(trend_data['trend_line'])))
    trend_line = trend_data['trend_line']
    
    fig = go.Figure()
    
    # Add trend line
    fig.add_trace(go.Scatter(
        x=years,
        y=trend_line,
        mode='lines',
        name='Trend Line',
        line=dict(color='red', width=3),
        hovertemplate='<b>Year:</b> %{x}<br><b>Trend:</b> %{y:.2f}<extra></extra>'
    ))
    
    # Add trend information annotation
    direction_symbol = '↑' if trend_data['direction'] == 'increasing' else '↓'
    trend_text = f"{direction_symbol} {trend_data['direction'].capitalize()}<br>"
    trend_text += f"Slope: {trend_data['slope']:.3f} per year<br>"
    trend_text += f"R²: {trend_data['r_squared']:.3f} ({trend_data['significance']})"
    
    fig.add_annotation(
        x=0.02,
        y=0.98,
        xref='paper',
        yref='paper',
        text=trend_text,
        showarrow=False,
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='black',
        borderwidth=1,
        align='left',
        xanchor='left',
        yanchor='top'
    )
    
    # Update layout
    fig.update_layout(
        title=f'{variable} - Long-term Trend Analysis',
        xaxis_title='Years from Start',
        yaxis_title=variable,
        template='plotly_white',
        height=400,
        showlegend=True
    )
    
    return fig

def create_histogram(data: np.ndarray, variable: str, threshold: Optional[float] = None) -> go.Figure:
    """
    Create a histogram showing frequency distribution.
    """
    
    fig = go.Figure()
    
    # Create histogram
    fig.add_trace(go.Histogram(
        x=data,
        nbinsx=20,
        name=variable,
        marker_color='#1f77b4',
        opacity=0.7,
        hovertemplate='<b>Range:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>'
    ))
    
    # Add threshold line if provided
    if threshold is not None:
        fig.add_vline(
            x=threshold,
            line_dash="dash",
            line_color="red",
            line_width=3,
            annotation_text=f"Threshold: {threshold:.2f}",
            annotation_position="top right"
        )
    
    # Update layout
    fig.update_layout(
        title=f'{variable} - Frequency Distribution',
        xaxis_title=variable,
        yaxis_title='Frequency',
        template='plotly_white',
        height=400,
        showlegend=False,
        bargap=0.1
    )
    
    return fig

def create_probability_gauge(probability: float, variable: str) -> go.Figure:
    """
    Create a gauge chart showing probability of exceeding threshold.
    """
    
    # Determine color based on probability
    if probability < 30:
        color = "green"
    elif probability < 60:
        color = "yellow"
    else:
        color = "red"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=probability,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"{variable}<br>Probability of Exceeding Threshold"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 60], 'color': "lightyellow"},
                {'range': [60, 100], 'color': "lightcoral"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=80, b=20)
    )
    
    return fig

def create_heatmap_calendar(data_by_date: pd.DataFrame, variable: str) -> go.Figure:
    """
    Create a calendar heatmap showing values across dates.
    """
    
    fig = go.Figure(data=go.Heatmap(
        z=data_by_date['value'],
        x=data_by_date['date'],
        y=data_by_date['year'],
        colorscale='RdYlBu_r',
        hovertemplate='<b>Date:</b> %{x}<br><b>Year:</b> %{y}<br><b>Value:</b> %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f'{variable} - Calendar Heatmap',
        xaxis_title='Date',
        yaxis_title='Year',
        template='plotly_white',
        height=400
    )
    
    return fig

def create_percentile_chart(percentiles: dict, variable: str) -> go.Figure:
    """
    Create a bar chart showing percentile values.
    """
    
    percentile_labels = list(percentiles.keys())
    percentile_values = list(percentiles.values())
    
    fig = go.Figure(data=[
        go.Bar(
            x=percentile_labels,
            y=percentile_values,
            marker_color='#1f77b4',
            text=[f"{val:.2f}" for val in percentile_values],
            textposition='auto',
            hovertemplate='<b>%{x}:</b> %{y:.2f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=f'{variable} - Percentile Distribution',
        xaxis_title='Percentile',
        yaxis_title='Value',
        template='plotly_white',
        height=400,
        showlegend=False
    )
    
    return fig