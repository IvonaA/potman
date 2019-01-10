from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.WGL import *

import win32ui
import sys
import math
from time import sleep

from random import randint, randrange

vel=0.05
window = 0
hrana=[]
smjer=0
boja=0.0
dozvola=True
nova_lista=[]
Kvadri=[]

#width, height = 1000, 8000


WHITE = (1.0, 1.0, 1.0)
PURPLE = (1.0, 0.0, 1.0)
YELLOW = (1.0, 1.0, 0.0)
RED = (1.0, 0.0, 0.0)
GREEN = (0.0, 1.0, 0.0)

START=1

        
##############################################################################
    ## TEKST ##
##############################################################################

font="Harrington"

def BuildFont():
    global base, font
    wgldc = wglGetCurrentDC()
    hDC = win32ui.CreateDCFromHandle (wgldc)
    base = glGenLists(96);
    
    font_properties = {"name" : font,
                                     "width" : 50,  #sirina fonta
                                     "height" : 50, #visina fonta
                                     "weight" : 1000 #debljina fonta
                                     }
    
    font = win32ui.CreateFont (font_properties)
    # //odabir fonta
    oldfont = hDC.SelectObject(font)
    # // Stvaranje 96 znakova pocevsi od 32. znaka
    wglUseFontBitmaps (wgldc, 32, 96, base)
    # // reset font
    hDC.SelectObject(oldfont)


def glPrint(str):
    global base
    glPushAttrib(GL_LIST_BIT);   #F-ja za ispisivanje teksta u OpenGLu
    glListBase(base - 32);       #Stvara listu znakova od 32. znaka
    glCallLists(str)             #Iscrtavanje teksta
    glPopAttrib();               #Resetiranje liste bitova


#############################################################################
     ## KAMERA ##
#############################################################################


class Camera:
    def __init__(self):     # konstruktor klase
        self.theta = 0     # određuje x i z koordinate
        self.y = 8          # trenutačna y pozicija
        self.dTheta = 0.1     # povećanje thete kojim se miče kamera u xz ravnini
        self.dy = 0.1         # povećanje po y za pomak gore/dolje
    def getX(self):         # funkcija koja vraća x koordinatu
        return -4
    def getY(self):         # funkcija koja vraća y koordinatu
        return self.y
    def getZ(self):         # funkcija koja vraća z koordinatu
        return 5 + self.theta
    def moveRight(self):        # funkcija koja pomiče pogled desno
        self.theta += self.dTheta
    def moveLeft(self):         # funkcija koja pomiče pogled lijevo
        self.theta -= self.dTheta
    def moveUp(self):           # funkcija koja pomiče pogled gore
        self.y += self.dy
    def moveDown(self):         # funkcija koja pomiče pogled dolje
            self.y -= self.dy





##########################################################################
         ## KLASA CAJNIK  ##
##########################################################################
class Sprite:
    global RED, GREEN
    def __init__(self, x, y, z, col):

        self.x = x
        self.y = y
        self.z = z
        self.kut=0
        self.col=col


    def RotateLeft(self):
        self.kut+=90
    def RotateRight(self):
        self.kut-=90

    def getX(self):         # funkcija koja vraća x koordinatu
        return self.x
    def getY(self):         # funkcija koja vraća y koordinatu
        return self.y
    def getZ(self):         # funkcija koja vraća z koordinatu
        return self.z

    def move2Right(self):        # funkcija koja pomiče pogled desno
        self.z += 0.5
    def move2Left(self):         # funkcija koja pomiče pogled lijevo
        self.z -= 0.5
    def move2Up(self):           # funkcija koja pomiče pogled gore
        self.x += 0.5
    def move2Down(self):         # funkcija koja pomiče pogled dolje
        self.x -= 0.5

    def update(self):
        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.col)
        glTranslated(self.x, self.y, self.z)  
        glRotatef(self.kut,0.0,1.0,0.0)
        glutSolidTeapot(0.2)        
        glPopMatrix()

    def getTan(self):
        return (self.z-5)/(self.x-5)

################################################################################
      ## KLASA KVADAR ##
################################################################################
class Kvadar:
    global PURPLE
    def __init__(self, x, y, z, a, b, c):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.c = c

    def update(self):
        lightPosition = (4.0, 3.0, 7.0, 1.0)
        glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, PURPLE)
        crtaj_kvadar(self.x,self.y,self.z,self.a,self.b,self.c)
        glPopMatrix()

###############################################################################
     ## CRTAJ KVADAR ##
###############################################################################

