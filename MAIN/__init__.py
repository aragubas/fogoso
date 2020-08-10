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
# -- ENGINE imports -- #
from ENGINE import utils
from ENGINE import MAIN
from ENGINE import fx
from ENGINE import appData
from ENGINE import shape
from ENGINE import cntMng
import ENGINE as tge

# -- Fogoso Module Imports -- #
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso.MAIN.Screens import Game as ScreenGame
from Fogoso.MAIN.Screens import MainMenu as ScreenMenu
from Fogoso.MAIN.Screens import Settings as ScreenSettings
from Fogoso.MAIN.Screens import Test as ScreenTest
from Fogoso.MAIN import GameVariables as gameVar
from Fogoso.MAIN.Screens import Intro as ScreenIntro
from Fogoso.MAIN.Screens.Game import MapRender as ScreenMap
from Fogoso.MAIN import GameVariables as save
from Fogoso.MAIN import ScreenTransition as transition
from Fogoso.MAIN import OverlayDialog as dialog
from Fogoso import MAIN as gameMain

# -- MISC Imports -- #
from random import randint
import pygame, sys, traceback


# -- Cursor Variables -- #
Cursor_Position = (20, 20)
Cursor_CurrentLevel = 0  #-- 0 = Arrow, 1 = Resize, 2 = Move, 3 = Hand, 4 = Ibeam, 5 = Pirate *x cursor*
CursorW = 0
CursorH = 0

# -- Engine Options -- #
Engine_MaxFPS = 0
Engine_ResW = 800
Engine_ResH = 600

# -- Last Error Overlay -- #
LastErrorText = ""
LastErrorTextEnabled = False
LastErrorTextDeltaTime = 0

# -- Objects -- #
DefaultDisplay = pygame.Surface((0, 0))

# -- Screens -- #
CurrentUpdate = ScreenIntro
ClearColor = (0, 0, 0)

# -- Error Message -- #
ErrorMessageEnabled = False
ErrorMessage = 'null'
ErrorMessageDelay = 0

CursorX = 0
CursorY = 0

OverlayDialogEnabled = False
ScreenLastFrame = pygame.Surface((0, 0))

# -- Content Managers -- #
DefaultCnt = cntMng.ContentManager

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
    global OverlayDialogEnabled
    global ScreenLastFrame
    global CurrentUpdate
    global DefaultCnt

    # -- Clear the Surface -- #
    DefaultDisplay = DISPLAY
    DISPLAY.fill(ClearColor)

    if not DefaultCnt.Get_RegKey("/OPTIONS/debug_enabled", bool):
        try:
            if not OverlayDialogEnabled:
                CurrentUpdate.GameDraw(DefaultDisplay)

                ScreenLastFrame = DefaultDisplay.copy()

            else:
                dialog.Draw(DISPLAY)

        except Exception as ex:
            WriteErrorLog(ex, "GameDraw", False)
    else:
        if not OverlayDialogEnabled:
            CurrentUpdate.GameDraw(DefaultDisplay)

            ScreenLastFrame = DefaultDisplay.copy()
        else:
            dialog.Draw(DISPLAY)

    # -- Render the Error Message -- #
    if ErrorMessageEnabled:
        ErrorMessageDelay += 1

        gameObjs.Draw_Panel(DISPLAY, (0, 5, DISPLAY.get_width(), gameMain.DefaultCnt.GetFont_height("/PressStart2P.ttf", gameMain.DefaultCnt.Get_RegKey("/props/error_message_text_size"), ErrorMessage)))
        SPRITE.FontRender(DISPLAY, "/PressStart2P.ttf", gameMain.DefaultCnt.Get_RegKey("/props/error_message_text_size", int), ErrorMessage, (150, 50, 50), 0, 5, False)

        if ErrorMessageDelay >= gameMain.DefaultCnt.Get_RegKey("/props/error_message_delay_max", int):
            ErrorMessageDelay = 0
            ErrorMessageEnabled = False

    # -- Render Cursor -- #
    gameMain.DefaultCnt.ImageRender(DefaultDisplay, "/cursors/{0}.png".format(str(Cursor_CurrentLevel)), Cursor_Position[0], Cursor_Position[1])

    # -- Render the Transition -- #
    transition.Render(DefaultDisplay)

    if DefaultCnt.Get_RegKey("/OPTIONS/debug_enabled", bool):
        gameMain.DefaultCnt.FontRender(DefaultDisplay, "/PressStart2P.ttf", 10, "FPS: {0}".format(utils.FormatNumber(MAIN.clock.get_fps())), (240, 240, 240), 5, 5, backgroundColor=(5, 8, 13))

    # -- Render the Error Overlay -- #
    if LastErrorTextEnabled:
        LastErrorTextDeltaTime += 1

        gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 9, LastErrorText, (200, 0, 0), 5, 5, False, (10, 20, 27))

        if LastErrorTextDeltaTime >= 1500:
            LastErrorTextDeltaTime = 0
            LastErrorTextEnabled = False
            LastErrorText = ""


def GeneratedWindowTitle():
    if DefaultCnt.Get_RegKey("/OPTIONS/random_title", bool):
        NumberMax = DefaultCnt.Get_RegKey("/strings/gme_wt/all", int)
        Current = randint(0, NumberMax)

        MAIN.ReceiveCommand(5, "Fogoso : {0}".format(DefaultCnt.Get_RegKey("/strings/gme_wt/{0}".format(Current))))

