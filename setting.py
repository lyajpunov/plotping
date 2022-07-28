'''
@ author:Lyj
@ data:"2022-07-28 15:58:21"
@ e-mail:"lyjlove1314@gmail.com"
'''

# 请求间隔时间,单位ms
time_every = 50

# 请求最大延迟ms
timeout = 100

# 需要ping的IP
need_ip = ['www.baidu.com']

# 是否需要将全程数据结果保存
is_save_data = True

# 全部数据的保存地址
data_uri = './data.json'

# 是否实时绘图
is_real_picture = True

# 绘制图形对应IP颜色 基本颜色代码b,c,g,k,m,r,w,y
need_color = ['aquamarine','dodgerblue']

# 多长时间显示一张图ms
time_plot = 500

# 多长时间保存一张图ms
save_time_plot = 1000

# 每张图片显示的时间宽度最大值ms
time_length = 4000

# 是否需要将图片保存
is_save_picture = True

# 图片的保存地址
picture_uri = './picture/'

# 异常日志保存地址
log_uri = './error.log'


#################################################
# 不需要配置部分，部分全局变量的设置

# 长度
length = len(need_ip)

# 每张图的最大点数
point = int(time_length / time_every)

# 插图数量
picture_of_save = save_time_plot / time_plot