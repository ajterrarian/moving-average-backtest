import pytest
import pandas as pd
from project import generate_signals, simulate_trading, compute_performance

fast_window = 2
slow_window = 3

def test_generate_signals():
    data = pd.DataFrame({'Close': [20, 20, 20, 21, 22, 23, 22, 21, 20, 19]})
    result = generate_signals(data, fast_window, slow_window)

    #check the results
    assert result['Signal'].tolist() == [0, 0, 0, 1, 1, 1, 1, 0, 0, 0]
    assert result['Fast_MA'].iloc[3] == 20.5
    assert result['Slow_MA'].iloc[4] == 21.0

def test_simulate_trading():
    data = pd.DataFrame({'Close': [20, 20, 20, 21, 22, 23, 22, 21, 20, 19]})
    data = generate_signals(data, fast_window=2, slow_window=3)
    result = simulate_trading(data, initial_capital=1000)

    #check the results
    assert result['Position'].tolist()[1:] == [0, 0, 0, 1, 1, 1, 1, 0, 0]
    assert result['Daily_Return'].tolist()[1:] == pytest.approx([0, 0, 0.05, 1/21, 1/22, -1/23, -1/22, -1/21, -0.05])
    assert result['Strategy_Return'].tolist()[1:] == pytest.approx([0, 0, 0, 1/21, 1/22, -1/23, -1/22, 0, 0])
    assert result['Equity_Curve'].tolist()[1:] == pytest.approx([1000, 1000, 1000, 1000*22/21, 1000*23/21, 1000*22/21, 1000, 1000, 1000])
    assert result['Buy_Hold'].tolist()[1:] == pytest.approx([1000, 1000, 1050, 1100, 1150, 1100, 1050, 1000, 950])


def test_compute_performance():
    ...