#!/usr/bin/env python

# Import a library of functions called 'pygame'
import pygame, sys
import random
import math
import time
from pygame import gfxdraw
from pygame.locals import *

###################################
try:
    import pycogworks as cw
    print ('success')
    E_Support = True
except ImportError:
    E_Support = False
logging_enabled = True

class Logger ():
    tm = time.localtime()
    path_fn = 'Data/PT_%02i%02i%4i_%02i%02i%02i' % (tm.tm_mon, tm.tm_mday, tm.tm_year,
                                             tm.tm_hour, tm.tm_min, tm.tm_sec)
    def __init__(self):
        self.log_file = file(self.path_fn + ".txt", 'w')
        return
    
    def LogInfo (self, *args):               
        if logging_enabled:
            ln = map(lambda x: str(x) + '\t', args)                               
            self.log_file.write(repr(time.time()) + '\t')
            self.log_file.writelines(ln)
            self.log_file.write('\n')
        else:
            print (time.time(), args)
        return
    def info (self, *args):
        self.LogInfo (*args)
        return
            
    def CloseLog(self):
        if logging_enabled:                                
            self.log_file.close()
            
        return
class Subject ():
    def __init__(self, fn):
        if E_Support:
            self.subj_info = cw.getSubjectInfo()
            cw.writeHistoryFile(fn, self.subj_info)
            logging.LogInfo('subject', 'init', self.subj_info)
        return
    def dispStartMsg (self):
        msg.dispSubjectMsg(['Start Experiment'])
        return
logging = Logger()
subject = Subject(logging.path_fn)
#####################################
        
