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
from ENGINE import APPDATA as reg
from Fogoso.MAIN import GameVariables as save
from Fogoso import MAIN as gameMain
from Fogoso.MAIN import ClassesUtils as gtk
import pygame

# -- Variables -- #
SecondsText = ""
DateText = ""
ClockBoxPos = (0, 0, 0, 0)
ClockBox = pygame.Surface
CommonSurface = None

def Draw(HUD_Surface):
    global SecondsText
    global DateText
    global ClockBoxPos
    global ClockBox
    global CommonSurface

    if CommonSurface == None:
        CommonSurface = HUD_Surface
        return
    CommonSurface = HUD_Surface

    # -- Render Background -- #
    gtk.Draw_Panel(ClockBox, (0, 0, ClockBoxPos[2] - 2, ClockBoxPos[3] - 2), True)

    # -- Locations -- #
    TimeTextY = 7
    DayTextY = 22

    # -- Time -- #
    gameMain.DefaultCnt.FontRender(ClockBox, "/PressStart2P.ttf", 10, SecondsText, (0, 0, 0), ClockBox.get_width() / 2 - gameMain.DefaultCnt.GetFont_width("/PressStart2P.ttf", 10, SecondsText) / 2 + 2, TimeTextY - 2, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))
    gameMain.DefaultCnt.FontRender(ClockBox, "/PressStart2P.ttf", 10, SecondsText, (230, 230, 230), ClockBox.get_width() / 2 - gameMain.DefaultCnt.GetFont_width("/PressStart2P.ttf", 10, SecondsText) / 2, TimeTextY, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

    # -- Day -- #
    gameMain.DefaultCnt.FontRender(ClockBox, "/PressStart2P.ttf", 10, DateText, (0, 0, 0), ClockBox.get_width() / 2 - gameMain.DefaultCnt.GetFont_width("/PressStart2P.ttf", 10, DateText) / 2 + 2, DayTextY - 2, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))
    gameMain.DefaultCnt.FontRender(ClockBox, "/PressStart2P.ttf", 10, DateText, (230, 230, 230), ClockBox.get_width() / 2 - gameMain.DefaultCnt.GetFont_width("/PressStart2P.ttf", 10, DateText) / 2, DayTextY, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

    gameMain.shape.Shape_Rectangle(ClockBox, (0, 0, 0), (0, 0, ClockBoxPos[2], ClockBoxPos[3]), 3, 5)

    HUD_Surface.blit(ClockBox, (ClockBoxPos[0], ClockBoxPos[1]))


def Update():
    global SecondsText
    global DateText
    global ClockBoxPos
    global ClockBox
    global CommonSurface

    if CommonSurface == None:
        return

    ClockBoxPos = (CommonSurface.get_width() / 2 - 300 / 2, 0, 300, 40)
    ClockBox = pygame.Surface((ClockBoxPos[2], ClockBoxPos[3]), pygame.SRCALPHA)

    DateText = gameMain.DefaultCnt.Get_RegKey("/strings/game/calendar").format(str(save.CurrentDate_Day), str(save.CurrentDate_Month), str(save.CurrentDate_Year), str(save.CurrentDate_MonthLimiter), str(save.CurrentDate_YearLimiter))
    SecondsText = gameMain.DefaultCnt.Get_RegKey("/strings/game/clock").format(str(save.CurrentDate_Minute), str(save.CurrentDate_Second), str(save.CurrentDate_DayLimiter), str(save.CurrentDate_MinuteLimiter))
