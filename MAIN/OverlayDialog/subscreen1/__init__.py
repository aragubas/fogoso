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
import ENGINE as tge
from Fogoso import MAIN as gameMain
from ENGINE import utils

from ENGINE import APPDATA as reg
from Fogoso.MAIN import OverlayDialog as Handler
from Fogoso import MAIN as fogosoMain

MessageTitle = "undefined_title"
Message = "undefined_message"
Yes_Button = gtk.Button
No_Button = gtk.Button
InputBox = gtk.InputBox
OK_Button = gtk.Button

ResponseTrigger = False
Response = "null"
ResponseType = "OK"
ResponseEnabled = False

def Initialize():
    global Yes_Button
    global No_Button
    global InputBox
    global OK_Button

    Yes_Button = gtk.Button(pygame.Rect(0,0,0,0), gameMain.DefaultCnt.Get_RegKey("/strings/dialog/yes_button"), 18)
    Yes_Button.CustomColisionRectangle = True

    No_Button = gtk.Button(pygame.Rect(0,0,0,0), gameMain.DefaultCnt.Get_RegKey("/strings/dialog/no_button"), 18)
    No_Button.CustomColisionRectangle = True

    OK_Button = gtk.Button(pygame.Rect(0, 0, 0, 0), gameMain.DefaultCnt.Get_RegKey("/strings/dialog/ok_button"), 18)
    OK_Button.CustomColisionRectangle = True

    InputBox = gtk.InputBox(0, 0, 0, 0, "Default", 20)

    InputBox.CustomColision = True

TextAnimInitialized = False
TextAnimWordList = list()
TextCurrentPhase = ""
TextAnimLoopIndex = 0
TextAnimEnded = False
TextAnimLoopDelay = 0
TextAnimMessageTypeDelay = 5
TextAnimWordStep = 1

def Draw(DISPLAY):
    global Message
    global Yes_Button
    global No_Button
    global ResponseType
    global InputBox
    global OK_Button

    # -- Render Buttons -- #
    if ResponseEnabled:
        if ResponseType == "YESNO":
            No_Button.Render(DISPLAY)
            Yes_Button.Render(DISPLAY)

        elif ResponseType == "INPUT":
            InputBox.Render(DISPLAY)

        elif ResponseType == "OK":
            OK_Button.Render(DISPLAY)

    # -- Render Message -- #
    gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 10, TextCurrentPhase, (230, 230, 230), 5, 26)

def Update():
    global MessageTitle
    global Yes_Button
    global No_Button
    global ResponseTrigger
    global Response
    global InputBox
    global OK_Button
    global ResponseEnabled
    if ResponseEnabled:
        if ResponseType == "YESNO":
            # -- Update Yes Button -- #
            Yes_Button.Set_ColisionX(Handler.CommonDisplayScreenPos[0] + Yes_Button.Rectangle[0])
            Yes_Button.Set_ColisionY(Handler.CommonDisplayScreenPos[1] + Yes_Button.Rectangle[1])
            Yes_Button.Set_X(5)
            Yes_Button.Set_Y(Handler.CommonDisplay.get_height() - Yes_Button.Rectangle[3] - 5)

            # -- Update No Button -- #
            No_Button.Set_ColisionX(Handler.CommonDisplayScreenPos[0] + No_Button.Rectangle[0])
            No_Button.Set_ColisionY(Handler.CommonDisplayScreenPos[1] + No_Button.Rectangle[1])
            No_Button.Set_X(Yes_Button.Rectangle[0] + Yes_Button.Rectangle[2] + 3)
            No_Button.Set_Y(Handler.CommonDisplay.get_height() - No_Button.Rectangle[3] - 5)

            if Yes_Button.ButtonState == 2:
                Response = "YES"
                ResponseTrigger = True
                Handler.DialogOpctAnim_AnimEnabled = True

            if No_Button.ButtonState == 2:
                Response = "NO"
                ResponseTrigger = True
                Handler.DialogOpctAnim_AnimEnabled = True

        elif ResponseType == "INPUT":
            # -- Update Input Button -- #
            InputBox.Set_X(5)
            InputBox.Set_Y(Handler.CommonDisplay.get_height() - InputBox.rect[3] - 5)

            InputBox.colisionRect = pygame.Rect(Handler.CommonDisplayScreenPos[0] + InputBox.rect[0], Handler.CommonDisplayScreenPos[1] + InputBox.rect[1], InputBox.rect[2], InputBox.rect[3])

        elif ResponseType == "OK":
            # -- Update OK Button -- #
            OK_Button.Set_ColisionX(Handler.CommonDisplayScreenPos[0] + OK_Button.Rectangle[0])
            OK_Button.Set_ColisionY(Handler.CommonDisplayScreenPos[1] + OK_Button.Rectangle[1])
            OK_Button.Set_X(5)
            OK_Button.Set_Y(Handler.CommonDisplay.get_height() - OK_Button.Rectangle[3] - 5)

            if OK_Button.ButtonState == 2:
                Handler.DialogOpctAnim_AnimEnabled = True
                ResponseTrigger = True
                Response = "OK"

    Handler.MessageTitle = MessageTitle
    UpdateMessageAnim()

