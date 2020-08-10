#!/usr/bin/python3.7
#   Copyright 2020 Aragubas
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#
import pygame, math
from random import randint
from ENGINE import UTILS as utils


GraphPoints = list()

def Initialize(DISPLAY):
    global GraphPoints

    for _ in range(20):
        GraphPoints.append(randint(0, 50))

# -- Resolution 200, 300
ScrollX = 0
GraphPointSpace = 64
HightestPoint = 0
MouseX, MouseY = (0, 0)


def GameDraw(DISPLAY):
    global GraphPoints
    global GraphHeight
    global ScrollX
    global GraphPointSpace
    global HightestPoint

    DISPLAY.fill((100, 100, 100))
    CurrentSelectedIndex = None

    GraphSurface = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()))
    for i, point in enumerate(GraphPoints):
        X = i * GraphPointSpace
        Y = point / GraphSurface.get_height()
        Y = (GraphSurface.get_height() - 5) - Y

        if HightestPoint < point:
            HightestPoint = point
            debug.Set_Parameter("Hight Point was Set to:", point)

        if X + ScrollX > -GraphPointSpace and not X + ScrollX > GraphSurface.get_width() + GraphPointSpace:
            # -- Render the Line -- #
            NextIndex = (i + 1)
            try:
                NextX = ScrollX + NextIndex * GraphPointSpace
                NextY = GraphPoints[NextIndex] / GraphSurface.get_height()

                CONTENT_MANAGER.Shape_Line(GraphSurface, (255, 0, 50), ScrollX + X, Y, NextX, NextY, 2)

            except IndexError:
                pass

            # -- Render Square -- #
            if HightestPoint == point:
                pygame.draw.circle(GraphSurface, (255, 0, 255), (ScrollX + X, Y), 5)
            else:
                CONTENT_MANAGER.Shape_Rectangle(GraphSurface, (255, 255, 255), (ScrollX + X, Y, 5, 5), BorderRadius=5)

            MouseRect = pygame.Rect(MouseX, MouseY, 12, 12)
            PointRect = (ScrollX + X, Y, 5, 5)

            if MouseRect.colliderect(PointRect):
                CurrentSelectedIndex = i

        CONTENT_MANAGER.Shape_Rectangle(GraphSurface, (150, 150, 150), (ScrollX + X, 0, 2, GraphSurface.get_height() - 5))

    # -- Draw the Graph Peak -- #
    peakY = HightestPoint / GraphSurface.get_height()

    CONTENT_MANAGER.Shape_Rectangle(GraphSurface, (100, 100, 100), (0, peakY, GraphSurface.get_width(), 2))
    CONTENT_MANAGER.FontRender(GraphSurface, "/PressStart2P.ttf", 10, "Peak: {0}".format(str(HightestPoint)), (220, 220, 220), 5, peakY - 10, backgroundColor=(0, 0, 0))

    debug.Set_Parameter("HightestPoint", HightestPoint)

    DISPLAY.blit(GraphSurface, (0, 0))

    if not CurrentSelectedIndex == None:
        point = GraphPoints[CurrentSelectedIndex]

        CONTENT_MANAGER.FontRender(DISPLAY, "/PressStart2P.ttf", 8, "Data: " + str(point), (255, 255, 255), MouseX + 15, MouseY, backgroundColor=(0, 0, 0))

        debug.Set_Parameter("point", point)
        debug.Set_Parameter("MouseX", MouseX)
        debug.Set_Parameter("MouseY", MouseY)


def Update():
    global ScrollX
    global GraphPoints
    global MouseX
    global MouseY

    if pygame.key.get_pressed()[pygame.K_q]:
        ScrollX -= 5
    if pygame.key.get_pressed()[pygame.K_e]:
        ScrollX += 5

    if pygame.key.get_pressed()[pygame.K_h]:
        Randomfy()

    # -- Set Mouse Position -- #
    MouseX, MouseY = pygame.mouse.get_pos()


def Randomfy():
    global GraphPoints
    global ScrollX
    global GraphPointSpace
    global HightestPoint

    HightestPoint = 0
    GraphPoints.clear()

    for _ in range(12):
        GraphPoints.append(randint(randint(0, 1000), randint(1000, 2000)))

    for i in range(100):
        GraphPoints.append(i)


def EventUpdate(event):
    global GraphPoints
    global ScrollX
    global GraphPointSpace
    global HightestPoint

    if event.type == pygame.KEYUP and event.key == pygame.K_g:
        Randomfy()

    if event.type == pygame.KEYUP and event.key == pygame.K_r:
        ScrollX = 0

    if event.type == pygame.KEYUP and event.key == pygame.K_b:
        GraphPointSpace = GraphPointSpace * 2

    if event.type == pygame.KEYUP and event.key == pygame.K_n:
        GraphPointSpace = GraphPointSpace / 2



 
