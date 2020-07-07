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
from ENGINE import REGISTRY as reg
from ENGINE import TaiyouMain as taiyouMain
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso.MAIN.Screens import Game as ScreenGame
from Fogoso.MAIN.Screens import MainMenu as ScreenMenu
from Fogoso.MAIN.Screens import Settings as ScreenSettings
from Fogoso.MAIN import GameVariables as gameVar
from Fogoso.MAIN.Screens import Intro as ScreenIntro
from Fogoso.MAIN.Screens.Game import MapRender as ScreenMap
from ENGINE import SPRITE as sprite
from random import randint
from Fogoso.MAIN import GameVariables as save
from ENGINE import DEBUGGING as debug
from Fogoso.MAIN import ScreenTransition as transition
import pygame, sys, traceback


# -- Cursor Variables -- #
Cursor_Position = list((20, 20))
Cursor_CurrentLevel = 0  #-- 0 = Arrow, 1 = Resize, 2 = Move, 3 = Hand, 4 = Ibeam, 5 = Pirate *x cursor*
CursorW = 0
CursorH = 0

# -- Engine Options -- #
Engine_MaxFPS = 0
Engine_ResW = 1024
Engine_ResH = 720

# -- Last Error Overlay -- #
LastErrorText = ""
LastErrorTextEnabled = False
LastErrorTextDeltaTime = 0

# -- Objects -- #
DefaultDisplay = pygame.Surface((0, 0))

# -- Screens -- #
CurrentScreen = 3
ClearColor = (0, 0, 0)

# -- Error Message -- #
ErrorMessageEnabled = False
ErrorMessage = 'null'
ErrorMessageDelay = 0

CursorX = 0
CursorY = 0


def GameDraw(DISPLAY):  # -- Engine Required Function
    global DefaultDisplay
    global LastErrorText
    global LastErrorTextDeltaTime
    global LastErrorTextEnabled
    global DefaultDisplay
    global CursorW
    global CursorH
    global ClearColor
    global ErrorMessageEnabled
    global ErrorMessage
    global ErrorMessageDelay

    # -- Clear the Surface -- #
    DefaultDisplay = DISPLAY
#    DISPLAY.fill(ClearColor)

    if not reg.ReadKey_bool("/OPTIONS/debug_enabled"):
        try:
            ScreenDraw(DefaultDisplay)
        except Exception as ex:
            WriteErrorLog(ex, "GameDraw", False)
    else:
        ScreenDraw(DefaultDisplay)

    # -- Render the Error Message -- #
    if ErrorMessageEnabled:
        ErrorMessageDelay += 1

        gameObjs.Draw_Panel(DISPLAY, (0,5,DISPLAY.get_width(), sprite.GetFont_height("/PressStart2P.ttf", reg.ReadKey_int("/props/error_message_text_size"), ErrorMessage)))
        sprite.FontRender(DISPLAY, "/PressStart2P.ttf", reg.ReadKey_int("/props/error_message_text_size"), ErrorMessage, (150, 50, 50), 0, 5, False)

        if ErrorMessageDelay >= reg.ReadKey_int("/props/error_message_delay_max"):
            ErrorMessageDelay = 0
            ErrorMessageEnabled = False

    # -- Render Cursor -- #
    sprite.ImageRender(DefaultDisplay, "/cursors/{0}.png".format(str(Cursor_CurrentLevel)), Cursor_Position[0], Cursor_Position[1])

    # -- Render the Transition -- #
    transition.Render(DefaultDisplay)

    # -- Render the Error Overlay -- #
    if LastErrorTextEnabled:
        LastErrorTextDeltaTime += 1

        sprite.Shape_Rectangle(DISPLAY, (0, 0, 0), (0, 2, DISPLAY.get_width() , sprite.GetFont_height("/PressStart2P.ttf", 9, LastErrorText) * 2 + 4))
        sprite.FontRender(DISPLAY, "/PressStart2P.ttf", 9, LastErrorText, (200, 0, 0), 5, 5, False)

        if LastErrorTextDeltaTime >= 1500:
            LastErrorTextDeltaTime = 0
            LastErrorTextEnabled = False
            LastErrorText = ""

def GeneratedWindowTitle():
    if reg.ReadKey_bool("/OPTIONS/random_title"):
        NumberMax = reg.ReadKey_int("/strings/gme_wt/all")
        Current = randint(0, NumberMax)

        taiyouMain.ReceiveCommand("SET_TITLE;{0}{1}".format("Fogoso : ", reg.ReadKey("/strings/gme_wt/" + str(Current))))

def Update():  # -- Engine Required Function
    global CursorW
    global CursorH
    
    # -- Set the Cursor Size -- #
    CursorW = reg.ReadKey_int("/CursorSize/" + str(Cursor_CurrentLevel) + "/w")
    CursorH = reg.ReadKey_int("/CursorSize/" + str(Cursor_CurrentLevel) + "/h")

    if not reg.ReadKey_bool("/OPTIONS/debug_enabled"):
        try:
            ScreensUpdate()
        except Exception as ex:
            WriteErrorLog(ex, "Update", True)
    else:
        ScreensUpdate()

    # -- Update the Screen Transtion -- #
    try:
        transition.Update()
    except Exception as ex:
        WriteErrorLog(ex, "TransitionUpdate", False)


