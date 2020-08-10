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
from Fogoso.MAIN.Screens import MainMenu as ScreenMenu
from Fogoso import MAIN as gameMain
from Fogoso.MAIN import ScreenTransition as transition
import pygame, os
from random import randint

CurrentLogo_Current = 0
CurrentLogo_AnimType = 0
CurrentLogo_Opacity = 0
CurrentLogo_AnimEnabled = True
CurrentLogo_DeltaBeforeNext = 0
BlackScreenDelay = 0

def Initialize(DISPLAY):
    global CurrentLogo_Current
    global CurrentLogo_AnimType
    global CurrentLogo_Opacity
    global CurrentLogo_AnimEnabled
    print("ScreenLogos : Initialize.")
    CurrentLogo_AnimType = 0
    CurrentLogo_AnimEnabled = True
    CurrentLogo_Opacity = 0
    CurrentLogo_Current = 0
    transition.Run()
    gameMain.ClearColor = (0,0,0)

def Update():
    global CurrentLogo_Current
    global CurrentLogo_AnimType
    global CurrentLogo_Opacity
    global CurrentLogo_AnimEnabled
    global CurrentLogo_DeltaBeforeNext
    global BlackScreenDelay

    if CurrentLogo_AnimEnabled:
        if CurrentLogo_AnimType == 0:
            CurrentLogo_Opacity += gameMain.DefaultCnt.Get_RegKey("/props/intro_adder", int)

            if CurrentLogo_Opacity >= 255 - gameMain.DefaultCnt.Get_RegKey("/props/intro_adder", int):
                CurrentLogo_Opacity = 255
                CurrentLogo_DeltaBeforeNext += 1

                if CurrentLogo_DeltaBeforeNext >= gameMain.DefaultCnt.Get_RegKey("/props/intro_delay", int):
                    CurrentLogo_DeltaBeforeNext = 0
                    CurrentLogo_AnimType = 1

        if CurrentLogo_AnimType == 1:
            CurrentLogo_Opacity -= gameMain.DefaultCnt.Get_RegKey("/props/intro_adder", int)

            if CurrentLogo_Opacity <= 0:
                CurrentLogo_Opacity = 0
                CurrentLogo_Current += 1
                CurrentLogo_DeltaBeforeNext += 1

                if CurrentLogo_DeltaBeforeNext >= gameMain.DefaultCnt.Get_RegKey("/props/intro_delay", int):
                    CurrentLogo_AnimType = 0
                    CurrentLogo_AnimEnabled = True
                    CurrentLogo_DeltaBeforeNext = 0

    # -- Detect Animation End -- #
    if CurrentLogo_Current >= 1:
        BlackScreenDelay += 1

        if BlackScreenDelay >= gameMain.DefaultCnt.Get_RegKey("/props/intro_end_delay", int):
            ScreenMenu.Initialize(gameMain.DefaultDisplay)
            gameMain.SetScreen_ByID(0)
            BlackScreenDelay = 0
            transition.Run()

    # -- Set the Fill Color -- #
    gameMain.CurrentFillColor = (0,0,0)


def GameDraw(DISPLAY):
    global CurrentLogo_Current
    global CurrentLogo_AnimType
    global CurrentLogo_Opacity
    global CurrentLogo_AnimEnabled
    
    LogoSurface = pygame.Surface((790,280))
    BottomTextSurface = pygame.Surface((790, 120))
    LogoSurface.set_alpha(CurrentLogo_Opacity)
    BottomTextSurface.set_alpha(CurrentLogo_Opacity)

    if CurrentLogo_Current == 0:
        gameMain.DefaultCnt.ImageRender(LogoSurface, "/icon.png", 5, 15, 167, 145)
        gameMain.DefaultCnt.FontRender(LogoSurface, "/PressStart2P.ttf", 20, gameMain.DefaultCnt.Get_RegKey("/strings/intro/text") + "\n\n" + gameMain.DefaultCnt.Get_RegKey("/VersionStatus"), (240, 240, 240), 180, 15, True)

        gameMain.DefaultCnt.FontRender(BottomTextSurface, "/PressStart2P.ttf", 10, gameMain.DefaultCnt.Get_RegKey("/strings/intro/license_text"), (250, 250, 250), 5, 5, True)

    DISPLAY.blit(LogoSurface, (DISPLAY.get_width() / 2 - LogoSurface.get_width() / 2, DISPLAY.get_height() / 2 - LogoSurface.get_height() / 2 - 50))
    DISPLAY.blit(BottomTextSurface, (DISPLAY.get_width() / 2 - BottomTextSurface.get_width() / 2, DISPLAY.get_height() / 2 - LogoSurface.get_height() / 2 + BottomTextSurface.get_height() * 2))
    
def EventUpdate(event):
    global CurrentLogo_Current
    global CurrentLogo_AnimType
    global CurrentLogo_Opacity
    global CurrentLogo_AnimEnabled
    
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            CurrentLogo_AnimEnabled = True


