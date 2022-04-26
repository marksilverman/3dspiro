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
    
    def multiply(self, input, output):
        output.x = input.x * self.data[0][0] + input.y * self.data[1][0] + input.z * self.data[2][0] + self.data[3][0]
        output.y = input.x * self.data[0][1] + input.y * self.data[1][1] + input.z * self.data[2][1] + self.data[3][1]
        output.z = input.x * self.data[0][2] + input.y * self.data[1][2] + input.z * self.data[2][2] + self.data[3][2]
        w = input.x * self.data[0][3] + input.y * self.data[1][3] + input.z * self.data[2][3] + self.data[3][3]
        if w != 0.0:
            output.x /= w
            output.y /= w
            output.z /= w

def draw(p1, p2):
    l = Line(p1, p2)
    l.setFill(white)
    l.setWidth(4)
    l.draw(win)

width = 800
height = 800
halfWidth = width * 0.5
halfHeight = height * 0.5
fAspectRatio = height / width
white = color_rgb(255, 255, 255)

win = GraphWin('lines', width, height)
win.setCoords(0, 0, win.width, win.height)
win.setBackground('black')

radius1 = 0.5
radius2 = 0.2
radius = radius1 - radius2

pointCloud = []

pen = 0.8
angle = 0.0
ctr = 0.0
while angle < 5 * math.pi:
    x = radius * math.cos(angle) + pen * math.cos(angle * radius / radius2)
    y = radius * math.sin(angle) - pen * math.sin(angle * radius / radius2)
    z = math.sin(ctr) * radius1
    ctr += 0.2
    #print(f'x={x}, y={y}, z={z}')
    pointCloud.append(point3d(x, y, z))
    angle += 0.05

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

angle1 = 0.0
angle2 = 0.0

while True:
    angle1 += fElapsedTime
    angle2 += 0.02

    matRotZ.data[0][0] = math.cos(angle2)
    matRotZ.data[0][1] = math.sin(angle2)
    matRotZ.data[1][0] = -math.sin(angle2)
    matRotZ.data[1][1] = math.cos(angle2)

    matRotX.data[1][1] = math.cos(angle1 * 0.5)
    matRotX.data[1][2] = math.sin(angle1 * 0.5)
    matRotX.data[2][1] = -math.sin(angle1 * 0.5)
    matRotX.data[2][2] = math.cos(angle1 * 0.5)

    p2 = None
    for thisPoint in pointCloud:
        # rotate on Z
        matRotZ.multiply(thisPoint, rotated_on_z)

        # rotate on X
        matRotX.multiply(rotated_on_z, rotated_on_zx)
        # matRotX.multiply(thisPoint, rotated_on_zx)

        # translate
        rotated_on_zx.z = rotated_on_zx.z + 3.0

        # project to 2D
        matProj.multiply(rotated_on_zx, projected)

        # scale into view
        projected.x = halfWidth * (projected.x + 1.0)
        projected.y = halfHeight * (projected.y + 1.0)

        p1 = Point(projected.x, projected.y)
        if p2:
            l = Line(p1, p2)
            l.setWidth(3)
            l.setFill(white)
            l.draw(win)
        p2 = p1


    if win.checkMouse() != None: break
    if win.checkKey() == " ": break

#    time.sleep(0.025)
    # win.getMouse()

    # clear the screen
    #if (int(angle1) % 2) == 0:
    win.delete("all")