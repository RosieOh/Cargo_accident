import dash_bootstrap_components as dbc
from dash import html, dcc

def create_analysis_layout():
    return dbc.Container([
        # Navigation Bar
        dbc.Navbar(
            dbc.Container([
                dbc.NavbarBrand("화물차 사고 데이터 분석 대시보드", className="ms-2"),
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("대시보드", href="/", active="exact")),
                    dbc.NavItem(dbc.NavLink("데이터 분석", href="/analysis", active="exact")),
                    dbc.NavItem(dbc.NavLink("보고서", href="/report", active="exact")),
                ], className="ms-auto")
            ]),
            color="white",
            className="mb-4"
        ),

        # Main Content
        dbc.Row([
            # Left Sidebar
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("분석 설정"),
                    dbc.CardBody([
                        html.H5("데이터 선택", className="mb-3"),
                        dcc.Dropdown(
                            id='analysis-data-selector',
                            options=[
                                {'label': '화물차 사고 데이터', 'value': 'cargo'},
                                {'label': '차종별 교통사고', 'value': 'vehicle'},
                                {'label': '사망사고 및 휴게소', 'value': 'fatal'}
                            ],
                            value='cargo',
                            className="mb-3"
                        ),
                        html.Hr(),
                        html.H5("분석 기간", className="mb-3"),
                        dcc.DatePickerRange(
                            id='date-range',
                            className="mb-3"
                        ),
                        html.Hr(),
                        html.H5("분석 유형", className="mb-3"),
                        dcc.Checklist(
                            id='analysis-types',
                            options=[
                                {'label': '시계열 분석', 'value': 'time'},
                                {'label': '지역별 분석', 'value': 'region'},
                                {'label': '사고 유형 분석', 'value': 'type'},
                                {'label': '상관관계 분석', 'value': 'correlation'}
                            ],
                            value=['time'],
                            className="mb-3"
                        )
                    ])
                ], className="mb-4")
            ], width=3),

            # Main Content Area
            dbc.Col([
                # Analysis Results
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("시계열 분석"),
                            dbc.CardBody([
                                dcc.Graph(id='time-series-analysis')
                            ])
                        ], className="mb-4")
                    ], width=12)
                ]),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("지역별 분석"),
                            dbc.CardBody([
                                dcc.Graph(id='regional-analysis')
                            ])
                        ], className="mb-4")
                    ], width=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("사고 유형 분석"),
                            dbc.CardBody([
                                dcc.Graph(id='accident-type-analysis')
                            ])
                        ], className="mb-4")
                    ], width=6)
                ]),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("상관관계 분석"),
                            dbc.CardBody([
                                dcc.Graph(id='correlation-analysis')
                            ])
                        ])
                    ], width=12)
                ])
            ], width=9)
        ])
    ], fluid=True, className="px-4 py-3") 