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
    assert result['Slow_MA'].iloc[4] == 20.0

def test_simulate_trading():
    assert simulate_trading(...) == ...

def test_compute_performance():
    ...