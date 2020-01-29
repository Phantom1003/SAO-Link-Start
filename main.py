from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.raw.GLU import gluPerspective, gluLookAt
import cv2, numpy, random, time

# python 3.6
# sudo apt-get install freeglut3
# sudo apt-get install freeglut3-dev
# package: pyopengl, pyopengl_accelerate, opencv_python, numpy

def keyBoard(key, x, y):
    global step, delta, pause
    print(key)
    if key == b' ':
        pause = ~pause
    elif key == b'r':
        step = delta

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    whRatio = width/height
    gluPerspective(90.0, whRatio, 0.1, 500.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def genList():
    lid = glGenLists(1)
    glNewList(lid, GL_COMPILE)
    drawTunnel(35,    2, 2012)
    drawTunnel(30,    5, 2013)
    drawTunnel(25,   10, 2014)
    drawTunnel(20,   15, 2015)
    drawTunnel(15,   30, 2016)
    drawTunnel(10,   50, 2017)
    drawTunnel( 5,  100, 2018)
    drawTunnel( 0,  200, 2019)
    drawTunnel(-5,  150, 2020)
    glEndList()
    return lid

def drawTunnel(depth, num, seed):
    random.seed(seed)
    for i in range(0, num):
        if i % 7 == 0:
            glColor3f(0.0, 1.0, 1.0) # Cyan
        elif i % 7 == 1:
            glColor3f(1.0, 1.0, 0.0) # Yellow
        elif i % 7 == 2:
            glColor3f(1.0, 0.0, 1.0) # Magenta
        elif i % 7 == 3:
            glColor3f(0.0, 1.0, 0.0) # Green
        elif i % 7 == 4:
            glColor3f(1.0, 0.0, 0.0) # Red
        elif i % 7 == 5:
            glColor3f(0.0, 0.0, 0.0) # Black
        else:
            glColor3f(0.5, 0.5, 0.5) # Grey
        glPushMatrix()
        glRotatef(random.randint(0,359), 0, 0, 1)
        glTranslatef(0.75 + 3*random.random(), 0, depth - 2 + 4*random.random())
        glutSolidCylinder(0.07, 2+2*random.random(), 360, 10)
        glPopMatrix()

def draw():
    global step, delta, lid
    glClearColor(1, 1, 1, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    gluLookAt(0.0, 0.0, step,
              0.0, 0.0, step-delta,
              0.0, 1.0, 0.0)

    glCallList(lid)
    glEnable(GL_DEPTH_TEST)
    glutSwapBuffers()

    time.sleep(0.05)

def screenCapture(width, height):
    global videoWriter
    data = glReadPixels(0, 0, width, height, GL_BGR, GL_UNSIGNED_BYTE)
    image = numpy.array(bytearray(data)).reshape(height, width, 3)
    image = numpy.flipud(image)
    # cv2.imshow('Monitor', image)
    # cv2.waitKey(10)
    videoWriter.write(image)

def redraw():
    global step, delta, pause, recode, width, height
    if pause:
        step = step
    elif step < -20:
        step = delta
        recode = False
    elif step < 10:
        step = step - 1.8
    elif step < 15:
        step = step - 1.6
    elif step < 25:
        step = step - 1.4
    elif step < 35:
        step = step - 1.2
    else:
        step = step - 1
    draw()
    if recode:
        screenCapture(width, height)



# OpenGL Parameters
scale = 1
width, height = int(1920*scale), int(1080*scale)
step = 60
delta = step
pause = False
recode = True

# OpenCV Parameters
fps = 30
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
videoWriter = cv2.VideoWriter('output.avi',fourcc, fps, (width, height),True)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH )
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
glutCreateWindow("Link Start!")

glutDisplayFunc(draw)
glutReshapeFunc(reshape)
glutIdleFunc(redraw)
glutKeyboardFunc(keyBoard)
lid = genList()

glutMainLoop()

videoWriter.release()


