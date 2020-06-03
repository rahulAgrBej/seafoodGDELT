import threading

COUNTER_LOCK = threading.Lock()

COUNTER = 50

def plusCount(num):
    COUNTER_LOCK.acquire()
    global COUNTER
    COUNTER += num
    print(f'INCREASE OF {num} DONE: {COUNTER}')
    COUNTER_LOCK.release()
    
    return None

def multiplyCount(num):
    COUNTER_LOCK.acquire()
    global COUNTER
    COUNTER *= num
    print(f'Multiply OF {num} DONE {COUNTER}')
    COUNTER_LOCK.release()
    return None

t0 = threading.Thread(target=plusCount, args=(3,))
t1 = threading.Thread(target=multiplyCount, args=(10,))

t0.start()
t1.start()

t0.join()
t1.join()
