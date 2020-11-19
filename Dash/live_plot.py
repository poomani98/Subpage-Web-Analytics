import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
from random import random
import pandas as pd
import numpy as np

click = 0
hover = 0
scroll = 0

app = dash.Dash(__name__) 

app.layout = html.Div([

    html.Div([
            dcc.Graph(id = 'live-graph'), 
            dcc.Interval( 
                id = 'graph-update', 
                interval = 3000, 
            )
        ] ),
    html.Div([
            dcc.Graph(id = 'live-graph2'), 
            dcc.Interval( 
                id = 'graph-update2', 
                interval = 3000, 
                n_intervals = 0
            ) 
        ], style={"float": "left"} ),
    html.Div([
            dcc.Graph(id = 'live-graph3'), 
            dcc.Interval( 
                id = 'graph-update3', 
                interval = 3000, 
                n_intervals = 0
            )
        ], style={"float": "left"})

    ])



@app.callback( 
    Output('live-graph', 'figure'), 
    [ Input('graph-update', 'n_intervals') ] 
) 
  
def update_graph_scatter(n): 
    X = np.array(pd.read_csv("../Server/heatmap.csv",header=None))[-1::-1,]
    global hover
    hover = np.sum(X)
    data = plotly.graph_objs.Heatmap( 
            z = X,
            colorscale="Jet",
            name='User Attention Heatmap' )

  
    return {'data': [data], 
            'layout' : go.Layout(width=1500,height=720,title="User Attention Heatmap"),
            }

@app.callback( 
    Output('live-graph2', 'figure'), 
    [ Input('graph-update2', 'n_intervals') ] 
) 
def update_graph_scatter2(n):

    data2 = pd.read_csv("../Server/events.csv")
    t = {'table':data2['table'][0],'image':data2['image'][0],'ads':data2['ad'][0],'text':data2['text'][0]}
    global click
    click = sum(list(t.values()))
    data2 = plotly.graph_objs.Bar( 
            x=list(t.values()), 
            y=list(t.keys()), orientation='h'
    )
  
    return {
            'data' : [data2],
            'layout' : go.Layout(width=700,height=500, title="Click frequency")
            }
  

@app.callback( 
    Output('live-graph3', 'figure'), 
    [ Input('graph-update3', 'n_intervals') ] 
) 
def update_graph_scatter3(n):
    
    t = {'hover':hover,'click':click,'scroll':scroll}
    data2 = plotly.graph_objs.Pie( 
            labels=list(t.keys()), 
            values=list(t.values()), 
    )
  
    return {
            'data' : [data2],
            'layout' : go.Layout(width=700,height=500,title="Event Proportion")
            }


if __name__ == '__main__': 
    app.run_server()
