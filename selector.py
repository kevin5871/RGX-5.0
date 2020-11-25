from collections import deque

class selector() :
    def __init__(self, menu) :
        self.queue = deque([])
        for l in menu :
            self.queue.append(l)
        self.ptr = 0

    def right(self) :
        if(len(self.queue)-1 > self.ptr) :
            self.ptr = self.ptr + 1
        else :
            self.ptr = 0
    def left(self) :
        if(self.ptr > -1) :
            self.ptr = self.ptr - 1
        else :
            self.ptr = len(self.queue) - 1
            
    def rptr(self) :
        return self.ptr

    def print(self) :
        #print(self.ptr)
        return str(self.queue[self.ptr])