def crtaj_kvadar(x,y,z,a,b,c):
    glBegin(GL_QUADS)
    glNormal3d(0, 1, 0)
    
    glVertex3f(x+a,y+b,z-c)
    glVertex3f(x-a,y+b,z-c)
    glVertex3f(x-a,y+b,z+c)
    glVertex3f(x+a,y+b,z+c)
    
    glColor3f(1.0,0.5,0.0)
    glVertex3f(x+a,y-b,z+c)
    glVertex3f(x-a,y-b,z+c)
    glVertex3f(x-a,y-b,z-c)
    glVertex3f(x+a,y-b,z-c)
    
    glColor3f(1.0,0.0,0.0)
    glVertex3f(x+a,y+b,z+c)
    glVertex3f(x-a,y+b,z+c)
    glVertex3f(x-a,y-b,z+c)
    glVertex3f(x+a,y-b,z+c)
    
    glColor3f(1.0,1.0,0.0)
    glVertex3f(x+a,y-b,z-c)
    glVertex3f(x-a,y-b,z-c)
    glVertex3f(x-a,y+b,z-c)
    glVertex3f(x+a,y+b,z-c)
    
    glColor3f(0.0,0.0,1.0)
    glVertex3f(x-a,y+b,z+c)
    glVertex3f(x-a,y+b,z-c)
    glVertex3f(x-a,y-b,z-c)
    glVertex3f(x-a,y-b,z+c)
    
    glColor3f(1.0,0.0,1.0)
    glVertex3f(x+a,y+b,z-c)
    glVertex3f(x+a,y+b,z+c)
    glVertex3f(x+a,y-b,z+c)
    glVertex3f(x+a,y-b,z-c)
    
    glEnd()


################################################################################
        ## KUGLICE - HRANA##
################################################################################

def crtaj_kuglicu(x,y,z):
    glTranslated(x, 0, z)
    glutSolidSphere(0.3, 30, 30)
    

def crtaj_hranu():
    global YELLOW
    for x,y in hrana:
        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, YELLOW)
        glTranslated(x+0.5, 0, y+0.5)
        glutSolidSphere(0.08, 20, 20)
        glPopMatrix()

for i in range(1,9):
    for j in range(1,9):
        hrana.append((i,j))
##############################################################################

    
def timer(v):
    global START

    for x,y in hrana:
        if abs(Cajnik.x-0.5-x)<0.1 and abs(Cajnik.z-0.5-y)<0.1:
            hrana.remove((x,y))
    if (len(hrana)==0): 
        START=0               
    if (abs(Cajnik1.x-Cajnik.x)<0.4 and abs(Cajnik1.z-Cajnik.z)<0.4):
        START=2        
            
    glutPostRedisplay()
    glutTimerFunc(int(1000/60), timer, v)


   
################################################################################            
       ## INICIJALIZACIJA KLASA ##
#################################################################################

camera = Camera()
Cajnik=Sprite(2,0,8,YELLOW)
Cajnik1=Sprite(5,0,5,RED)

k1=Kvadar(5,0,1,4.1,0.1,0.1)
k2=Kvadar(9,0,5,0.1,0.1,4.1)
k3=Kvadar(5,0,9,4.1,0.1,0.1)
k4=Kvadar(1,0,5,0.1,0.1,4.1)

k25=Kvadar(2,0,5,0.1,0.1,2.1)
k85=Kvadar(8,0,5,0.1,0.1,2.1)
k54=Kvadar(5,0,4,1.1,0.1,0.1)
k56=Kvadar(5,0,6,1.1,0.1,0.1)
k65=Kvadar(6,0,5,0.1,0.1,1.1)

k42=Kvadar(4,0,2.5,0.1,0.1,0.6)
k43=Kvadar(3.5,0,3,0.6,0.1,0.1)
k33=Kvadar(3,0,3.5,0.1,0.1,0.6)

k62=Kvadar(6,0,2.5,0.1,0.1,0.6)
k63=Kvadar(6.5,0,3,0.6,0.1,0.1)
k73=Kvadar(7,0,3.5,0.1,0.1,0.6)

k76=Kvadar(7,0,6.5,0.1,0.1,0.6)
k77=Kvadar(6.5,0,7,0.6,0.1,0.1)
k67=Kvadar(6,0,7.5,0.1,0.1,0.6)

k36=Kvadar(3,0,6.5,0.1,0.1,0.6)
k37=Kvadar(3.5,0,7,0.6,0.1,0.1)
k47=Kvadar(4,0,7.5,0.1,0.1,0.6)

Kvadri = [k1,k2,k3,k4,
          k25,k85,
          k54,k56,k65,
          k42,k43,k33,
          k62,k63,k73,
          k76,k77,k67,
          k36,k37,k47]


##############################################################################
    ## DETEKCIJA SUDARA SA ZIDOVIMA ##
