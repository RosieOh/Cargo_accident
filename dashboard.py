import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import pandas as pd
import numpy as np
import os

# Initialize the Dash app with a modern theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.FLATLY,  # Modern flat theme
        'https://use.fontawesome.com/releases/v5.15.4/css/all.css'  # Font Awesome icons
    ]
)

# Custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>화물차 사고 데이터 분석 대시보드</title>
        {%favicon%}
        {%css%}
        <style>
            .dashboard-container {
                background-color: #f8f9fa;
                min-height: 100vh;
                padding: 20px;
            }
            .card {
                border: none;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s;
            }
            .card:hover {
                transform: translateY(-5px);
            }
            .card-header {
                background-color: #fff;
                border-bottom: none;
                padding: 20px;
            }
            .card-body {
                padding: 20px;
            }
            .stat-card {
                background: linear-gradient(45deg, #4b6cb7, #182848);
                color: white;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
            }
            .stat-card h3 {
                font-size: 2rem;
                margin-bottom: 10px;
            }
            .stat-card p {
                margin: 0;
                opacity: 0.8;
            }
            .dropdown-menu {
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .btn-group {
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            .btn {
                border-radius: 5px;
                padding: 8px 16px;
            }
            .graph-container {
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Data loading functions
def load_cargo_data():
    data_dir = "화물차 사고 데이터 시각화"
    data = {}
    
    # Load yearly data
    yearly_file = os.path.join(data_dir, "2018-2020 화물차 연도별 교통사고.xls")
    data['yearly'] = pd.read_excel(yearly_file)
    
    # Load regional data
    regional_file = os.path.join(data_dir, "2020년 화물차 지자체별 교통사고.xls")
    data['regional'] = pd.read_excel(regional_file)
    
    # Load accident type data
    accident_file = os.path.join(data_dir, "2020년 화물차 사고유형별 교통사고.xls")
    data['accident_type'] = pd.read_excel(accident_file)
    
    # Load weather data
    weather_file = os.path.join(data_dir, "2020년 화물차 기상상태별 교통사고.xls")
    data['weather'] = pd.read_excel(weather_file)
    
    return data

# Load data
data = load_cargo_data()

# Define the layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("화물차 사고 데이터 분석 대시보드", 
                       className="text-center mb-4",
                       style={'color': '#2c3e50', 'fontWeight': 'bold'}),
                html.P("화물차 교통사고 데이터를 다양한 관점에서 분석하고 시각화합니다.",
                      className="text-center text-muted mb-4")
            ], className="mb-5")
        ])
    ]),
    
    # Main Content
    dbc.Row([
        # Control Panel
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("분석 컨트롤", className="mb-0"),
                    html.Small("데이터와 시각화 옵션을 선택하세요", className="text-muted")
                ]),
                dbc.CardBody([
                    html.Div([
                        html.H5("데이터 선택", className="mb-3"),
                        dcc.Dropdown(
                            id='data-selector',
                            options=[
                                {'label': '연도별 분석', 'value': 'yearly'},
                                {'label': '지역별 분석', 'value': 'regional'},
                                {'label': '사고유형별 분석', 'value': 'accident_type'},
                                {'label': '기상상태별 분석', 'value': 'weather'}
                            ],
                            value='yearly',
                            className="mb-4"
                        ),
                        
                        html.H5("시각화 유형", className="mb-3"),
                        dbc.ButtonGroup([
                            dbc.Button([
                                html.I(className="fas fa-chart-bar mr-2"),
                                "막대 그래프"
                            ], id="bar-btn", color="primary", className="mr-2"),
                            dbc.Button([
                                html.I(className="fas fa-chart-line mr-2"),
                                "선 그래프"
                            ], id="line-btn", color="primary", className="mr-2"),
                            dbc.Button([
                                html.I(className="fas fa-chart-pie mr-2"),
                                "파이 차트"
                            ], id="pie-btn", color="primary", className="mr-2"),
                            dbc.Button([
                                html.I(className="fas fa-map-marker-alt mr-2"),
                                "지도"
                            ], id="map-btn", color="primary")
                        ], className="mb-4"),
                        
                        html.H5("추가 옵션", className="mb-3"),
                        dbc.Checklist(
                            id='visualization-options',
                            options=[
                                {'label': '트렌드 라인', 'value': 'trend'},
                                {'label': '평균값 표시', 'value': 'mean'},
                                {'label': '비교 분석', 'value': 'compare'}
                            ],
                            value=['trend'],
                            switch=True,
                            className="mb-3"
                        )
                    ])
                ])
            ], className="mb-4")
        ], width=4),
        
        # Main Visualization Area
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("데이터 시각화", className="mb-0"),
                    html.Small("선택한 데이터의 시각화 결과를 확인하세요", className="text-muted")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='main-graph', style={'height': '600px'})
                ])
            ])
        ], width=8)
    ]),
    
    # Statistics Summary
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("통계 요약", className="mb-0"),
                    html.Small("주요 통계 지표를 확인하세요", className="text-muted")
                ]),
                dbc.CardBody([
                    html.Div(id='stats-summary', className="row")
                ])
            ])
        ], width=12)
    ], className="mt-4")
], fluid=True, className="dashboard-container")

