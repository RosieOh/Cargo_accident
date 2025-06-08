import dash_bootstrap_components as dbc
from dash import html, dcc

def create_report_layout():
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
                    dbc.CardHeader("보고서 설정"),
                    dbc.CardBody([
                        html.H5("보고서 유형", className="mb-3"),
                        dcc.Dropdown(
                            id='report-type-selector',
                            options=[
                                {'label': '일간 보고서', 'value': 'daily'},
                                {'label': '주간 보고서', 'value': 'weekly'},
                                {'label': '월간 보고서', 'value': 'monthly'},
                                {'label': '분기 보고서', 'value': 'quarterly'},
                                {'label': '연간 보고서', 'value': 'yearly'}
                            ],
                            value='daily',
                            className="mb-3"
                        ),
                        html.Hr(),
                        html.H5("보고서 기간", className="mb-3"),
                        dcc.DatePickerRange(
                            id='report-date-range',
                            className="mb-3"
                        ),
                        html.Hr(),
                        html.H5("보고서 항목", className="mb-3"),
                        dcc.Checklist(
                            id='report-sections',
                            options=[
                                {'label': '요약 통계', 'value': 'summary'},
                                {'label': '주요 지표', 'value': 'metrics'},
                                {'label': '추세 분석', 'value': 'trends'},
                                {'label': '지역별 분석', 'value': 'regional'},
                                {'label': '사고 유형 분석', 'value': 'accident_types'},
                                {'label': '권장 사항', 'value': 'recommendations'}
                            ],
                            value=['summary', 'metrics'],
                            className="mb-3"
                        ),
                        html.Hr(),
                        dbc.Button("보고서 생성", id="generate-report", color="primary", className="w-100")
                    ])
                ], className="mb-4")
            ], width=3),

            # Main Content Area
            dbc.Col([
                # Report Content
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("사고 데이터 분석 보고서", className="mb-0"),
                        html.Small(id="report-date-range-display", className="text-muted")
                    ]),
                    dbc.CardBody([
                        # Summary Section
                        html.Div(id="summary-section", className="mb-4"),
                        
                        # Metrics Section
                        html.Div(id="metrics-section", className="mb-4"),
                        
                        # Trends Section
                        html.Div(id="trends-section", className="mb-4"),
                        
                        # Regional Analysis Section
                        html.Div(id="regional-section", className="mb-4"),
                        
                        # Accident Types Section
                        html.Div(id="accident-types-section", className="mb-4"),
                        
                        # Recommendations Section
                        html.Div(id="recommendations-section", className="mb-4"),
                        
                        # Download Button
                        dbc.Button(
                            "보고서 다운로드",
                            id="download-report",
                            color="success",
                            className="mt-3"
                        )
                    ])
                ])
            ], width=9)
        ])
    ], fluid=True, className="px-4 py-3") 