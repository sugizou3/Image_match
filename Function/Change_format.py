#ライブラリのインポート
import numpy as np
import pandas as pd
import math

# zのみのデータをxyzのデータにする
def z_xyzData(zData,data_span=0.125):
  data_xyz = np.empty((zData.shape[0], zData.shape[1],3))
  for i in range(zData.shape[0]):
    for j in range(zData.shape[1]):
      data_xyz[i][j] = [i*data_span,j*data_span,zData[i][j]]
  return data_xyz

# zのみのデータをxyzのデータにする
def z_xyzDataFrame(zData,data_span=0.125):
  # df_xyz = np.empty((zData.size,3))
  df_xyz = []
  range1 = int(zData.shape[0] )
  range2 = int(zData.shape[1] )
  for i in range(range1):
    for j in range(range2):
      if not math.isnan(zData[i][j]):
        df_xyz.append([i*data_span,j*data_span,zData[i][j]])
  df_xyz = pd.DataFrame(df_xyz,columns=['x', 'y', 'z'])
  return df_xyz