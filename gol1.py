
from direct.gui.DirectGui import DirectFrame
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import TextNode
from direct.showbase.ShowBase import ShowBase
import direct.directbase.DirectStart
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import AmbientLight,DirectionalLight,LightAttrib
from panda3d.core import TextNode
from panda3d.core import Point3,Vec3,Vec4,BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.actor.Actor import Actor
import sys
import random
from direct.gui.DirectGui import *

#First we define some contants for the colors
BLACK = Vec4(0.5,0.1,0.1,1)
WHITE = Vec4(1,1,1,1)
HIGHLIGHT = Vec4(0,1,1,1)


#Now we define some helper functions that we will need later

#This function, given a line (vector plus origin point) and a desired z value,
#will give us the point on the line where the desired z value is what we want.
#This is how we know where to position an object in 3D space based on a 2D mouse
#position. It also assumes that we are dragging in the XY plane.
#
#This is derived from the mathmatical of a plane, solved for a given point
def PointAtZ(z, point, vec):
  return point + vec * ((z-point.getZ()) / vec.getZ())

#A handy little function for getting the proper position for a given square
def SquarePos1(i):
  return Point3((i%8)-3.5, int(i/8)-3.5, 0)

def SquarePos(i):
  return Point3((i%8)-3.5, int(i/8)-3.5, 0.15)

def SquarePosTuple(i):
  return [7-(int(i/8)), (i%8)]

#Helper function for determining wheter a square should be white or black
#The modulo operations (%) generate the every-other pattern of a chess-board
def SquareColor(i):
  if (i + ((i/8)%2))%2: return BLACK
  else: return WHITE



class World(DirectObject):
  mySound = base.loader.loadSfx("trial.mp3")
  def random_vgen(self):
    print 'I am in random'
    for i in range(0,5):
      
      self.a[random.randint(0,7)][random.randint(0,7)] = 1
  

  def initializer(self,level):
    
  
    self.turns = 0
      
##   Level Definition 
    
    def levelone():
        self.a[4][4] = 1
        self.a[4][5] = 1
        self.a[4][6] = 1
        self.a[5][2] = 1
        self.a[3][5] = 1
        self.a[4][6] = 1
        self.a[5][5] = 1
    def leveltwo():
        self.a[4][3] = 1
        self.a[4][5] = 1
        self.a[4][7] = 1
        self.a[5][2] = 1
        self.a[3][5] = 1
        self.a[2][2] = 1
        self.a[5][3] = 1
        self.a[1][2] = 1

    def levelthree():
        self.a[4][4] = 1
        self.a[4][5] = 1
        self.a[4][6] = 1
        self.a[5][2] = 1
        self.a[3][5] = 1
        self.a[4][6] = 1
        self.a[5][5] = 1
        self.a[4][3] = 1
        self.a[4][5] = 1
        self.a[4][7] = 1
        self.a[5][2] = 1
        self.a[3][5] = 1
        self.a[2][2] = 1
        self.a[5][3] = 1


    options = {1: levelone,
               2: leveltwo,
               3: levelthree
            
            }

    options[level]()
    
    
    temp = []
    count = 0
    for element in reversed(self.a):
        for ele in element:
            #print 'cheking element is 1 : ' + str(ele)
            if ele == 1:
                temp.append(count)
                self.pieces[count] = Pawn(count,WHITE)
                #self.squares[count].setColor(HIGHLIGHT)
            count = count + 1
    self.list=temp
    
  def showscore(self):
        try:
            self.score.destroy()
        except:
            pass
        self.score = OnscreenText(text = 'Number of Turns : %s'%(self.turns), pos = (0.5, 0.95), scale = 0.07, mayChange = True)
  def menuscreen(self):
      
      # Callback function to set  text
    def setText():
        b.destroy()
        helptext.destroy()
        
    
    # Add button
    b = DirectButton(text = ("START", "START", "START", "disabled"), scale=0.15, command=setText, pos=(0,0,0.85))

    helptext = OnscreenText(text ='''
    STORY:
    Hello Mad Scientist!
    You are so close to finding the cure to aids!
    You understood the behaviour and can finally manipulate the virus to kill itself!
    But time is running out!
    You have a red and white blood cell sample infected with AIDS Virus.

    INSTRUCTIONS:
    The AIDS Virus obeys the Conway's Game of Life. Who would have guessed?
    1.  If virus is surrounded by more than 3 viruses, it dies of suffocation
    2.  If virus is surrounded by less than 2 viruses, it dies of underpopulation
    3.  If dead empty cell, is surrounded by exactly 3 viruses, a new virus is spawned due to breeding.

    AIM:
    To kill all the viruses, by moving one of them every turn.

    ''', pos = (-0.90,0.72),frame = (123,123,123,1), wordwrap = 25, align = TextNode.ALeft, bg = (0.23,0.243,0.13,0.9))

  def endscreen(self):     
    def restart():        
        scorecard.destroy()
        restartb.destroy()
        end.destroy()
        nextlevelb.destroy()
        self.reference.destroy()
        self.mySound.stop()
        try:            
            self.score.destroy()
        except:
            pass
            
        World()
        
    def quitgame():
        sys.exit()

    def nextLevel():
        self.currlevel = self.currlevel + 1
        nextlevelb.destroy()
        scorecard.destroy()
        restartb.destroy()
        end.destroy()
        self.score.destroy()
        self.initializer(self.currlevel)

    

    # Add button

    scorecard = OnscreenText(text = 'You finished it in %s turns! '%(self.turns),frame = (123,123,123,0), wordwrap = 25, bg = (0.2,0,0.8,1))

    nextlevelb = DirectButton(text = ("NEXT LEVEL", "NEXT LEVEL", "NEXT LEVEL", "disabled"), scale=0.15, command=nextLevel, pos=(0,0,-0.15))
    restartb = DirectButton(text = ("RESTART", "RESTART", "RESTART", "disabled"), scale=0.15, command=restart, pos=(0,0,-0.35))
    end = DirectButton(text = ("QUIT", "QUIT", "QUIT", "disabled"), scale=0.15, command=quitgame, pos=(0,0,-0.55))
    if self.currlevel == self.maxlevel:
      nextlevelb.destroy()


  def __init__(self):
    #music
    
    
    self.mySound.play()
      

    print 'I am being initialized'
    
          
    self.menuscreen()
    self.list = []
    self.turns = 0
    self.maxlevel = 3
    self.currlevel = 1
    self.a =[[0 for x in range(8)] for y in range(8)]
    
    
        
    #This code puts the standard title and instruction text on screen
    self.title = OnscreenText(text="Game of Life : Help in ending AIDS!",
                              style=1, fg=(1,1,1,1),
                              pos=(0,-0.95), scale = .07)
    self.escapeEvent = OnscreenText( 
      text="ESC: Quit",
      style=1, fg=(1,1,1,1), pos=(-1.3, 0.95),
      align=TextNode.ALeft, scale = .05)
