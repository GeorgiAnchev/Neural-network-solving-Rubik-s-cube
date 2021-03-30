from collections import Counter
import itertools
import matplotlib.pyplot as plt
from Rubik2.Rubik2 import *

def balanceData(data):
    maxMoves = 14 #god's number
    length = len(data)
    
    splitData = [[] for i in range(maxMoves + 1)]
    
    for key in data:
        (move, steps) = data[key]
        splitData[steps].append((key, move))

    #print([ len(moveGroup) for moveGroup in splitData])
    
    averageLength = len(splitData[11])//2 #close enough

    for index in range(1, 14):
        length = len(splitData[index])
        if(length > averageLength): continue
            
        multiplier = averageLength // length
        remainder = averageLength % length
        
        splitData[index] = list(itertools.chain.from_iterable(itertools.repeat(x, multiplier) for x in splitData[index]))
        splitData[index] += splitData[index][ : remainder]
    
    finalArray = []
    
    for steps in range(1, len(splitData)):
        group = splitData[steps]
        finalArray += [(state, move, steps) for (state, move)  in group]
    
    return finalArray
    
def transformWithoutBalansing(data):
    
    return [ (state, move, steps) for (state, (move, steps)) in data.items()]
    
def showDistribution(data):
    onlySteps = [ steps for (_, steps) in list(data.values())]
    #print(onlySteps)
    plt.figure(figsize=(12, 5))
    n, bins, patches = plt.hist(x = onlySteps, bins='auto', color='#0504aa', width=0.8)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Distance from solved')
    plt.ylabel('Examples')
    plt.title('Dataset distribution')
    plt.show()
    
    counts = Counter(onlySteps)
    print(counts)
    
def showDistributionList(data):
    onlySteps = [ steps for (_, _, steps) in data]
    #print(onlySteps)
    plt.figure(figsize=(12, 5))
    n, bins, patches = plt.hist(x = onlySteps, bins='auto', color='#0504aa', width=0.8)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Distance from solved')
    plt.ylabel('Examples')
    plt.title('Dataset distribution')
    plt.show()
    
    counts = Counter(onlySteps)
    print(counts)
    
def transformDataIntoExamples(data):
    states = [state for (state, _, _) in data]
    
    moveLabels = np.asarray( [move for (_, move, _) in data] )
    cubesAsVectors = np.asarray( [convertStringToVector(state) for state in states] )
    
    return moveLabels, cubesAsVectors, states
    