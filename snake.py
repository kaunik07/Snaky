from config import Config
import random

class Snake():
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    HEAD = 0

    def __init__(self):
        self.x = random.randint(5,Config.CELLWIDTH-6)
        self.y = random.randint(5,Config.CELLHIGHT-6)
        self.direction = self.RIGHT

        #snake representation : length of 3
        self.snakeCoords  = [{'x':self.x, 'y':self.y},
                            {'x':self.x-1, 'y':self.y-1},
                            {'x':self.x-2, 'y':self.y-2}]

    def update(self,apple):
    #check if snake has eaten an apple
        if self.snakeCoords[self.HEAD]['x'] == apple.x and self.snakeCoords[self.HEAD]['y'] == apple.y:
            apple.setNewLocation()
        else:
            del self.snakeCoords[-1] #remove snake's tail segment

        #move the snake by adding a segment in the drirection it is moveing    
        if self.direction == self.UP:
            newHead = {'x':self.snakeCoords[self.HEAD]['x'],'y':self.snakeCoords[self.HEAD]['y'] - 1}
        if self.direction == self.DOWN:
            newHead = {'x':self.snakeCoords[self.HEAD]['x'],'y':self.snakeCoords[self.HEAD]['y'] + 1}
        if self.direction == self.LEFT:
            newHead = {'x':self.snakeCoords[self.HEAD]['x'] - 1,'y':self.snakeCoords[self.HEAD]['y']}
        if self.direction == self.RIGHT:
            newHead = {'x':self.snakeCoords[self.HEAD]['x'] + 1,'y':self.snakeCoords[self.HEAD]['y']}

        self.snakeCoords.insert(0,newHead)
