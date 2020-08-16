import random
from config import Config

class Apple():
    def __init__(self):
        self.setNewLocation()
     
    #apple position
    def setNewLocation(self):
        self.x = random.randint(0,Config.CELLWIDTH-1)
        self.y = random.randint(0,Config.CELLHIGHT-1)
      