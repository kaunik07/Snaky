import pygame, sys
from config import Config
from snake import Snake
from apple import Apple

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.WINDOW_WIDTH,Config.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.BASICFONT = pygame.font.Font('freesansbold.ttf',18)
        pygame.display.set_caption('Snaky')
        self.apple = Apple()
        self.snake = Snake()

    def drawGrid(self):
        for x in range(0,Config.WINDOW_WIDTH,Config.CELLSIZE):
            pygame.draw.line(self.screen, Config.DARKGREY, (x,0) , (x,Config.WINDOW_HEIGHT))
        
        for y in range(0,Config.WINDOW_HEIGHT,Config.CELLSIZE):
            pygame.draw.line(self.screen, Config.DARKGREY, (0,y) , (Config.WINDOW_WIDTH,y))

    def drawSnake(self):
        for coord in self.snake.snakeCoords:
            x = coord['x'] * Config.CELLSIZE
            y = coord['y'] * Config.CELLSIZE
            snakeSegmentRect = pygame.Rect(x,y,Config.CELLSIZE,Config.CELLSIZE)
            pygame.draw.rect(self.screen,Config.DARKGREEN,snakeSegmentRect)
            snakeInnerSegmentRect = pygame.Rect(x+4,y+4,Config.CELLSIZE - 8,Config.CELLSIZE -8)
            pygame.draw.rect(self.screen,Config.GREEN,snakeInnerSegmentRect)

    def drawApple(self):
        x = self.apple.x * Config.CELLSIZE
        y = self.apple.y * Config.CELLSIZE
        appleRect = pygame.Rect(x,y,Config.CELLSIZE,Config.CELLSIZE)
        pygame.draw.rect(self.screen, Config.RED , appleRect)

    def drawScore(self,score):
        scoreSurf = self.BASICFONT.render('Score: %s' % (score) , True,Config.WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (Config.WINDOW_WIDTH - 120, 10)
        self.screen.blit(scoreSurf,scoreRect)
        


    def draw(self):
        self.screen.fill(Config.BG_COLOR)
        self.drawGrid()
        self.drawScore(len(self.snake.snakeCoords) -3)
        self.drawApple()
        self.drawSnake()
        pygame.display.update()
        self.clock.tick(Config.FPS)


    def checkForKeyPress(self):
        if len(pygame.event.get(pygame.QUIT)) > 0 :
            pygame.quit()

        keyUpEvents = pygame.event.get(pygame.KEYUP)

        if len(keyUpEvents) == 0:
            return None
        
        if keyUpEvents[0].key == pygame.K_ESCAPE:
            pygame.quit()
            quit()
        
        return keyUpEvents[0].key
    
    def handleKeyEvents(self,event):
        if event.key == pygame.K_LEFT and self.snake.direction != self.snake.RIGHT:
            self.snake.direction = self.snake.LEFT
        elif event.key == pygame.K_RIGHT and self.snake.direction != self.snake.LEFT:
            self.snake.direction = self.snake.RIGHT
        elif event.key == pygame.K_UP and self.snake.direction != self.snake.DOWN:
            self.snake.direction = self.snake.UP
        elif event.key == pygame.K_DOWN and self.snake.direction != self.snake.UP:
            self.snake.direction = self.snake.DOWN
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()

    def resetGame(self):
        del self.snake
        del self.apple
        self.snake = Snake()
        self.apple = Apple()
        return True

    def isGameOver(self):
        if(self.snake.snakeCoords[self.snake.HEAD]['x'] == -1 or self.snake.snakeCoords[self.snake.HEAD]['x'] == Config.CELLWIDTH ):
            return self.resetGame()
        if(self.snake.snakeCoords[self.snake.HEAD]['y'] == -1 or self.snake.snakeCoords[self.snake.HEAD]['y'] == Config.CELLHIGHT ):
            return self.resetGame()

        for snakeBody in self.snake.snakeCoords[1:]:
            if snakeBody['x'] == self.snake.snakeCoords[self.snake.HEAD]['x'] and snakeBody['y'] ==  self.snake.snakeCoords[self.snake.HEAD]['y']:
                return self.resetGame()

    def drawPressKeyMsg(self):
        pressKeySurf = self.BASICFONT.render('Press a key to play', True, Config.DARKGREY)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (Config.WINDOW_WIDTH - 200, Config.WINDOW_HEIGHT - 50)
        pressKeyExit = self.BASICFONT.render('Press ESC to exit', True, Config.DARKGREY)
        pressKeyExitRect = pressKeySurf.get_rect()
        pressKeyExitRect.topleft = (Config.WINDOW_WIDTH - 200, Config.WINDOW_HEIGHT - 20)
        self.screen.blit(pressKeySurf,pressKeyRect)
        self.screen.blit(pressKeyExit, pressKeyExitRect)

    def displayGameOver(self):
        gameOverFont = pygame.font.Font('freesansbold.ttf',150)
        gameSurf = gameOverFont.render('Game',True,Config.WHITE)
        overSurf = gameOverFont.render('Over',True,Config.WHITE)
        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()
        gameRect.midtop = (Config.WINDOW_WIDTH/2,10)
        overRect.midtop = (Config.WINDOW_WIDTH/2 , gameRect.height +10 + 25)
        self.screen.blit(gameSurf,gameRect)
        self.screen.blit(overSurf,overRect)

        self.drawPressKeyMsg()
        pygame.display.update()
        pygame.time.wait(500)

        self.checkForKeyPress() #clear out any key press in the event queue

        while True:
            if self.checkForKeyPress():
                pygame.event.get()
                return

    def run(self):
        # self.showStartScreen()

        while True:
            self.gameloop()
            self.displayGameOver()

    def gameloop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyEvents(event)

            self.snake.update(self.apple)
            self.draw()
            if self.isGameOver():
                break
