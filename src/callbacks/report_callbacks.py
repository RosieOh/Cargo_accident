from dash import Input, Output, State, callback, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from utils.data_loader import load_data
from utils.data_processor import process_cargo_data, process_vehicle_data, process_fatal_data
from utils.cache import get_cached_data

@callback(
    [Output('summary-section', 'children'),
     Output('metrics-section', 'children'),
     Output('trends-section', 'children'),
     Output('regional-section', 'children'),
     Output('accident-types-section', 'children'),
     Output('recommendations-section', 'children'),
     Output('report-date-range-display', 'children')],
    [Input('generate-report', 'n_clicks')],
    [State('report-type-selector', 'value'),
     State('report-date-range', 'start_date'),
     State('report-date-range', 'end_date'),
     State('report-sections', 'value')]
)
def generate_report(n_clicks, report_type, start_date, end_date, sections):
    if not n_clicks:
        return [html.Div()] * 7
    
    # Load and process data
    df = get_cached_data('cargo')  # Default to cargo data
    df = process_cargo_data(df)
    
    # Filter by date range
    if start_date and end_date:
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # Initialize empty sections
    summary = html.Div()
    metrics = html.Div()
    trends = html.Div()
    regional = html.Div()
    accident_types = html.Div()
    recommendations = html.Div()
    date_display = f"보고서 기간: {start_date} ~ {end_date}"
    
    # Generate sections based on selection
    if 'summary' in sections:
        summary = create_summary_section(df, report_type)
    
    if 'metrics' in sections:
        metrics = create_metrics_section(df, report_type)
    
    if 'trends' in sections:
        trends = create_trends_section(df, report_type)
    
    if 'regional' in sections:
        regional = create_regional_section(df, report_type)
    
    if 'accident_types' in sections:
        accident_types = create_accident_types_section(df, report_type)
    
    if 'recommendations' in sections:
        recommendations = create_recommendations_section(df, report_type)
    
    return summary, metrics, trends, regional, accident_types, recommendations, date_display

def create_summary_section(df, report_type):
    total_accidents = df['accident_count'].sum()
    avg_accidents = df['accident_count'].mean()
    max_accidents = df['accident_count'].max()
    min_accidents = df['accident_count'].min()
    
    return html.Div([
        html.H4("요약 통계", className="mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("총 사고 건수", className="card-title"),
                        html.H3(f"{total_accidents:,}건", className="card-text")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("평균 사고 건수", className="card-title"),
                        html.H3(f"{avg_accidents:.1f}건", className="card-text")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("최대 사고 건수", className="card-title"),
                        html.H3(f"{max_accidents:,}건", className="card-text")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("최소 사고 건수", className="card-title"),
                        html.H3(f"{min_accidents:,}건", className="card-text")
                    ])
                ])
            ], width=3)
        ])
    ])

def create_metrics_section(df, report_type):
    # Calculate key metrics
    metrics = {
        '사고 발생률': df['accident_count'].mean(),
        '사고 증가율': ((df['accident_count'].iloc[-1] / df['accident_count'].iloc[0]) - 1) * 100,
        '평균 사고 심각도': df['accident_severity'].mean(),
        '최다 사고 지역': df.groupby('region')['accident_count'].sum().idxmax()
    }
    
    return html.Div([
        html.H4("주요 지표", className="mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6(metric, className="card-title"),
                        html.H3(f"{value:.1f}" if isinstance(value, float) else value,
                               className="card-text")
                    ])
                ])
            ], width=3) for metric, value in metrics.items()
        ])
    ])

def create_trends_section(df, report_type):
    # Create trend analysis
    fig = px.line(df, x='date', y='accident_count',
                  title='사고 건수 추이')
    
    return html.Div([
        html.H4("추세 분석", className="mb-3"),
        dcc.Graph(figure=fig)
    ])

def create_regional_section(df, report_type):
    # Create regional analysis
    regional_data = df.groupby('region')['accident_count'].sum().reset_index()
    fig = px.bar(regional_data, x='region', y='accident_count',
                 title='지역별 사고 건수')
    
    return html.Div([
        html.H4("지역별 분석", className="mb-3"),
        dcc.Graph(figure=fig)
    ])

def create_accident_types_section(df, report_type):
    # Create accident type analysis
    type_data = df.groupby('accident_type')['accident_count'].sum().reset_index()
    fig = px.pie(type_data, values='accident_count', names='accident_type',
                 title='사고 유형 분포')
    
    return html.Div([
        html.H4("사고 유형 분석", className="mb-3"),
        dcc.Graph(figure=fig)
    ])

def create_recommendations_section(df, report_type):
    # Generate recommendations based on data analysis
    recommendations = [
        "사고가 많이 발생하는 지역에 대한 추가 안전 점검 실시",
        "악천후 시 운행 제한 강화",
        "휴게소 이용률이 낮은 구간에 대한 휴게소 확충 검토",
        "사고 유형별 맞춤형 안전 교육 프로그램 개발"
    ]
    
    return html.Div([
        html.H4("권장 사항", className="mb-3"),
        html.Ul([
            html.Li(recommendation) for recommendation in recommendations
        ])
    ])

@callback(
    Output('download-report', 'data'),
    Input('download-report', 'n_clicks'),
    prevent_initial_call=True
)
def download_report(n_clicks):
    if not n_clicks:
        return None
    
    # Generate report content
    report_content = "화물차 사고 데이터 분석 보고서\n\n"
    report_content += "1. 요약 통계\n"
    report_content += "2. 주요 지표\n"
    report_content += "3. 추세 분석\n"
    report_content += "4. 지역별 분석\n"
    report_content += "5. 사고 유형 분석\n"
    report_content += "6. 권장 사항\n"
    
    return dcc.send_string(report_content, filename="accident_report.txt") 