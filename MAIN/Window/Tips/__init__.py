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
# -- Window Test
from Fogoso.MAIN import ClassesUtils as gameObjs
import pygame
from Fogoso import MAIN as gameMain
from ENGINE import APPDATA as reg
from random import randint
from Fogoso.MAIN.Screens import MainMenu as mainMenu

WindowObj = gameObjs.Window
WindowObj_Title = "Wait"
WindowObj_Text = "Loading message..."
WindowObj_UpdateMessage = True
WindowObj_RefreshButton = gameObjs.Button
WindowObj_LastMessageID = -1

def Initialize(DISPLAY):
    global WindowObj
    global WindowObj_RefreshButton

    WindowObj = gameObjs.Window(pygame.Rect(350, 50, 550, 200), gameMain.DefaultCnt.Get_RegKey("/strings/main_menu/message_window/window_title"), True)
    WindowObj_RefreshButton = gameObjs.Button(pygame.Rect(0, 0, 0, 0), gameMain.DefaultCnt.Get_RegKey("/strings/main_menu/message_window/next_button"), 18)
    WindowObj_RefreshButton.CustomColisionRectangle = True

def Draw(DISPLAY):
    global WindowObj
    global WindowObj_Title
    global WindowObj_Text
    global WindowObj_RefreshButton
    global WindowObj

    # -- Draw the Window Frame -- #
    WindowObj.Render(DISPLAY)

    # -- Clear Surface -- #
    WindowSurface = pygame.Surface((WindowObj.WindowSurface_Rect[2], WindowObj.WindowSurface_Rect[3]), pygame.SRCALPHA)

    # -- Render Title Background -- #
    gameMain.shape.Shape_Rectangle(WindowSurface, (56, 65, 74), (0, 0, WindowSurface.get_width(), 30))

    # -- Render the Title -- #
    gameMain.DefaultCnt.FontRender(WindowSurface, "/PressStart2P.ttf", 18, WindowObj_Title, (255, 255, 255), 5, 7, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

    # -- Render the Text -- #
    gameMain.DefaultCnt.FontRender(WindowSurface, "/PressStart2P.ttf", 10, WindowObj_Text, (255, 255, 255), 5, 37, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

    # -- Render Next Button -- ##
    WindowObj_RefreshButton.Render(WindowSurface)

    # -- Blit Window to Screen -- #
    DISPLAY.blit(WindowSurface, (WindowObj.WindowSurface_Rect[0], WindowObj.WindowSurface_Rect[1]))

def Update():
    global WindowObj_UpdateMessage
    global WindowObj_Title
    global WindowObj_Text
    global WindowObj_LastMessageID
    global WindowObj_RefreshButton

    if WindowObj_UpdateMessage:
        WindowObj_UpdateMessage = False
        if gameMain.DefaultCnt.Get_RegKey("/strings/main_menu/EMW/first_message", True):
            WindowObj_Title = "Welcome!"
            WindowObj_Text = gameMain.DefaultCnt.Get_RegKey("/strings/main_menu/EMW/first")
            gameMain.DefaultCnt.Write_RegKey("/strings/main_menu/EMW/first_message", "False")

        MessageID = randint(0, gameMain.DefaultCnt.Get_RegKey("/strings/main_menu/EMW/total_messages", int))
        if WindowObj_LastMessageID == MessageID:
            MessageID = randint(MessageID, gameMain.DefaultCnt.Get_RegKey("/strings/main_menu/EMW/total_messages", int))

        WindowObj_Title = gameMain.DefaultCnt.Get_RegKey("/strings/main_menu/EMW/" + str(MessageID) + "_title")
        WindowObj_Text = gameMain.DefaultCnt.Get_RegKey("/strings/main_menu/EMW/" + str(MessageID))
        print("EverdayMessage_UpdateMessage : MessageID[" + str(MessageID) + "]")

    if WindowObj.TitleBarRectangle[0] <= 300:
        WindowObj.TitleBarRectangle[0] = 300

    WindowObj_RefreshButton.Set_X(WindowObj.WindowRectangle[2] - WindowObj_RefreshButton.Rectangle[2] - 5)
    WindowObj_RefreshButton.Set_Y(WindowObj.WindowRectangle[3] - WindowObj_RefreshButton.Rectangle[3] * 1.7)

    WindowObj_RefreshButton.Set_ColisionX(WindowObj.WindowRectangle[0] + WindowObj_RefreshButton.Rectangle[0])
    WindowObj_RefreshButton.Set_ColisionY(WindowObj.WindowRectangle[1] + WindowObj_RefreshButton.Rectangle[1] + WindowObj_RefreshButton.Rectangle[3] - 8)

    if WindowObj_RefreshButton.ButtonState == 2:
        WindowObj_UpdateMessage = True

def EventUpdate(event):
    global WindowObj
    global WindowObj_RefreshButton

    WindowObj_RefreshButton.Update(event)
    WindowObj.EventUpdate(event)
