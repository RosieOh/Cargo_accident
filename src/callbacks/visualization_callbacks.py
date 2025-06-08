from dash import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from utils.data_loader import load_data

def register_visualization_callbacks(app):
    @app.callback(
        Output('main-graph', 'figure'),
        [Input('data-selector', 'value'),
         Input('time-btn', 'n_clicks'),
         Input('region-btn', 'n_clicks'),
         Input('accident-btn', 'n_clicks'),
         Input('visualization-options', 'value')]
    )
    def update_main_graph(data_type, time_clicks, region_clicks, accident_clicks, viz_options):
        # Load data based on type
        df = load_data(data_type)
        
        # Determine which button was clicked
        ctx = dash.callback_context
        if not ctx.triggered:
            button_id = 'time-btn'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Create visualization based on button and data type
        if data_type == 'cargo':
            if button_id == 'time-btn':
                fig = create_time_series(df, viz_options)
            elif button_id == 'region-btn':
                fig = create_regional_map(df, viz_options)
            else:
                fig = create_accident_type_chart(df, viz_options)
        elif data_type == 'vehicle':
            if button_id == 'time-btn':
                fig = create_vehicle_time_series(df, viz_options)
            elif button_id == 'region-btn':
                fig = create_vehicle_regional_map(df, viz_options)
            else:
                fig = create_vehicle_type_chart(df, viz_options)
        else:  # fatal
            if button_id == 'time-btn':
                fig = create_fatal_time_series(df, viz_options)
            elif button_id == 'region-btn':
                fig = create_fatal_regional_map(df, viz_options)
            else:
                fig = create_fatal_type_chart(df, viz_options)
        
        return fig

def create_time_series(df, viz_options):
    # Create time series visualization for cargo data
    fig = go.Figure()
    
    # Check if the dataframe is empty
    if df.empty:
        fig.add_annotation(
            text="No data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False
        )
    else:
        # Add main line
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['accident_count'],  # Use standardized column name
            mode='lines+markers',
            name='사고 건수',
            line=dict(color='#1f77b4', width=2)
        ))
        
        # Add trend line if selected
        if 'trend' in viz_options:
            z = np.polyfit(range(len(df)), df['accident_count'], 1)
            p = np.poly1d(z)
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=p(range(len(df))),
                mode='lines',
                name='트렌드',
                line=dict(color='#ff7f0e', width=2, dash='dash')
            ))
        
        # Add mean line if selected
        if 'mean' in viz_options:
            mean_value = df['accident_count'].mean()
            fig.add_hline(
                y=mean_value,
                line_dash="dash",
                line_color="red",
                annotation_text="평균",
                annotation_position="right"
            )
    
    fig.update_layout(
        title='시간별 화물차 사고 추이',
        xaxis_title='날짜',
        yaxis_title='사고 건수',
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig

def create_regional_map(df, viz_options):
    # Create regional map visualization
    fig = px.choropleth(
        df,
        locations='region',
        locationmode='geojson-id',
        color='accidents',
        hover_name='region',
        color_continuous_scale='Viridis',
        title='지역별 화물차 사고 현황'
    )
    
    fig.update_geos(
        visible=False,
        scope='asia',
        center=dict(lat=35.907757, lon=127.766922),
        projection_scale=5
    )
    
    return fig

def create_accident_type_chart(df, viz_options):
    # Create accident type visualization
    fig = px.sunburst(
        df,
        path=['accident_type', 'severity'],
        values='count',
        title='사고 유형별 분석'
    )
    
    return fig

# Similar functions for vehicle and fatal data types... 