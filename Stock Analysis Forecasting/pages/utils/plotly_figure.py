import dateutil.relativedelta
import plotly.graph_objects as go
import pandas_ta as pta
import datetime
import numpy as np

npNaN = np.nan

def plotly_table(dataframe):
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=[col for col in dataframe.columns],
            fill_color='#4C9ED9',
            font=dict(color='white', size=12),
            align='center',
            height=40
        ),
        cells=dict(
            values=[dataframe[col] for col in dataframe.columns],
            fill_color=[['#F0F4F8' if i % 2 == 0 else '#E0E8F3' for i in range(len(dataframe))]],
            font=dict(color='black', size=11),
            align='center',
            height=30
        )
    )])

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='white',
        height=350,
        autosize=True,
        plot_bgcolor='white',
        title_text="Stock Information",
        title_x=0.5,
        title_font=dict(size=18, color='black')
    )

    return fig

def filter_data(dataframe, num_period):
    if num_period == '1mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1)
    elif num_period == '5d':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-5)
    elif num_period == '6mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6)
    elif num_period == '1y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)
    elif num_period == '5y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)
    elif num_period == 'ytd':
        date = datetime.datetime(dataframe.index[-1].year, 1, 1)
    else:
        date = dataframe.index[0]

    return dataframe.reset_index()[dataframe.reset_index()['Date'] > date]

def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                             mode='lines',
                             name='Open', line=dict(width=2, color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                             mode='lines',
                             name='Close', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                             mode='lines',
                             name='High', line=dict(width=2, color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                             mode='lines',
                             name='Low', line=dict(width=2, color='red')))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500, margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor='white', paper_bgcolor='#e1efff',
                      legend=dict(yanchor='top', xanchor='right'))
    return fig

def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=dataframe['Date'],
                                 open=dataframe['Open'], high=dataframe['High'],
                                 low=dataframe['Low'], close=dataframe['Close']))
    fig.update_layout(showlegend=False, height=500, margin=dict(l=0, r=20, t=20, b=0),
                      plot_bgcolor='white', paper_bgcolor='#e1efff')
    return fig

def RSI(dataframe, num_period):
    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe.RSI, name='RSI', marker_color='orange', line=dict(width=2, color='red', dash='dash'),
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[70] * len(dataframe), name='Overbought', marker_color='red', line=dict(width=2, color='red', dash='dash'),
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[30] * len(dataframe), fill='tonexty', name='Oversold', marker_color='#79da84', line=dict(width=2, color='#79da84', dash='dash'),
    ))

    fig.update_layout(yaxis_range=[0, 100],
                      height=200, plot_bgcolor='#e1efff', margin=dict(l=0, r=0, t=0, b=0),
                      legend=dict(orientation='h',
                                  yanchor='top',
                                  y=1.02,
                                  xanchor='right',
                                  x=1
                                  ))
    return fig

def Moving_average(dataframe, num_period):
    dataframe['SMA_50'] = pta.sma(dataframe['Close'], 50)
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                             mode='lines',
                             name='Open', line=dict(width=2, color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                             mode='lines',
                             name='Close', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                             mode='lines',
                             name='High', line=dict(width=2, color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                             mode='lines',
                             name='Low', line=dict(width=2, color='red')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'],
                             mode='lines',
                             name='SMA 50', line=dict(width=2, color='purple')))

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500, margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor='white', paper_bgcolor='#e1efff',
                      legend=dict(yanchor='top', xanchor='right'))
    return fig

def MACD(dataframe, num_period):
    macd_data = pta.macd(dataframe['Close'])
    macd = macd_data.iloc[:, 0]
    macd_signal = macd_data.iloc[:, 1]
    macd_hist = macd_data.iloc[:, 2]
    dataframe['MACD'] = macd
    dataframe['MACD Signal'] = macd_signal
    dataframe['MACD Hist'] = macd_hist
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD'], name='MACD', marker_color='orange', line=dict(width=2, color='orange'),
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD Signal'], name='MACD Signal', marker_color='red', line=dict(width=2, color='red', dash='dash'),
    ))

    fig.add_trace(go.Bar(
        x=dataframe['Date'],
        y=dataframe['MACD Hist'],
        marker_color=['red' if val < 0 else 'green' for val in dataframe['MACD Hist']],
        name='MACD Hist'
    ))

    fig.update_layout(
        height=200, plot_bgcolor='white', paper_bgcolor='#e1efff', margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation='h',
                    yanchor='top',
                    y=1.02,
                    xanchor='right',
                    x=1
                    ))
    return fig

def Moving_average_forecast(forecast_df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=forecast_df.index,
        y=forecast_df['Close'],
        mode='lines+markers',
        name='Forecast Close',
        line=dict(color='dodgerblue', width=3),
        marker=dict(size=5)
    ))

    fig.update_layout(
        title=dict(text='📈 Stock Price Forecast (With Rolling Mean)', x=0.5, font=dict(size=22, color='black')),
        xaxis_title='Date',
        yaxis_title='Close Price (USD)',
        template='plotly_white',
        height=500,
        plot_bgcolor='rgba(240,240,240,0.95)',
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgrey'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgrey'),
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0)', borderwidth=1)
    )

    return fig