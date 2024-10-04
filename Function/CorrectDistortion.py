#ライブラリのインポート
import numpy as np
from sklearn import linear_model

def getDistortion(df_xyz):
  # データを用意する
  x = df_xyz["x"]
  y = df_xyz["y"]
  z = df_xyz["z"]

  X = np.c_[x, y]
  model = linear_model.LinearRegression()    # 線形回帰モデルを定義
  model.fit(X, z)                            # 学習実行
  # reg_y = model.predict(X)                   # xに対する予測値を計算

  # # パラメータ算出
  reg_wn = model.coef_                       # 偏回帰係数
  reg_w0 = model.intercept_                  # 切片
  r2 = model.score(X, z)                     # 決定係数
  res = [reg_wn[0],reg_wn[1],reg_w0]
  print(r2)
  return res

def correctDistortion(data_xyz,array):
  a = array[0]
  b = array[1]
  c = array[2]

  z_div_array = np.zeros((data_xyz.shape[0],data_xyz.shape[1]))
  for i in range(data_xyz.shape[0]):
    for j in range(data_xyz.shape[1]):
      point = data_xyz[i][j]
      x = point[0]
      y = point[1]
      z_data = point[2]
      z_calc = a*x+b*y+c
      z_div = z_data-z_calc
      z_div_array[i][j] = z_div
      data_xyz[i][j][2] = z_div
  z_div_array = z_div_array.astype(np.float32)

  return z_div_array,data_xyz

def matchDistortion(data_xyz,array1,array2):
  a1 = array1[0]
  b1 = array1[1]
  c1 = array1[2]
  a2 = array2[0]
  b2 = array2[1]
  c2 = array2[2]

  z_div_array = np.zeros((data_xyz.shape[0],data_xyz.shape[1]))
  for i in range(data_xyz.shape[0]):
    for j in range(data_xyz.shape[1]):
      point = data_xyz[i][j]
      x = point[0]
      y = point[1]
      z_data = point[2]
      z_calc1 = a1*x+b1*y+c1
      z_calc2 = a2*x+b2*y+c2
      z_div = z_data-z_calc2+z_calc1
      z_div_array[i][j] = z_div
      data_xyz[i][j][2] = z_div
  z_div_array = z_div_array.astype(np.float32)

  return z_div_array,data_xyz
