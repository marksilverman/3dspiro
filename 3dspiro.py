from graphics import *
from random import *
import time
import math
import sys

class point3d:
   def __init__(self, x=0.0, y=0.0, z=0.0):
       self.x = x
       self.y = y
       self.z = z

class mat4x4:
    def __init__(self):
        self.data = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]

def draw(p1, p2):
    l = Line(p1, p2)
    l.setFill(white)
    l.setWidth(4)
    l.draw(win)

def MultiplyMatrixVector(input, output, matrix):
    output.x = input.x * matrix.data[0][0] + input.y * matrix.data[1][0] + input.z * matrix.data[2][0] + matrix.data[3][0]
    output.y = input.x * matrix.data[0][1] + input.y * matrix.data[1][1] + input.z * matrix.data[2][1] + matrix.data[3][1]
    output.z = input.x * matrix.data[0][2] + input.y * matrix.data[1][2] + input.z * matrix.data[2][2] + matrix.data[3][2]
    w = input.x * matrix.data[0][3] + input.y * matrix.data[1][3] + input.z * matrix.data[2][3] + matrix.data[3][3]
    if w != 0.0:
        output.x /= w
        output.y /= w
        output.z /= w

width = 800
height = 800
halfWidth = width * 0.5
halfHeight = height * 0.5
fAspectRatio = height / width
white = color_rgb(255, 255, 255)

win = GraphWin('lines', width, height)
win.setCoords(0, 0, win.width, win.height)
win.setBackground('black')

radius1 = 0.3
radius2 = 0.1
radius = radius1 - radius2

pointCloud = []

pen = 0.2
angle = 0.0
while angle < 2 * math.pi:
    x = radius * math.cos(angle) + pen * math.cos(angle * radius / radius2)
    y = radius * math.sin(angle) - pen * math.sin(angle * radius / radius2)
    pointCloud.append(point3d(x, y))
    angle += 0.1

# Projection Matrix
fNear = 0.1
fFar = 1000.0
fFov = 90.0
fFovRad = 1.0 / math.tan(fFov * 0.5 / 180.0 * math.pi)

fElapsedTime = 0.2

# projection from 3d to 2d
matProj = mat4x4()
matProj.data[0][0] = fAspectRatio * fFovRad
matProj.data[1][1] = fFovRad
matProj.data[2][2] = fFar / (fFar - fNear)
matProj.data[3][2] = (-fFar * fNear) / (fFar - fNear)
matProj.data[2][3] = 1.0
matProj.data[3][3] = 0.0

# rotation around the Z axis
matRotZ = mat4x4()
matRotZ.data[2][2] = 1
matRotZ.data[3][3] = 1

# rotation around the X axis
matRotX = mat4x4()
matRotX.data[0][0] = 1
matRotX.data[3][3] = 1

rotated_on_z = point3d()
rotated_on_zx = point3d()
projected = point3d()

angle = 0.0

while True:
    angle += fElapsedTime
    matRotZ.data[0][0] = math.cos(angle)
    matRotZ.data[0][1] = math.sin(angle)
    matRotZ.data[1][0] = -math.sin(angle)
    matRotZ.data[1][1] = math.cos(angle)

    matRotX.data[1][1] = math.cos(angle * 0.5)
    matRotX.data[1][2] = math.sin(angle * 0.5)
    matRotX.data[2][1] = -math.sin(angle * 0.5)
    matRotX.data[2][2] = math.cos(angle * 0.5)

    stop = False

    for thisPoint in pointCloud:
        # rotate on Z-Axis
        MultiplyMatrixVector(thisPoint, rotated_on_z, matRotZ)

        # rotate on X-Axis
        MultiplyMatrixVector(rotated_on_z, rotated_on_zx, matRotX)

        # translate into the screen
        rotated_on_zx.z = rotated_on_zx.z + 3.0

        # project from 3D to 2D
        MultiplyMatrixVector(rotated_on_zx, projected, matProj)

        # scale into view
        projected.x = halfWidth * (projected.x + 1.0)
        projected.y = halfHeight * (projected.y + 1.0)

        c = Circle(Point(projected.x, projected.y), 2)
        c.setFill(white)
        c.draw(win)

        if win.checkMouse() != None:
            stop = True
            break
        if win.checkKey() == " ": break
        if win.checkKey() != "": sys.exit

    if stop:
        break
        
#    time.sleep(0.025)
    # win.getMouse()

    # clear the screen
    screenRectangle = Rectangle(Point(0, 0), Point(width, height))
    screenRectangle.setFill('black')
    screenRectangle.draw(win)
