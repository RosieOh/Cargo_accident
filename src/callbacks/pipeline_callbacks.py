from dash import Input, Output
import networkx as nx
import plotly.graph_objects as go

def register_pipeline_callbacks(app):
    @app.callback(
        Output('pipeline-graph', 'figure'),
        Input('data-selector', 'value')
    )
    def update_pipeline(data_type):
        # Create a directed graph
        G = nx.DiGraph()
        
        # Add nodes based on data type
        if data_type == 'cargo':
            nodes = [
                ('raw_data', '원본 데이터'),
                ('preprocessing', '전처리'),
                ('analysis', '분석'),
                ('visualization', '시각화')
            ]
        elif data_type == 'vehicle':
            nodes = [
                ('raw_data', '차종별 데이터'),
                ('classification', '분류'),
                ('statistics', '통계'),
                ('visualization', '시각화')
            ]
        else:
            nodes = [
                ('raw_data', '사망사고 데이터'),
                ('location', '위치 분석'),
                ('pattern', '패턴 분석'),
                ('visualization', '시각화')
            ]
        
        # Add nodes to graph
        for node_id, node_label in nodes:
            G.add_node(node_id, label=node_label)
        
        # Add edges
        for i in range(len(nodes)-1):
            G.add_edge(nodes[i][0], nodes[i+1][0])
        
        # Create layout
        pos = nx.spring_layout(G)
        
        # Create edge trace
        edge_trace = go.Scatter(
            x=[], y=[],
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines+markers+text',
            marker=dict(size=10, symbol='arrow'),
            text=[],
            textposition='middle center'
        )
        
        # Add edges to trace
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += (x0, x1, None)
            edge_trace['y'] += (y0, y1, None)
        
        # Create node trace
        node_trace = go.Scatter(
            x=[], y=[],
            mode='markers+text',
            hoverinfo='text',
            text=[],
            textposition='top center',
            marker=dict(
                size=50,
                color='lightblue',
                line=dict(width=2)
            )
        )
        
        # Add nodes to trace
        for node in G.nodes():
            x, y = pos[node]
            node_trace['x'] += (x,)
            node_trace['y'] += (y,)
            node_trace['text'] += (G.nodes[node]['label'],)
        
        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                       ))
        
        return fig 