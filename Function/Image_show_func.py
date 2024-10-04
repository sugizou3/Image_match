#ライブラリのインポート
import numpy as np
import cv2


# 表面データを高さ方向をグレースケールに変換して画像データに変換
def dataToImg(zData,std_show=False):
  mean = np.mean(zData)
  std = np.std(zData)
  if std_show:
    print(std)
  if std < 0.001:
    std = 0.001
  data = (zData-mean)/std
  data_sigmoid = 1/(1+np.exp(-data))
  zDataImg = data_sigmoid*255
  cv2.cvtColor(zDataImg, cv2.COLOR_BGR2RGB)
  return zDataImg

# 画像を表示するときに画像の大きさを変更する
def resizeData(data,per_reduction=0.2):  #per_reductionは画像を小さくする割合
  dataSize_x = data.shape[1]
  dataSize_y = data.shape[0]
  reductedSize_x = int(dataSize_x*per_reduction)
  reductedSize_y = int(dataSize_y*per_reduction)
  data_resize = cv2.resize(data,(reductedSize_x,reductedSize_y))
  return data_resize