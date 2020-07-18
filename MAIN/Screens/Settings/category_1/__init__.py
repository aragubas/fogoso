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
from ENGINE import REGISTRY as reg
from ENGINE import sprite as sprite

# -- Objects Definition -- #
OptionsScreen_UI_Blur_Enabled = gameObjs.UpDownButton
OptionsScreen_UI_Blur_Ammount = gameObjs.UpDownButton
OptionsScreen_UI_Blur_Contrast = gameObjs.UpDownButton
OptionsScreen_UI_PixalizateInstedOfBlur = gameObjs.UpDownButton
OptionsScreen_Windows_Transitions = gameObjs.UpDownButton
OptionsScreen_Window_Indicator = gameObjs.UpDownButton
OptionsScreen_Scanline_Effect = gameObjs.UpDownButton


ElementsX = 0
ElementsY = 0

def Initialize():
    global OptionsScreen_UI_Blur_Enabled
    global OptionsScreen_UI_Blur_Ammount
    global OptionsScreen_UI_Blur_Contrast
    global OptionsScreen_UI_PixalizateInstedOfBlur
    global OptionsScreen_Windows_Transitions
    global OptionsScreen_Window_Indicator
    global OptionsScreen_Scanline_Effect

    OptionsScreen_UI_Blur_Enabled = gameObjs.UpDownButton(0,0,14)
    OptionsScreen_UI_Blur_Ammount = gameObjs.UpDownButton(0,0,14)
    OptionsScreen_UI_Blur_Contrast = gameObjs.UpDownButton(0,0,14)
    OptionsScreen_UI_PixalizateInstedOfBlur = gameObjs.UpDownButton(0,0,14)
    OptionsScreen_Windows_Transitions = gameObjs.UpDownButton(0,0,14)
    OptionsScreen_Window_Indicator = gameObjs.UpDownButton(0,0,14)
    OptionsScreen_Scanline_Effect = gameObjs.UpDownButton(0,0,14)

