import threading
import queue

class tPool:
    def __init__(self, function, maxThreads, threadBlocklen):
        self.work = function
        self.maxThreads = maxThreads
        self.threadBlocklen = threadBlocklen
        self.connectionArgs = None
        self.queueLock = False
        self.qtdThreads = 0
        self.freeThreadQueue = queue.Queue()

        self.noThreadsEvent()

    def createThreadBlock(self, function=None):
        self.qtdThreads += self.threadBlocklen

        if function is None:
            return [threading.Thread(target=self.work) for i in range(self.threadBlocklen)]

        return [threading.Thread(target=function) for i in range(self.threadBlocklen)]

    def setConnection(self, connection):
        self.connectionArgs = connection

    def getThread(self, argList):
        if self.freeThreadQueue.empty():
            if self.qtdThreads < self.maxThreads:
                self.noThreadsEvent()
            else:
                while self.freeThreadQueue.empty():
                    pass

        t = self.freeThreadQueue.get()

        t._args = argList

        return t

    def noThreadsEvent(self):
        for i in self.createThreadBlock():
            self.freeThreadQueue.put(i)

    def createThread(self, function=None):
        if function is None:
            return threading.Thread(target=self.work)

        return threading.Thread(target=function)

    def addQueue(self, thread):
        self.freeThreadQueue.put(thread)

    # TODO : Implementar um controle de concorrencia na fila de threads
