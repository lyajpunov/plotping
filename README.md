# 功能

本脚本的功能是ping一个地址，实时检测与次地址之间的通信状态，并绘图，并带有截图和log功能，可以把断连时间写入log文件中

# 安装

需要安装python3的包：

```
pip3 install matplotlib
pip3 install schedule
pip3 install ping3
```


# 操作
获取数据(需要修改源文件的IP),ping3需要root权限，所以

```
sudo python3 plotping.py
```


# 配置
请在`setting.py`中进行配置

```
# 主要的配置，要ping的地址，可以是网址也可以是ip
need_ip = ['www.baidu.com']
```