# Callback for main visualization
@app.callback(
    [Output('main-graph', 'figure'),
     Output('stats-summary', 'children')],
    [Input('data-selector', 'value'),
     Input('bar-btn', 'n_clicks'),
     Input('line-btn', 'n_clicks'),
     Input('pie-btn', 'n_clicks'),
     Input('map-btn', 'n_clicks'),
     Input('visualization-options', 'value')]
)
def update_visualization(data_type, bar_clicks, line_clicks, pie_clicks, map_clicks, viz_options):
    # Determine chart type based on button clicks
    ctx = dash.callback_context
    if not ctx.triggered:
        chart_type = 'bar'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        chart_type = button_id.replace('-btn', '')
    
    if data_type == 'yearly':
        df = data['yearly']
        if chart_type == 'bar':
            fig = px.bar(df, x='연도', y='발생건수',
                        title='연도별 화물차 교통사고 현황',
                        labels={'발생건수': '사고 건수', '연도': '연도'})
        elif chart_type == 'line':
            fig = px.line(df, x='연도', y='발생건수',
                         title='연도별 화물차 교통사고 추이',
                         labels={'발생건수': '사고 건수', '연도': '연도'})
            
        stats = [
            dbc.Col([
                html.Div([
                    html.H3(f"{df['발생건수'].sum():,}건", className="mb-2"),
                    html.P("총 사고 건수", className="text-muted mb-0")
                ], className="stat-card")
            ], width=4),
            dbc.Col([
                html.Div([
                    html.H3(f"{df['발생건수'].mean():.1f}건", className="mb-2"),
                    html.P("평균 사고 건수", className="text-muted mb-0")
                ], className="stat-card")
            ], width=4),
            dbc.Col([
                html.Div([
                    html.H3(f"{df['발생건수'].max():,}건", className="mb-2"),
                    html.P(f"최대 사고 건수 ({df.loc[df['발생건수'].idxmax(), '연도']}년)", className="text-muted mb-0")
                ], className="stat-card")
            ], width=4)
        ]
        
    elif data_type == 'regional':
        df = data['regional']
        if chart_type == 'bar':
            fig = px.bar(df, x='지자체', y='발생건수',
                        title='지자체별 화물차 교통사고 현황',
                        labels={'발생건수': '사고 건수', '지자체': '지역'})
        elif chart_type == 'map':
            fig = go.Figure(data=go.Scattergeo(
                lon=[127.5, 126.5, 129.0, 128.5, 127.0, 126.5, 127.5, 128.5, 127.0, 126.5, 127.5, 128.5, 127.0, 126.5, 127.5, 128.5, 127.0],
                lat=[37.5, 37.5, 35.5, 35.5, 35.5, 35.5, 35.5, 35.5, 35.5, 35.5, 35.5, 35.5, 35.5, 35.5, 35.5, 35.5, 35.5],
                text=df['지자체'],
                mode='markers',
                marker=dict(
                    size=df['발생건수']/100,
                    color=df['발생건수'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar_title='사고 건수'
                )
            ))
            
            fig.update_geos(
                center=dict(lat=36.5, lon=127.5),
                projection_scale=7,
                visible=True,
                scope='asia'
            )
            
            fig.update_layout(
                title='지역별 화물차 교통사고 현황',
                geo=dict(
                    showland=True,
                    landcolor='rgb(243, 243, 243)',
                    countrycolor='rgb(204, 204, 204)',
                )
            )
            
        stats = [
            dbc.Col([
                html.Div([
                    html.H3(f"{df['발생건수'].sum():,}건", className="mb-2"),
                    html.P("총 사고 건수", className="text-muted mb-0")
                ], className="stat-card")
            ], width=4),
            dbc.Col([
                html.Div([
                    html.H3(f"{df['발생건수'].mean():.1f}건", className="mb-2"),
                    html.P("평균 사고 건수", className="text-muted mb-0")
                ], className="stat-card")
            ], width=4),
            dbc.Col([
                html.Div([
                    html.H3(f"{df['발생건수'].max():,}건", className="mb-2"),
                    html.P(f"최다 사고 지역 ({df.loc[df['발생건수'].idxmax(), '지자체']})", className="text-muted mb-0")
                ], className="stat-card")
            ], width=4)
        ]
        
    elif data_type == 'accident_type':
        df = data['accident_type']
        if chart_type == 'bar':
            fig = px.bar(df, x='사고유형', y='발생건수',
                        title='사고유형별 화물차 교통사고 현황',
                        labels={'발생건수': '사고 건수', '사고유형': '사고 유형'})
        elif chart_type == 'pie':
            fig = px.pie(df, values='발생건수', names='사고유형',
                        title='사고유형별 화물차 교통사고 비율')
            
        stats = [
            dbc.Col([
                html.Div([
                    html.H3(f"{df['발생건수'].sum():,}건", className="mb-2"),
                    html.P("총 사고 건수", className="text-muted mb-0")
                ], className="stat-card")
            ], width=4),
            dbc.Col([
                html.Div([
                    html.H3(f"{df['발생건수'].mean():.1f}건", className="mb-2"),
                    html.P("평균 사고 건수", className="text-muted mb-0")
                ], className="stat-card")
            ], width=4),
            dbc.Col([
                html.Div([
                    html.H3(f"{df['발생건수'].max():,}건", className="mb-2"),
                    html.P(f"최다 발생 유형 ({df.loc[df['발생건수'].idxmax(), '사고유형']})", className="text-muted mb-0")
                ], className="stat-card")
            ], width=4)
        ]
        
    else:  # weather
        df = data['weather']
        if chart_type == 'bar':
            fig = px.bar(df, x='기상상태', y='발생건수',
                        title='기상상태별 화물차 교통사고 현황',
                        labels={'발생건수': '사고 건수', '기상상태': '기상 상태'})
        elif chart_type == 'pie':
            fig = px.pie(df, values='발생건수', names='기상상태',
                        title='기상상태별 화물차 교통사고 비율')
            
        stats = [
            dbc.Col([
                html.Div([
                    html.H3(f"{df['발생건수'].sum():,}건", className="mb-2"),
                    html.P("총 사고 건수", className="text-muted mb-0")
                ], className="stat-card")
            ], width=4),
            dbc.Col([
                html.Div([
                    html.H3(f"{df['발생건수'].mean():.1f}건", className="mb-2"),
                    html.P("평균 사고 건수", className="text-muted mb-0")
                ], className="stat-card")
            ], width=4),
            dbc.Col([
                html.Div([
                    html.H3(f"{df['발생건수'].max():,}건", className="mb-2"),
                    html.P(f"최다 발생 기상 ({df.loc[df['발생건수'].idxmax(), '기상상태']})", className="text-muted mb-0")
                ], className="stat-card")
            ], width=4)
        ]
    
    # Add trend line if selected
    if 'trend' in viz_options and chart_type in ['bar', 'line']:
        fig.add_trace(go.Scatter(
            x=df.iloc[:, 0],
            y=np.poly1d(np.polyfit(range(len(df)), df['발생건수'], 1))(range(len(df))),
            mode='lines',
            name='추세선',
            line=dict(dash='dash', color='red')
        ))
    
    # Add mean line if selected
    if 'mean' in viz_options and chart_type in ['bar', 'line']:
        fig.add_hline(y=df['발생건수'].mean(),
                     line_dash="dash",
                     line_color="green",
                     annotation_text="평균",
                     annotation_position="right")
    
    # Update layout for better visualization
    fig.update_layout(
        template='plotly_white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="#2c3e50"
        ),
        margin=dict(t=50, l=50, r=50, b=50)
    )
    
    return fig, stats

if __name__ == '__main__':
    app.run_server(debug=True) 