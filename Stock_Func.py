import numpy as np
import pandas as pd


def RSV_compute(inlist):
    minin9d = 0
    maxin9d = 0
    closingprice = inlist[-1]
    inlist.sort()
    minin9d = inlist[0]
    maxin9d = inlist[-1]
    RSV = (closingprice - minin9d)/(maxin9d - minin9d)
    return RSV*100

def K_compute(RSV, Kpre):
    Ktoday = RSV * 1 / 3 + Kpre * 2 / 3
    return Ktoday

def D_compute(Ktoday, Dpre):
    Dtoday = Ktoday * 1 / 3 + Dpre * 2 / 3 
    return Dtoday

def NewFeature(Dataframe):
    DataNum = Dataframe.shape[0]
    ClosingPrice = Dataframe["Close Price"].tolist()
    Kvalue = []
    Dvalue = []
    RSValue = []
    Rise = []
    for i in range(DataNum):
    
        if i != DataNum - 1:
            if Dataframe.iloc[i+1,1] > Dataframe.iloc[i,1]:
                Rise.append(1)
            else:
                Rise.append(0)
        else:
            Rise.append(0)
        
        if i < 8:
            Kvalue.append(0)
            Dvalue.append(0)
            RSValue.append(0)
        elif i == 8:
            Kvalue.append(50)
            Dvalue.append(50)
            RSValue.append(0)
        else:
            RSV = RSV_compute(ClosingPrice[i-8:i+1])
            RSValue.append(RSV)
            Kvalue.append(K_compute(RSV,Kvalue[i-1]))
            Dvalue.append(D_compute(Kvalue[i],Dvalue[i-1]))
    Dataframe['RSV'] = RSValue
    Dataframe['Kvalue'] = Kvalue
    Dataframe['Dvalue'] = Dvalue
    Dataframe['RisePredict'] = Rise
    return Dataframe

def KD_strength(Dataframe):
    DataNum = Dataframe.shape[0]
    KD_strength = []
    for i in range(DataNum):
        if Dataframe.iloc[i,6] < 20 and Dataframe.iloc[i,7] < 20:
            KD_strength.append(-1)
        elif Dataframe.iloc[i,6] > 80 and Dataframe.iloc[i,7] > 80:
            KD_strength.append(1)
        else:
            KD_strength.append(0)
    Dataframe['KD_strength'] = KD_strength
    return Dataframe

def KD_variation(Dataframe):
    DataNum = Dataframe.shape[0]
    KD_variation = []
    for i in range(DataNum):
        if i == 0:
            KD_variation.append(0)
        else:
            if Dataframe.iloc[i,6] < Dataframe.iloc[i,7]:
                if Dataframe.iloc[i-1,6] > Dataframe.iloc[i-1,7]:
                    KD_variation.append(-2)
                else:
                    KD_variation.append(-1)
            elif Dataframe.iloc[i,6] > Dataframe.iloc[i,7]:
                if Dataframe.iloc[i-1,6] < Dataframe.iloc[i-1,7]:
                    KD_variation.append(2)
                else:
                    KD_variation.append(1)
            else:
                if Dataframe.iloc[i-1,6] > Dataframe.iloc[i-1,7]:
                    KD_variation.append(-1)
                elif Dataframe.iloc[i,6] < Dataframe.iloc[i,7]:
                    KD_variation.append(1)
                else:
                    KD_variation.append(0)
                    

    Dataframe['KD_variation'] = KD_variation
    return Dataframe
        
def Up_Down(Dataframe):
    DataNum = Dataframe.shape[0]
    Up_Down = []
    for i in range(DataNum):
        if i == 0 :
            Up_Down.append(0)
        else:
            updowntoday = Dataframe.iloc[i,1] - Dataframe.iloc[i-1,1]
            Up_Down.append(updowntoday)
    Dataframe['Up_Down'] = Up_Down
    return Dataframe
        
def ComputeRSI(inlist):
    ups = 0
    downs = 0
    for i in range(len(inlist)):
        if inlist[i] > 0:
            ups = ups + inlist[i]
        else:
            downs = downs + inlist[i]

    result = ups * 100 / (ups - downs)
    return result
        
        
        
def AddRSI6(Dataframe):
    DataNum = Dataframe.shape[0]
    Up_Down = Dataframe["Up_Down"].tolist()
    RSI6 = []
    for i in range(DataNum):
        if i < 6:
            RSI6.append(0)
        else:
            RSI = ComputeRSI(Up_Down[i-5:i+1])
            RSI6.append(RSI)
    Dataframe['RSI6'] = RSI6
    return Dataframe

def AddRSI12(Dataframe):
    DataNum = Dataframe.shape[0]
    Up_Down = Dataframe["Up_Down"].tolist()
    RSI12 = []
    for i in range(DataNum):
        if i < 12:
            RSI12.append(0)
        else:
            RSI = ComputeRSI(Up_Down[i-11:i+1])
            RSI12.append(RSI)
    Dataframe['RSI12'] = RSI12
    return Dataframe

def RSI_variation(Dataframe):
    DataNum = Dataframe.shape[0]
    RSI_variation = []
    for i in range(DataNum):
        if i == 0:
            RSI_variation.append(0)
        else:
            if Dataframe.iloc[i,10] < Dataframe.iloc[i,11]:
                if Dataframe.iloc[i-1,10] > Dataframe.iloc[i-1,11]:
                    RSI_variation.append(-2)
                else:
                    RSI_variation.append(-1)
            elif Dataframe.iloc[i,10] > Dataframe.iloc[i,11]:
                if Dataframe.iloc[i-1,10] < Dataframe.iloc[i-1,11]:
                    RSI_variation.append(2)
                else:
                    RSI_variation.append(1)
            else:
                if Dataframe.iloc[i-1,10] > Dataframe.iloc[i-1,11]:
                    RSI_variation.append(-1)
                elif Dataframe.iloc[i,10] < Dataframe.iloc[i,11]:
                    RSI_variation.append(1)
                else:
                    RSI_variation.append(0)
                    

    Dataframe['RSI_variation'] = RSI_variation
    return Dataframe