import tkinter as tk
from function import *

# 建立視窗
root = tk.Tk()
root.geometry('350x500')
root.title('圖片處理')

# 建立載入/存檔按鈕
tk.Button(root, text='選擇圖片', command=open_file).grid(column=0, row=0, padx=10, pady=10)
tk.Button(root, text="儲存圖片", command=save_file).grid(column=1, row=0, padx=10, pady=10)

# 查看是哪一項功能被選取
def check(item):
    if item['text'] == "雙邊濾波":
        # 將選取方塊勾選時
        if Bilateral_var.get() == 1:
            reset() # 將全部功能取消勾選
            Bilateral_var.set(1)  # 將此功能勾選
            # 讓滑桿物件可以使用
            Bilateral_sigma_scale['state'] = tk.NORMAL
            Bilateral_size_scale['state'] = tk.NORMAL
            # 呼叫函式將影像進行處理
            Bilateral_func(Bilateral_size_scale, Bilateral_sigma_scale)
        else:  # 選取方塊取消勾選時
            # 將滑桿物件停用
            Bilateral_sigma_scale['state'] = tk.DISABLED
            Bilateral_size_scale['state'] = tk.DISABLED
            default()  # 呼叫函式將影像恢復成原始影像
    elif item['text'] == "去背":
        if background_var.get() == 1:
            reset()
            background_var.set(1)
            background_scale['state'] = tk.NORMAL
            background_func(background_scale.get())
        else:
            background_scale['state'] = tk.DISABLED
            default()
    elif item['text'] == "調整曝光":
        if gamma_var.get() == 1:
            reset()
            gamma_var.set(1)
            gamma_scale['state'] = tk.NORMAL
            gamma_func(gamma_scale.get())
        else:
            gamma_scale['state'] = tk.DISABLED
            default()
    elif item['text'] == "影像對比":
        if beta_var.get() == 1:
            reset()
            beta_var.set(1)
            beta_A_scale['state'] = tk.NORMAL
            beta_B_scale['state'] = tk.NORMAL
            beta_func(beta_A_scale, beta_B_scale)
        else:
            beta_A_scale['state'] = tk.DISABLED
            beta_B_scale['state'] = tk.DISABLED
            default()
    elif item['text'] == "影像銳化":
        if sharp_var.get() == 1:
            reset()
            sharp_var.set(1)
            sharp_scale['state'] = tk.NORMAL
            sharp_func(sharp_scale.get())
        else:
            sharp_scale['state'] = tk.DISABLED
            default()


################ Bilateral雙邊濾波
# Button 物件是否勾選時的變數
Bilateral_var = tk.IntVar()
# 建立Button物件
Bilateral_btn = tk.Checkbutton(root, text='雙邊濾波', command=lambda: check(Bilateral_btn),var=Bilateral_var)
# 設定Button物件的位置
Bilateral_btn.grid(column=0, row=1, padx=10, pady=10)
# 建立Scale物件
Bilateral_size_scale = tk.Scale(orient='horizontal', label='size',
    command=lambda x: Bilateral_func(Bilateral_size_scale, Bilateral_sigma_scale))
# 設定Scale物件數值大小的界線
Bilateral_size_scale.config(from_=1, to=30, tickinterval=29)
# 初始化Scale物件的數值
Bilateral_size_scale.set(1)
# 設定Scale物件的位置
Bilateral_size_scale.grid(column=1, row=1)

Bilateral_sigma_scale = tk.Scale(orient='horizontal', label='sigma',
    command=lambda x: Bilateral_func(Bilateral_size_scale, Bilateral_sigma_scale))
Bilateral_sigma_scale.config(from_=1, to=200, tickinterval=199)
Bilateral_sigma_scale.set(1)
Bilateral_sigma_scale.grid(column=2, row=1)


################ background去背
background_var = tk.IntVar()
background_btn = tk.Checkbutton(root, text='去背', command=lambda: check(background_btn),var=background_var)
background_btn.grid(column=0, row=2, padx=10, pady=10)

background_scale = tk.Scale(orient='horizontal', label='門檻值',command=background_func)
background_scale.config(from_=200, to=255, tickinterval=55)
background_scale.set(230)
background_scale.grid(column=1, row=2)


################ gamma_correction調整曝光
gamma_var = tk.IntVar()
gamma_btn = tk.Checkbutton(root, text='調整曝光', command=lambda: check(gamma_btn),var=gamma_var)
gamma_btn.grid(column=0, row=3, padx=10, pady=10)

gamma_scale = tk.Scale(orient='horizontal', label='γ(Gamma)', resolution=0.1,command=gamma_func)
gamma_scale.config(from_=0.1, to=2.0, tickinterval=1.9)
gamma_scale.set(1.0)
gamma_scale.grid(column=1, row=3)


################ beta_correction調整對比
beta_var = tk.IntVar()
beta_btn = tk.Checkbutton(root, text='影像對比', command=lambda: check(beta_btn),var=beta_var)
beta_btn.grid(column=0, row=4, padx=10, pady=10)

beta_A_scale = tk.Scale(orient='horizontal', label='a', resolution=0.1,command=lambda x: beta_func(beta_A_scale, beta_B_scale))
beta_A_scale.set(1.0)
beta_A_scale.config(from_=0.1, to=2.0, tickinterval=1.9)
beta_A_scale.grid(column=1, row=4)

beta_B_scale = tk.Scale(orient='horizontal', label='b', resolution=0.1,command=lambda x: beta_func(beta_A_scale, beta_B_scale))
beta_B_scale.set(1.0)
beta_B_scale.config(from_=0.1, to=2.0, tickinterval=1.9)
beta_B_scale.grid(column=2, row=4)


################ sharp影像銳化
sharp_var = tk.IntVar()
sharp_btn = tk.Checkbutton(root, text='影像銳化', command=lambda: check(sharp_btn), var=sharp_var)
sharp_btn.grid(column=0, row=5, padx=10, pady=10)

sharp_scale = tk.Scale(orient='horizontal', label='sigma',resolution=1, command=sharp_func)
sharp_scale.config(from_=1, to=100, tickinterval=99)
sharp_scale.set(1)
sharp_scale.grid(column=1, row=5)

# 將全部的物件設定為停用狀態
def reset():
    Bilateral_sigma_scale['state'] = tk.DISABLED
    Bilateral_size_scale['state'] = tk.DISABLED
    background_scale['state'] = tk.DISABLED
    gamma_scale['state'] = tk.DISABLED
    beta_A_scale['state'] = tk.DISABLED
    beta_B_scale['state'] = tk.DISABLED
    sharp_scale['state'] = tk.DISABLED
    Bilateral_var.set(0)
    background_var.set(0)
    gamma_var.set(0)
    beta_var.set(0)
    sharp_var.set(0)

reset()
root.mainloop()
