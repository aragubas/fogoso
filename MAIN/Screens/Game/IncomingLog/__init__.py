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

from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso import MAIN as gameMain
from Fogoso.MAIN.Screens import Game as gameScr
from Fogoso.MAIN import GameVariables as save
import pygame, os

# -- Receive Log -- #
ReceiveLog_Y_Offset = 0
ReceiveLog_Y_OffsetAdder = 0
ReceiveLog_Y_AnimEnabled = False
ReceiveLog_Y_AnimType = 0
TextGrind_Text = list()
TextGrind_X = list()
TextGrind_Y = list()
TextGrind_IsGrindText = list()
TextGrind_TextColor = list()
TextGrind_Value = list()
TextGrind_FontSize = list()
ResultSurface = pygame.Surface
ReceiveLog_CloseButton = gameObjs.Button
IncomingLogPos = (0, 0)

def Initialize():
    global ReceiveLog_CloseButton
    global ResultSurface
    ResultSurface = pygame.Surface((350, 350), pygame.SRCALPHA)
    ReceiveLog_CloseButton = gameObjs.Button(pygame.rect.Rect(320, 0, 0, 0), gameMain.DefaultCnt.Get_RegKey("/strings/button/game/down_arrow"),16)


def EventUpdate(event):
    global ReceiveLog_CloseButton
    ReceiveLog_CloseButton.Update(event)

def Unload():
    TextGrind_Y.clear()
    TextGrind_X.clear()
    TextGrind_IsGrindText.clear()
    TextGrind_Value.clear()
    TextGrind_Text.clear()
    TextGrind_TextColor.clear()
    TextGrind_FontSize.clear()

def Update():
    global ReceiveLog_CloseButton
    global ReceiveLog_Y_AnimType
    global ReceiveLog_Y_OffsetAdder
    global ReceiveLog_Y_Offset
    global ReceiveLog_Y_AnimEnabled

    if ReceiveLog_CloseButton .ButtonState == 2:
        ReceiveLog_Y_AnimEnabled = True

    # -- Update Buttons Location -- #
    ReceiveLog_CloseButton.Rectangle = pygame.rect.Rect(gameMain.DefaultDisplay.get_width() - 30, ReceiveLog_Y_Offset + gameMain.DefaultDisplay.get_height() - 353, ReceiveLog_CloseButton.Rectangle[2], ReceiveLog_CloseButton.Rectangle[3])

    # -- Update the Receive Log Hide Animation -- #
    if ReceiveLog_Y_AnimEnabled:
        if ReceiveLog_Y_AnimType == 0:
            ReceiveLog_Y_OffsetAdder += 1
            ReceiveLog_Y_Offset += ReceiveLog_Y_OffsetAdder

            if ReceiveLog_Y_Offset >= 270:
                ReceiveLog_Y_Offset = 270
                ReceiveLog_Y_OffsetAdder = 0
                ReceiveLog_Y_AnimType = 1
                ReceiveLog_Y_AnimEnabled = False
                ReceiveLog_CloseButton.ButtonText = gameMain.DefaultCnt.Get_RegKey("/strings/button/game/up_arrow")

        if ReceiveLog_Y_AnimType == 1:
            ReceiveLog_Y_OffsetAdder += 1
            ReceiveLog_Y_Offset -= ReceiveLog_Y_OffsetAdder

            if ReceiveLog_Y_Offset <= 0:
                ReceiveLog_Y_Offset = 0
                ReceiveLog_Y_OffsetAdder = 0
                ReceiveLog_Y_AnimType = 0
                ReceiveLog_Y_AnimEnabled = False
                ReceiveLog_CloseButton.ButtonText = gameMain.DefaultCnt.Get_RegKey("/strings/button/game/down_arrow")

    for x, TextGrind_TxT in enumerate(TextGrind_Text):
        # -- Delete Object -- #
        if x > 24 or not gameScr.IsControlsEnabled or TextGrind_Y[x] <= 0:
            if TextGrind_IsGrindText[x]:
                AddMoney(TextGrind_Value[x])

            # -- Remove Item -- #
            TextGrind_Text.pop(x)
            TextGrind_X.pop(x)
            TextGrind_Y.pop(x)
            TextGrind_IsGrindText.pop(x)
            TextGrind_TextColor.pop(x)
            TextGrind_Value.pop(x)
            TextGrind_FontSize.pop(x)
            break
        else:
            # -- Move the Text -- #
            if TextGrind_IsGrindText[x]:
                TextGrind_Y[x] -= gameMain.DefaultCnt.GetFont_height("/PressStart2P.ttf", TextGrind_FontSize[x], TextGrind_TxT) / max(1, 1.05 - x)

                if TextGrind_Value[x] < 0:
                    TextGrind_X[x] = 350 / 2 - gameMain.DefaultCnt.GetFont_width("/PressStart2P.ttf", TextGrind_FontSize[x], TextGrind_TxT) / 2

            else:
                TextGrind_Y[x] -= gameMain.DefaultCnt.GetFont_height("/PressStart2P.ttf", TextGrind_FontSize[x], TextGrind_TxT) / 5.5
                TextGrind_X[x] = 345 - gameMain.DefaultCnt.GetFont_width("/PressStart2P.ttf", TextGrind_FontSize[x], TextGrind_TxT)

