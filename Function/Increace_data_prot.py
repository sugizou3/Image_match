#ライブラリのインポート
import numpy as np

from scipy.interpolate import interp2d
def increase_data_plot(data,exCond,num=10):
    data_span_new = exCond['data_span']/num
    x = np.arange(data.shape[0])*exCond['data_span']
    y = np.arange(data.shape[1])*exCond['data_span']
    f = interp2d(y, x, data, kind='cubic')
    
    x2 = np.arange(data.shape[0]*num)*data_span_new
    y2 = np.arange(data.shape[1]*num)*data_span_new
    
    data_new = f(y2,x2)
    data_new=data_new.astype(np.float32)  
    return data_new,data_span_new