def SendErrorMessage(Message):
    global ErrorMessageEnabled
    global ErrorMessage
    global ErrorMessageDelay
    ErrorMessage = Message
    ErrorMessageEnabled = True
    ErrorMessageDelay = 0

def ScreensUpdate():
    if CurrentScreen == -1:
        ScreenIntro.Update()
    elif CurrentScreen == 0:
        ScreenMenu.Update()
    elif CurrentScreen == 1:
        ScreenGame.Update()
    elif CurrentScreen == 2:
        ScreenSettings.Update()
    elif CurrentScreen == 3:
        ScreenMap.Update()

def ScreenDraw(DefaultDisplay):
    if CurrentScreen == -1:
        ScreenIntro.GameDraw(DefaultDisplay)
    elif CurrentScreen == 0:
        ScreenMenu.GameDraw(DefaultDisplay)
    elif CurrentScreen == 1:
        ScreenGame.GameDraw(DefaultDisplay)
    elif CurrentScreen == 2:
        ScreenSettings.GameDraw(DefaultDisplay)
    elif CurrentScreen == 3:
        ScreenMap.GameDraw(DefaultDisplay)

def ScreenEventUpdate(event):
    if CurrentScreen == -1:
        ScreenIntro.EventUpdate(event)
    elif CurrentScreen == 0:
        ScreenMenu.EventUpdate(event)
    elif CurrentScreen == 1:
        ScreenGame.EventUpdate(event)
    elif CurrentScreen == 2:
        ScreenSettings.EventUpdate(event)
    elif CurrentScreen == 3:
        ScreenMap.EventUpdate(event)

def ScreensInitialize(DISPLAY):
    if CurrentScreen == -1:
        ScreenIntro.Initialize(DISPLAY)
    elif CurrentScreen == 0:
        ScreenMenu.Initialize(DISPLAY)
    elif CurrentScreen == 1:
        ScreenGame.Initialize(DISPLAY)
    elif CurrentScreen == 2:
        ScreenSettings.Initialize()
    elif CurrentScreen == 3:
        ScreenMap.Initialize()

def EventUpdate(event):  # -- Engine Required Function
    global Cursor_Position
    global CursorX
    global CursorY
    global DefaultDisplay
    global CursorW
    global CursorH
    # -- Update Cursor Location -- #
    if event.type == pygame.MOUSEMOTION:
        Cursor_Position[0], Cursor_Position[1] = pygame.mouse.get_pos()

    if not reg.ReadKey_bool("/OPTIONS/debug_enabled"):
        try:
            ScreenEventUpdate(event)
        except Exception as ex:
            WriteErrorLog(ex, "EventUpdate", False)
    else:
        ScreenEventUpdate(event)

def LoadOptions():
    global Engine_ResH
    global Engine_ResW
    global Engine_MaxFPS
    global Cursor_CurrentLevel
    print("LoadOptions : Init")

    # -- Engine Flags -- #
    Engine_MaxFPS = reg.ReadKey_int("/OPTIONS/maxFPS")

    # -- Fade Effect -- #
    transition.Initialize()

    print("LoadOptions : Data loading complete")

    
def Initialize(DISPLAY):  # -- Engine Required Function
    global CurrentScreen
    print("Fogoso : Game Initialization Called")

    # -- Load Engine Options -- #
    LoadOptions()

    # -- Apply Engine Options -- #
    SetWindowParameters()
    GeneratedWindowTitle()

    # -- Set the Default Screen -- #
    CurrentScreen = reg.ReadKey_int("/props/CurrentScreen")

    if not reg.ReadKey_bool("/OPTIONS/debug_enabled"):
        try:
            ScreensInitialize(DISPLAY)

        except Exception as ex:
            WriteErrorLog(ex,"Initialize", True)

    else:
        ScreensInitialize(DISPLAY)


def Unload():  # -- Engine Required Function
    gameVar.Unload()

def SetWindowParameters():
    global DefaultDisplay
    global Engine_MaxFPS

    DefaultDisplay = pygame.Surface((reg.ReadKey_int("/props/default_resW"), reg.ReadKey_int("/props/default_resH")))

    taiyouMain.ReceiveCommand("SET_RESOLUTION:{0}:{1}".format(str(reg.ReadKey_int("/props/default_resW")), str(reg.ReadKey_int("/props/default_resH"))))
    taiyouMain.ReceiveCommand("SET_FPS:" + str(Engine_MaxFPS))

def WriteErrorLog(ex, func, ExitWhenFinished=False):
    global LastErrorText
    global LastErrorTextEnabled

    print("A fatal error has been occoured:\n" + str(ex))

    ExcTraceback = traceback.format_exc()

    LastErrorText = str(ex) + "\nfunc(" + func + ")"
    LastErrorTextEnabled = True

    if ExitWhenFinished:
        ErrorLogName = "/LOG/crash_func(" + str(func) + ")"
        print("WriteErrorLog ; Error log file write at:\n" + ErrorLogName)

        print("WriteErrorLog ; Exception Traceback:\n\n" + ExcTraceback + "\n\n")

        reg.WriteKey(ErrorLogName, ExcTraceback)
