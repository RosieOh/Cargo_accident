import dash
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc
from components.layouts.main_layout import create_main_layout
from components.layouts.analysis_layout import create_analysis_layout
from components.layouts.report_layout import create_report_layout
from callbacks import pipeline_callbacks, visualization_callbacks, metrics_callbacks
from callbacks import analysis_callbacks, report_callbacks

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap'
    ],
    suppress_callback_exceptions=True
)

# Set custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>화물차 사고 데이터 분석 대시보드</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Noto Sans KR', sans-serif;
                background-color: #f8f9fa;
            }
            .navbar {
                box-shadow: 0 2px 4px rgba(0,0,0,.1);
            }
            .card {
                box-shadow: 0 2px 4px rgba(0,0,0,.05);
                border: none;
                border-radius: 10px;
            }
            .card-header {
                background-color: #fff;
                border-bottom: 1px solid rgba(0,0,0,.05);
                border-radius: 10px 10px 0 0 !important;
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

# Create the layout with routing
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Add routing callback
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/':
        return create_main_layout()
    elif pathname == '/analysis':
        return create_analysis_layout()
    elif pathname == '/report':
        return create_report_layout()
    else:
        return create_main_layout()  # Default to main layout

if __name__ == '__main__':
    app.run_server(debug=True, port=8051) 