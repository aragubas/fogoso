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

import pygame, sys

import importlib
import time
from random import randint

OptionsScreen_DebugModeEnabled = gameObjs.UpDownButton
OptionsScreen_RandomWindowTitle = gameObjs.UpDownButton
OptionsScreen_NumberFormatting = gameObjs.UpDownButton

ElementsX = 0
ElementsY = 0

def Initialize():
    global OptionsScreen_DebugModeEnabled
    global OptionsScreen_RandomWindowTitle
    global OptionsScreen_NumberFormatting
    OptionsScreen_DebugModeEnabled = gameObjs.UpDownButton(0,0,14)
    OptionsScreen_RandomWindowTitle = gameObjs.UpDownButton(0,0,14)
    OptionsScreen_NumberFormatting = gameObjs.UpDownButton(0,0,14)

def Update():
    global OptionsScreen_DebugModeEnabled
    global OptionsScreen_RandomWindowTitle
    global OptionsScreen_NumberFormatting
    global ElementsX
    global ElementsY

    if OptionsScreen_DebugModeEnabled .ButtonState == 2 or OptionsScreen_DebugModeEnabled.ButtonState == 1:
        current_val = gameMain.DefaultCnt.Get_RegKey("/OPTIONS/debug_enabled", bool)
        if current_val:
            gameMain.DefaultCnt.Write_RegKey("/OPTIONS/debug_enabled", "False")
        if not current_val:
            gameMain.DefaultCnt.Write_RegKey("/OPTIONS/debug_enabled", "True")

    if OptionsScreen_RandomWindowTitle .ButtonState == 2 or OptionsScreen_RandomWindowTitle.ButtonState == 1:
        current_val = gameMain.DefaultCnt.Get_RegKey("/OPTIONS/random_title", bool)

        if current_val:
            gameMain.DefaultCnt.Write_RegKey("/OPTIONS/random_title", "False")
        if not current_val:
            gameMain.DefaultCnt.Write_RegKey("/OPTIONS/random_title", "True")

    if OptionsScreen_NumberFormatting .ButtonState == 2 or OptionsScreen_NumberFormatting.ButtonState == 1:
        current_val = gameMain.DefaultCnt.Get_RegKey("/OPTIONS/format_numbers", bool)

        if current_val:
            gameMain.DefaultCnt.Write_RegKey("/OPTIONS/format_numbers", "False")
        if not current_val:
            gameMain.DefaultCnt.Write_RegKey("/OPTIONS/format_numbers", "True")

    OptionsScreen_DebugModeEnabled.Set_X(ElementsX + 20)
    OptionsScreen_RandomWindowTitle.Set_X(ElementsX + 20)
    OptionsScreen_NumberFormatting.Set_X(ElementsX + 20)

    OptionsScreen_DebugModeEnabled.Set_Y(ElementsY + 50)
    OptionsScreen_RandomWindowTitle.Set_Y(ElementsY + 75)
    OptionsScreen_NumberFormatting.Set_Y(ElementsY + 100)

def Render(DISPLAY):
    global OptionsScreen_DebugModeEnabled
    global OptionsScreen_RandomWindowTitle
    global OptionsScreen_NumberFormatting

    OptionsScreen_DebugModeEnabled.Render(DISPLAY)
    OptionsScreen_RandomWindowTitle.Render(DISPLAY)
    OptionsScreen_NumberFormatting.Render(DISPLAY)

    # -- Debug Mode -- #
    gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 14, gameMain.DefaultCnt.Get_RegKey("/strings/settings/debug_mode") + str(gameMain.DefaultCnt.Get_RegKey("/OPTIONS/debug_enabled")), (240, 240, 240), ElementsX + 95, ElementsY + 52, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

    # -- Random Title -- #
    gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 14, gameMain.DefaultCnt.Get_RegKey("/strings/settings/random_title") + str(gameMain.DefaultCnt.Get_RegKey("/OPTIONS/random_title")), (240, 240, 240), ElementsX + 95, ElementsY + 77, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

    # -- Number Formatting -- #
    gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 14, gameMain.DefaultCnt.Get_RegKey("/strings/settings/number_formatting") + str(gameMain.DefaultCnt.Get_RegKey("/OPTIONS/format_numbers")), (240, 240, 240), ElementsX + 95, ElementsY + 102, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))



def EventUpdate(event):
    global OptionsScreen_DebugModeEnabled
    global OptionsScreen_RandomWindowTitle
    global OptionsScreen_NumberFormatting

    OptionsScreen_DebugModeEnabled.Update(event)
    OptionsScreen_RandomWindowTitle.Update(event)
    OptionsScreen_NumberFormatting.Update(event)