import dash_bootstrap_components as dbc
from dash import html, dcc
from components.graphs.pipeline_graph import create_pipeline_graph

def create_main_layout():
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
                    dbc.CardHeader("데이터 파이프라인"),
                    dbc.CardBody([
                        create_pipeline_graph()
                    ])
                ], className="mb-4"),
                
                dbc.Card([
                    dbc.CardHeader("데이터 선택"),
                    dbc.CardBody([
                        dcc.Dropdown(
                            id='data-selector',
                            options=[
                                {'label': '화물차 사고 데이터', 'value': 'cargo'},
                                {'label': '차종별 교통사고', 'value': 'vehicle'},
                                {'label': '사망사고 및 휴게소', 'value': 'fatal'}
                            ],
                            value='cargo',
                            className="mb-3"
                        ),
                        html.Hr(),
                        html.H5("기간 선택", className="mb-3"),
                        dcc.DatePickerRange(
                            id='date-range',
                            className="mb-3"
                        )
                    ])
                ])
            ], width=3),

            # Main Content Area
            dbc.Col([
                # Summary Cards
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("총 사고 건수", className="card-title"),
                                html.H3(id="total-accidents", className="card-text")
                            ])
                        ])
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("평균 사고 건수", className="card-title"),
                                html.H3(id="avg-accidents", className="card-text")
                            ])
                        ])
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("최대 사고 건수", className="card-title"),
                                html.H3(id="max-accidents", className="card-text")
                            ])
                        ])
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("최소 사고 건수", className="card-title"),
                                html.H3(id="min-accidents", className="card-text")
                            ])
                        ])
                    ], width=3)
                ], className="mb-4"),
                
                # Charts
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("사고 건수 추이"),
                            dbc.CardBody([
                                dcc.Graph(id='accident-trend')
                            ])
                        ], className="mb-4")
                    ], width=12)
                ]),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("지역별 사고 건수"),
                            dbc.CardBody([
                                dcc.Graph(id='regional-accidents')
                            ])
                        ], className="mb-4")
                    ], width=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("사고 유형 분포"),
                            dbc.CardBody([
                                dcc.Graph(id='accident-types')
                            ])
                        ], className="mb-4")
                    ], width=6)
                ])
            ], width=9)
        ])
    ], fluid=True, className="px-4 py-3") 