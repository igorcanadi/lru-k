#!/usr/bin/python3

import random

class pageInfo:
    def __init__(self, k):
        self.hist = [0] * k
        self.last = 0
        self.CRP = 0;
        
    def getHist(self):
        return self.hist
    
    def getLast(self):
        return self.last
    
    def getCRP(self):
        return self.CRP
    
    def updateCRP(self, value):
        self.CRP = value
    
    def updateHist(self, value, pos):
        self.hist[pos] = value
    
    def updateLast(self, value):
        self.last = value

class LRUKRP:
    #initialize the object
    #bufferSize: number of pages in memory
    #k: LRU-K algorithm parameter
    #CRP:correlated reference period
    #RIP:retained information period
    def __init__(self, bufferSize, k, CRP, RIP):
        self.buffer = [0] * bufferSize
        self.pageinfo = {}
        self.k = k
        self.CRP = CRP
        self.RIP = RIP
        self.t = 0
        self.hits = 0
        self.requests = 0

    def clearStats(self):
        self.hits = 0
        self.requests = 0
        
    def requestPage(self, p):
        self.t += 1
        self.requests += 1
        page = str(p)
        #if this disk page is referenced for the first time, we create a history for the disk page
        if page not in self.pageinfo:
            self.pageinfo[page] = pageInfo(self.k)
            
        if p in self.buffer:
            self.hits += 1
            if self.pageinfo[page].getLast() != 0 and self.t - self.pageinfo[page].getLast() > self.CRP:
                if self.pageinfo[page].getHist()[0] == 0:
                    self.pageinfo[page].updateHist(self.t, 0)
                else:
                    self.pageinfo[page].updateCRP(self.pageinfo[page].getLast() - self.pageinfo[page].getHist()[0])
                    pageObj = self.pageinfo[page]
                    for i in range(1, self.k):
                        pageObj.updateHist(pageObj.getHist()[self.k-i-1]+ pageObj.getCRP(), self.k-i)
                    pageObj.updateHist(self.t, 0)
                    self.pageinfo[page].updateLast(self.t)
             
        #p is not in buffer and buffer is full       
        else:
            #if there is space in buffer, put it into free space, else select a victim
            if 0 in self.buffer:
                self.buffer[self.buffer.index(0)] = p
                self.requests -= 1
            else:
                min = self.t
                victim = self.buffer[0]
                for q in self.buffer:
                    page = self.pageinfo[str(q)]
                    if self.t - page.getLast() > self.CRP and page.getHist()[self.k-1] < min:
                        victim = q
                        min = page.getHist()[self.k-1]
                self.buffer[self.buffer.index(victim)] = p
            #now fetch p into the buffer frame previously held by victim
            
            pageObj = self.pageinfo[str(p)]
            if pageObj.getHist()[0] == 0:
                pass
            else:
                for i in range(1, self.k):
                        pageObj.updateHist(pageObj.getHist()[self.k-i-1], self.k-i)
            
            pageObj.updateHist(self.t, 0)
            pageObj.updateLast(self.t)

    def getHitRatio(self):
        return float(self.hits) / self.requests

def main():
    #generate a reference string
    R = []
    
    random.seed(20)
    
    for i in range(100000):
        m = random.randint(1,100)
        if m < 90:
            R.append(random.randint(1,100))
        else:
            R.append(random.randint(101, 1000))

    bufManager = LRUKRP(50, 2, 30, 10000)
    
    #print(bufManager.buffer)
    for p in R:
        bufManager.requestPage(p)
        #bufManager.buffer.sort()
    #print(bufManager.buffer)
    print(bufManager.buffer)
    print("number of hits: ", bufManager.hits)
    print("number of requests: ", bufManager.requests)
    print("hit ratio: ", bufManager.hits/bufManager.requests)
    




if __name__ == "__main__":main()
