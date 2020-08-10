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
import pygame, os, sys, shutil

from Fogoso.MAIN import ClassesUtils as gtk
from Fogoso import MAIN as fogosoMain
from Fogoso import MAIN as gameMain
import ENGINE as tge
from ENGINE import utils

from ENGINE import APPDATA as reg
from Fogoso.MAIN.OverlayDialog import subscreen1

DialogRectangle = pygame.Rect
CommonDisplay = pygame.Surface
CommonDisplayScreenPos = (0,0)
CommonDisplayInitialized = False
BGDarkSurfaceCreated = False
BGDarkSurface = pygame.Surface((0, 0))

# -- Application Details -- #
ApplicationName = "null"
ApplicationID = "null"
ApplicationVersion = 1.0
ApplicationFolder = "null"
MessageTitle = "null"

# -- Animation Variables -- #
DialogOpctAnim_AnimEnabled = True
DialogOpctAnim_AnimMode = 0
DialogOpctAnim_AnimOpacity = 0
DialogOpctAnim_AnimNumb = 0

DialogOpctAnim_Enabled = False
DialogOpenSoundPlayed = False

# -- Copy of Screen -- #
CopyOfScreen_Last = False
CopyOfScreen_Result = pygame.Surface
CopyOfScreen_BlurAmount = 0
CopyOfScreen_Set = False

Subscreen = 1

def Initialize():
    global DialogRectangle
    global MessageTitle
    global CommonDisplayScreenPos
    DialogRectangle = pygame.Rect(0, 0, 395, 250)

    subscreen1.Initialize()

    CommonDisplayScreenPos = (-1000, -1000)

    MessageTitle = "undefined"

def Draw(Display):
    global DialogRectangle
    global CommonDisplay
    global CommonDisplayInitialized
    global CommonDisplayScreenPos
    global DialogOpctAnim_AnimNumb
    global MessageTitle
    global BGDarkSurfaceCreated
    global BGDarkSurface

    # -- Draw the Copy of Screen -- #
    Draw_ScreenshotOfGameScreen(Display)

    if CommonDisplayInitialized:
        # -- Draw the Background -- #
        gtk.Draw_Panel(CommonDisplay, DialogRectangle)

        # -- Draw the Titlebar -- #
        gameMain.shape.Shape_Rectangle(CommonDisplay, (10, 32, 49), (0, 0, DialogRectangle[2], 25))
        gameMain.DefaultCnt.FontRender(CommonDisplay, "/PressStart2P.ttf", 18, MessageTitle, (240, 240, 240), DialogRectangle[2] / 2 - gameMain.DefaultCnt.GetFont_width("/PressStart2P.ttf", 18, MessageTitle) / 2, 4)

        if Subscreen == 1:
            subscreen1.Draw(CommonDisplay)

        CommonDisplayScreenPos = (Display.get_width() / 2 - 395 / 2, Display.get_height() / 2 - 150 / 2 - DialogOpctAnim_AnimNumb * 2.5 / 3.10)
        if not BGDarkSurfaceCreated:
            BGDarkSurfaceCreated = True
            BGDarkSurface = pygame.Surface((Display.get_width(), Display.get_height()))

        BGDarkSurface.set_alpha(DialogOpctAnim_AnimOpacity)
        Display.blit(BGDarkSurface, (0, 0))

        Display.blit(CommonDisplay, CommonDisplayScreenPos)

