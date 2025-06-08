from dash import Input, Output
import dash_bootstrap_components as dbc
from utils.data_loader import load_data

def register_metrics_callbacks(app):
    @app.callback(
        Output('key-metrics', 'children'),
        Input('data-selector', 'value')
    )
    def update_metrics(data_type):
        # Load data
        df = load_data(data_type)
        
        # Calculate metrics based on data type
        if data_type == 'cargo':
            metrics = calculate_cargo_metrics(df)
        elif data_type == 'vehicle':
            metrics = calculate_vehicle_metrics(df)
        else:  # fatal
            metrics = calculate_fatal_metrics(df)
        
        # Create metric cards
        return dbc.Row([
            dbc.Col(create_metric_card(title, value, change), width=3)
            for title, value, change in metrics
        ])

def create_metric_card(title, value, change):
    return dbc.Card([
        dbc.CardBody([
            html.H6(title, className="card-subtitle mb-2 text-muted"),
            html.H3(value, className="card-title mb-0"),
            html.Small(
                f"{change:+.1f}%",
                className=f"text-{'success' if change > 0 else 'danger'}"
            )
        ])
    ], className="mb-3")

def calculate_cargo_metrics(df):
    total_accidents = df['accidents'].sum()
    avg_accidents = df['accidents'].mean()
    max_accidents = df['accidents'].max()
    min_accidents = df['accidents'].min()
    
    return [
        ("총 사고 건수", f"{total_accidents:,}", 0),
        ("평균 사고 건수", f"{avg_accidents:.1f}", 0),
        ("최대 사고 건수", f"{max_accidents:,}", 0),
        ("최소 사고 건수", f"{min_accidents:,}", 0)
    ]

def calculate_vehicle_metrics(df):
    # Similar to cargo metrics but for vehicle data
    pass

def calculate_fatal_metrics(df):
    # Similar to cargo metrics but for fatal data
    pass 