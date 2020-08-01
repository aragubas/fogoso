#!/usr/bin/ python3.7
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

from Fogoso.MAIN.Screens import Game as gameScr
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso.MAIN import GameItems as gameItems
from ENGINE import utils
from ENGINE import fx
from Fogoso import MAIN as gameMain
from ENGINE import *
import pygame
print("Fogoso Screens Transtion, version 1.0")

# -- Variables -- #
FadeEffectState = False
FadeEffectCurrentState = 0
FadeEffectValue = 0
FadeEffectSpeed = 5
FadeEffectStyle = 0 # 0 = Blur, 1 = Pixalizate, 2 = Blur + Pixalizate, 3 = Pixalizate + Blur

def Update():
    global FadeEffectSpeed
    global FadeEffectValue
    global FadeEffectState
    global FadeEffectCurrentState

    # -- Update the Fade Effect -- #
    if FadeEffectState:
        if FadeEffectCurrentState == 0:
            FadeEffectValue -= FadeEffectSpeed

            if FadeEffectValue <= 0:
                FadeEffectState = False
                FadeEffectValue = 0
                FadeEffectCurrentState = 0

def Render(DISPLAY):
    if FadeEffectValue > 0:
        FadeEffect = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()))
        if gameMain.DefaultCnt.Get_RegKey("/OPTIONS/random_title"):
            gameMain.GeneratedWindowTitle()

        if FadeEffectStyle == 0:
            FadeEffect.blit(fx.Surface_Blur(DISPLAY, FadeEffectValue), (0, 0))

        elif FadeEffectStyle == 1:
            FadeEffect.blit(fx.Surface_Blur(DISPLAY, FadeEffectValue, True), (0, 0))

        elif FadeEffectStyle == 2:
            FadeEffect.blit(fx.Surface_Blur(fx.Surface_Blur(DISPLAY, FadeEffectValue), FadeEffectValue, True), (0, 0))

        elif FadeEffectStyle == 3:
            FadeEffect.blit(fx.Surface_Blur(fx.Surface_Blur(DISPLAY, FadeEffectValue), FadeEffectValue, True), (0, 0))

        DISPLAY.blit(FadeEffect, (0, 0))


def Run():
    global FadeEffectCurrentState
    global FadeEffectValue
    global FadeEffectState
    FadeEffectCurrentState = 0
    FadeEffectValue = 255
    FadeEffectState = True

def Initialize():
    global FadeEffectSpeed
    global FadeEffectStyle
    # -- Fade Effect -- #
    FadeEffectSpeed = gameMain.DefaultCnt.Get_RegKey("/OPTIONS/fade_flash_speed", int)

    # -- Fade Style -- #
    FadeEffectStyle = gameMain.DefaultCnt.Get_RegKey("/OPTIONS/fade_flash_style", int)

    Run()