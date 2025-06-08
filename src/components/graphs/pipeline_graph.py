import plotly.graph_objects as go
from dash import dcc

def create_pipeline_graph():
    # Create a sample pipeline graph
    fig = go.Figure()
    
    # Add nodes
    fig.add_trace(go.Scatter(
        x=[0, 1, 2, 3],
        y=[0, 0, 0, 0],
        mode='markers+text',
        marker=dict(size=50, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']),
        text=['데이터 수집', '전처리', '분석', '시각화'],
        textposition='top center',
        hoverinfo='text'
    ))
    
    # Add edges
    fig.add_trace(go.Scatter(
        x=[0.2, 0.8],
        y=[0, 0],
        mode='lines',
        line=dict(color='gray', width=2),
        hoverinfo='none'
    ))
    
    fig.add_trace(go.Scatter(
        x=[1.2, 1.8],
        y=[0, 0],
        mode='lines',
        line=dict(color='gray', width=2),
        hoverinfo='none'
    ))
    
    fig.add_trace(go.Scatter(
        x=[2.2, 2.8],
        y=[0, 0],
        mode='lines',
        line=dict(color='gray', width=2),
        hoverinfo='none'
    ))
    
    # Update layout
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            range=[-0.5, 3.5]
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            range=[-0.5, 0.5]
        ),
        height=200
    )
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False}) 