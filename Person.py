from random import randint
import time

class MyPerson:
    tracks = []
    def __init__(self, i, xi, yi, max_age):
        self.i = i
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.done = False
        self.state = '0'
        self.age = 0
        self.max_age = max_age
        self.dir = None
    def getRGB(self):
        return (self.R,self.G,self.B)
    def getTracks(self):
        return self.tracks
    def getId(self):
        return self.i
    def getState(self):
        return self.state
    def getDir(self):
        return self.dir
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def updateCoords(self, xn, yn):
        self.age = 0
        self.tracks.append([self.x,self.y])
        self.x = xn
        self.y = yn
    def setDone(self):
        self.done = True
    def timedOut(self):
        return self.done
    def going_UP(self,mid_start,mid_end):#track mid_end = line_up리스트에 마지막으로 들어간 값이 위에서 2번째선보다 작고 그 전에 들어간 값이 크거나 같을 경우 선을 넘는것으로 판단한다.
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][1] < mid_end and self.tracks[-2][1] >= mid_end: #위의 선을 넘는것으로 판단하고 state=1, dir에 up을 넣음.
                    state = '1'
                    self.dir = 'up'
                    return True
            else:
                return False
        else:
            return False
    def going_DOWN(self,mid_start,mid_end): #mid_start= line_down
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][1] > mid_start and self.tracks[-2][1] <= mid_start: #cruzo la linea
                    state = '1'
                    self.dir = 'down'
                    return True
            else:
                return False
        else:
            return False

    def going_LEFT(self,line_left,line_right):#mid_start 에는 line_left
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][0] > line_left and self.tracks[-2][0] <= line_left: #위의 선을 넘는것으로 판단하고 state=1, dir에 up을 넣음.
                    state = '1'
                    self.dir = 'left'
                    return True
            else:
                return False
        else:
            return False

    def going_RIGHT(self,line_left,line_right):#mid_end 에는 line_right
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][0] < line_right and self.tracks[-2][0] >= line_right: #위의 선을 넘는것으로 판단하고 state=1, dir에 up을 넣음.
                    state = '1'
                    self.dir = 'right'
                    return True
            else:
                return False
        else:
            return False
    def age_one(self):
        self.age += 1
        if self.age > self.max_age:
            self.done = True
        return True
# class MultiPerson:
#     def __init__(self, persons, xi, yi):
#         self.persons = persons
#         self.x = xi
#         self.y = yi
#         self.tracks = []
#         self.R = randint(0,255)
#         self.G = randint(0,255)
#         self.B = randint(0,255)
#         self.done = False
#
