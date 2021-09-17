import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame,Series

def danZuZheXian():
    np.random.seed(0)  # 使得每次生成的随机数相同
    ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))
    ts1 = ts.cumsum()  # 累加
    ts1.plot(kind="line")  # 默认绘制折线图

def duoZuZheXian():
    np.random.seed(0)  # 使得每次生成的随机数相同
    ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))
    np.random.seed(0)
    df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list("ABCD"))
    df = df.cumsum()
    df.plot()  # 默认绘制折线图

if __name__ == '__main__':
    plt.style.use('dark_background')  # 设置绘图风格
    duoZuZheXian()