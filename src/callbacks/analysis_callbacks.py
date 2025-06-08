from dash import Input, Output, State, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_loader import load_data
from utils.data_processor import process_cargo_data, process_vehicle_data, process_fatal_data
from utils.cache import get_cached_data

@callback(
    [Output('time-series-analysis', 'figure'),
     Output('regional-analysis', 'figure'),
     Output('accident-type-analysis', 'figure'),
     Output('correlation-analysis', 'figure')],
    [Input('analysis-data-selector', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('analysis-types', 'value')]
)
def update_analysis_graphs(data_type, start_date, end_date, analysis_types):
    # Load and process data
    df = get_cached_data(data_type)
    if data_type == 'cargo':
        df = process_cargo_data(df)
    elif data_type == 'vehicle':
        df = process_vehicle_data(df)
    else:
        df = process_fatal_data(df)
    
    # Filter by date range
    if start_date and end_date:
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # Initialize empty figures
    time_series_fig = go.Figure()
    regional_fig = go.Figure()
    accident_type_fig = go.Figure()
    correlation_fig = go.Figure()
    
    # Update figures based on selected analysis types
    if 'time' in analysis_types:
        time_series_fig = create_time_series_analysis(df, data_type)
    
    if 'region' in analysis_types:
        regional_fig = create_regional_analysis(df, data_type)
    
    if 'type' in analysis_types:
        accident_type_fig = create_accident_type_analysis(df, data_type)
    
    if 'correlation' in analysis_types:
        correlation_fig = create_correlation_analysis(df, data_type)
    
    return time_series_fig, regional_fig, accident_type_fig, correlation_fig

def create_time_series_analysis(df, data_type):
    if data_type == 'cargo':
        fig = px.line(df, x='date', y='accident_count',
                     title='화물차 사고 건수 추이')
    elif data_type == 'vehicle':
        fig = px.line(df, x='date', y=['car_accidents', 'truck_accidents'],
                     title='차종별 사고 건수 추이')
    else:
        fig = px.line(df, x='date', y='fatal_accidents',
                     title='사망사고 건수 추이')
    
    fig.update_layout(
        template='plotly_white',
        xaxis_title='날짜',
        yaxis_title='사고 건수',
        showlegend=True
    )
    return fig

def create_regional_analysis(df, data_type):
    if data_type == 'cargo':
        fig = px.bar(df.groupby('region')['accident_count'].sum().reset_index(),
                    x='region', y='accident_count',
                    title='지역별 화물차 사고 건수')
    elif data_type == 'vehicle':
        fig = px.bar(df.groupby('region')[['car_accidents', 'truck_accidents']].sum().reset_index(),
                    x='region', y=['car_accidents', 'truck_accidents'],
                    title='지역별 차종 사고 건수')
    else:
        fig = px.bar(df.groupby('region')['fatal_accidents'].sum().reset_index(),
                    x='region', y='fatal_accidents',
                    title='지역별 사망사고 건수')
    
    fig.update_layout(
        template='plotly_white',
        xaxis_title='지역',
        yaxis_title='사고 건수',
        showlegend=True
    )
    return fig

def create_accident_type_analysis(df, data_type):
    if data_type == 'cargo':
        fig = px.pie(df, values='accident_count', names='accident_type',
                    title='화물차 사고 유형 분포')
    elif data_type == 'vehicle':
        fig = px.pie(df, values='total_accidents', names='accident_type',
                    title='차종별 사고 유형 분포')
    else:
        fig = px.pie(df, values='fatal_accidents', names='accident_type',
                    title='사망사고 유형 분포')
    
    fig.update_layout(
        template='plotly_white',
        showlegend=True
    )
    return fig

def create_correlation_analysis(df, data_type):
    if data_type == 'cargo':
        corr_matrix = df[['accident_count', 'weather', 'road_condition']].corr()
    elif data_type == 'vehicle':
        corr_matrix = df[['car_accidents', 'truck_accidents', 'weather']].corr()
    else:
        corr_matrix = df[['fatal_accidents', 'rest_area_count', 'weather']].corr()
    
    fig = px.imshow(corr_matrix,
                    title='상관관계 분석',
                    labels=dict(color='상관계수'))
    
    fig.update_layout(
        template='plotly_white',
        xaxis_title='변수',
        yaxis_title='변수'
    )
    return fig 