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

import pygame
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso import MAIN as gameMain
from ENGINE import APPDATA as reg
from ENGINE import CONTENT_MANAGER as sprite
from Fogoso.MAIN import ScreenTransition as transition
from ENGINE import taiyouMain as taiyouMain

# -- Objects Definition -- #
OptionsScreen_ChangeFps = gameObjs.UpDownButton
OptionsScreen_FlashAnimationSpeed = gameObjs.UpDownButton
OptionsScreen_FontAntiAlias = gameObjs.Button
OptionsScreen_FlashAnimStyle = gameObjs.UpDownButton
OptionsScreen_SpritesAntiAlias = gameObjs.Button

ElementsX = 0
ElementsY = 0

def Initialize():
    global OptionsScreen_ChangeFps
    global OptionsScreen_FlashAnimationSpeed
    global OptionsScreen_FontAntiAlias
    global OptionsScreen_FlashAnimStyle
    global OptionsScreen_SpritesAntiAlias

    OptionsScreen_ChangeFps = gameObjs.UpDownButton(20, 100, 14)
    OptionsScreen_FlashAnimationSpeed = gameObjs.UpDownButton(20, 160, 14)
    OptionsScreen_FontAntiAlias = gameObjs.Button(pygame.Rect(0, 0, 0, 0), gameMain.DefaultCnt.Get_RegKey("/strings/settings/toggle_button"), 14)
    OptionsScreen_FlashAnimStyle = gameObjs.UpDownButton(0, 0, 14)
    OptionsScreen_SpritesAntiAlias = gameObjs.UpDownButton(0, 0, 14)

def EventUpdate(event):
    global OptionsScreen_ChangeFps
    global OptionsScreen_FlashAnimationSpeed
    global OptionsScreen_FontAntiAlias
    global OptionsScreen_FlashAnimStyle
    global OptionsScreen_SpritesAntiAlias

    OptionsScreen_ChangeFps.Update(event)
    OptionsScreen_FlashAnimationSpeed.Update(event)
    OptionsScreen_FontAntiAlias.Update(event)
    OptionsScreen_FlashAnimStyle.Update(event)
    OptionsScreen_SpritesAntiAlias.Update(event)

