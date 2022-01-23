#coding=utf-8

import matplotlib.pyplot as plt


#定义图片大小及清晰度。dpi参数是清晰度。
fig = plt.figure(figsize=(20,8),dpi=80)
x = range(2,26,2)
y = [15,13,14.5,17,20,25,26,26,24,22,18,15]

#绘制图形
plt.plot(x,y)
#x轴刻度.取X的数据
plt.xticks(x)
#y轴刻度。取y的数据，最大数加2
plt.yticks(range(min(y),max(y)+2))
#保存图片文件.
plt.savefig("./png/test1.png")
#展示图形
plt.show()