def Update():
    global OptionsScreen_UI_Blur_Enabled
    global OptionsScreen_UI_Blur_Ammount
    global OptionsScreen_UI_Blur_Contrast
    global OptionsScreen_UI_PixalizateInstedOfBlur
    global OptionsScreen_Windows_Transitions
    global OptionsScreen_Window_Indicator
    global OptionsScreen_Scanline_Effect
    global ElementsY
    global ElementsX

    # -- Set Positions X -- #
    OptionsScreen_UI_Blur_Enabled.Set_X(ElementsX + 20)
    OptionsScreen_UI_Blur_Ammount.Set_X(ElementsX + 20)
    OptionsScreen_UI_Blur_Contrast.Set_X(ElementsX + 20)
    OptionsScreen_UI_PixalizateInstedOfBlur.Set_X(ElementsX + 20)
    OptionsScreen_Windows_Transitions.Set_X(ElementsX + 20)
    OptionsScreen_Window_Indicator.Set_X(ElementsX + 20)
    OptionsScreen_Scanline_Effect.Set_X(ElementsX + 20)
    # -- Set Positions Y -- #
    OptionsScreen_UI_Blur_Enabled.Set_Y(ElementsY + 50)
    OptionsScreen_UI_Blur_Ammount.Set_Y(ElementsY + 75)
    OptionsScreen_UI_Blur_Contrast.Set_Y(ElementsY + 100)
    OptionsScreen_UI_PixalizateInstedOfBlur.Set_Y(ElementsY + 125)
    OptionsScreen_Windows_Transitions.Set_Y(ElementsY + 150)
    OptionsScreen_Window_Indicator.Set_Y(ElementsY + 175)
    OptionsScreen_Scanline_Effect.Set_Y(ElementsY + 200)

    # -- UI Blur Enabled -- #
    if OptionsScreen_UI_Blur_Enabled .ButtonState == 2 or OptionsScreen_UI_Blur_Enabled.ButtonState == 1:
        CurrentVal = reg.ReadKey_bool("/OPTIONS/UI_blur_enabled")
        if CurrentVal:
            reg.WriteKey("/OPTIONS/UI_blur_enabled", "False")
        if not CurrentVal:
            reg.WriteKey("/OPTIONS/UI_blur_enabled", "True")

    # -- UI Blur Ammount -- #
    if OptionsScreen_UI_Blur_Ammount .ButtonState == 2:
        CurrentVal = reg.ReadKey_float("/OPTIONS/UI_blur_ammount")
        CurrentVal += 0.5
        if CurrentVal >= 100:
            reg.WriteKey("/OPTIONS/UI_blur_ammount", "50.0")
        else:
            reg.WriteKey("/OPTIONS/UI_blur_ammount", str(CurrentVal))
    if OptionsScreen_UI_Blur_Ammount.ButtonState == 1:
        CurrentVal = reg.ReadKey_float("/OPTIONS/UI_blur_ammount")
        CurrentVal -= 0.5
        if CurrentVal < 50.0:
            reg.WriteKey("/OPTIONS/UI_blur_ammount", "100.0")
        else:
            reg.WriteKey("/OPTIONS/UI_blur_ammount", str(CurrentVal))

    # -- UI Blur Contrast -- #
    if OptionsScreen_UI_Blur_Contrast.ButtonState == 2:
        CurrentVal = reg.ReadKey_int("/OPTIONS/UI_contrast")
        CurrentVal += 1
        if CurrentVal >= 151:
            reg.WriteKey("/OPTIONS/UI_contrast", "0")
        else:
            reg.WriteKey("/OPTIONS/UI_contrast", str(CurrentVal))
    if OptionsScreen_UI_Blur_Contrast.ButtonState == 1:
        CurrentVal = reg.ReadKey_int("/OPTIONS/UI_contrast")
        CurrentVal -= 1
        if CurrentVal <= -1:
            reg.WriteKey("/OPTIONS/UI_contrast", "150")
        else:
            reg.WriteKey("/OPTIONS/UI_contrast", str(CurrentVal))

    # -- UI Pixalizate -- #
    if OptionsScreen_UI_PixalizateInstedOfBlur .ButtonState == 2 or OptionsScreen_UI_PixalizateInstedOfBlur.ButtonState == 1:
        CurrentVal = reg.ReadKey_bool("/OPTIONS/UI_Pixelate")
        if CurrentVal:
            reg.WriteKey("/OPTIONS/UI_Pixelate", "False")
        if not CurrentVal:
            reg.WriteKey("/OPTIONS/UI_Pixelate", "True")

    # -- Windows Transitions -- #
    if OptionsScreen_Windows_Transitions .ButtonState == 2 or OptionsScreen_Windows_Transitions.ButtonState == 1:
        CurrentVal = reg.ReadKey_bool("/OPTIONS/Windows_transitions")
        if CurrentVal:
            reg.WriteKey("/OPTIONS/Windows_transitions", "False")
        if not CurrentVal:
            reg.WriteKey("/OPTIONS/Windows_transitions", "True")

    # -- Window Indicator -- #
    if OptionsScreen_Window_Indicator .ButtonState == 2 or OptionsScreen_Window_Indicator.ButtonState == 1:
        CurrentVal = reg.ReadKey_bool("/OPTIONS/UI_WindowIndicator")
        if CurrentVal:
            reg.WriteKey("/OPTIONS/UI_WindowIndicator", "False")
        if not CurrentVal:
            reg.WriteKey("/OPTIONS/UI_WindowIndicator", "True")

    # -- Scanline Effect -- #
    if OptionsScreen_Scanline_Effect .ButtonState == 2 or OptionsScreen_Scanline_Effect.ButtonState == 1:
        CurrentVal = reg.ReadKey_bool("/OPTIONS/scanline_effect")
        if CurrentVal:
            reg.WriteKey("/OPTIONS/scanline_effect", "False")
        if not CurrentVal:
            reg.WriteKey("/OPTIONS/scanline_effect", "True")



