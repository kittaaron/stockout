# -*- coding: utf-8 -*-

#%% 导入包
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt

#%% 获取中国平安三年内K线数据
ZGPA=ts.get_hist_data('000001')
ZGPA.index=pd.to_datetime(ZGPA.index)

#%% 相关指数
print(ZGPA.tail())
plt.plot(ZGPA['close'],label='收盘价')
plt.plot(ZGPA['ma5'],label='MA5')
plt.plot(ZGPA['ma20'],label='MA20')
plt.legend()
plt.xlabel('日期')
plt.ylabel('股价')
plt.title('中国平安收盘价，MA5，MA20时间序列')

#%% 获取中国平安全部历史数据
ZGPA_all=ts.get_h_data('000001',start='2006-01-01')
ZGPA_all.index=pd.to_datetime(ZGPA_all.index)

#%% 相关指数
print(ZGPA_all.tail())
plt.plot(ZGPA_all['close'],label='收盘价')
plt.legend()
plt.xlabel('日期')
plt.ylabel('股价')
plt.title('中国平安收盘价时间序列(2006至今)')

#%% 计算收益率
ZPGA_Return=((ZGPA_all['close']-ZGPA_all['close'].shift(1))/ZGPA_all\
                    ['close'].shift(1)).dropna() #收益率
plt.plot(ZPGA_Return)
print('中国平安的平均日收益率：',ZPGA_Return.mean(),'\n中国平安的收益率标准差：',\
              ZPGA_Return.std())
