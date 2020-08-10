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

from Fogoso import MAIN as gameMain
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso.MAIN.Screens import Game as ScreenGame
from Fogoso.MAIN.Screens import Settings as ScreenSettings
from Fogoso.MAIN.Screens import Intro as ScreenIntro
from Fogoso.MAIN import ScreenTransition as transition
from Fogoso import MAIN as gameMainObj
from Fogoso.MAIN.Window import Tips as tipsWindow
import pygame, sys
import importlib
import time
from random import randint

# -- Vars
Animation_Value = -300
Animation_ValueAdder = 1
Animation_CurrentAnim = 0
Animation_Enabled = True
Animation_NextScreen = 0

CommonScreenObj = pygame.Surface
ControlsInitialized = False

# -- Objects Declaration -- #
PlayButton = gameObjs.Button
SettingsButton = gameObjs.Button
IntroSpriteButton = gameObjs.SpriteButton

def Initialize(DISPLAY):
    global PlayButton
    global SettingsButton
    global IntroSpriteButton
    PlayButton = gameObjs.Button(pygame.Rect(50, 50, 0, 0), gameMain.DefaultCnt.Get_RegKey("/strings/main_menu/play_button"), 18)
    SettingsButton = gameObjs.Button(pygame.Rect(50 ,50 ,0 ,0), gameMain.DefaultCnt.Get_RegKey("/strings/main_menu/settings_button"), 18)
    gameMainObj.ClearColor = (1, 20, 30)
    IntroSpriteButton = gameObjs.SpriteButton(pygame.Rect(0,0,47, 45), ("/icon.png","/icon.png","/icon.png"))

    print("GameMenu : Initialize")
    tipsWindow.Initialize(DISPLAY)

def EventUpdate(event):
    global PlayButton
    global SettingsButton
    global ControlsInitialized
    global IntroSpriteButton

    if ControlsInitialized:
        PlayButton.Update(event)
        SettingsButton.Update(event)
        IntroSpriteButton.EventUpdate(event)

        tipsWindow.EventUpdate(event)

def GameDraw(DISPLAY):
    global PlayButton
    global SettingsButton
    global CommonScreenObj
    global ControlsInitialized
    global IntroSpriteButton
    CommonScreenObj = DISPLAY

    if ControlsInitialized:
        gameObjs.Draw_Panel(DISPLAY, (Animation_Value, 0, 300, DISPLAY.get_height()))

        gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 18, gameMain.DefaultCnt.Get_RegKey("/strings/main_menu/game_title"), (240, 250, 250), Animation_Value + 15, 20, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

        PlayButton.Render(DISPLAY)
        SettingsButton.Render(DISPLAY)

        IntroSpriteButton.Render(DISPLAY)
        gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 10, gameMain.DefaultCnt.Get_RegKey("/strings/main_menu/about"), (240, 250, 250), IntroSpriteButton.Rectangle[0] + IntroSpriteButton.Rectangle[2] + 5, IntroSpriteButton.Rectangle[1] + 3, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

        tipsWindow.Draw(DISPLAY)


MenuDelay = 0
def Update():
    global PlayButton
    global SettingsButton
    global CommonScreenObj
    global Animation_Value
    global Animation_Enabled
    global Animation_CurrentAnim
    global ControlsInitialized
    global MenuDelay
    global Animation_ValueAdder
    global Animation_NextScreen
    global IntroSpriteButton

    if not ControlsInitialized:
        MenuDelay += 1
        if MenuDelay > 1:
            MenuDelay = 0
            ControlsInitialized = True

    UpdateAnimation()

    if ControlsInitialized:
        tipsWindow.Update()
        # -- Menu Buttons Click -- #
        if PlayButton.ButtonState == 2:
            Animation_NextScreen = 1
            Animation_Enabled = True

        elif SettingsButton.ButtonState == 2:
            Animation_NextScreen = 2
            Animation_Enabled = True

        elif IntroSpriteButton.ButtonState == 2:
            Animation_NextScreen = -1
            Animation_Enabled = True

        # -- Update Play Button Position -- #
        PlayButton.Set_X(Animation_Value + 20)
        PlayButton.Set_Y(CommonScreenObj.get_height() / 2 - PlayButton.Rectangle[3])

        # -- Update Settings Button Position -- #
        SettingsButton.Set_X(PlayButton.Rectangle[0])
        SettingsButton.Set_Y(PlayButton.Rectangle[1] + SettingsButton.Rectangle[3] + 5)

        # -- Update Intro Button Position -- #
        IntroSpriteButton.Set_X(Animation_Value + 15)
        IntroSpriteButton.Set_Y(CommonScreenObj.get_height() - IntroSpriteButton.Rectangle[3] - 15)

def UpdateAnimation():
    global Animation_Enabled
    global Animation_CurrentAnim
    global Animation_ValueAdder
    global Animation_Value
    global Animation_NextScreen

    if Animation_Enabled:
        if Animation_CurrentAnim == 0:
            Animation_ValueAdder += 2
            Animation_Value += Animation_ValueAdder

            if Animation_Value >= 0:
                Animation_Value = 0
                Animation_ValueAdder = 1
                Animation_Enabled = False
                Animation_CurrentAnim = 1

        if Animation_CurrentAnim == 1:
            Animation_ValueAdder += 2
            Animation_Value -= Animation_ValueAdder

            if Animation_Value <= -300:
                Animation_Value = -300
                Animation_Enabled = True
                Animation_CurrentAnim = 0
                Animation_ValueAdder = 1

                ScreenSettings.ScreenToReturn = 0

                transition.Run()
                gameMain.SetScreen_ByID(Animation_NextScreen)