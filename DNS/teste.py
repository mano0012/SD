import threadPool as tp
import time

def teste(thread = None, x = None):
    print(thread)

    time.sleep(2)

    if thread is not None:
        threads.addQueue(threads.createThread())

threads = tp.tPool(teste)

for i in range(1000):
    print("TCHAMA")
    threads.start(i)