def UpdateMessageAnim():
    global TextAnimInitialized
    global TextAnimWordList
    global TextCurrentPhase
    global TextAnimLoopIndex
    global TextAnimEnded
    global TextAnimLoopDelay
    global ResponseEnabled

    if not TextAnimEnded:
        if not TextAnimInitialized:
            TextAnimWordList = list(Message)

        TextAnimLoopDelay += 1

        if TextAnimLoopDelay >= TextAnimMessageTypeDelay:
            for i in range(0, TextAnimWordStep):
                if TextAnimLoopIndex < len(TextAnimWordList):
                    TextCurrentPhase += TextAnimWordList[TextAnimLoopIndex]
                    TextAnimLoopIndex += 1
                    TextAnimLoopDelay = 0
                    gameMain.DefaultCnt.PlaySound("/hit_1.wav", Volume=0.3)
                else:
                    TextAnimEnded = True
                    ResponseEnabled = True


def SetMessage(title, message, responseType="OK", typeDelay=10, wordStep=1):
    global MessageTitle
    global Message
    global ResponseType
    global TextAnimMessageTypeDelay
    global TextAnimInitialized
    global TextAnimEnded
    global TextCurrentPhase
    global TextAnimLoopDelay
    global TextAnimWordList
    global TextAnimLoopIndex
    global TextAnimWordStep

    MessageTitle = title.rstrip()
    Message = message.rstrip()
    ResponseType = responseType
    TextAnimMessageTypeDelay = typeDelay

    TextAnimInitialized = False
    TextAnimWordList.clear()
    TextCurrentPhase = ""
    TextAnimLoopIndex = 0
    TextAnimEnded = False
    TextAnimLoopDelay = 0
    TextAnimMessageTypeDelay = 5
    TextAnimWordStep = wordStep

    fogosoMain.OverlayDialogEnabled = True

def EventUpdate(event):
    global Yes_Button
    global No_Button
    global InputBox
    global ResponseType
    global ResponseTrigger
    global Response
    global OK_Button
    global ResponseEnabled
    global TextAnimWordStep
    if ResponseEnabled:
        if ResponseType == "YESNO":
            No_Button.Update(event)
            Yes_Button.Update(event)

        elif ResponseType == "INPUT":
            InputBox.Update(event)

            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                Handler.DialogOpctAnim_AnimEnabled = True
                ResponseTrigger = True
                Response = InputBox.text
                InputBox.active = False

        elif ResponseType == "OK":
            OK_Button.Update(event)

    if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and TextAnimWordStep < 3:
        TextAnimWordStep += 1