import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

class MLBTC(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)  # Set Start Date
        self.SetEndDate(2021, 1, 1)  # Set End Date
        self.SetCash(100000)  # Set Strategy Cash
        
        self.btc = self.AddEquity("BTC", Resolution.Hour).Symbol
        
        self.SetBenchmark("BTC")
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)
        history = self.History(self.Symbol("BTC"), timedelta(minutes = 207077), Resolution.Hour)
        
        history = history[:105189]
        
        self.entryPrice = 0
        self.period = timedelta(hours = 1)
        self.nextEntryTime = self.Time
        
        history = pd.DataFrame(history)
        hdata = history[["close"]].copy()
        
        hdata["target"] = hdata.close.shift(-1)
        hdata.dropna(inplace=True)
        
        train = hdata.values[:int(len(hdata)*0.8)]
        test = hdata.values[int(len(hdata)*0.8):]
        
        X = train[:,:-1]
        y = train[:, -1]

        rf = RandomForestRegressor(n_estimators=50, max_samples=0.8, max_features=0.8, n_jobs=-1)

        rf.fit(X, y)
        
        self.rf = rf


    def OnData(self, data):
        
        try:
            val = np.array(data[self.btc].Close).reshape(1,-1)
        
            price = self.rf.predict(val)[0]
            
        except:
            price = self.entryPrice
        
        if self.nextEntryTime <= self.Time:
            try:
                self.SetHoldings(self.btc,0.1)
                self.Log("BUY BTC @" + str(price))
                self.entryPrice = price
            except:
                self.Log("no money to buy @" + str(price))
                
        elif self.entryPrice * 0.99783 > price:
            self.Liquidate()
            self.Log("SELL BTC @" + str(price))
            self.nextEntryTime = self.Time + self.period