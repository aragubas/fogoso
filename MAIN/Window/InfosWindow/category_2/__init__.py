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
from Fogoso.MAIN import PlanetData as planets

import pygame
PlanetAnimation = utils.AnimationController
AnimationValue = 1
InfosList = gameObjs.ValueBlock

def Initialize():
    global PlanetAnimation
    global InfosList

    InfosList = gameObjs.ValuesView(pygame.Rect(0, 0, 320, 200), "ceira")
    PlanetAnimation = utils.AnimationController(1.2)

def Render(DISPLAY):
    global AnimationValue
    global InfosList

    # -- Render Planet Icon -- #
    gameMain.DefaultCnt.ImageRender(DISPLAY, "/icons/planet/id_{0}.png".format(save.PlanetID), (DISPLAY.get_width() / 2 - 123 / 2) - (AnimationValue - 255) / 2, 25 - (AnimationValue - 255), 123 + (AnimationValue - 255), 123 + (AnimationValue - 255), Opacity=AnimationValue)

    # -- Render Planet Name -- #
    gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 13, planets.GetPlanetName_ByID(save.PlanetID), (230, 230, 230), DISPLAY.get_width() / 2 - gameMain.DefaultCnt.GetFont_width("/PressStart2P.ttf", 13, planets.GetPlanetName_ByID(save.PlanetID)) / 2, 157 - (AnimationValue - 255), Opacity=AnimationValue)

    # -- Render the Value Block -- #
    InfosList.Draw(DISPLAY)

    InfosList.Rectangle[1] = DISPLAY.get_height() - InfosList.Rectangle[3] + 120 - (AnimationValue - 255)

def Reset():
    PlanetAnimation.Enabled = True
    PlanetAnimation.CurrentMode = True
    PlanetAnimation.Value = 0
    PlanetAnimation.ValueMultiplier = 0


def Update():
    global PlanetAnimation
    global AnimationValue
    global InfosList

    PlanetAnimation.Update()

    UpdateValues()

    AnimationValue = int(PlanetAnimation.Value + 1)


def UpdateValues():
    global InfosList

    InfosList.ChangeValue("Inflation", utils.FormatNumber(planets.GetPlanetInflation_ByID(save.PlanetID)))


def EventUpdate(event):
    pass