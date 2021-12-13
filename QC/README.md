In addition to our ML algorithm analysis we tried implementing some NON-ML solutions into QC.
Here are some of the results it provided. The test period was the year 2020, since it had large ups and downs (best for seeing drawdown).

BASELINE - buying in beginning and selling at end:

Sharpe ratio - 3.742

Drawdown - 59.6%


RSI based buy-sell:

Sharpe ratio - 1.601

Drawdown - 1.9%


EMA based buy-sell:

Sharpe ratio - 0.941

Drawdown 3.1%


DCA+RSI+SMA ensemble based buy-sell:

Sharpe ratio - -0.719

Drawdown - 7.5%


Random XGBoost ML prediction (take this with a grain of salt as it is pretty much a random prediction):

Sharpe ratio - 1.386

Drawdown - 23.6%

