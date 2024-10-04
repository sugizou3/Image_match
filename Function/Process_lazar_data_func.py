#ライブラリのインポート
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Function.Image_show_func import dataToImg

# レーザ顕微鏡のデータ処理　csvデータのｚ方向データだけ抜き出す
def dataProcessing_lazar(df_original):
  df = df_original.iloc[19:,1:1025]
  zData = df.values
  zData=zData.astype(np.float32)
  return df,zData

# 白色顕微鏡のデータ処理　csvデータのｚ方向データだけ抜き出す
def dataProcessing_white(df_original):
  df = df_original
  zData = df.values
  zData=zData.astype(np.float32)
  return df,zData

def process_data(filename,rotation = False,lazar=True,col_range=1026):
  if lazar:
    col_names = ['{0:02d}'.format(i) for i in range(col_range)]
    df_original = pd.read_csv(filename ,encoding='utf-8', names = col_names)
    df_original = df_original.dropna(how='all', axis=1)
    df,zData = dataProcessing_lazar(df_original)
  else:
    col_names = ['{0:02d}'.format(i) for i in range(col_range)]
    df_original = pd.read_table(filename ,encoding='utf-8', names = col_names)
    df_original = df_original.dropna(how='all', axis=1)
    df,zData = dataProcessing_white(df_original)

  if rotation ==True:
      zData = zData.T
      zData = np.flipud(zData)
      
  print(col_range-df_original.shape[0])
  print(col_range-df_original.shape[1])

  fig = plt.figure()
  zData_img = dataToImg(zData)
  plt.imshow(zData_img,cmap = "gray", origin='lower')
  return zData