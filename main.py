from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.raw.GLU import gluPerspective, gluLookAt
import cv2, numpy, random, time
import numpy.matlib

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
            glColor3f(0.6, 0.6, 0.6)  # Grey
        else:
            glColor3f(0.2, 0.2, 0.1)  # Black
        glPushMatrix()
        glRotatef(random.randint(0,359), 0, 0, 1)
        glTranslatef(0.75 + 3*random.random(), 0, depth - 3.5 + 4*random.random())
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


def motion_blur(image, row, col, channel):
    img_out = image.copy()
    global center_x, center_y, R, Num

    for i in range(row):
        for j in range(col):
            R_arr = R[i, j] - arr
            R_arr[R_arr < 0] = 0

            new_x = R_arr * numpy.cos(angle[i, j]) + center_x
            new_y = R_arr * numpy.sin(angle[i, j]) + center_y

            int_x = new_x.astype(int)
            int_y = new_y.astype(int)

            int_x[int_x > col - 1] = col - 1
            int_x[int_x < 0] = 0
            int_y[int_y < 0] = 0
            int_y[int_y > row - 1] = row - 1

            img_out[i, j, 0] = image[int_y, int_x, 0].sum() / Num
            img_out[i, j, 1] = image[int_y, int_x, 1].sum() / Num
            img_out[i, j, 2] = image[int_y, int_x, 2].sum() / Num
    return img_out


def screenCapture(width, height):
    global videoWriter
    data = glReadPixels(0, 0, width, height, GL_BGR, GL_UNSIGNED_BYTE)
    image = numpy.array(bytearray(data)).reshape(height, width, 3)
    image = numpy.flipud(image)

    row, col, channel = image.shape
    image = motion_blur(image, row, col, channel)

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
        sys.exit()
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
    print(step)
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
glutHideWindow()

glutDisplayFunc(draw)
glutReshapeFunc(reshape)
glutIdleFunc(redraw)
glutKeyboardFunc(keyBoard)
lid = genList()

xx = numpy.arange(width)
yy = numpy.arange(height)

x_mask = numpy.matlib.repmat(xx, height, 1)
y_mask = numpy.matlib.repmat(yy, width, 1)
y_mask = numpy.transpose(y_mask)

center_y = (height - 1) / 2.0
center_x = (width - 1) / 2.0

R = numpy.sqrt((x_mask - center_x) ** 2 + (y_mask - center_y) ** 2)
R[R < 0] = 0
angle = numpy.arctan2(y_mask - center_y, x_mask - center_x)

Num = 5
arr = numpy.arange(Num)

glutMainLoop()

videoWriter.release()