##    self.mouse1Event = OnscreenText(
##      text="Left-click and drag: Pick up virus and drag it to a new bloodcell",
##      style=1, fg=(1,1,1,1), pos=(-1.3, 0.90),
##      align=TextNode.ALeft, scale = .05)
##    
    
        
    
    self.accept('escape', sys.exit)              #Escape quits
    
    base.disableMouse()                          #Disble mouse camera control
    camera.setPosHpr(0, -13.75, 6, 0, -25, 0)    #Set the camera
    self.setupLights()                           #Setup default lighting
    
    #Since we are using collision detection to do picking, we set it up like
    #any other collision detection system with a traverser and a handler
    self.picker = CollisionTraverser()            #Make a traverser
    self.pq     = CollisionHandlerQueue()         #Make a handler
    #Make a collision node for our picker ray
    self.pickerNode = CollisionNode('mouseRay')
    #Attach that node to the camera since the ray will need to be positioned
    #relative to it
    self.pickerNP = camera.attachNewNode(self.pickerNode)
    #Everything to be picked will use bit 1. This way if we were doing other
    #collision we could seperate it
    self.pickerNode.setFromCollideMask(BitMask32.bit(1))
    self.pickerRay = CollisionRay()               #Make our ray
    self.pickerNode.addSolid(self.pickerRay)      #Add it to the collision node
    #Register the ray as something that can cause collisions
    self.picker.addCollider(self.pickerNP, self.pq)
    #self.picker.showCollisions(render)

    #Now we create the chess board and its pieces

    #We will attach all of the squares to their own root. This way we can do the
    #collision pass just on the sqaures and save the time of checking the rest
    #of the scene
    self.squareRoot = render.attachNewNode("squareRoot")
    
    #For each square
    self.squares = [None for i in range(64)]
    self.pieces = [None for i in range(64)]

    
    for i in range(64):
      #Load, parent, color, and position the model (a single square polygon)
      self.squares[i] = loader.loadModel("models/square")
      self.squares[i].reparentTo(self.squareRoot)
      self.squares[i].setPos(SquarePos1(i))
      self.squares[i].setColor(SquareColor(i))
      #Set the model itself to be collideable with the ray. If this model was
      #any more complex than a single polygon, you should set up a collision
      #sphere around it instead. But for single polygons this works fine.
      self.squares[i].find("**/polygon").node().setIntoCollideMask(
        BitMask32.bit(1))
      #Set a tag on the square's node so we can look up what square this is
      #later during the collision pass
      self.squares[i].find("**/polygon").node().setTag('square', str(i))

      #We will use this variable as a pointer to whatever piece is currently
      #in this square

    #The order of pieces on a chessboard from white's perspective. This list
    #contains the constructor functions for the piece classes defined below

    self.initializer(self.currlevel)
    
    
      #Load the white pawns
      

    

    #This will represent the index of the currently highlited square
    self.hiSq = False
    #This wil represent the index of the square where currently dragged piece
    #was grabbed from
    self.dragging = False

    #Start the task that handles the picking
    self.mouseTask = taskMgr.add(self.mouseTask, 'mouseTask')
    #self.trial = taskMgr.add(self.trial,'trial')
    self.accept("mouse1", self.grabPiece)       #left-click grabs a piece
    self.accept("mouse1-up", self.releasePiece) #releasing places it
    
   

  #This function swaps the positions of two pieces
  def swapPieces(self, fr, to):
    temp = self.pieces[fr]
    self.pieces[fr] = self.pieces[to]
    self.pieces[to] = temp
    if self.pieces[fr]:
      print 'imma swapping'  
      self.pieces[fr].square = fr
      print fr
      print SquarePos(fr)
      try:
          self.pieces[fr].obj.setPos(SquarePos(fr))
      except:
          pass
      print 'done'
    if self.pieces[to]:
      self.pieces[to].square = to
      try:
          self.pieces[to].obj.setPos(SquarePos(to))
      except:
          pass
  def trial(self):
      self.turns = self.turns + 1
      try:
        self.reference.destroy()
      except:
        pass
      self.reference = OnscreenText( 
      text='''
Reference:
virus is surrounded by more than 3 viruses, it dies
virus is surrounded by less than 2 viruses, it dies
If dead empty cell, is surrounded by exactly 3 viruses, a new virus is spawned.
'''  ,
      style=1, fg=(1,1,1,1), pos=(-1, 0.95),
      align=TextNode.ALeft, scale = .05)
      
      
      self.showscore()
      a = self.a
      while True:
          for i in self.list:
              #insert deletion code
              print 'imma deleting the sq : ' + str(i)
              self.pieces[i].obj.delete()
              
              self.squares[i].setColor(SquareColor(i))
          count = 0
          a=[[([[sum(b[y1][x1] for b in [[[((-1<x2+dx<len(a[0])) and (-1<y2+dy<len(a))) and a[y2+dy][x2+dx] or 0 for x2 in range(len(a[0]))] for y2 in range(len(a))] for (dx,dy) in [(dx,dy) for dx in [-1,0,1] for dy in [-1,0,1] if (dy!=0 or dx!=0)]]) for x1 in range(len(a[0]))] for y1 in range(len(a))][y][x]== 3 or ([[sum(c[y3][x3] for c in [[[((-1<x4+dx<len(a[0])) and (-1<y4+dy<len(a))) and a[y4+dy][x4+dx] or 0 for x4 in range(len(a[0]))] for y4 in range(len(a))] for (dx,dy) in [(dx,dy) for dx in [-1,0,1] for dy in [-1,0,1] if (dy!=0 or dx!=0)]]) for x3 in range(len(a[0]))] for y3 in range(len(a))][y][x] == 2 and a[y][x]==1)) and 1 or 0 for x in range(len(a[0]))] for y in range(len(a))]
          lis = []
          diceroll = random.randint(0,5)
          if diceroll == 2:
            
            self.random_vgen()
          for element in reversed(a):
              
              for ele in element:
                  #print 'cheking element is 1 : ' + str(ele)
                  if ele == 1:
                      lis.append(count)
                  count = count + 1
          print lis  
          self.list = lis
          
          self.a = a
          print self.list
          
          for i in self.list:
              self.pieces[i] = Pawn(i,WHITE)
              #self.squares[i].setColor(HIGHLIGHT)
          print 'leaving trial'  
          if len(self.list)==0:
              self.endscreen()
          break
        
      return
  def mouseTask(self, task):
    #This task deals with the highlighting and dragging based on the mouse
    
    #First, clear the current highlight
    if self.hiSq is not False:
      self.squares[self.hiSq].setColor(SquareColor(self.hiSq))
      self.hiSq = False
      
    #Check to see if we can access the mouse. We need it to do anything else
    if base.mouseWatcherNode.hasMouse():
      #get the mouse position
      mpos = base.mouseWatcherNode.getMouse()
      
      #Set the position of the ray based on the mouse position
      self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
      
      #If we are dragging something, set the position of the object
      #to be at the appropriate point over the plane of the board
      if self.dragging is not False:
        #Gets the point described by pickerRay.getOrigin(), which is relative to
        #camera, relative instead to render
        nearPoint = render.getRelativePoint(camera, self.pickerRay.getOrigin())
        #Same thing with the direction of the ray
        nearVec = render.getRelativeVector(camera, self.pickerRay.getDirection())
        try:
            self.pieces[self.dragging].obj.setPos(PointAtZ(.5, nearPoint, nearVec))
        except:
            pass
      #Do the actual collision pass (Do it only on the squares for
      #efficiency purposes)
      self.picker.traverse(self.squareRoot)
      if self.pq.getNumEntries() > 0:
        #if we have hit something, sort the hits so that the closest
        #is first, and highlight that node
        self.pq.sortEntries()
        i = int(self.pq.getEntry(0).getIntoNode().getTag('square'))
        #Set the highlight on the picked square
        self.squares[i].setColor(HIGHLIGHT)
        self.hiSq = i
        #print 'selected is ' + str(i)

    return Task.cont

  def grabPiece(self):
    #If a square is highlighted and it has a piece, set it to dragging mode
    if (self.hiSq is not False and
      self.pieces[self.hiSq]):
      self.dragging = self.hiSq
      self.hiSq = False
    
  def releasePiece(self):
    #Letting go of a piece. If we are not on a square, return it to its original
    #position. Otherwise, swap it with the piece in the new square
    if self.dragging is not False:   #Make sure we really are dragging something
      #We have let go of the piece, but we are not on a square
      if self.hiSq is False:
        try:
            self.pieces[self.dragging].obj.setPos(SquarePos(self.dragging))
        except:
            pass
      else:
        #Otherwise, swap the pieces
        self.swapPieces(self.dragging, self.hiSq)
        #self.draggin is the from
        print self.list
        print 'you picked this, so Imma deleting this ' + str(self.dragging)
        #deletion of i after picking it up.
        try:
            self.list.remove(self.dragging)
        except:
            pass
        temp2 = []
        temp2 = SquarePosTuple(self.dragging)
        self.a[temp2[0]][temp2[1]] = 0
        
        i = self.hiSq
        print self.list
        print 'highlighted sq is ' + str(i)
        templis = []
        templis = SquarePosTuple(i)
        print templis
        self.list.append(i)
        print self.list
        print templis
        self.a[templis[0]][templis[1]] = 1

        
        
        for line in self.a:
            print line
        self.trial()
        
    #We are no longer dragging anything
    self.dragging = False

  def setupLights(self):    #This function sets up some default lighting
    ambientLight = AmbientLight( "ambientLight" )
    ambientLight.setColor( Vec4(.8, .8, .8, 1) )
    directionalLight = DirectionalLight( "directionalLight" )
    directionalLight.setDirection( Vec3( 0, 45, -45 ) )
    directionalLight.setColor( Vec4( 0.2, 0.2, 0.2, 1 ) )
    render.setLight(render.attachNewNode( directionalLight ) )
    render.setLight(render.attachNewNode( ambientLight ) )

#Class for a piece. This just handels loading the model and setting initial
#position and color
class Piece:
  def __init__(self, square, color,live=1):
    if live==1:
      
      self.obj = Actor(self.model,{"move": "models/monster1-pincer-attack-both"})
      self.obj.loop("move")
      self.obj.reparentTo(render)
      self.obj.setColor(color)
      #scale decided by ronit scientifically
      self.obj.setScale(0.15, 0.15, 0.15)
      self.obj.setHpr(180,0,0)
      self.obj.setPos(SquarePos(square))
    else:
      
      self.delete()
#Classes for each type of chess piece
#Obviously, we could have done this by just passing a string to Piece's init.
#But if you watned to make rules for how the pieces move, a good place to start
#would be to make an isValidMove(toSquare) method for each piece type
#and then check if the destination square is acceptible during ReleasePiece
class Pawn(Piece):
  model = "models/monster1"

#Do the main initialization and start 3D rendering
w = World()
run()