##############################################################################
def Provjera(x,z):
    global dozvola, nova_lista
    for a, b, c, d in nova_lista:
        if (x>a and x<b and z>c and z<d):
            dozvola=False


def PunjenjeListe():
    global nova_lista, Kvadri
    for Kvadar in Kvadri:
        nova_lista.append((Kvadar.x-Kvadar.a,Kvadar.x+Kvadar.a,Kvadar.z-Kvadar.c,Kvadar.z+Kvadar.c))

PunjenjeListe()


###############################################################################

def init():
    glEnable(GL_DEPTH_TEST)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, WHITE)
    glLightfv(GL_LIGHT0, GL_SPECULAR, WHITE)
    glMaterialfv(GL_FRONT, GL_SPECULAR, WHITE)
    glMaterialf(GL_FRONT, GL_SHININESS, 30)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, float(w) / float(h), 1.0, 150.0)
    glMatrixMode(GL_MODELVIEW)

    
###############################################################################
     ## DISPLAY ##
###############################################################################

def display():
    global boja, START, hrana
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(camera.getX(), camera.getY(), camera.getZ(), 5, 0, 5 ,0.0, 1.0, 0.0)
    crtaj_hranu()
    
    for i in range(len(Kvadri)):
        Kvadri[i].update()
    
    Cajnik.update()
    Cajnik1.update()
    Cajnik1.x+=(Cajnik.x-Cajnik1.x)/200
    Cajnik1.z+=(Cajnik.z-Cajnik1.z)/200

    if START == 0:
        sleep(1)
        glRasterPos3f(0,5,3)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPrint(b'YOU WIN!')
    elif START == 2:
        sleep(1)
        glRasterPos3f(0,5,3)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPrint(b'Game over!')
            
    glFlush()
    glutSwapBuffers()


############################################################################
     ## SPECIAL - KRETANJE ##
############################################################################
    
def special(key,x,y):       # iako se ne koriste x,y parametri moraju biti tu
    global smjer,boja,Cajnik, dozvola
            
    if key == GLUT_KEY_LEFT:
        Provjera(Cajnik.x,Cajnik.z-0.5)
        if dozvola==True:
            camera.moveLeft()
            Cajnik.move2Left()
            if smjer == 0:
                Cajnik.RotateLeft()
                smjer=3
            elif smjer==1:
                Cajnik.RotateRight()            
                smjer=3
            elif smjer==2:
                Cajnik.RotateLeft()
                Cajnik.RotateLeft()
                smjer=3
                                      
            
    elif key == GLUT_KEY_RIGHT:
        Provjera(Cajnik.x,Cajnik.z+0.5)
        if dozvola==True:
            if smjer==0:
                Cajnik.RotateRight()
                smjer=2
            elif smjer==1:
                Cajnik.RotateLeft()
                smjer=2
            elif smjer==3:
                Cajnik.RotateLeft()
                Cajnik.RotateLeft()
                smjer=2
            camera.moveRight()
            Cajnik.move2Right()
        
    elif key == GLUT_KEY_UP:
        Provjera(Cajnik.x+0.5,Cajnik.z)
        if dozvola==True:
            camera.moveUp()
            Cajnik.move2Up()
            if smjer==3:
                Cajnik.RotateRight()
                smjer=0
            elif smjer==2:
                Cajnik.RotateLeft()
                smjer=0
            elif smjer==1:
                Cajnik.RotateLeft()
                Cajnik.RotateLeft()
                smjer=0

            
    elif key == GLUT_KEY_DOWN:
        Provjera(Cajnik.x-0.5,Cajnik.z)
        if dozvola==True:
            camera.moveDown()
            Cajnik.move2Down()
            if smjer==3:
                Cajnik.RotateLeft()
                smjer=1
            elif smjer==2:
                Cajnik.RotateRight()
                smjer=1
            elif smjer==0:
                Cajnik.RotateLeft()
                Cajnik.RotateLeft()
                smjer=1

            
    dozvola=True
    Cajnik1.kut=0

    if Cajnik.x<5:
        Cajnik1.kut=180-math.degrees(math.atan(Cajnik.getTan()))  
    elif Cajnik.x>5:
        Cajnik1.kut=-math.degrees(math.atan(Cajnik.getTan()))
    elif Cajnik.x==5:
        if Cajnik.z<5:
            Cajnik1.kut=90
        else:
            Cajnik1.kut=270


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    
glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutInitWindowPosition(80, 80)
glutCreateWindow(b'Projekt - Alkovic')
#InitGL(width,height)
glutDisplayFunc(display)
glutReshapeFunc(reshape)
#glutIdleFunc(display)
glutSpecialFunc(special)    
glutTimerFunc(100, timer, 0)
init()
BuildFont()
glutMainLoop()



















