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

# -- Fogoso Imports -- #
from Fogoso.MAIN import GameVariables as save
from Fogoso.MAIN.Screens.Game import Maintenance as maintenance
from Fogoso.MAIN.Window import InfosWindow as handler
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso import MAIN as gameMain

import pygame

DeltaTime = 0
DeltaMax = 50

ValuesViewer = gameObjs.ValuesView

def Initialize():
    global ValuesViewer

    ValuesViewer = gameObjs.ValuesView(pygame.Rect(0, 25, 5, 5), True)

    UpdateValues()

def Render(DISPLAY):
    global ValuesViewer

    if handler.DrawnSurfaceGlob is None:
        return

    # -- Set the Correct Size -- #
    ValuesViewer.Rectangle[2] = handler.DrawnSurfaceGlob.get_width()
    ValuesViewer.Rectangle[3] = handler.DrawnSurfaceGlob.get_height()

    ValuesViewer.Draw(DISPLAY)

def Update():
    global DeltaTime
    global DeltaMax

    DeltaTime += 1

    if DeltaTime >= DeltaMax:
        DeltaTime = 0
        UpdateValues()

def Reset():
    pass

def UpdateValues():
    global ValuesViewer

    if len(ValuesViewer.ValueBlocksList) > 1:
        ValuesViewer.ChangeValue(gameMain.DefaultCnt.Get_RegKey("/strings/window/infos/txt_money_per_click"), utils.FormatNumber(save.Current_MoneyValuePerClick))
        ValuesViewer.ChangeValue(gameMain.DefaultCnt.Get_RegKey("/strings/window/infos/txt_previuos_best"), utils.FormatNumber(save.Current_MoneyPerClickBest))
        ValuesViewer.ChangeValue(gameMain.DefaultCnt.Get_RegKey("/strings/window/infos/txt_money_per_click"), utils.FormatNumber(save.Current_MoneyValuePerClick))
        ValuesViewer.ChangeValue(gameMain.DefaultCnt.Get_RegKey("/strings/window/infos/txt_money_minimum"), utils.FormatNumber(save.Current_MoneyMinimun))

    else:
        ValuesViewer.AddValue(gameMain.DefaultCnt.Get_RegKey("/strings/window/infos/txt_money_per_click"), utils.FormatNumber(save.Current_MoneyValuePerClick))
        ValuesViewer.AddValue(gameMain.DefaultCnt.Get_RegKey("/strings/window/infos/txt_previuos_best"), utils.FormatNumber(save.Current_MoneyPerClickBest))
        ValuesViewer.AddValue(gameMain.DefaultCnt.Get_RegKey("/strings/window/infos/txt_money_per_click"), utils.FormatNumber(save.Current_MoneyValuePerClick))
        ValuesViewer.AddValue(gameMain.DefaultCnt.Get_RegKey("/strings/window/infos/txt_money_minimum"), utils.FormatNumber(save.Current_MoneyMinimun))


def EventUpdate(event):
    pass