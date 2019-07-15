# 如何使用仓库的 MicroPython 代码

## 下载 Sample 示例代码包

### 方式（一）

进入 Github 仓库 <https://github.com/BPI-STEAMMicroPython-Samples> 下载代码包，点击 clone or download 后选择 download zip 下载压缩包

![sample](images/sample.jpg)

### 方式（二）

如果电脑有安装git工具，可以使用 git 工具把 samples 库 clone 下来。
在指定的文件夹中右键选择 Git Bash Hear
![sample9](images/sample9.png)

输入`git clone https://github.com/BPI-STEAM/MicroPython-Samples`

![sample10](images/sample10.png)

按下回车键开始 clone ，完成后 samples 库就会出现在文件夹中。

![sample11](images/sample11.png)

## 运行 sample 示例代码

### 连接板子

使用 usb 线连接电脑和 bit 板，如果在设备管理器中查找到相应的串口设备，即表示连接成功。

![sample5](images/sample6.png)

### 用 vscode 打开文件

解压我们下载得到的压缩包，右键选择用 vscode 打开

![sample1](images/sample3.png)

在右侧的文件编辑区可以看到我们的 sample 库

![sample1](images/sample4.png)

我们以 helloworld.py 为例演示下如何运行示例代码，首先双击打开 [helloworld.py](https://github.com/BPI-STEAM/MicroPython-Samples/blob/master/00.basics/helloworld.py)，然后在代码区右键选择 `run this file` 即可运行这个代码。
![sample5](images/sample5.png)

如果是第一次使用sample库就需要设置一下使用的串口号，点击 run this file 后会提示输入使用的串口号，这一步需要输入对应的 com 口，比如 'com3'、'com4'。这一步不是必要的可以选择跳过，如果没有设定 com 口， mpfshell 会自动搜索可用的 com 口。
![sample5](images/sample7.png)

成功运行程序得到结果。
![sample5](images/sample8.png)