class Entry:
    def showIntro(self):
        self.blueColor = pygame.Color(0, 0, 255)
        self.fontObj = pygame.font.Font('freesansbold.ttf', 32)
        self.msg = 'Press C to continue, X to exit.'
        self.msgSurfaceObj = self.fontObj.render(self.msg, False, self.blueColor)
        self.msgRectObj = self.msgSurfaceObj.get_rect()
        self.msgRectObj.center = (screenWidth // 2, screenHeight // 2)
        screen.blit(self.msgSurfaceObj, self.msgRectObj)
        pygame.display.flip()
        screen.fill(pygame.Color(0, 0, 0))
        processing = True
        while processing:
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_c:
                        processing = False
                        break
                    if event.key == K_x:
                        pygame.event.post(pygame.event.Event(QUIT))
        
        print('done')

class CheckerBoard:
     def showBoard(self, cellsPerHeight, rate, duration):
        # White on black
        self.backColor = pygame.Color(0, 0, 0)
        self.foreColor = pygame.Color(255, 255, 255)
        self.dotColor = pygame.Color(255, 0, 0)
        # Black on white
        self.backColor = pygame.Color(255, 255, 255)
        self.foreColor = pygame.Color(0, 0, 0)
        self.dotColor = pygame.Color(255, 0, 0)
        surfaceBackground = screen.copy()
        surfaceBackground.fill(self.backColor)
        pygame.draw.circle(surfaceBackground, self.dotColor, screenCenter, 10) 
        surfaceCheckerboard = screen.copy()
        surfaceCheckerboard.fill(self.backColor)
        
        self.cellSize = screenHeight // cellsPerHeight
        self.widthHeight = (self.cellSize, self.cellSize)
        self.numRows = screenHeight // self.cellSize
        self.numCols = screenWidth // self.cellSize
        print ('Checkerboard rows, cols:', self.numRows, ',', self.numCols)
        offset = (screenWidth % self.cellSize // 2, screenHeight % self.cellSize // 2)
        for self.rowIndex in range (self.numRows):
            
            if self.rowIndex % 2 == 0:
                 self.draw = True
            else:
                 self.draw = False
               
            for self.colIndex in range (self.numCols):
                print 'rowIndex, colIndex:', self.rowIndex, ',', self.colIndex
                if self.draw == True:
                    self.rect = pygame.Rect(self.colIndex * self.cellSize + offset[0], self.rowIndex * self.cellSize + offset[1], self.cellSize, self.cellSize)
                    print 'rect:', self.rect, self.draw
                    self.draw = False
                else:
                    self.draw = True
                surfaceCheckerboard.fill(self.foreColor, self.rect)
        # Using the offset above - 4 rectngles can be drawn as a border to clean up the edges
        # draw the dot
        pygame.draw.circle(surfaceCheckerboard, self.dotColor, screenCenter, 10) 
        fpsClock = pygame.time.Clock()
        # rate = checkerboards / sec
        rate = 5
        # fps = 2 * rate - flash on / off
        fps = 9 * 2
        # duration of flashing total
        duration = 10
        # number of frames over time
        frames = fps * duration
        
        for self.index in range(frames):
            if self.index % 2 == 0:
                screen.blit(surfaceCheckerboard, (0, 0))
                pygame.display.flip()
            else:
                screen.blit(surfaceBackground, (0, 0))
                pygame.display.flip()
            fpsClock.tick(fps)
            
class ReadyDisplay:
    def prompt(self):
        self.blueColor = pygame.Color(0, 0, 255)
        self.fontObj = pygame.font.Font('freesansbold.ttf', 32)
        self.msg = 'Ready for the test? Press C to continue, X to exit.'
        self.msgSurfaceObj = self.fontObj.render(self.msg, False, self.blueColor)
        self.msgRectObj = self.msgSurfaceObj.get_rect()
        self.msgRectObj.center = (screenWidth // 2, screenHeight // 2)
        screen.fill(pygame.Color(0, 0, 0))
        screen.blit(self.msgSurfaceObj, self.msgRectObj)
        pygame.display.flip()
        processing = True
        while processing:
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_c:
                        processing = False
                        break
                    if event.key == K_x:
                        pygame.event.post(pygame.event.Event(QUIT))
        
class DotDisplay:
    def movePt(self, original, dist, angleDeg):
        self.angle = math.radians(angleDeg)
        self.deltaX = math.cos(self.angle) * dist
        self.deltaY = math.sin(self.angle) * dist
        moved = [original[0] + self.deltaX, original[1] + self.deltaY]
        print  dist, angleDeg, self.angle, original, moved
        return moved
    def drawDisplay(self, angleDeg, distance):
        
        desiredFps = 60
        black = [ 0, 0, 0]
        white = [255, 255, 255]
        
        fpsClock = pygame.time.Clock()
        self.apatureRect = Rect(int(screenCenter[0]) - self.apatureRadius, int(screenCenter[1]) - self.apatureRadius, self.apatureSize, self.apatureSize)
        # 10 deg / sec  8 deg display over 500 ms
        distanceToTravel = float(self.apatureSize) * 5.0 / 8.0
        numberOfFrames = int(float(desiredFps) / 2.0)
        distancePerFrame = distanceToTravel / numberOfFrames
        print ("distancePerFrame: ", distancePerFrame)
       
        distance = 0.0
        counter = 1.0
        sumMs = 0.0
        
        for frameIndex in range(numberOfFrames):
            
            screen.blit(self.surfaceBackground, (0, 0))
            # Process each star in the list
            for i in range(len(self.star_list)):
                self.moved = self.movePt(self.star_list[i], distance, angleDeg)
                self.x = int(self.moved[0])
                self.y = int(self.moved[1])
                #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  #
                if self.apatureRect.collidepoint(self.x, self.y):
                    pygame.draw.circle(screen, black, [self.x, self.y], 1)
                    pygame.gfxdraw.filled_circle(screen, math.trunc(self.moved[0]), math.trunc(self.moved[1]), 2, black)
                 
            pygame.display.flip()
            distance += distancePerFrame
            if frameIndex == 0:
                fpsClock.tick(desiredFps)
            elif frameIndex > 0:
                counter += 1.0
                sumMs += fpsClock.tick(desiredFps)
        perFrame = sumMs / counter
        print ('perframe: ', perFrame, 'fps', (1000 / perFrame))
        return distance
        
    def getAngle(self, angle):
        if random.randint(0, 1) == 0:
            return angle
        else:
            if random.randint(0, 1) == 0:
                return angle + 2
            else:
                return angle - 2
            
    # determine if a point is inside a given polygon or not
    # Polygon is a list of (x, y) pairs.
    def point_inside_polygon(self, x, y, poly):
        n = len(poly)
        inside = False
        p1x, p1y = poly[0]
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside
    def rotate2d(self, degrees, point, origin):
        
        # A rotation function that rotates a point around a point
        # to rotate around the origin use [0,0]
        
        x = point[0] - origin[0]
        yorz = point[1] - origin[1]
        newx = (x * math.cos(math.radians(degrees))) - (yorz * math.sin(math.radians(degrees)))
        newyorz = (x * math.sin(math.radians(degrees))) + (yorz * math.cos(math.radians(degrees)))
        newx += origin[0]
        newyorz += origin[1] 
        return newx, newyorz
        
    def display(self, apaturePercent, numTrials):
        
        # Black on white
        self.backColor = pygame.Color(0, 0, 0)
        self.backColor = pygame.Color(255, 255, 255)
        self.foreColor = pygame.Color(255, 255, 255)
        self.apatureColor = pygame.Color(255, 255, 255)
        # Create an empty array
        self.star_list = []
        self.apatureSize = int(round(screenHeight * apaturePercent))
        self.apatureRadius = int(round(screenHeight * apaturePercent / 2))
        baseAngle = random.randrange(0, 360, 45)
        ulx = int(screenCenter[0]) - (5.0 * self.apatureRadius)
        uly = int(screenCenter[1]) - self.apatureRadius
        urx = int(screenCenter[0]) + (1.1 * self.apatureRadius)
        ury = int(screenCenter[1]) - self.apatureRadius
        lrx = int(screenCenter[0]) + (1.1 * self.apatureRadius)
        lry = int(screenCenter[1]) + self.apatureRadius
        llx = int(screenCenter[0]) - (5.0 * self.apatureRadius)
        lly = int(screenCenter[1]) + self.apatureRadius
        p0x, p0y = self.rotate2d(baseAngle, (ulx, uly), (screenCenter[0], screenCenter[1]))
    
        p1x, p1y = self.rotate2d(baseAngle, (urx, ury), (screenCenter[0], screenCenter[1]))
     
        p2x, p2y = self.rotate2d(baseAngle, (lrx, lry), (screenCenter[0], screenCenter[1]))
       
        p3x, p3y = self.rotate2d(baseAngle, (llx, lly), (screenCenter[0], screenCenter[1]))
        # Rotate rect
        poly = []
        poly.append((p0x, p0y))
        poly.append((p1x, p1y))
        poly.append((p2x, p2y))
        poly.append((p3x, p3y))
        
        timeStart = time.clock()
        
        for i in range(12500):
            x = (random.random() * (self.apatureRadius * 10)) + (screenCenter[0] - (self.apatureRadius * 5))
            y = (random.random() * (self.apatureRadius * 10)) + (screenCenter[1] - (self.apatureRadius * 5))
            # if point in rectangle
            if self.point_inside_polygon(x, y, poly):
                self.star_list.append([x, y])
        timeFinish = time.clock()
        finalTime = timeFinish - timeStart
        print (finalTime)
        
        self.surfaceBackground = screen.copy()
        self.surfaceBackground.fill(self.backColor)
        pygame.draw.circle(self.surfaceBackground, self.apatureColor, screenCenter, self.apatureRadius)
 
        for trialIndex in range(numTrials):
            flag = ''
            typeOfAngle = ''
            if baseAngle == 0 or baseAngle == 90 or baseAngle == 180 or baseAngle == 270:
                typeOfAngle = 'CARDINAL'
            else:
                typeOfAngle = 'OBLIQUE'
            angle1 = self.getAngle(baseAngle)
            logging.LogInfo('Trial      ', 'Stage 1', 'Dots', 'Angle:', angle1)
            dist = self.drawDisplay(angle1, 0.0)
            maskDelay = 300
            screen.blit(self.surfaceBackground, (0, 0))
            logging.LogInfo('Trial      ', 'Stage 2', 'Mask', 'Mask Delay:', maskDelay)
            pygame.display.flip()
            pygame.time.delay(maskDelay)
            angle2 = self.getAngle(baseAngle)
            # Change "dist" to 'reset' dot origin, use 'dist' to use continuous dot flow
            logging.LogInfo('Trial      ', 'Stage 3', 'Dots', 'Angle:', angle2)
            self.drawDisplay(angle2, dist)
            if angle1 == angle2:
                flag = 'SAME(A)'
            else:
                flag = 'DIFFERENT(L)'
            logging.LogInfo('DisplayWindow', 'DataEntry')
            logging.LogInfo('Info       ', 'TrialInfo', 'Correct Response:', flag, 'Base Angle:', baseAngle, 'Type of Angle:', typeOfAngle)
            dataEntryDisplay = DataEntryDisplay()
            dataEntryDisplay.display((int(angle1) == int(angle2)))
class DataEntryDisplay:
    def display(self, isIdentical):
        self.blueColor = pygame.Color(0, 0, 255)
        self.fontObj = pygame.font.Font('freesansbold.ttf', 32)
        self.msg = 'Press A for same, L for different.'
        self.msgSurfaceObj = self.fontObj.render(self.msg, False, self.blueColor)
        self.msgRectObj = self.msgSurfaceObj.get_rect()
        self.msgRectObj.center = (screenWidth // 2, screenHeight // 2)
        screen.fill(pygame.Color(0, 0, 0))
        screen.blit(self.msgSurfaceObj, self.msgRectObj)
        pygame.display.flip()
        processing = True
        while processing:
            global numberCorrect
            global numberIncorrect
            
            for event in pygame.event.get():
                logging.LogInfo('Event', event.type)
                if event.type == KEYDOWN:
                    if event.key == K_a:
                        processing = False
                        if (isIdentical):
                            numberCorrect += 1
                            print ('Correct')
                            print ("Number Correct:", numberCorrect)
                            print ("Number Incorrect:", numberIncorrect)
                            logging.LogInfo('Info        ', 'UserInput', 'KeyDown', str(unichr(event.key)).upper(), 'CORRECT', numberCorrect)
                        else:
                            numberIncorrect += 1
                            print ('Incorrect')
                            print ("Number Correct:", numberCorrect)
                            print ("Number Incorrect:", numberIncorrect)
                            logging.LogInfo('Info        ', 'UserInput', 'KeyDown', str(unichr(event.key)).upper(), 'INCORRECT', numberIncorrect)
                                                   
                        pygame.time.delay(1000)
                        break
                    if event.key == K_l:
                        processing = False
                        if (isIdentical):
                            numberIncorrect += 1
                            print ('Incorrect')
                            print ("Number Correct:", numberCorrect)
                            print ("Number Incorrect:", numberIncorrect)
                            logging.LogInfo('Info        ', 'UserInput', 'KeyDown', str(unichr(event.key)).upper(), 'INCORRECT', numberIncorrect)
                        else:
                            numberCorrect += 1
                            print ('Correct')
                            print ("Number Correct:", numberCorrect)
                            print ("Number Incorrect:", numberIncorrect)
                            logging.LogInfo('Info        ', 'UserInput', 'KeyDown', str(unichr(event.key)).upper(), 'CORRECT', numberCorrect)
                        pygame.time.delay(1000)
                        break
 
class ResultsDisplay:
    # Comment out message 3 if only running one checker at 120s at beginning
    def display(self):
        self.blueColor = pygame.Color(0, 0, 255)
        self.fontObj = pygame.font.Font('freesansbold.ttf', 32)
        self.msg1 = 'End of the Block'
        self.msg2 = 'Please take a moment for yourself'
        self.msg3 = 'WARNING: The next screen will be the checkerBoard Stimuli'
        self.msg4 = 'Press C to Continue'
        self.msgSurfaceObj1 = self.fontObj.render(self.msg1, False, self.blueColor)
        self.msgSurfaceObj2 = self.fontObj.render(self.msg2, False, self.blueColor)
        self.msgSurfaceObj3 = self.fontObj.render(self.msg3, False, self.blueColor)
        self.msgSurfaceObj4 = self.fontObj.render(self.msg4, False, self.blueColor)
        self.msgRectObj1 = self.msgSurfaceObj1.get_rect()
        self.msgRectObj2 = self.msgSurfaceObj2.get_rect()
        self.msgRectObj3 = self.msgSurfaceObj3.get_rect()
        self.msgRectObj4 = self.msgSurfaceObj4.get_rect()
        self.msgRectObj1.center = (screenWidth // 2, screenHeight // 2)
        self.msgRectObj2.center = (screenWidth // 2, screenHeight // 2 + 40)
        self.msgRectObj3.center = (screenWidth // 2, screenHeight // 2 + 80)
        self.msgRectObj4.center = (screenWidth // 2, screenHeight // 2 + 120)
        screen.fill(pygame.Color(0, 0, 0))
        screen.blit(self.msgSurfaceObj1, self.msgRectObj1)
        screen.blit(self.msgSurfaceObj2, self.msgRectObj2)
        screen.blit(self.msgSurfaceObj3, self.msgRectObj3)
        screen.blit(self.msgSurfaceObj4, self.msgRectObj4)
        pygame.display.flip()
        processing = True
        while processing:
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_c:
                        processing = False
                        break
class ResultsDisplayEnd:
    
    def display(self):
        self.blueColor = pygame.Color(0, 0, 255)
        self.fontObj = pygame.font.Font('freesansbold.ttf', 32)
        self.msg = 'Thank You for participating! Press X to exit.'
        self.msgSurfaceObj = self.fontObj.render(self.msg, False, self.blueColor)
        self.msgRectObj = self.msgSurfaceObj.get_rect()
        self.msgRectObj.center = (screenWidth // 2, screenHeight // 2)
        screen.fill(pygame.Color(0, 0, 0))
        screen.blit(self.msgSurfaceObj, self.msgRectObj)
        pygame.display.flip()
        processing = True
        while processing:
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_x:
                        pygame.event.post(pygame.event.Event(QUIT))
        
# Initialize the game engine
pygame.init()
random.seed()
# Set the height and width of the screen
size = [800, 500]
entry = Entry()
readyDisplay = ReadyDisplay()
dotDisplay = DotDisplay()
resultsDisplay = ResultsDisplay()
resultsDisplayEnd = ResultsDisplayEnd()
info = pygame.display.Info()

screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
screenWidth, screenHeight = screen.get_size()
logging.info('Screen width:', screenWidth)
logging.info('Screen height:', screenHeight)
screenCenter = (screenWidth // 2, screenHeight // 2)
logging.info('Screen center:', screenCenter[0], ',', screenCenter[1])
numberCorrect = 0
numberIncorrect = 0
logging.info('<<<<<<<<<<<<<>>>>>>>>>>>>>>')
logging.info('-------PROGRAM START-------')
logging.info('TypeOfDisplay', 'DisplayInfo', 'ExtraInfo')
entry.showIntro()
logging.info('DisplayWindow', 'Intro')
# Roughly 22 trials per minute
# trials
numTrials = 1  # 330
numBlocks = 2
timeOfChecker = 15  # 60 for 2 blocks OR 120 for 1 block
# PRESENT CHECKER ONCE for 120 sec
# checkerBoard = CheckerBoard()
#
# logging.info('Info        ','Checkerboard', 'Time of Checker:', timeOfChecker)
# checkerBoard.showBoard(14, 9, timeOfChecker)
for block in range(numBlocks):
    # present checker every block
    checkerBoard = CheckerBoard()
    
    logging.info('Info        ', 'Checkerboard', 'Time of Checker:', timeOfChecker)
    checkerBoard.showBoard(14, 9, timeOfChecker)
    
    logging.info('DisplayWindow', 'ReadyPrompt')
    readyDisplay.prompt()
    logging.info('Info        ', 'Block Start')
    logging.info('Info        ', 'BlockInfo', "Number of Blocks:", numBlocks, 'Number of Trials:', numTrials)
    logging.info('            ', '---------')
    for i in range(numTrials):
        logging.info('Info        ', 'Trial Start')
        dotDisplay.display(0.50, 1)
        logging.info('Info        ', 'Trial End')
        logging.info('            ', '---------')
        
    if block == (numBlocks - 1):
        logging.info('DisplayWindow', 'ResultsDisplay')
        logging.info('DisplayWindow', 'Block End', 'total correct:', numberCorrect, 'total incorrect:', numberIncorrect)
        logging.info('Info        ', 'ExperiEnd')
        resultsDisplayEnd.display()
        
    else:
        logging.info('DisplayWindow', 'ResultsDisplay')
        logging.info('Info        ', 'Block End', 'total correct:', numberCorrect, 'total incorrect:', numberIncorrect)
        logging.info('            ', '---------')
        resultsDisplay.display()
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit ()
