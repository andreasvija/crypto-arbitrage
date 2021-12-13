from xgboost import XGBRegressor
import pandas as pd
import numpy as np

class MLBTC(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)  # Set Start Date
        self.SetEndDate(2021, 1, 1)  # Set End Date
        self.SetCash(100000)  # Set Strategy Cash
        
        self.btc = self.AddEquity("BTC", Resolution.Daily).Symbol
        
        self.SetBenchmark("BTC")
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)
        
        closing_prices = self.History(self.btc,30, Resolution.Daily)["close"]
        
        self.entryPrice = 0
        self.period = timedelta(31)
        self.nextEntryTime = self.Time


    def OnData(self, data):
        
        history = self.History(self.Symbol("BTC"), timedelta(365), Resolution.Daily)
        history = pd.DataFrame(history)
        hdata = history[["close"]].copy()
        
        hdata["target"] = hdata.close.shift(-5)
        hdata.dropna(inplace=True)
        
        train = hdata.values[:int(len(hdata)*0.8)]
        test = hdata.values[int(len(hdata)*0.8):]
        
        X = train[:,:-1]
        y = train[:, -1]

        xgb = XGBRegressor(objective="reg:squarederror", n_estimators=50)

        xgb.fit(X, y)
        
        val = np.array(data[self.btc].Close).reshape(1,-1)
        
        price = xgb.predict(val)[0]
        price = xgb.predict(price)[0]
        price = xgb.predict(price)[0]
        price = xgb.predict(price)[0]
        price = xgb.predict(price)[0]
        
        if not self.btc in data:
            return
        
        #price = data.Bars[self.btc].Close
        
        #price = data[self.btc].Close
        #price = self.Securities[self.btc].Close
        
        if not self.Portfolio.Invested:
            if self.nextEntryTime <= self.Time:
                self.SetHoldings(self.btc,1)
                self.Log("BUY BTC @" + str(price))
                self.entryPrice = price
                
        elif self.entryPrice * 0.9 > price:
            self.Liquidate()
            self.Log("SELL BTC @" + str(price))
            self.nextEntryTime = self.Time + self.period