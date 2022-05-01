import yfinance as yf

def get_data(ticker, period="1y", start=None, end=None):
    tick = yf.Ticker(ticker)

    if start == None or end == None:
        if start == None and end != None:
            hist = tick.history(period,end)
        if start != None and end == None:
            hist = tick.history(period,start)
        if start == None and end == None:
            hist = tick.history(period)
    else:
        hist = tick.history(period,start,end)

    hist = hist.iloc[: , :5]

    return hist