def Update():
    global OptionsScreen_ChangeFps
    global OptionsScreen_FlashAnimationSpeed
    global OptionsScreen_FontAntiAlias
    global OptionsScreen_FlashAnimStyle
    global OptionsScreen_SpritesAntiAlias

    if OptionsScreen_ChangeFps.ButtonState == 2:
        print("MaxFPS is [" + str(gameMain.Engine_MaxFPS) + "]")
        gameMain.Engine_MaxFPS += 5

        if gameMain.Engine_MaxFPS >= 75:
            gameMain.Engine_MaxFPS = 50

        taiyouMain.ReceiveCommand(0, gameMain.Engine_MaxFPS)
        gameMain.DefaultCnt.Write_RegKey("/OPTIONS/maxFPS", str(gameMain.Engine_MaxFPS))
        print("MaxFPS is now set to[" + str(gameMain.Engine_MaxFPS) + "]")

    if OptionsScreen_ChangeFps.ButtonState == 1:
        print("MaxFPS is [" + str(gameMain.Engine_MaxFPS) + "]")
        gameMain.Engine_MaxFPS -= 5

        if gameMain.Engine_MaxFPS <= 45:
            gameMain.Engine_MaxFPS = 70

        taiyouMain.ReceiveCommand(0, gameMain.Engine_MaxFPS)
        gameMain.DefaultCnt.Write_RegKey("/OPTIONS/maxFPS", str(gameMain.Engine_MaxFPS))
        print("MaxFPS is now set to[" + str(gameMain.Engine_MaxFPS) + "]")

    if OptionsScreen_FlashAnimationSpeed.ButtonState == 2:
        print("Old FlashAnimationSpeed : " + str(gameMain.DefaultCnt.Get_RegKey("/OPTIONS/fade_flash_speed", int)))
        if transition.FadeEffectSpeed <= gameMain.DefaultCnt.Get_RegKey("/OPTIONS/props/fade_flash_speed_max", int):
            transition.FadeEffectSpeed += 1
        gameMain.DefaultCnt.Write_RegKey("/OPTIONS/fade_flash_speed", str(transition.FadeEffectSpeed))
        print("New FlashAnimationSpeed : " + str(gameMain.DefaultCnt.Get_RegKey("/OPTIONS/fade_flash_speed", int)))

    if OptionsScreen_FlashAnimationSpeed.ButtonState == 1:
        print("Old FlashAnimationSpeed : " + str(gameMain.DefaultCnt.Get_RegKey("/OPTIONS/fade_flash_speed", int)))
        if transition.FadeEffectSpeed >= 2:
            transition.FadeEffectSpeed -= 1
        gameMain.DefaultCnt.Write_RegKey("/OPTIONS/fade_flash_speed", str(transition.FadeEffectSpeed))
        print("New FlashAnimationSpeed : " + str(gameMain.DefaultCnt.Get_RegKey("/OPTIONS/fade_flash_speed", int)))

    if OptionsScreen_FontAntiAlias.ButtonState == 2:
        if gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa", bool):
            gameMain.DefaultCnt.Write_RegKey("/OPTIONS/font_aa", "False")
        else:
            gameMain.DefaultCnt.Write_RegKey("/OPTIONS/font_aa", "True")

    if OptionsScreen_FlashAnimStyle.ButtonState == 2:
        CurrentValue = gameMain.DefaultCnt.Get_RegKey("/OPTIONS/fade_flash_style", int)
        MaxValue = gameMain.DefaultCnt.Get_RegKey("/OPTIONS/props/fade_flash_style_max", int)

        if CurrentValue < MaxValue:
            CurrentValue += 1
        else:
            CurrentValue = 0

        gameMain.DefaultCnt.Write_RegKey("/OPTIONS/fade_flash_style", str(CurrentValue))
        transition.FadeEffectStyle = CurrentValue

    if OptionsScreen_FlashAnimStyle.ButtonState == 1:
        CurrentValue = gameMain.DefaultCnt.Get_RegKey("/OPTIONS/fade_flash_style", int)
        MaxValue = gameMain.DefaultCnt.Get_RegKey("/OPTIONS/props/fade_flash_style_max", int)

        if CurrentValue > -1:
            CurrentValue -= 1
        if CurrentValue == -1:
            CurrentValue = MaxValue

        gameMain.DefaultCnt.Write_RegKey("/OPTIONS/fade_flash_style", str(CurrentValue))
        transition.FadeEffectStyle = CurrentValue

    if OptionsScreen_SpritesAntiAlias .ButtonState == 2 or OptionsScreen_SpritesAntiAlias.ButtonState == 1:
        if gameMain.DefaultCnt.Get_RegKey("/OPTIONS/sprite_aa", bool):
            gameMain.DefaultCnt.Write_RegKey("/OPTIONS/sprite_aa", "False")
        else:
            gameMain.DefaultCnt.Write_RegKey("/OPTIONS/sprite_aa", "True")

    # -- Set Positions -- #
    OptionsScreen_ChangeFps.Set_X(ElementsX + 20)
    OptionsScreen_ChangeFps.Set_Y(ElementsY + 50)

    OptionsScreen_FlashAnimationSpeed.Set_X(ElementsX + 20)
    OptionsScreen_FlashAnimationSpeed.Set_Y(ElementsY + 75)

    OptionsScreen_FontAntiAlias.Set_X(ElementsX + 20)
    OptionsScreen_FontAntiAlias.Set_Y(ElementsY + 100)

    OptionsScreen_FlashAnimStyle.Set_X(ElementsX + 20)
    OptionsScreen_FlashAnimStyle.Set_Y(ElementsY + 125)

    OptionsScreen_SpritesAntiAlias.Set_X(ElementsX + 20)
    OptionsScreen_SpritesAntiAlias.Set_Y(ElementsY + 150)

def Render(DISPLAY):
    # -- Render Max FPS Option -- #
    OptionsScreen_ChangeFps.Render(DISPLAY)
    gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 14, gameMain.DefaultCnt.Get_RegKey("/strings/settings/max_fps") + str(gameMain.Engine_MaxFPS), (255, 255, 255), ElementsX + 95, ElementsY + 52, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa", bool))

    # -- Render Flash Animation Speed -- #
    OptionsScreen_FlashAnimationSpeed.Render(DISPLAY)
    gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 14, gameMain.DefaultCnt.Get_RegKey("/strings/settings/flash_anim_speed") + str(transition.FadeEffectSpeed), (255, 255, 255), ElementsX + 95, ElementsY + 77, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

    # -- Render FontAntiAlias -- #
    OptionsScreen_FontAntiAlias.Render(DISPLAY)

    gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 14, gameMain.DefaultCnt.Get_RegKey("/strings/settings/font_aa") + str(gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa", bool)), (255, 255, 255), ElementsX + 120, ElementsY + 102, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa", bool))

    # -- Render FlashAnimStyle -- #
    OptionsScreen_FlashAnimStyle.Render(DISPLAY)
    gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 14, gameMain.DefaultCnt.Get_RegKey("/strings/settings/flash_anim_style") + gameMain.DefaultCnt.Get_RegKey("/OPTIONS/desc/fade_flash/" + gameMain.DefaultCnt.Get_RegKey("/OPTIONS/fade_flash_style")), (255, 255, 255), ElementsX + 95, ElementsY + 127, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa", bool))

    # -- Render Sprite Anti-Alias Option -- #
    OptionsScreen_SpritesAntiAlias.Render(DISPLAY)
    gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 14, gameMain.DefaultCnt.Get_RegKey("/strings/settings/sprite_aa") + str(gameMain.DefaultCnt.Get_RegKey("/OPTIONS/sprite_aa")), (255, 255, 255), ElementsX + 95, ElementsY + 157, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa", bool))
