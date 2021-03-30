import numpy as np

class Rubik2:
    oneHotVectors = np.eye(6, dtype="float32") # constant
    
    def __init__(self, initial_state = ""):
        
        if not initial_state:
            self.top     = np.full((2, 2), 'w')
            self.right   = np.full((2, 2), 'r')
            self.bottom  = np.full((2, 2), 'y')
            self.left    = np.full((2, 2), 'o')
            self.back    = np.full((2, 2), 'b')
            self.front   = np.full((2, 2), 'g')
        else:
            sides = [ initial_state[i:i+4] for i in range(0, len(initial_state), 4) ]
            sides = np.asarray(sides)

            self.top     = getStringAsSide(sides[0])
            self.right   = getStringAsSide(sides[1])
            self.bottom  = getStringAsSide(sides[2])
            self.left    = getStringAsSide(sides[3])
            self.back    = getStringAsSide(sides[4])
            self.front   = getStringAsSide(sides[5])
        
    def show(self):
        sp = np.full((2,1), ' ')
        printside(self.back)
        printside(np.concatenate((self.top, sp, self.right, sp, self.bottom, sp, self.left), axis=1))
        printside(self.front)
        print()
        
    def rotateLeft(self):
        self.left = np.rot90(self.left, 3)
        
        temp = self.top.copy()[:, 0]
        self.top[:, 0] = self.back[:, 0]
        self.back[:, 0] = np.flip(self.bottom[:, 1])
        self.bottom[:, 1] = np.flip(self.front[:,0])
        self.front[:,0] = temp
        
    def counterRotateLeft(self):
        self.counterRotate(self.rotateLeft)
        
    def rotateBottom(self):
        self.bottom = np.rot90(self.bottom, 3)
        
        temp = self.front.copy()[1]
        self.front[1] = self.left[:, 0]
        self.left[:, 0] = np.flip(self.back[0])
        self.back[0] = self.right[:, 1]
        self.right[:, 1] = np.flip(temp)
        
    def counterRotateBottom(self):
        self.counterRotate(self.rotateBottom)
            
    def rotateBack(self):
        self.back = np.rot90(self.back, 3)
        
        temp = self.top.copy()[0]
        self.top[0] = self.right[0]
        self.right[0] = self.bottom[0]
        self.bottom[0] = self.left[0]
        self.left[0] = temp
        
    def counterRotateBack(self):
        self.counterRotate(self.rotateBack)
        
    def counterRotate(self, rotation):
        rotation()
        rotation()
        rotation()
        
    def getStateCompact(self):
        return getSideAsString(self.top) + \
            getSideAsString(self.right) + \
            getSideAsString(self.bottom) + \
            getSideAsString(self.left) + \
            getSideAsString(self.back) + \
            getSideAsString(self.front)
    
    def performMove(self, move):
        action = self.moves[move]
        action(self)
        return self
    
    moves = [rotateBottom, counterRotateBottom, 
         rotateBack, counterRotateBack, 
         rotateLeft, counterRotateLeft]
        
def printside(side):
    [print(row.astype('|S1').tostring().decode('utf-8')) for row in side]

def getSideAsString(side):
    vector = side.reshape(-1)
    return vector.astype('|S1').tostring().decode('utf-8')

def getStringAsSide(string):
    arr = np.array(list(string))   
    return arr.reshape(2,2)

def convertStringToVector(state):
    short_state = removeFixedPiece(state)
    vectors = list(map(charToVector, short_state))
    return np.concatenate(vectors)

def convertVectorToString(vec):
    vec2 = vec.reshape(-1, 6)
    string = list(map(vectorТоChar, vec2))
    string = "".join(string)
    long_state = addFixedPiece(string)
    return long_state

def charToVector(character):    
    if(character == 'w'): return Rubik2.oneHotVectors[0]
    if(character == 'r'): return Rubik2.oneHotVectors[1]
    if(character == 'y'): return Rubik2.oneHotVectors[2]
    if(character == 'o'): return Rubik2.oneHotVectors[3]
    if(character == 'b'): return Rubik2.oneHotVectors[4]
    if(character == 'g'): return Rubik2.oneHotVectors[5]

def vectorТоChar(vector):    
    if(vector[0] == 1.): return 'w'
    if(vector[1] == 1.): return 'r'
    if(vector[2] == 1.): return 'y'
    if(vector[3] == 1.): return 'o'
    if(vector[4] == 1.): return 'b'
    if(vector[5] == 1.): return 'g'
    
def removeFixedPiece(s):
    g = 21
    r = 6
    w = 3
    
    s1 =  s[:g] + s[g+1:]
    s2 =  s1[:r] + s1[r+1:]
    s3 =  s2[:w] + s2[w+1:]
    
    return s3
    
def addFixedPiece(s):
    g = 21
    r = 6
    w = 3
    
    s1 =  s[:w] + 'w' + s[w:]
    s2 =  s1[:r] + 'r' + s1[r:]
    s3 =  s2[:g] + 'g' + s2[g:]
    
    return s3
    
def performCubeAntiMovement(state, move):
    cube = Rubik2(state)
    cube.performMove(reverseAction(move))
    as_string = cube.getStateCompact()
    as_vector = convertStringToVector(as_string)
    return (as_vector, as_string)
        
def reverseAction(action):
    if(action % 2 == 0): return action + 1
    return action - 1 
    