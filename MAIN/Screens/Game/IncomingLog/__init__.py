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
from ENGINE import SOUND as sound
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso import MAIN as gameMain
from ENGINE import SPRITE as sprite
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
TextGrind_AliveTime = list()
TextGrind_IsGrindText = list()
TextGrind_TextColor = list()
TextGrind_Value = list()
ResultSurface = pygame.Surface
ReceiveLog_CloseButton = gameObjs.Button
ObjsDeletionTime = 0

def Initialize():
    global ReceiveLog_CloseButton
    global ResultSurface
    ResultSurface = pygame.Surface((350, 350), pygame.SRCALPHA)

    ReceiveLog_CloseButton = gameObjs.Button(pygame.rect.Rect(320, 0, 0, 0), reg.ReadKey("/strings/button/game/down_arrow"),16)


def EventUpdate(event):
    global ReceiveLog_CloseButton
    ReceiveLog_CloseButton.Update(event)

def Unload():
    TextGrind_Y.clear()
    TextGrind_X.clear()
    TextGrind_AliveTime.clear()
    TextGrind_IsGrindText.clear()
    TextGrind_Value.clear()
    TextGrind_Text.clear()
    TextGrind_TextColor.clear()

def Update():
    global ReceiveLog_CloseButton
    global ReceiveLog_Y_AnimType
    global ReceiveLog_Y_OffsetAdder
    global ReceiveLog_Y_Offset
    global ReceiveLog_Y_AnimEnabled
    global ObjsDeletionTime

    if ReceiveLog_CloseButton.ButtonState == "UP":
        ReceiveLog_Y_AnimEnabled = True

    # -- Update Buttons Location -- #
    ReceiveLog_CloseButton.Rectangle = pygame.rect.Rect(gameMain.DefaultDisplay.get_width() - 30, ReceiveLog_Y_Offset + gameMain.DefaultDisplay.get_height() - 353, ReceiveLog_CloseButton.Rectangle[2], ReceiveLog_CloseButton.Rectangle[3])

    # -- Update the Receive Log Hide Animation -- #
    if ReceiveLog_Y_AnimEnabled:
        if ReceiveLog_Y_AnimType == 0:
            ReceiveLog_Y_OffsetAdder += 1
            ReceiveLog_Y_Offset += ReceiveLog_Y_OffsetAdder

            if ReceiveLog_Y_Offset >= 310:
                ReceiveLog_Y_Offset = 310
                ReceiveLog_Y_OffsetAdder = 0
                ReceiveLog_Y_AnimType = 1
                ReceiveLog_Y_AnimEnabled = False
                ReceiveLog_CloseButton.ButtonText = reg.ReadKey("/strings/button/game/up_arrow")

        if ReceiveLog_Y_AnimType == 1:
            ReceiveLog_Y_OffsetAdder += 1
            ReceiveLog_Y_Offset -= ReceiveLog_Y_OffsetAdder

            if ReceiveLog_Y_Offset <= 0:
                ReceiveLog_Y_Offset = 0
                ReceiveLog_Y_OffsetAdder = 0
                ReceiveLog_Y_AnimType = 0
                ReceiveLog_Y_AnimEnabled = False
                ReceiveLog_CloseButton.ButtonText = reg.ReadKey("/strings/button/game/down_arrow")

    for x, TextGrind_TxT in enumerate(TextGrind_Text):
        # -- Delete Object -- #
        if x > 32 or not gameScr.IsControlsEnabled or TextGrind_AliveTime[x] >= 50 or TextGrind_Y[x] <= 0:
            if TextGrind_IsGrindText[x]:
                # -- Increase Money -- #
                save.Current_Money += float(TextGrind_Value[x])

                if float(TextGrind_Value[x]) > 0:
                    sound.PlaySound("/hit_1.wav", 0.35)
                if float(TextGrind_Value[x]) < 0:
                    sound.PlaySound("/hit_2.wav", 0.7)

            TextGrind_Text.pop(x)
            TextGrind_X.pop(x)
            TextGrind_Y.pop(x)
            TextGrind_AliveTime.pop(x)
            TextGrind_IsGrindText.pop(x)
            TextGrind_TextColor.pop(x)
            TextGrind_Value.pop(x)
        else:
            # -- Move the Text -- #
            if TextGrind_IsGrindText[x]:
                TextGrind_Y[x] -= sprite.GetFont_height("/PressStart2P.ttf", 20, TextGrind_TxT) / 1.2
            else:
                TextGrind_Y[x] -= sprite.GetFont_height("/PressStart2P.ttf", 20, TextGrind_TxT) / 2.5

            # -- Increase Alive Time -- #
            TextGrind_AliveTime[x] += 1

    if ReceiveLog_Y_AnimType == 0:
        ObjsDeletionTime = 500
    else:
        ObjsDeletionTime = 50

def AddMessageText(Text, IsGrindText, TextColor, Value=0):
    global TextGrind_Text
    global TextGrind_X
    global TextGrind_Y
    global TextGrind_AliveTime
    global TextGrind_IsGrindText
    global TextGrind_TextColor
    global TextGrind_Value

    # -- Add to List Variables -- #
    TextGrind_Text.append(Text)
    TextGrind_X.append(5)
    TextGrind_Y.append(350 + sprite.GetFont_height("/PressStart2P.ttf", 20, Text) * len(TextGrind_Text))
    TextGrind_AliveTime.append(0)
    TextGrind_IsGrindText.append(IsGrindText)
    TextGrind_TextColor.append(TextColor)
    TextGrind_Value.append(Value)

    # -- Play Hit Sound -- #
    sound.PlaySound("/hit_1.wav", 0.35,)


def Draw(DISPLAY):
    global ResultSurface

    # -- Clear the Surface -- #
    ResultSurface.fill((0, 0, 0, 0))

    # -- Render the Background -- #
    gameObjs.Draw_Panel(DISPLAY, (DISPLAY.get_width() - 355, ReceiveLog_Y_Offset + DISPLAY.get_height() - 355, ResultSurface.get_width(), ResultSurface.get_height()))

    # -- Draw the Texts -- #
    for x, TextGrind_TxT in enumerate(TextGrind_Text):
        # -- Render Object -- #
        sprite.FontRender(ResultSurface, "/PressStart2P.ttf", 18, TextGrind_TxT, TextGrind_TextColor[x], TextGrind_X[x], TextGrind_Y[x])

    # -- Render the Container Title -- #
    sprite.Shape_Rectangle(ResultSurface, (13, 10, 13), (2, 2, 350 - 4, 24 - 4))
    sprite.FontRender(ResultSurface, "/PressStart2P.ttf", 18, reg.ReadKey("/strings/game/receiving_log"), (250, 250, 255), 3, 3)

    # -- Blit everthing to screen -- #
    DISPLAY.blit(ResultSurface, (DISPLAY.get_width() - 355, ReceiveLog_Y_Offset + DISPLAY.get_height() - 355))

    ReceiveLog_CloseButton.Render(DISPLAY)
