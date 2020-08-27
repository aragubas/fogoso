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

from ENGINE import utils
# -- Category -- #
from Fogoso.MAIN.Window.InfosWindow import category_0
from Fogoso.MAIN.Window.InfosWindow import category_1
from Fogoso.MAIN.Window.InfosWindow import category_2
from Fogoso.MAIN.Window.InfosWindow import category_2

# -- ETC -- #
from Fogoso.MAIN.Screens import Game as GameScreen
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso.MAIN import GameVariables as save
from Fogoso.MAIN.Screens.Game import Maintenance as maintenance
from Fogoso import MAIN as gameMain
import pygame


print("Fogoso Infos Window, Version 1.4")

# -- Field -- #
WindowObject = gameObjs.Window
DrawnSurface = pygame.Surface((0,0))

# -- Buttons Declaration -- #
NextButton = gameObjs.Button
PreviousButton = gameObjs.Button
ScreenSize = (0, 0)

def Initialize():
    global WindowObject
    global BuyButton
    global DrawnSurface
    global ListItems
    global BuyAmout
    global PreviousButton
    global NextButton
    WindowObject = gameObjs.Window(pygame.Rect(100,100,gameMain.DefaultCnt.Get_RegKey("/props/window/infos/last_w", int),gameMain.DefaultCnt.Get_RegKey("/props/window/infos/last_h", int)), gameMain.DefaultCnt.Get_RegKey("/strings/window/infos/window_title"),True)
    NextButton = gameObjs.Button(pygame.Rect(0,0,0,0), ">", 12)
    PreviousButton = gameObjs.Button(pygame.Rect(0,0,0,0), "<", 12)
    NextButton.CustomColisionRectangle = True
    PreviousButton.CustomColisionRectangle = True
    WindowObject.Minimizable = False
    DrawnSurface = pygame.Surface((WindowObject.WindowSurface_Rect[2], WindowObject.WindowSurface_Rect[3]), pygame.SRCALPHA)

    category_0.Initialize()
    category_1.Initialize()
    category_2.Initialize()

    Set_Category(0)


CurrentCategory = 0
DrawnSurfaceGlob = None
CurrentUpdater = category_0
def Render(DISPLAY):
    global WindowObject
    global DrawnSurface
    global NextButton
    global PreviousButton
    global DrawnSurfaceGlob
    global ScreenSize
    global CurrentUpdater

    # -- Update the Surface -- #
    DrawnSurface = pygame.Surface((WindowObject.WindowSurface_Rect[2], WindowObject.WindowSurface_Rect[3]), pygame.SRCALPHA)

    # -- Draw the Top Bar -- #
    gameMain.shape.Shape_Rectangle(DrawnSurface, (1, 22, 39, 100), (0, 0, DrawnSurface.get_width(), 20))
    gameMain.DefaultCnt.FontRender(DrawnSurface, "/PressStart2P.ttf", 15, gameMain.DefaultCnt.Get_RegKey("/strings/window/infos/category_" + str(CurrentCategory)), (240, 240, 240), 5, 3, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

    # -- Draw the Arrows -- #
    NextButton.Render(DrawnSurface)
    PreviousButton.Render(DrawnSurface)

    # -- Draw the Category -- #
    CurrentUpdater.Render(DrawnSurface)

    WindowObject.Render(DISPLAY)
    DISPLAY.blit(DrawnSurface, (WindowObject.WindowSurface_Rect[0], WindowObject.WindowSurface_Rect[1]))
    DrawnSurfaceGlob = DrawnSurface

def Update():
    global NextButton
    global PreviousButton
    global WindowObject
    global CurrentCategory
    global DrawnSurfaceGlob
    global CurrentUpdater

    if DrawnSurfaceGlob is None:
        return

    # -- Update the Seletectd Categorys -- #
    CurrentUpdater.Update()

    # -- Update Next Button -- #
    NextButton.Set_X(DrawnSurfaceGlob.get_width() - NextButton.Rectangle[2])
    NextButton.Set_Y(2)
    NextButton.Set_ColisionX(WindowObject.WindowRectangle[0] + NextButton.Rectangle[0])
    NextButton.Set_ColisionY(WindowObject.WindowRectangle[1] + NextButton.Rectangle[1] + NextButton.Rectangle[3])

    # -- Update Previous Button -- #
    PreviousButton.Set_X(NextButton.Rectangle[0] - PreviousButton.Rectangle[2] - 5)
    PreviousButton.Set_Y(NextButton.Rectangle[1])
    PreviousButton.Set_ColisionX(WindowObject.WindowRectangle[0] + PreviousButton.Rectangle[0])
    PreviousButton.Set_ColisionY(WindowObject.WindowRectangle[1] + PreviousButton.Rectangle[1] + PreviousButton.Rectangle[3])

def Set_Category(CategoryID):
    global CurrentUpdater

    if CategoryID == 0:
        CurrentUpdater = category_0
        CurrentUpdater.Reset()

    elif CategoryID == 1:
        CurrentUpdater = category_1
        CurrentUpdater.Reset()

    elif CategoryID == 2:
        CurrentUpdater = category_2
        CurrentUpdater.Reset()

def EventUpdate(event):
    global NextButton
    global PreviousButton
    global CurrentCategory
    global DrawnSurfaceGlob
    global CurrentCategory
    global CurrentUpdater

    # -- Update Events -- #
    WindowObject.EventUpdate(event)
    NextButton.Update(event)
    PreviousButton.Update(event)

    CurrentUpdater.EventUpdate(event)

    # -- Go to Previus Category -- #
    if PreviousButton .ButtonState == 2:
        if CurrentCategory > 0:
            CurrentCategory -= 1
        else:
            CurrentCategory = gameMain.DefaultCnt.Get_RegKey("/strings/window/infos/category_max", int)

        Set_Category(CurrentCategory)

    # -- Go to Next Category -- #
    if NextButton .ButtonState == 2:
        if CurrentCategory < gameMain.DefaultCnt.Get_RegKey("/strings/window/infos/category_max", int):
            CurrentCategory += 1
        else:
            CurrentCategory = 0

        Set_Category(CurrentCategory)
