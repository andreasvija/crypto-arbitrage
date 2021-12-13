import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

class MLBTC(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2017, 1, 1)  # Set Start Date
        self.SetEndDate(2019, 1, 1)  # Set End Date
        self.SetCash(100000)  # Set Strategy Cash
        
        self.btc = self.AddEquity("BTC", Resolution.Hour).Symbol
        
        self.SetBenchmark("BTC")
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)
        
        self.entryPrice = 0
        self.period = timedelta(hours = 1)
        self.nextEntryTime = self.Time
        
        self.sma = self.SMA("BTC", 50, Resolution.Hour);
        
        self.rsi = self.RSI("BTC", 7)
        self.SetWarmUp(timedelta(20))
        
        #history = self.History(self.Symbol("BTC"), timedelta(hours = 26297), Resolution.Hour)
        
        #history = history[17531:]
        
        #history = pd.DataFrame(history)
        #hdata = history[["close"]].copy()
        
        #hdata["target"] = hdata.close.shift(-1)
        #hdata.dropna(inplace=True)
        
        #train = hdata.values[:int(len(hdata)*0.8)]
        #test = hdata.values[int(len(hdata)*0.8):]
        
        #X = train[:,:-1]
        #y = train[:, -1]

        #rf = RandomForestRegressor(n_estimators=50, max_samples=0.8, max_features=0.8, n_jobs=-1)

        #rf.fit(X, y)
        
        #self.rf = rf


    def OnData(self, data):
        
        try:
            close = data[self.btc].Close
            openn = data[self.btc].Open
            
        except:
            return
        
        if not self.rsi.IsReady: 
            return
            
        if self.rsi.Current.Value < 20 and self.Portfolio["BTC"].Invested <= 0:
            self.SetHoldings("BTC", 0.2)
        
        if self.rsi.Current.Value > 80:
            self.Liquidate()