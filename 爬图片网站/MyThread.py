
import threading
import down

#单个下载线程类
class CDownThread(threading.Thread):
    def __init__(self,sourceImg,localPath):
        threading.Thread.__init__(self)
        self.sourceImg=sourceImg
        self.localPath=localPath
    def run(self):
        down.downImg(self.sourceImg,self.localPath)


class CMultiDownThread:
    nMaxThreads=5
    threads = []
    def __init__(self,nMax=10):
        self.nMaxThreads = nMax
    #如果线程数少于规定的总线程数，则直接添加
    #否则，删除不活动的线程后，再添加
    def AddThread(self,thread):
        if self.threads.__len__()<self.nMaxThreads:
            thread.start()
            self.threads.append(thread)
            return True
        else:

            for th in self.threads:
                if not th.isAlive():   #线程已经执行完毕
                    self.threads.remove(th)

            if self.threads.__len__()<self.nMaxThreads:
                thread.start()
                self.threads.append(thread)
                return True
            return False

    def join(self):#等待所有线程执行完毕
        for t in self.threads:
            t.join()