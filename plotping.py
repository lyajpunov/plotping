'''
@ author:Lyj
@ data:"2022-07-28 15:58:21"
@ e-mail:"lyjlove1314@gmail.com"
'''


from ping3 import ping
import schedule
import sys
import select
import datetime
import json
from setting import *
import matplotlib.pyplot as plt
from multiprocessing import Process
from multiprocessing import Queue
import os

class getdata:
    def __init__(self) -> None:
        self.data = {}
        self.length = length

        # 将配置文件保存入最后数据保存位置
        self.data['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.data['time_every'] = time_every
        self.data['timeout'] = timeout
        self.data['need_ip'] = need_ip
        self.data['is_save_data'] = is_save_data
        self.data['data_uri'] = data_uri
        self.data['is_real_picture'] = is_real_picture
        self.data['need_color'] = need_color
        self.data['time_plot'] = time_plot
        self.data['save_time_plot'] = save_time_plot
        self.data['time_length'] = time_length
        self.data['is_save_picture'] = is_save_picture
        self.data['picture_uri'] = picture_uri
        self.data['log_uri'] = log_uri
        self.data['data'] = [[] for _ in range(self.length)]

        # log文件
        self.log = open(log_uri,'a')

        # 创建线程和管道
        self.data_queue = Queue()
        self.t = Process(target=self.realtime_plot,args=(self.data_queue,))

        # 查看是否存在保存图片的目录，不存在则创建一个
        if not os.path.exists(picture_uri):
            os.mkdir(picture_uri)

        # 如果颜色不够用那就使用默认颜色
        if len(need_ip) > len(need_color):
            for i in range(len(need_ip) - len(need_color)):
                need_color.append('aquamarine')

        
    def ping_ip(self):
        # 进程运行
        self.t.start()

        # 终止进程
        print('请输入c来中止程序运行')

        # 定时器进行任务调度
        schedule.every(time_every/1000).seconds.do(self.job)
        schedule.every(time_plot/1000).seconds.do(self.realtime_plot_start)

        # 死循环将任务抛入队列
        while True:
            schedule.run_pending()
        
    '''
    ping的主要任务
    '''
    def job(self):
        for i, ip in enumerate(need_ip):
            sec = ping(ip, unit='ms',timeout=timeout/1000)
            
            # 断连则返回None,所以需要进行异常处理 
            print(sec)
            if sec is None:
                err = '['+ip+'@'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+']'+'  timeout!'
                print(err + 'sec被置为0')
                self.log.write(err+'\n')
                sec = 0

            self.data['data'][i].append(sec)

        # 进行无堵塞的键盘输入,检测键盘输入是否为'c'
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            c = sys.stdin.read(1)
            if c == 'c':
                self.exit_data()

    '''
    消费者
    '''
    def realtime_plot(self,x_y):
        plt.ion()
        flag = 0
        while True:
            # 保存通过管道传入的数据
            my_x_y = x_y.get()

            # 当管道传入false时准备结束进程
            if my_x_y == False:
                break

            # 是否实时绘图
            if is_real_picture:
                plt.clf() # 清除之前画得图
                for i, ip in enumerate(need_ip):
                    ydata = my_x_y['data'][i]
                    xdata = [m*time_every/1000 for m in range(len(ydata))]
                    plt.subplot(length,1,i+1) # 字图位置
                    plt.plot(xdata, ydata, need_color[i]) # 画字图
                    plt.title(ip) # 字图title
                    plt.pause(0.01) # 停留0.01s

            # 是否保存图片
            if is_save_picture:
                if flag != flag % picture_of_save:
                    flag = flag % picture_of_save
                    plt.savefig(picture_uri+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'.jpg')
                flag = flag + 1

        # 在进程结束之前关闭plt窗口
        plt.close()
    
    '''
    生产者，将数据抛入管道
    '''
    def realtime_plot_start(self):
        queue_data = self.data
        for i in range(len(need_ip)):
            if len(queue_data['data'][i]) > point:
                queue_data['data'][i] = queue_data['data'][i][len(queue_data['data'][i])-point:]
        self.data_queue.put(self.data)


    '''
    结束之前的准备工作，保存数据图片等
    '''
    def exit_data(self):
        # 准备让绘图进程结束
        self.data_queue.put(False)
        # 结束进程
        self.t.join()
        self.t.close()
        # 关闭log文件
        self.log.close()

        # 保存数据
        with open(data_uri, 'w') as f:
            fstr = json.dumps(self.data)
            f.write(fstr)
            f.close()
        print('数据已经保存到文件'+data_uri)
        print('程序准备结束！！！！')

        # 退出程序
        exit()
        

if __name__ == '__main__':
    D = getdata()
    D.ping_ip()
