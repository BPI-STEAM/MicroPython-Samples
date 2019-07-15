# 常见 FAQ 收集

本页主要是收集各类常见的问题的解决方案，若是其他硬件不一定对应下述解答，下述只针对 BPI-BIT 的 MicroPython 固件有效。

## 连不上硬件，找不到驱动

- 确保使用 USB 2.0 以上的接口接入设备，且供电至少高于 200ma ，避免使用大电流的电源直接供电。

- 检查串口驱动是否安装完成，即插上板子的时候在设备管理器中找不到串口设备，大概率就是没有安装好驱动，这时候需要 [安装驱动](https://bpi-steam-docs.readthedocs.io/zh_CN/latest/bpi-steam/driver.html)

## 运行 Mpfshell 没有反应

- 检查设备的串口号，你可以通过拔插设备来核对串口号。

- 检查串口设备是否 **被其他应用程序占用** ，不知道发生什么就重启电脑。
  
- 避开下述代码段在 main 函数中无延时死循环运行（特指 Mac 系统无法控制 RST 重启板子）。

    ```python
    while True:
        pass
    ```

- 建议写死循环的时候添加适当的延时或代码循环执行，千万不要让程序空转，例如如下代码。

    ```python
    while True:
        print('你好')
    ```

## 连不上 WIFI

- 手机配置板子联网教程可以参考[此文档](https://doc.bpi-steam.com/zh_CN/latest/bpi-mpy/advanced/wifi.html)。

- 确认账号密码无误，确保 WIFI 路由的热点连接为 2.4Ghz ，文本编码均为 UTF-8 。
