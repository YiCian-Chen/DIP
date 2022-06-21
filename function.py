import scipy.special as special
from tkinter.filedialog import askopenfilename, asksaveasfile
import cv2
import numpy as np

# 儲存影像
def save_file():
    global tmp
    # 詢問影像儲存位置
    path = asksaveasfile(initialfile='output.png',
                        defaultextension=".png",
                        filetypes=[
                            ("All Files", "*.*"),
                            ("png files", "*.png"),
                            ("jpeg files", "*.jpg")])
    # 將影像寫入指定的位置
    cv2.imwrite(path.name, tmp)

# 載入影像
def open_file():
    global img,tmp
    # 詢問影像開啟位置
    path = askopenfilename(title='選擇',
                            filetypes=[
                                ('All Files', '*'),
                                ("jpeg files", "*.jpg"),
                                ("png files", "*.png")])
    # 將載入影像從指定的位置，透過解碼來解決讀入中文檔名問題
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)
    tmp = img
    cv2.imshow("picture",tmp)

# 去背函式
def background_func(val):
    global img,tmp
    val = int(val) # 將數值從str轉成int
    tmp = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA) # 因為是 jpg，要轉換顏色為 BGRA
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 轉成灰階方便做出判斷
    tmp_show = tmp.copy()
    h, w = img.shape[:2]
    for x in range(w):
        for y in range(h):
            if gray[y, x] > val: # 若該像素大於門檻值
                tmp[y, x, 3] = 255 - gray[y, x] # 調整該像素位置的透明度
                tmp_show[y, x] = [0, 255, 255, 255] # 將有調整的地方用黃色顯示
                # 使用 255 - gray[y, x] 可以將一些邊緣的像素變成半透明，避免太過鋸齒的邊緣
    cv2.imshow('picture', tmp_show)

# 雙邊濾波
def Bilateral_func(item1,item2):
    global img,tmp
    size = int(item1.get())
    sigma = int(item2.get())
    tmp = cv2.bilateralFilter(img,size,sigma,sigma)
    cv2.imshow('picture', tmp)

# 顯示預設影像
def default():
    global img,tmp
    tmp = img
    cv2.imshow('picture', tmp)

# 調整曝光
def gamma_func(val):
    global img, tmp
    val = float(val)
    tmp = gamma_correction(img, val)
    cv2.imshow('picture', tmp)

# 調整對比
def beta_func(item1, item2):
    global img, tmp
    A = float(item1.get())
    B = float(item2.get())
    tmp = beta_correction(img,A,B)
    cv2.imshow('picture', tmp)

# 伽瑪矯正函式
def gamma_correction(f, gamma):
	g = f.copy()
	nr, nc = f.shape[:2]
	c = 255.0 / (255.0 ** gamma)
	table = np.zeros(256)
	for i in range(256):
		table[i] = round(i ** gamma * c, 0)
	if f.ndim != 3:
		for x in range(nr):
			for y in range(nc):
				g[x, y] = table[f[x, y]]
	else:
		for x in range(nr):
			for y in range(nc):
				for k in range(3):
					g[x, y, k] = table[f[x, y, k]]
	return g

# Beta矯正函式
def beta_correction(f, a, b):
	g = f.copy()
	nr, nc = f.shape[:2]
	x = np.linspace(0, 1, 256) # 在0~1之間產生256個點
    # 將不完整Beta函數輸出正規化至0~255
	table = np.round(special.betainc(a, b, x) * 255, 0)
	if f.ndim != 3:
		for x in range(nr):
			for y in range(nc):
				g[x, y] = table[f[x, y]]
	else:
		for x in range(nr):
			for y in range(nc):
				for k in range(3):
					g[x, y, k] = table[f[x, y, k]]
	return g

# 影像銳化
def sharp_func(val):
    global img, tmp
    val = int(val)
    blur = cv2.GaussianBlur(img, (0, 0), val) # 先將影像模糊
    tmp = cv2.addWeighted(img, 1.5, blur, -0.5, 0) # 模糊的反操作來實現銳化
    cv2.imshow('picture', tmp)
