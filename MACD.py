import numpy as np
import matplotlib.pyplot as plt
import talib

seed = np.random.randint(1000000)
# seed =  39303  # 점진적인 상승

np.random.seed(seed)
n = 500
p_lst = []
p = 800
start_p = 800

for i in range(n):
    delta = 2 * np.random.randn(1)[0]
    if p < delta:
        delta = 0
    p += delta
    p_lst.append(p)
    
close = np.array(p_lst)
ma5 = talib.MA(close, timeperiod=5, matype=0)
ma5_slope = np.array([np.nan] + [ma5[i]-ma5[i-1] for i in range(1,n)])
ma20 = talib.MA(close, timeperiod=20, matype=0)
ma20_slope = np.array([np.nan] + [ma20[i]-ma20[i-1] for i in range(1,n)])
ma60 = talib.MA(close, timeperiod=60, matype=0)
ma60_slope = np.array([np.nan] + [ma60[i]-ma60[i-1] for i in range(1,n)])
ma120 = talib.MA(close, timeperiod=120, matype=0)
ma120_slope = np.array([np.nan] + [ma60[i]-ma60[i-1] for i in range(1,n)])

# Bolinger Band
upperband, middleband, lowerband = talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)

# MACD
macd, signal, hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

# diff0 = macd[i] - signal[i]

plt.figure(1).clf()
plt.xlim(0,n)
plt.plot(p_lst, 'o-', label='prices')
plt.plot(ma5, label='ma5')
plt.plot(ma20, label='ma20')
plt.plot(ma60, label='ma60')


print("MA5-MA60을 이용한 매수/매수")
i = 60
asset = 50000
stock = 0
threshold = 3

for i in range(61,n):
    diff = ma5[i] - ma60[i]
    pur_stk = 1
    if diff > 0 and asset > p_lst[i]:
        asset -= pur_stk * p_lst[i]
        stock += pur_stk
        # print(f'>> {pur_stk}:{p_lst[i]} || {asset}')
        # plt.plot(i,p_lst[i],'bx',ms=10,mew=4)
    elif diff < 0 and stock > 0:
        stock -= pur_stk
        asset += pur_stk * p_lst[i]
        # print(f'<< {pur_stk}:{p_lst[i]} || {asset}')
        # plt.plot(i,p_lst[i],'rx',ms=10,mew=4)
    if i == n-1:
        asset += stock * p_lst[i]
        stock = 0
        # print(f'<< {pur_stk}:{p_lst[i]} || {asset}')
        # plt.plot(i,p_lst[i],'rx',ms=10,mew=4)
print('total asset:', asset, '\n')



print("MA5-MA60을 이용한 매수/매수")
i = 60
asset = 50000
start_asset = 50000
stock = 0
threshold = 0
save = 0
for i in range(65,n):
    buy = (ma5[i-2] - ma60[i-2]) < 0
    sell = (ma5[i-2]-ma60[i-2]) > 0 and stock * p_lst[i] > start_asset

    if buy:
        trans = int(ma60[i-2] - ma5[i-2])//2
        trans = max(trans, 0)
        trans = min(trans, int(asset//p_lst[i]))
        asset -= trans * p_lst[i]
        stock += trans
        save = p_lst[i]
        if trans > 0:
            print(f'{i} / {trans}:{p_lst[i]} || {int(asset + stock * p_lst[i])}, {int(asset)}, {stock}')
            plt.plot(i,p_lst[i],'bx',ms=10,mew=4)
    elif sell:
        trans = int(ma5[i-2] - ma60[i-2])//3
        trans = max(trans, 0)
        trans = min(trans, int(stock))
        stock -= trans
        asset += trans * p_lst[i]
        if trans > 0:
            print(f'  {i} / {trans}:{p_lst[i]} || {int(asset + stock * p_lst[i])}, {int(asset)}, {stock}')
            plt.plot(i,p_lst[i],'rx',ms=10,mew=4)
    if i == n-1:
        asset += stock * p_lst[i]
        stock = 0
        print(f'  {i} / {stock}:{p_lst[i]} || {int(asset + stock * p_lst[i])}, {int(asset)}, {stock}')
        plt.plot(i,p_lst[i],'rx',ms=10,mew=4)
print('total asset:', asset, round(100*asset/start_asset,2), '%\n')
print('seed = ', seed)
plt.grid(); plt.legend()
plt.show()