def Draw_ScreenshotOfGameScreen(Display):
    global CopyOfScreen_Result
    global CopyOfScreen_Last
    global CopyOfScreen_BlurAmount

    # -- Blur Amount Value -- #
    if not CopyOfScreen_Last:
        CopyOfScreen_BlurAmount = max(1.0, DialogOpctAnim_AnimOpacity / gameMain.DefaultCnt.Get_RegKey("/OPTIONS/UI_blur_ammount", float) * 2.5)

    if DialogOpctAnim_AnimEnabled:  # -- Draw the Animation -- #
        CopyOfScreen_Last = False
        if gameMain.DefaultCnt.Get_RegKey("/OPTIONS/UI_blur_enabled"):
            Display.blit(gameMain.fx.Surface_Blur(fogosoMain.ScreenLastFrame, CopyOfScreen_BlurAmount, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/UI_Pixelate", bool)), (0, 0))

        else:
            Display.blit(fogosoMain.ScreenLastFrame, (0, 0))

    # -- Draw the Last Frame -- #
    if not CopyOfScreen_Last and not DialogOpctAnim_AnimEnabled:
        if gameMain.DefaultCnt.Get_RegKey("/OPTIONS/UI_blur_enabled", bool):
            CopyOfScreen_Result = gameMain.fx.Surface_Blur(fogosoMain.ScreenLastFrame, CopyOfScreen_BlurAmount)
        else:
            CopyOfScreen_Result = fogosoMain.ScreenLastFrame

        CopyOfScreen_Last = True

    # -- Render the Last Frame -- #
    if CopyOfScreen_Last and not DialogOpctAnim_AnimEnabled:  # -- Render the last frame of animation -- #
        Display.blit(CopyOfScreen_Result, (0, 0))

def EventUpdate(event):
    if Subscreen == 1:
        subscreen1.EventUpdate(event)

def Update():
    global DialogRectangle
    global CommonDisplay
    global CommonDisplayInitialized
    global DialogOpctAnim_AnimNumb
    global DialogOpctAnim_AnimOpacity
    global CommonDisplayScreenPos
    global DialogOpctAnim_AnimEnabled

    if not CommonDisplayInitialized:
        CommonDisplay = pygame.Surface((395, 150))
        CommonDisplayInitialized = True

    if CommonDisplayInitialized:
        # -- Update Anim -- #
        DialogOpctOpacity()
        DialogRectangle = pygame.Rect(0, 0, 395, 150)
        CommonDisplay.set_alpha(DialogOpctAnim_AnimOpacity)

        if Subscreen == 1:
            subscreen1.Update()

def DialogOpctOpacity():
    global DialogOpctAnim_AnimEnabled
    global DialogOpctAnim_AnimMode
    global DialogOpctAnim_AnimOpacity
    global DialogOpctAnim_AnimNumb
    global DialogOpenSoundPlayed
    global BGDarkSurfaceCreated
    global BGDarkSurface

    if DialogOpctAnim_AnimEnabled:
        DialogOpctAnim_AnimNumb = DialogOpctAnim_AnimOpacity - 255 + 15

        if not DialogOpenSoundPlayed:
            DialogOpenSoundPlayed = True

        if DialogOpctAnim_AnimMode == 0:
            DialogOpctAnim_AnimOpacity += 15

            if DialogOpctAnim_AnimOpacity >= 255:
                DialogOpctAnim_AnimOpacity = 255
                DialogOpctAnim_AnimMode = 1
                DialogOpctAnim_AnimEnabled = False

        if DialogOpctAnim_AnimMode == 1:
            DialogOpctAnim_AnimOpacity -= 15

            if DialogOpctAnim_AnimOpacity <= 0:
                DialogOpctAnim_AnimOpacity = 0
                DialogOpctAnim_AnimMode = 0
                DialogOpctAnim_AnimEnabled = True
                DialogOpenSoundPlayed = False
                BGDarkSurfaceCreated = False
                BGDarkSurface.fill((0, 0, 0))
                fogosoMain.OverlayDialogEnabled = False

def ResetAnimation():
    global DialogOpctAnim_AnimEnabled
    global DialogOpctAnim_AnimMode
    global DialogOpctAnim_AnimOpacity
    global DialogOpctAnim_AnimNumb
    global DialogOpenSoundPlayed

    DialogOpctAnim_AnimOpacity = 0
    DialogOpctAnim_AnimMode = 0
    DialogOpctAnim_AnimEnabled = True
    DialogOpenSoundPlayed = False

    seletorScreen.ApplicationUpdateDialogEnabled = False
