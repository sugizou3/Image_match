#ライブラリのインポート
import numpy as np
import cv2

# 画像を回転させながら一致する箇所を探す関数
# rotateDegは回転の範囲、changeDegは回転間隔

def matchingData(data,data_rot,templateData,rotateDeg,changeDeg):
  maxdeg=None
  value=0

  # 画像を回転させる処理
  rotRange = np.arange(-rotateDeg, rotateDeg, changeDeg)
  rotRange = np.round(rotRange, 3)
  for i in rotRange:
    rows,cols = data.shape[:2]
    #画像の回転量を決定して変数に格納
    M = cv2.getRotationMatrix2D((cols/2,rows/2),i,1)
    #画像を回転
    data_div = cv2.warpAffine(data_rot,M,(cols,rows))

    res = cv2.matchTemplate(data_div, templateData, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val > value:
      top_left=max_loc
      changeDeg=i
      changeImg=data_div
      value =max_val

  # res = cv2.matchTemplate(data_rot, templateData, cv2.TM_CCOEFF_NORMED)
  # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
  # top_left=max_loc
  # changeImg=data_rot



  print(changeDeg)
  print(value)
  print("max_val",max_val)

  #回転によってできた空間部分の削除
  roundCutIndex = -1
  #左上らへんに0があるか確認
  for i in range(changeImg.shape[0]):
    if changeImg[0][i] ==0 and changeImg[i][0] == 0 :
      roundCutIndex = i
    else:
      break
  #左下にゼロがあるか確認
  for i in range(changeImg.shape[0]):
    if changeImg[0][-i] ==0 and changeImg[-i][0] == 0 :
      roundCutIndex = i
    else:
      break



  roundCutNum = roundCutIndex+1 #切り取る行列数，配列のインデックスは0からはじまるので
  if roundCutNum != 0:
    changeData_corrected = np.delete(changeImg,np.s_[:roundCutNum],0)
    changeData_corrected = np.delete(changeData_corrected,np.s_[-roundCutNum:],0)
    changeData_corrected = np.delete(changeData_corrected,np.s_[:roundCutNum],1)
    changeData_corrected = np.delete(changeData_corrected,np.s_[-roundCutNum:],1)
  else:
    changeData_corrected = changeImg

  top_left = [top_left[1]-roundCutNum,top_left[0]-roundCutNum] #[縦,横]
  # top_left = [top_left[1],top_left[0]]


  return changeImg,top_left,changeDeg



def rotateData(data,deg):
  rows,cols = data.shape[:2]
  #画像の回転量を決定して変数に格納
  M = cv2.getRotationMatrix2D((cols/2,rows/2),deg,1)
  #画像を回転
  data_div = cv2.warpAffine(data,M,(cols,rows))

  #回転によってできた空間部分の削除
  roundCutIndex = -1
  #左上らへんに0があるか確認
  for i in range(data_div.shape[0]):
    if data_div[0][i] ==0 and data_div[i][0] == 0 :
      roundCutIndex = i
    else:
      break
  # #左下にゼロがあるか確認
  for i in range(data_div.shape[0]):
    if data_div[0][-i] ==0 and data_div[-i][0] == 0 :
      if i > roundCutIndex:
        roundCutIndex = i
    else:
      break

  roundCutNum = roundCutIndex+1 #切り取る行列数，配列のインデックスは0からはじまるので
  if roundCutNum != 0:
    changeData_corrected = np.delete(data_div,np.s_[:roundCutNum],0)
    changeData_corrected = np.delete(changeData_corrected,np.s_[-roundCutNum:],0)
    changeData_corrected = np.delete(changeData_corrected,np.s_[:roundCutNum],1)
    changeData_corrected = np.delete(changeData_corrected,np.s_[-roundCutNum:],1)
  else:
    changeData_corrected = data_div


  return changeData_corrected