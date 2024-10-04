#ライブラリのインポート
import numpy as np
import matplotlib.pyplot as plt
import cv2

from Function.Image_show_func import dataToImg

# データの一部をマスクする関数　maskPointで指定された値をすべて０にする
def maskData_legacy(data,maskPoints):
  data_change = data.copy()
  dataImg = dataToImg(data)
  for i in range(len(maskPoints)):
    maskPoint = maskPoints[i]
    data_change[maskPoint[0]:maskPoint[1],maskPoint[2]:maskPoint[3]] = np.nan
    dataImg[maskPoint[0]:maskPoint[1],maskPoint[2]:maskPoint[3]] = 0
    
  fig = plt.figure()
  ax = fig.add_subplot(1, 2, 1)
  plt.imshow(dataImg, cmap = "gray", origin='lower')

  return data_change

def create_maskData(zData,conv_smooth_size,conv2_height,conv2_width,conv2_roop):
    n = conv_smooth_size
    # 4x4配列で値が1/16の畳込フィルタ要素を用意
    kernel = np.ones((n+1,n+1)) /n**2

    laplacian_kernel = np.array([[1,  2, 1],
                                [0, 0, 0],
                                [-1,  -2, -1]])

    # 畳み込み操作
    conv_img = cv2.filter2D(zData,-1,kernel)
    conv2_img = cv2.filter2D(conv_img,-1,laplacian_kernel)
    conv2_img = dataToImg(conv2_img)
    _, conv3_img = cv2.threshold(conv2_img, 200, 255, cv2.THRESH_BINARY)
    # 入力画像
    img = conv3_img

    height = conv2_height
    width = conv2_width
    roop = conv2_roop
    # 4x4配列で値が1/16の畳込フィルタ要素を用意
    kernel = np.ones((height+1,width+1)) /(height*width)

    # fig = plt.figure(figsize=(50,50))
    # fig.suptitle('title')

    for i in range(roop):
        # 畳み込み操作
        img = cv2.filter2D(img,-1,kernel)                                 
        _, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    
    return img

def maskData(data,maskData):
    data_change = data.copy()
    dataImg = dataToImg(data)
    for i in range(data_change.shape[0]):
        for j in range(data_change.shape[1]):
            if maskData[i][j] == 255:
                data_change[i][j] = np.nan
                dataImg[i][j] = 0
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(dataImg, cmap = "gray", origin='lower')

    return data_change


def cut_data(data_after,data_before,range):
    after= data_after[range[0]:range[1],range[2]:range[3]]
    before=data_before[range[0]:range[1],range[2]:range[3]]
    return after,before





# データを切り抜く cutPointは切り抜く配列のインデックスを指定
def cutTemplateData(data,cutPoint,bool_ImgShow=True):
  # cutImg = [0,0,0,0]
  # for i in range(4):
  #   if i <2:
  #     axis = 0;
  #   else:
  #     axis = 1;
  #   cutImg[i] = int(cutPoint[i]*data.shape[axis])

  top_left = [cutPoint[0],cutPoint[2]]
  # templateRange = [cutPoint[0],cutPoint[1],cutPoint[2],cutPoint[3]]
  templateData = data[cutPoint[0]:cutPoint[1],cutPoint[2]:cutPoint[3]]
  templateData = np.array(templateData)
  imgData = dataToImg(templateData)
  data_img = dataToImg(data)
  data_change = data_img.copy()
  data_change[cutPoint[0]:cutPoint[1],cutPoint[2]:cutPoint[3]] = 0
  if bool_ImgShow:
    fig = plt.figure()
    ax = fig.add_subplot(1, 3, 1)
    plt.imshow(dataToImg(data_img), cmap = "gray", origin='lower')
    ax = fig.add_subplot(1, 3, 2)
    plt.imshow(dataToImg(data_change), cmap = "gray", origin='lower')
    ax = fig.add_subplot(1, 3, 3)
    plt.imshow(dataToImg(imgData), cmap = "gray", origin='lower')
  return templateData,top_left


def matchCutData(data1,data2,top_left1,top_left2):
  bottom_right1 = [data1.shape[0]-top_left1[0],data1.shape[1]-top_left1[1]]
  bottom_right2 = [data2.shape[0]-top_left2[0],data2.shape[1]-top_left2[1]]

  vec1 = [top_left1[0]-top_left2[0],top_left1[1]-top_left2[1]]
  vec2 = [bottom_right1[0]-bottom_right2[0],bottom_right1[1]-bottom_right2[1]]

  print("vec1",vec1)
  print("vec2",vec2)


  if vec1[0]>0: #たて
      vec = vec1[0]
      data1_corrected = np.delete(data1,np.s_[:vec],0)
      data2_corrected = data2
  if vec1[0]<0: #たて
      vec = np.abs(vec1[0])
      data1_corrected = data1
      data2_corrected = np.delete(data2,np.s_[:vec],0)
  if vec1[0] == 0: #たて
    data1_corrected = data1
    data2_corrected = data2

  if vec1[1]>0: #よこ
      vec = vec1[1]
      data1_corrected = np.delete(data1_corrected,np.s_[:vec],1)
      data2_corrected = data2_corrected
  if vec1[1]<0: #よこ
      vec = np.abs(vec1[1])
      data1_corrected = data1_corrected
      data2_corrected = np.delete(data2_corrected,np.s_[:vec],1)



  if vec2[0]>0: #たて
      vec = vec2[0]
      data1_corrected = np.delete(data1_corrected,np.s_[-vec:],0)
      data2_corrected = data2_corrected
  if vec2[0]<0: #たて
      vec = np.abs(vec2[0])
      data1_corrected = data1_corrected
      data2_corrected = np.delete(data2_corrected,np.s_[-vec:],0)

  if vec2[1]>0: #よこ
      vec = vec2[1]
      data1_corrected = np.delete(data1_corrected,np.s_[-vec:],1)
      data2_corrected = data2_corrected
  if vec2[1]<0: #よこ
      vec = np.abs(vec2[1])
      data1_corrected = data1_corrected
      data2_corrected = np.delete(data2_corrected,np.s_[-vec:],1)

  return data1_corrected,data2_corrected


