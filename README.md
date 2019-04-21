# Computer Animation and Applications

## 程序说明

实现了3种不同的morphing方法，并对结果进行对比.

三种方法分别为:

cross-dissolve (详见utils.cross_dissolve)

基于特征点的方法(详见face.py)

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

## 例子

输入图片分别为:

![img_src.bmp](<https://raw.githubusercontent.com/666haiwen/morphying/master/img/1.bmp>)

![img_dst.bmp](<https://raw.githubusercontent.com/666haiwen/morphying/master/img/2.bmp>)

cross-dissolve结果为:



face-features-based结果为:



muli-feature-lines结果为:





所有结果详见result文件夹