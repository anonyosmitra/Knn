import sys
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
trainingFile=None
testFile=None
trainingData=[]
testData=[]
matrixSize=None
k=0
guessTab=[]

accuracy={}
class neighbour:
    def __init__(self,cls,dist):
        self.cls=cls
        self.dist=dist
class item:
    def __init__(self,row):
        global matrixSize
        row=row.split(",")
        self.cls=row[len(row)-1]
        self.val=row[:len(row)-1]
        self.val=list(np.float_(self.val))
        self.neighbours=[]
        self.isSorted=True

        if matrixSize is None:
            matrixSize=len(self.val)
        elif matrixSize!=len(self.val):
            raise Exception("Matrix size not consistent!")
    def Is(self,cls):
        return self.cls==cls

    def sortNeighbours(self):
        self.neighbours.sort(key=lambda x: x.dist)
        self.isSorted = True
    def guessClass(self,k):
        if not self.isSorted:
            self.sortNeighbours()
        l=[i.cls for i in self.neighbours[:k]]
        return max(set(l), key=l.count)
    def __str__(self):
        return ",".join([str(i) for i in self.val]+[self.cls])
    def distSqr(self,it):
        sum=0
        for i in range(len(self.val)):
            sum+=(self.val[i]-it.val[i])**2
        self.neighbours.append(neighbour(it.cls,sum))
        self.isSorted = False
        return sum
def readTo(file,l):
    with open(file) as file:
        for line in file:
            l.append(item(line.rstrip()))
def calculateDist():
    for i in trainingData:
        for j in testData:
            j.distSqr(i)

def checkAccuracy():
    for i in testData:
        a=[str(i)]
        for j in range(1,k+1):
            success=i.Is(i.guessClass(j))
            a.append(success)
            if success:
                if j in accuracy:
                    accuracy[j]+=1
                else:
                    accuracy[j] = 1
        guessTab.append(a)

def printResults():
    ks=list(range(1,k+1))
    ks.insert(0,"Item")
    print(tabulate(guessTab,ks))
    print("\n\n")
    print(tabulate([[i,accuracy[i]*100/len(testData)] for i in accuracy],headers=["k","Accuracy%"]))
    v=[i*100/len(testData) for i in accuracy.values()]

    plt.plot(accuracy.keys(),v)
    plt.ylim(ymin=0)
    plt.show()

def UIMode():
    print("Entering UI Mode\n\tEnter values with commas(,)\n\tEnter \"quit\" to exit")
    a=input("Waiting for input: ")
    while(a!="quit"):
        e=item(a+",unknown")
        for i in testData:
            e.distSqr(i)
        print("Class: "+e.guessClass(k))
        a = input("Waiting for input: ")
    print("bye")

if __name__ == "__main__":
    trainingFile=sys.argv[1]
    testFile=sys.argv[2]
    k=int(sys.argv[3])
    readTo(trainingFile,trainingData)
    readTo(testFile,testData)
    print(testData[0])
    calculateDist()
    checkAccuracy()
    printResults()
    UIMode()