def EventUpdate(event):
    global OptionsScreen_UI_Blur_Enabled
    global OptionsScreen_UI_Blur_Ammount
    global OptionsScreen_UI_Blur_Contrast
    global OptionsScreen_UI_PixalizateInstedOfBlur
    global OptionsScreen_Windows_Transitions
    global OptionsScreen_Window_Indicator
    global OptionsScreen_Scanline_Effect

    OptionsScreen_UI_Blur_Enabled.Update(event)
    OptionsScreen_UI_Blur_Ammount.Update(event)
    OptionsScreen_UI_Blur_Contrast.Update(event)
    OptionsScreen_UI_PixalizateInstedOfBlur.Update(event)
    OptionsScreen_Windows_Transitions.Update(event)
    OptionsScreen_Window_Indicator.Update(event)
    OptionsScreen_Scanline_Effect.Update(event)

def Render(DISPLAY):
    global OptionsScreen_UI_Blur_Enabled
    global OptionsScreen_UI_Blur_Ammount
    global OptionsScreen_UI_Blur_Contrast
    global OptionsScreen_UI_PixalizateInstedOfBlur
    global OptionsScreen_Windows_Transitions
    global OptionsScreen_Window_Indicator
    global OptionsScreen_Scanline_Effect

    OptionsScreen_UI_Blur_Enabled.Render(DISPLAY)
    OptionsScreen_UI_Blur_Ammount.Render(DISPLAY)
    OptionsScreen_UI_Blur_Contrast.Render(DISPLAY)
    OptionsScreen_UI_PixalizateInstedOfBlur.Render(DISPLAY)
    OptionsScreen_Windows_Transitions.Render(DISPLAY)
    OptionsScreen_Window_Indicator.Render(DISPLAY)
    OptionsScreen_Scanline_Effect.Render(DISPLAY)

    # -- UI Blur -- #
    sprite.FontRender(DISPLAY, "/PressStart2P.ttf", 14, "UI Blur:" + str(reg.ReadKey_bool("/OPTIONS/UI_blur_enabled")), (240, 240, 240), ElementsX + 95, ElementsY + 52, reg.ReadKey_bool("/OPTIONS/font_aa"))

    # -- UI Blur Ammount -- #
    sprite.FontRender(DISPLAY, "/PressStart2P.ttf", 14, "Blur Ammount:" + str(reg.ReadKey_float("/OPTIONS/UI_blur_ammount")), (240, 240, 240), ElementsX + 95, ElementsY + 77, reg.ReadKey_bool("/OPTIONS/font_aa"))

    # -- UI Contrast -- #
    sprite.FontRender(DISPLAY, "/PressStart2P.ttf", 14, "BG Contrast:" + str(reg.ReadKey_int("/OPTIONS/UI_contrast")), (240, 240, 240), ElementsX + 95, ElementsY + 102, reg.ReadKey_bool("/OPTIONS/font_aa"))

    # -- UI Pixalizate Instead of Blur -- #
    sprite.FontRender(DISPLAY, "/PressStart2P.ttf", 14, "Pixalizate:" + str(reg.ReadKey_bool("/OPTIONS/UI_Pixelate")), (240, 240, 240), ElementsX + 95, ElementsY + 127, reg.ReadKey_bool("/OPTIONS/font_aa"))

    # -- Windows Transitions -- #
    sprite.FontRender(DISPLAY, "/PressStart2P.ttf", 14, "Windows Transitions:" + str(reg.ReadKey_bool("/OPTIONS/Windows_transitions")), (240, 240, 240), ElementsX + 95, ElementsY + 152, reg.ReadKey_bool("/OPTIONS/font_aa"))

    # -- Windows Indicator -- #
    sprite.FontRender(DISPLAY, "/PressStart2P.ttf", 14, "Windows Indicator:" + str(reg.ReadKey_bool("/OPTIONS/UI_WindowIndicator")), (240, 240, 240), ElementsX + 95, ElementsY + 177, reg.ReadKey_bool("/OPTIONS/font_aa"))

    # -- Scanline Effect -- #
    sprite.FontRender(DISPLAY, "/PressStart2P.ttf", 14, "Scanline Effect:" + str(reg.ReadKey_bool("/OPTIONS/scanline_effect")), (240, 240, 240), ElementsX + 95, ElementsY + 202, reg.ReadKey_bool("/OPTIONS/font_aa"))
