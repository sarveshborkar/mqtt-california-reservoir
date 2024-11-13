import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
from cache import get_cached_data

app = Dash(__name__, assets_folder='assets')
app.title = "California Water Reservoir Dashboard"

def get_latest_date(data):
    if not data:
        return None
    df = pd.DataFrame(data)
    return df['Date'].max() if not df.empty else None

app.layout = html.Div(
    children=[
        html.H1("California Reservoir Water Levels"),
        html.P("Select a date to view the water levels of major reservoirs in California."),
        
        html.Div(
            className='dropdown-container',
            children=[
                dcc.Dropdown(
                    id='date-dropdown',
                    placeholder="Select a date",
                    clearable=True
                )
            ]
        ),
        
        html.Div(id='chart-container'),
        dcc.Interval(id='interval', interval=5000, n_intervals=0)
    ]
)

@app.callback(
    Output('date-dropdown', 'options'),
    Output('date-dropdown', 'value'),
    Input('interval', 'n_intervals')
)
def update_date_dropdown(_):
    data = get_cached_data()
    if not data:
        return [], None

    df = pd.DataFrame(data)
    unique_dates = sorted(df['Date'].unique())
    latest_date = unique_dates[-1] if unique_dates else None

    return [{'label': date, 'value': date} for date in unique_dates], latest_date

@app.callback(
    Output('chart-container', 'children'),
    Input('date-dropdown', 'value')
)
def update_chart(selected_date):
    data = get_cached_data()
    if not data or not selected_date:
        return html.Div("No data available", style={'textAlign': 'center', 'color': '#888'})

    df = pd.DataFrame(data)
    filtered_df = df[df['Date'] == selected_date]

    if filtered_df.empty:
        return html.Div("No data available", style={'textAlign': 'center', 'color': '#888'})

    fig = go.Figure()

    reservoirs = ["Oroville", "Shasta", "Sonoma"]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    for i, reservoir in enumerate(reservoirs):
        reservoir_data = filtered_df[filtered_df['Reservoir'] == reservoir]
        if not reservoir_data.empty:
            fig.add_trace(go.Bar(
                x=reservoir_data['Reservoir'],
                y=reservoir_data['TAF'],
                name=reservoir,
                marker_color=colors[i],
                text=reservoir_data['TAF'],
                textposition='auto'
            ))

    fig.update_layout(
        title=f"Water Levels of California Reservoirs on {selected_date}",
        barmode='group',
        xaxis_title='Reservoir',
        yaxis_title='Water Level (TAF)',
        legend_title='Reservoir',
        template='plotly_white',
        height=500
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False})

if __name__ == '__main__':
    app.run_server(debug=True)
