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

# -- Imports -- #
from ENGINE import APPDATA as reg
from ENGINE import UTILS as utils
import ENGINE as tge

from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso import MAIN as gameMain
from Fogoso.MAIN.Screens.Settings import category_0 as Category0
from Fogoso.MAIN.Screens.Settings import category_1 as Category1
from Fogoso.MAIN.Screens.Settings import category_2 as Category2
from Fogoso.MAIN import ScreenTransition as transition
import pygame, sys

import importlib
import time
from random import randint

ScreenToReturn = 0
OptionsScreen_CloseButton = gameObjs.Button
OptionsScreen_UpDownCategory = gameObjs.UpDownButton

# -- Category -- #
Current_Category = 0
CurrentCategoryUpdate = Category0

# -- Elements -- #
ElementsX = 0
ElementsY = 0

def Update():
    global ScreenToReturn
    global Current_Category
    global ElementsY
    global ElementsX
    global OptionsScreen_UpDownCategory
    global CurrentCategoryUpdate

    # -- Update Elements Location -- #
    ElementsX = gameMain.DefaultDisplay.get_width() / 2 - 275
    ElementsY = gameMain.DefaultDisplay.get_height() / 2 - 125

    # -- Update UpDown Button Location -- #
    OptionsScreen_UpDownCategory.Set_X(ElementsX + 558 - OptionsScreen_UpDownCategory.Get_Width() - 5)
    OptionsScreen_UpDownCategory.Set_Y(ElementsY + 3)

    # -- Change Category UP Button -- #
    if OptionsScreen_UpDownCategory .ButtonState == 2:
        MaxCategory = gameMain.DefaultCnt.Get_RegKey("/props/settings_max_category", int)
        Current_Category += 1
        if Current_Category > MaxCategory:
            Current_Category = 0
        transition.Run()
        Set_Category(Current_Category)

    if OptionsScreen_UpDownCategory.ButtonState == 1:
        MaxCategory = gameMain.DefaultCnt.Get_RegKey("/props/settings_max_category", int)
        Current_Category -= 1
        if Current_Category < 0:
            Current_Category = MaxCategory
        transition.Run()
        Set_Category(Current_Category)

    # -- Update current Category -- #
    CurrentCategoryUpdate.Update()
    # -- Set the Elements Position -- #
    CurrentCategoryUpdate.ElementsX = ElementsX
    CurrentCategoryUpdate.ElementsY = ElementsY

    if OptionsScreen_CloseButton .ButtonState == 2:
        transition.Run()
        gameMain.SetScreen_ByID(ScreenToReturn)

    OptionsScreen_CloseButton.Set_X(gameMain.DefaultDisplay.get_width() - 120)

def Set_Category(CategoryID):
    global CurrentCategoryUpdate

    if CategoryID == 0:
        CurrentCategoryUpdate = Category0

    elif CategoryID == 1:
        CurrentCategoryUpdate = Category1

    elif CategoryID == 2:
        CurrentCategoryUpdate = Category2


def GameDraw(DISPLAY):
    global Current_Category
    global ElementsY
    global ElementsX
    global OptionsScreen_UpDownCategory
    global CurrentCategoryUpdate

    # -- Draw the Background -- #
    gameObjs.Draw_Panel(DISPLAY, (ElementsX, ElementsY, 558, 258))

    # -- Render the Title Text -- #
    gameMain.shape.Shape_Rectangle(DISPLAY, (1, 22, 39), (ElementsX, ElementsY, 558, 22))
    gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 15, gameMain.DefaultCnt.Get_RegKey("/strings/settings/category/{0}".format(str(Current_Category))), (246, 247, 248), ElementsX + 5,
                               ElementsY + 4, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

    # -- Render Close Button -- #
    OptionsScreen_CloseButton.Render(DISPLAY)

    # -- Render UpDown Button -- #
    OptionsScreen_UpDownCategory.Render(DISPLAY)

    # -- Render Categorys -- #
    CurrentCategoryUpdate.Render(DISPLAY)

def Initialize():
    global OptionsScreen_CloseButton
    global OptionsScreen_UpDownCategory
    global Current_Category

    OptionsScreen_CloseButton = gameObjs.Button(pygame.rect.Rect(0, 5, 0, 0), gameMain.DefaultCnt.Get_RegKey("/strings/settings/back_button"), 14)
    OptionsScreen_UpDownCategory = gameObjs.UpDownButton(5, 5, 14)

    gameMain.ClearColor = (1, 24, 32)

    Category0.Initialize()
    Category1.Initialize()
    Category2.Initialize()

    Set_Category(Current_Category)

def EventUpdate(event):
    global Current_Category
    global OptionsScreen_CloseButton
    global OptionsScreen_UpDownCategory
    global CurrentCategoryUpdate

    OptionsScreen_CloseButton.Update(event)
    OptionsScreen_UpDownCategory.Update(event)

    CurrentCategoryUpdate.EventUpdate(event)