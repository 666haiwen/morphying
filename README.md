# Computer Animation and Applications

## 程序说明

实现了3种不同的morphing方法，并对结果进行对比.

三种方法分别为:

cross-dissolve (详见utils.cross_dissolve)

基于人脸特征点的方法(详见face.py)

基于多条特征线的方法(详见morphing.py)



## 运行说明

#### 文件：

```
img\       (存放着测试用图)
model\     (dlib库所用的人脸特征检测模型)
result\    (程序运行结果)
main.py    (运行程序)
const.py   (参数设定)
```

#### 版本：

```
python: v3.6.0b1+
```

#### 库依赖：

```
dlib==19.17.0
imageio==2.5.0
numpy==1.13.0+mkl
opencv-python==4.1.0.25
```

#### 模型依赖:

下载dlib库所用的68-features人脸检测模型: **shape_predictor_68_face_landmarks.dat.bz2**,并将其放入**model**文件夹中

**links**：http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2  

#### 运行：

直接运行main.py即可.

cross-dissolve方法和基于人脸特征点的方法自动获得结果.

基于多条特征线的方法需要人手动设定特征线条来完成。例子如下：

![img_dst.bmp](<https://raw.githubusercontent.com/666haiwen/morphying/master/img/muli-lines.png>)

选取方法：

鼠标左键点击产生点，产生两点之后自动产生两点之间的连线，即为特征线的选取.

要保持左右两张图片特征线产生的顺序一致.

按esc或者回车表示选取完成.



## 例子

输入图片分别为:

![img_src.bmp](<https://raw.githubusercontent.com/666haiwen/morphying/master/img/1.bmp>)

![img_dst.bmp](<https://raw.githubusercontent.com/666haiwen/morphying/master/img/2.bmp>)

cross-dissolve结果为:

![](<https://raw.githubusercontent.com/666haiwen/morphying/master/result/cross_dissolve_transfer.png>)

face-features-based结果为:

![](<https://raw.githubusercontent.com/666haiwen/morphying/master/result/face_features_transfer.png>)

muli-feature-lines结果为:

![](<https://raw.githubusercontent.com/666haiwen/morphying/master/result/mult_lines_transfer.png>)



所有结果详见result文件夹



## 结果分析

#### cross-dissolve

优点：实现简单，容易理解

缺点：效果往往不好



#### face-features-points

优点：自动标注，效果好，借助了dlib获得的68个人脸特征点

缺点：由于借助了dlib库，所以同样有一定局限性，只能对人脸进行morphing

其他： 真正在程序中，除了68个人脸特征点之外，另外增加了8点图像边缘点(4个顶点及4条边的中点)



#### muli-feature-lines:

优点：效果好于cross-dissolve,取决于特征线条的选取，当特征线选取较好时，结果较好.

缺点：基于方法本身，所以在morphing开始时，原始图像已经发生了一定程度的形变以对应特征线.而图像内容形变的过程是直接通过计算得到的，没有一个缓慢过渡的过程。

计算复杂度高。

其他：在实现过程中，需要人手工的选取特征线来获得结果。
