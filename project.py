import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def main():
    #inputs for ticker, start date and end date, and initial capital for analysis
    ticker = input("Enter your stock ticker (for example, AAPL for Apple): ")
    start_date = input("Enter the analysis start date (YYYY-MM-DD): ")
    end_date = input("Enter the analysis end date(YYYY-MM-DD): ")
    initial_capital = float(input("Enter your starting capital amount: "))
    
    #load in the desired stock and clean the data to only have closing prices and remove empty rows
    data = load_and_clean_data(ticker, start_date, end_date)
    
    #define fast and slow moving window ranges
    fast_window = 20
    slow_window = 50
    
    #return the last 10 rows of the data to see generated signals and moving averages
    data = generate_signals(data, fast_window, slow_window)
    
    #deal with look-ahead bias b/c you cant trade on the same day as a signal change; shift the signal column down by 1
    data = simulate_trading(data, initial_capital)

    total_return, sharpe_ratio, drawdown = compute_performance(data, initial_capital)
    print(data.tail(20))
    print(f"Total Return: {total_return:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Max Drawdown: {drawdown:.2%}")

def load_and_clean_data(ticker, start_date, end_date):
    #download the data from the yfinance library
    data = yf.download(ticker, start=start_date, end=end_date)
    
    #keep only the closing price column and delete any rows with empty values
    data = data[['Close']]
    data.columns = ['Close']
    data = data.dropna()
    return data

def generate_signals(data, fast_window, slow_window):
    #calculate the fast and slow moving averages, given the fast/slow window sizes
    data['Fast_MA'] = data['Close'].rolling(window=fast_window).mean()
    data['Slow_MA'] = data['Close'].rolling(window=slow_window).mean()

    #generate the buy/sell signals based on the calculated moving averages
    data['Signal'] = (data['Fast_MA'] > data['Slow_MA']).astype(int)
    return data

def simulate_trading(data, initial_capital):
    #shift the signal column down by 1 to avoid look ahead bias
    data['Position'] = data['Signal'].shift(1)

    #daily percent change in the stock price
    data['Daily_Return'] = data['Close'].pct_change()

    #strategy return based on position and daily return
    data['Strategy_Return'] = data['Position'] * data['Daily_Return']

    #create an equity curve based on the strategy return and initial capital
    data['Equity_Curve'] = initial_capital * (1 + data['Strategy_Return']).cumprod()

    return data

def compute_performance(data, initial_capital):
    ##SHARPE RATIO CALCULATION
    #return total returns over the whole backtest
    total_return = (data['Equity_Curve'].iloc[-1] / initial_capital) - 1
    
    #assuming a fixed 4% annual risk-free rate, converted to a daily rate
    annual_rfr = 0.04
    daily_rfr = (1 + annual_rfr) ** (1/252) - 1
    
    #calculate the sharpe ratio to account for risk in returns
    sharpe_ratio = ((data['Strategy_Return'].mean() - daily_rfr) * 252 ** 0.5) /data['Strategy_Return'].std()

    ##MAX DRAWDOWN CALCULATION
    #calculate the running maximum of the equity curve
    data['Running_Max'] = data['Equity_Curve'].cummax()

    #calculate the drawdown point
    data['Drawdown'] = (data['Running_Max'] - data['Equity_Curve']) / data['Running_Max']
    drawdown = data['Drawdown'].max()
    
    return total_return, sharpe_ratio, drawdown


if __name__ == "__main__":
    main()