def Update():  # -- Engine Required Function
    global CursorW
    global CursorH
    global OverlayDialogEnabled
    global CurrentUpdate
    global DefaultCnt

    # -- Set the Cursor Size -- #
    CursorW = DefaultCnt.Get_RegKey("/CursorSize/" + str(Cursor_CurrentLevel) + "/w")
    CursorH = DefaultCnt.Get_RegKey("/CursorSize/" + str(Cursor_CurrentLevel) + "/h")

    if not DefaultCnt.Get_RegKey("/OPTIONS/debug_enabled", bool):
        try:
            if not OverlayDialogEnabled:
                CurrentUpdate.Update()
            else:
                dialog.Update()

        except Exception as ex:
            WriteErrorLog(ex, "Update", True)
    else:
        if not OverlayDialogEnabled:
            CurrentUpdate.Update()
        else:
            dialog.Update()

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

def ScreensInitialize(DISPLAY):
    ScreenTest.Initialize(DISPLAY)
    ScreenIntro.Initialize(DISPLAY)
    ScreenMenu.Initialize(DISPLAY)
    ScreenGame.Initialize(DISPLAY)
    ScreenSettings.Initialize()
    ScreenMap.Initialize()

def SetScreen_ByID(ScreenID):
    global CurrentUpdate

    if ScreenID == -2:
        CurrentUpdate = ScreenTest

    elif ScreenID == -1:
        CurrentUpdate = ScreenIntro

    elif ScreenID == 0:
        CurrentUpdate = ScreenMenu

    elif ScreenID == 1:
        CurrentUpdate = ScreenGame

    elif ScreenID == 2:
        CurrentUpdate = ScreenSettings

    elif ScreenID == 3:
        CurrentUpdate = ScreenMap

def EventUpdate(event):  # -- Engine Required Function
    global Cursor_Position
    global CursorX
    global CursorY
    global DefaultDisplay
    global CursorW
    global CursorH
    global OverlayDialogEnabled
    # -- Update Cursor Location -- #
    if event.type == pygame.MOUSEMOTION:
        Cursor_Position = pygame.mouse.get_pos()

    if not DefaultCnt.Get_RegKey("/OPTIONS/debug_enabled", bool):
        try:
            if not OverlayDialogEnabled:
                CurrentUpdate.EventUpdate(event)
            else:
                dialog.EventUpdate(event)

        except Exception as ex:
            WriteErrorLog(ex, "EventUpdate", False)
    else:
        if not OverlayDialogEnabled:
            CurrentUpdate.EventUpdate(event)
        else:
            dialog.EventUpdate(event)


def LoadOptions():
    global Engine_ResH
    global Engine_ResW
    global Engine_MaxFPS
    global Cursor_CurrentLevel
    global DefaultCnt
    print("LoadOptions : Init")

    # -- Engine Flags -- #
    Engine_MaxFPS = DefaultCnt.Get_RegKey("/OPTIONS/maxFPS", int)

    # -- Fade Effect -- #
    transition.Initialize()

    print("LoadOptions : Data loading complete")

    
def Initialize(DISPLAY):  # -- Engine Required Function
    global DefaultCnt
    print("Fogoso : Game Initialization Called")

    DefaultCnt = cntMng.ContentManager()

    # -- Load All Fonts -- #
    DefaultCnt.SetFontPath("Data/FONT")

    # -- Load Default SpriteSet -- #
    DefaultCnt.LoadSpritesInFolder("Data/SPRITE")

    # -- Load Default RegKeys Set -- #
    DefaultCnt.LoadRegKeysInFolder("Data/REG")

    # -- Load Default Sounds -- #
    DefaultCnt.LoadSoundsInFolder("Data/SOUND")

    # -- Load Engine Options -- #
    LoadOptions()

    # -- Apply Engine Options -- #
    SetWindowParameters()
    GeneratedWindowTitle()

    # -- Set the Default Screen -- #
    SetScreen_ByID(DefaultCnt.Get_RegKey("/props/CurrentScreen", int))

    if not DefaultCnt.Get_RegKey("/OPTIONS/debug_enabled", bool):
        try:
            ScreensInitialize(DISPLAY)

        except Exception as ex:
            WriteErrorLog(ex,"Initialize", True)

    else:
        ScreensInitialize(DISPLAY)

    dialog.Initialize()

def Exit():
    print("Fogoso.Exit called.")

def SetWindowParameters():
    global DefaultDisplay
    global Engine_MaxFPS

    DefaultDisplay = pygame.Surface((DefaultCnt.Get_RegKey("/props/default_resW", int), DefaultCnt.Get_RegKey("/props/default_resH", int)))

    MAIN.ReceiveCommand(1, "{0}x{1}".format(str(DefaultCnt.Get_RegKey("/props/default_resW", int)), str(DefaultCnt.Get_RegKey("/props/default_resH", int))))
    MAIN.ReceiveCommand(0, Engine_MaxFPS)

    pygame.mouse.set_visible(False)

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

        gameMain.DefaultCnt.Write_RegKey(ErrorLogName, ExcTraceback)
