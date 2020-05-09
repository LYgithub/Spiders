#
# -*- coding: utf-8 -*-
# Thread.py 
# Created by MacBook Air PyCharm on 2020/3/29 2:34 下午 
# Copyright © 2020 LiYang. All rights reserved.
#
import threading
import time


class myThread(threading.Thread):
    ignal = True

    def __init__(self, name):
        self.threadID = name
        super().__init__()

    def run(self):
        while myThread.ignal is False:
            pass
        myThread.ignal = False
        for i in range(1, 10):
            print(self.threadID, i)
        myThread.ignal = True


if __name__ == '__main__':
    thrad1 = myThread('1')
    thrad2 = myThread('2')
    thrad1.start()
    thrad2.start()

    thrad2.join()
    thrad1.join()
