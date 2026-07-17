# **Rolling Average Backtester**

A simulation of a moving-average crossover trading strategy, tested with historical market data and compared against a buy-and-hold benchmark.

## What it does

The program pulls historical daily closing prices for a chosen stock from Yahoo Finance, and then computes two rolling averages of that price: a fast one (a 20-day short window) and a slow one (a 50-day longer window). When the fast average is greater than the slow average, the strategy simulates holding the stock. Alternatively, when the fast average falls below the slow average, it simulates sitting out in cash.

From there, the program simulates what an account following this rule would be worth over time (via an "equity curve"), and compares that to a benchmark simulation (one in which you bought the stock on day one and held onto it the entire time). The program outputs total return, Sharpe ratio, max drawdown, and win rate for the strategy, and plots both curves side by side so the strategy can be judged against simply holding onto a stock.

## How it works
There are four main functions at work.

1. `load_and_clean_data(ticker, start_date, end_date)` -- downloads the daily closing prices of chosen stock via yfinance and drops any missing rows.

2. `generate_signals(data, fast_window, slow_window)` -- computes the fast and slow rolling averages and outputs a 1/0 signal for every day in which the average is on top.

3. `simulate_trading(data, initial_capital)` -- turns signals into simulated trades, tracks the day by day account value, and computes a benchmark buy/hold curve.

4. `compute_performance(data, initial_capital)` -- derives total return, Sharpe ratio, max drawdown, and win rate from the equity curve.

These functions then feed into `plot_results(data)` which outputs the strategy's equity curve against buy/hold on a single matplotlib graph.

## How to run it
`pip install -r requirements.txt`
`python project.py`
You will be prompted for a stock ticker (for example, AAPL for Apple), a start and end date (YYYY-MM-DD), and a starting cash amount.

## Design decisions and simplifications

**Look-ahead bias**
The trading signal is computed from the same day's closing price, but you wouldn't actually know the moving averages had crossed until the market closed that day. To avoid trading with info one wouldn't have yet, the signal is shifted forward by one day before being used to simulate trades.

**Trading costs**
This project assumes zero-commission trading (which is realistic for a US retail trader today). It does not take into account trading slippage.

**Risk-free rate**
The Sharpe ratio calculation is based upon a fixed 4% annual risk-free rate, converted to a daily compounding rate, rather than pulling from historical Treasury data. 

**Single ticker**
You can only test one stock or ETF at a time, rather than a basket of assets, to keep the focus on the core simulation, not just portfolio allocations.

## Limitations
This project is a backtest, meaning it cannot make predictions about the market. A future project that would be cool would be an expansion of this using AI/ML concepts to expand my moving average strategy and predict whether or not certain stock purchases would be profitable.

## Testing
`test_project.py` containts pytest tests for `generate_signals`, `simulate_trading`, and `compute_performance`. Tests are built with small, hand-constructed prices series (not live market data) and check function outputs against independently calculated values.

Run tests with:
`pytest test_project.py`