def AddMoney(Value, WithSound=True):
    # -- Increase Money -- #
    save.Current_Money += float(Value)

    # -- Play the Hit Sound -- #
    if WithSound:
        if float(Value) > 0:
            gameMain.DefaultCnt.PlaySound("/hit_1.wav", 0.35)
        if float(Value) < 0:
            gameMain.DefaultCnt.PlaySound("/hit_2.wav", 0.7)


def AddMessageText(Text, IsGrindText, TextColor, Value=0):
    global TextGrind_Text
    global TextGrind_X
    global TextGrind_Y
    global TextGrind_IsGrindText
    global TextGrind_TextColor
    global TextGrind_Value
    global TextGrind_FontSize

    if len(TextGrind_Text) >= 32:  # -- Limit the Input of Items
        if IsGrindText:
            AddMoney(Value, False)

    else:
        # -- Add to List Variables -- #
        TextGrind_Text.append(Text)
        TextGrind_X.append(5)
        TextGrind_Y.append(350 + gameMain.DefaultCnt.GetFont_height("/PressStart2P.ttf", 20, Text) * len(TextGrind_Text))
        TextGrind_IsGrindText.append(IsGrindText)
        TextGrind_TextColor.append(TextColor)
        TextGrind_Value.append(Value)

        if not Value == 0:
            TextGrind_FontSize.append(14)
        else:
            TextGrind_FontSize.append(9)

def Draw(DISPLAY):
    global ResultSurface
    global TextGrind_Text

    # -- Set Position -- #
    IncomingLogPos = (DISPLAY.get_width() - 355, ReceiveLog_Y_Offset + DISPLAY.get_height() - 355)

    # -- Update the Surface -- #
    ResultSurface = pygame.Surface((350, 350), pygame.SRCALPHA)

    # -- Render the Background -- #
    gameObjs.Draw_Panel(DISPLAY, (IncomingLogPos[0], IncomingLogPos[1], ResultSurface.get_width(), ResultSurface.get_height()))

    # -- Draw the Texts -- #
    for x, TextGrind_TxT in enumerate(TextGrind_Text):
        # -- Render Object -- #
        ObjOpacity = TextGrind_Y[x] * 2
        gameMain.DefaultCnt.FontRender(ResultSurface, "/PressStart2P.ttf", TextGrind_FontSize[x], TextGrind_TxT, TextGrind_TextColor[x], TextGrind_X[x], TextGrind_Y[x], Opacity=ObjOpacity, antialias=gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

    if gameMain.DefaultCnt.Get_RegKey("/OPTIONS/scanline_effect"):
        for y in range(0, 175):
            gameMain.shape.Shape_Line(ResultSurface, (0, 0, 0), 3, 4 + y * 2, ResultSurface.get_width() - 3, 4 + y * 2, 1)

        gameMain.shape.Shape_Rectangle(ResultSurface, (0, 0, 0), (0, 24, ResultSurface.get_width(), ResultSurface.get_height() - 24), 5, 8)


    # -- Render the Container Title -- #
    gameMain.shape.Shape_Rectangle(ResultSurface, (0, 12, 30), (0, 0, 350, 24))
    gameMain.DefaultCnt.FontRender(ResultSurface, "/PressStart2P.ttf", 18, gameMain.DefaultCnt.Get_RegKey("/strings/game/receiving_log"), (250, 250, 255), 3, 3)

    # -- Blit everthing to screen -- #
    DISPLAY.blit(ResultSurface, IncomingLogPos)

    ReceiveLog_CloseButton.Render(DISPLAY)
