#!/usr/bin/ python3.7
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

from Fogoso import MAIN as mainScript
from ENGINE import fx
from ENGINE import utils
import pygame
import random
from Fogoso.MAIN import GameItems as gameItems

# -- UI Color -- #
# -- Buttons Color -- #
Button_Active_IndicatorColor = (46, 196, 182)
Button_Active_BackgroundColor = (15, 27, 44, 150)
Button_Inactive_IndicatorColor = (255, 51, 102)
Button_Inactive_BackgroundColor = (1, 22, 39, 150)
Button_BackgroundColor = (12, 22, 14)

# Value View Color #
ValueView_TextColor = (155, 155, 155)
ValueView_ValueColor = (235, 235, 235)

print("Game : Classes Utils v1.1")

def Draw_Panel(DISPLAY, Rectangle, DisableBlur=False):
    # -- the Result Surface -- #
    ResultPanel = pygame.Surface((Rectangle[2], Rectangle[3]), pygame.HWSURFACE | pygame.HWACCEL)

    if not DisableBlur:
        if mainScript.DefaultCnt.Get_RegKey("/OPTIONS/UI_blur_enabled", bool):  # -- If Blur is Enabled -- #
            DarkerBG = pygame.Surface((Rectangle[2], Rectangle[3]), pygame.HWSURFACE | pygame.HWACCEL)
            DarkerBG.set_alpha(mainScript.DefaultCnt.Get_RegKey("/OPTIONS/UI_contrast", int))
            DISPLAY.blit(DarkerBG, Rectangle)

            # -- Only Blur the Necessary Area -- #
            AreaToBlur = pygame.Surface((Rectangle[2], Rectangle[3]), pygame.HWSURFACE | pygame.HWACCEL)
            AreaToBlur.blit(DISPLAY, (0, 0), Rectangle)


            # -- Then Finnaly, blit the Blurred Result -- #
            ResultPanel.blit(fx.Surface_Blur(AreaToBlur, mainScript.DefaultCnt.Get_RegKey("/OPTIONS/UI_blur_ammount", float), mainScript.DefaultCnt.Get_RegKey("/OPTIONS/UI_Pixelate", bool)), (0, 0))


        else:  # -- If blur is Disabled -- #
            ResultPanel.fill((0, 12, 29))

            mainScript.shape.Shape_Rectangle(ResultPanel, (1, 22, 39), (0, 0, Rectangle[2], Rectangle[3]), 2, 5)
    else:
        ResultPanel.fill((0, 12, 29))

        mainScript.shape.Shape_Rectangle(ResultPanel, (1, 22, 39), (0, 0, Rectangle[2], Rectangle[3]), 2, 5)

    DISPLAY.blit(ResultPanel, (Rectangle[0], Rectangle[1]))

COLOR_INACTIVE = (1, 22, 39)
COLOR_ACTIVE = (15, 27, 44)

class InputBox:
    def __init__(self, x, y, w, h, text='LO', FontSize=12):
        self.rect = pygame.Rect(x, y, w, h)
        self.colisionRect = pygame.Rect(x, y, w, h)
        self.CustomColision = False
        self.color = COLOR_INACTIVE
        self.text = text
        self.active = False
        self.DefaultText = text
        self.LastHeight = 1
        self.CustomWidth = False
        self.width = 1
        self.FontSize = FontSize
        self.CharacterLimit = 0

    def Set_X(self, Value):
        if not self.rect[0] == Value:
            self.rect = pygame.Rect(Value, self.rect[1], self.rect[2], self.rect[3])

    def Set_Y(self, Value):
        if not self.rect[1] == Value:
            self.rect = pygame.Rect(self.rect[0], Value, self.rect[2], self.rect[3])

    def Update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.colisionRect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.text) > 0:
                        self.text = self.text[:-1]
                    else:
                        self.text = self.DefaultText

                else:
                    if not self.CharacterLimit == 0:
                        if len(self.text) < self.CharacterLimit:
                            self.text += event.unicode
                    else:
                        self.text += event.unicode

    def Render(self, screen):
        # -- Resize the Textbox -- #
        try:
            if not self.CustomWidth:
                self.width = max(100, mainScript.DefaultCnt.GetFont_width(InputBox_FontFile, self.FontSize, self.text) + 10)
            self.rect.w = self.width
            self.rect.h = mainScript.DefaultCnt.GetFont_height(InputBox_FontFile, self.FontSize, self.text)
            self.LastHeight = self.rect.h
        except:
            if not self.CustomWidth:
                self.rect.w = 100
            self.rect.h = self.LastHeight

        if not self.CustomColision:
            self.colisionRect = self.rect

        # Blit the rect.
        Draw_Panel(screen, self.rect, "UP")

        if self.text == self.DefaultText:
            mainScript.DefaultCnt.FontRender(screen, InputBox_FontFile, self.FontSize, self.text, (140, 140, 140), self.rect[0], self.rect[1])
        else:
            if not self.text == "":
                mainScript.DefaultCnt.FontRender(screen, InputBox_FontFile, self.FontSize, self.text, (240, 240, 240), self.rect[0], self.rect[1])

        if not self.active:
            mainScript.shape.Shape_Rectangle(screen, (255, 51, 102), (self.rect[0], self.rect[1] - 1, self.rect[2], 1))
        else:
            mainScript.shape.Shape_Rectangle(screen, (46, 196, 182), (self.rect[0], self.rect[1] - 1, self.rect[2], 1))


class SpriteButton:
    def __init__(self, Rectangle, SpriteList):
        self.Rectangle = Rectangle
        self.SpriteList = SpriteList
        self.ButtonState = 0
        self.CursorSettedToggle = False
        self.CustomColisionRectangle = False
        self.ButtonDowed = False
        self.IsButtonEnabled = True
        self.ColisionRectangle = pygame.Rect(0,0,0,0)

    def Render(self,DISPLAY):
        mainScript.DefaultCnt.ImageRender(DISPLAY, self.SpriteList[self.ButtonState], self.Rectangle[0], self.Rectangle[1], self.Rectangle[2], self.Rectangle[3])

    def EventUpdate(self, event):
        if not self.CustomColisionRectangle:
            self.ColisionRectangle = self.Rectangle

        if self.IsButtonEnabled:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.ColisionRectangle.collidepoint(mainScript.Cursor_Position):
                    self.ButtonState = 1
                    self.ButtonDowed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.ColisionRectangle.collidepoint(mainScript.Cursor_Position):
                    if self.ButtonDowed:
                        self.ButtonState = 2
                        self.ButtonDowed = False
            if event.type == pygame.MOUSEMOTION:
                if self.ColisionRectangle.collidepoint(mainScript.Cursor_Position):
                    self.CursorSettedToggle = True
                    mainScript.Cursor_CurrentLevel = 3
                else:
                    if self.CursorSettedToggle:
                        self.CursorSettedToggle = False
                        mainScript.Cursor_CurrentLevel = 0
                        self.ButtonState = 0

        else:
            self.ButtonState = 0

    def Set_X(self, Value):
        self.Rectangle[0] = Value

    def Set_Y(self, Value):
        self.Rectangle[1] = Value

    def Set_W(self, Value):
        self.Rectangle[2] = Value

    def Set_H(self, Value):
        self.Rectangle[3] = Value

class Button:
    def __init__(self, Rectangle, ButtonText, TextSize):
        self.Rectangle = Rectangle
        self.ButtonText = ButtonText
        self.TextSize = TextSize
        self.ButtonState = 0 # 0 - INACTIVE, 1 - DOWN, 2 - UP
        self.FontFile = "/PressStart2P.ttf"
        self.IsButtonEnabled = True
        self.Rectangle = pygame.rect.Rect(self.Rectangle[0], self.Rectangle[1], mainScript.DefaultCnt.GetFont_width(self.FontFile, self.TextSize, self.ButtonText) + 5, mainScript.DefaultCnt.GetFont_height(self.FontFile, self.TextSize, self.ButtonText) + 6)
        self.LastRect = self.Rectangle
        self.CursorSettedToggle = False
        self.ButtonDowed = False
        self.ColisionRectangle = self.Rectangle
        self.CustomColisionRectangle = False
        self.BackgroundColor = Button_BackgroundColor
        self.SurfaceUpdated = False
        self.LastRect = pygame.Rect(0, 0, 0, 0)
        self.Surface = pygame.Surface((Rectangle[2], Rectangle[3]))

    def Update(self, event):
        # -- Set the Custom Colision Rectangle -- #
        if not self.CustomColisionRectangle:
            self.ColisionRectangle = self.Rectangle
        else:
            self.ColisionRectangle = pygame.Rect(self.ColisionRectangle[0], self.ColisionRectangle[1], self.Rectangle[2], self.Rectangle[3])

        if self.IsButtonEnabled:  # -- Only update the button, when is enabled.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Set the button to the DOWN state
                if self.ColisionRectangle.collidepoint(mainScript.Cursor_Position):
                    self.ButtonState = 1
                    self.ButtonDowed = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Set the button to the UP state
                if self.ButtonDowed:
                    self.ButtonState = 2
                    self.ButtonDowed = False

            if event.type == pygame.MOUSEMOTION:  # Change the Cursor
                if self.ColisionRectangle.collidepoint(mainScript.Cursor_Position):
                    self.CursorSettedToggle = True
                    mainScript.Cursor_CurrentLevel = 3
                else:
                    if self.CursorSettedToggle:
                        self.CursorSettedToggle = False
                        mainScript.Cursor_CurrentLevel = 0
                        self.ButtonState = 0

        else:
            self.ButtonState = 0
            if self.CursorSettedToggle:
                self.CursorSettedToggle = False
                mainScript.Cursor_CurrentLevel = 0

    def Set_X(self, Value):
        self.Rectangle[0] = Value

    def Set_Y(self, Value):
        self.Rectangle[1] = Value

    def Set_Width(self, Value):
        self.Rectangle[2] = Value

    def Set_Height(self, Value):
        self.Rectangle[3] = Value

    def Set_ColisionX(self, Value):
        self.ColisionRectangle[0] = Value

    def Set_ColisionY(self, Value):
        self.ColisionRectangle[1] = Value

    def Set_Text(self, Value):
        self.ButtonText = Value

    def Render(self, DISPLAY):
        # -- Update the Surface -- #
        self.Rectangle = pygame.rect.Rect(self.Rectangle[0], self.Rectangle[1], mainScript.DefaultCnt.GetFont_width(self.FontFile, self.TextSize, self.ButtonText) + 5, mainScript.DefaultCnt.GetFont_height(self.FontFile, self.TextSize, self.ButtonText) + 6)

        # -- Update the Rect Wheen Needed -- #
        if self.Rectangle == self.LastRect:
            self.Surface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]))

        # -- Update Surface when the size is changed -- #
        if not self.LastRect == self.Rectangle:
            self.SurfaceUpdated = False
            self.LastRect = self.Rectangle

        # -- Set the Button Colors -- #
        IndicatorColor = (0, 0, 0)

        if self.ButtonState == 0:
            IndicatorColor = Button_Inactive_IndicatorColor
            self.BackgroundColor = Button_Inactive_BackgroundColor

        elif self.ButtonState == 1:
            IndicatorColor = Button_Active_IndicatorColor
            self.BackgroundColor = Button_Active_BackgroundColor

        # -- Render Background -- #
        self.Surface.fill(self.BackgroundColor)

        # -- Indicator Bar -- #
        mainScript.shape.Shape_Rectangle(self.Surface, IndicatorColor, (0, 0, self.Rectangle[2], 2), 0, 0)

        # -- Text -- #
        mainScript.DefaultCnt.FontRender(self.Surface, self.FontFile, self.TextSize, self.ButtonText, (200, 200, 200), 3, 3, mainScript.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

        # -- Draw the Button -- #
        DISPLAY.blit(self.Surface, (self.Rectangle[0], self.Rectangle[1]))

        if self.ButtonState == 2:
            self.ButtonState = 0

class UpDownButton:
    def __init__(self, X, Y, TextSize):
        self.X = X
        self.Y = Y
        self.TextSize = TextSize
        self.UpButton = Button(pygame.Rect(X, Y, 20, 20), "/\\", TextSize)
        self.DownButton = Button(pygame.Rect(X + mainScript.DefaultCnt.GetFont_width("/PressStart2P.ttf", TextSize, "\/") + 5, Y, 20, 20), "\/", TextSize)
        self.ButtonState = 0
        self.BackStateWaitLoop = 0
        print("ObjectCreation : UpDownButton created.")

    def Update(self, event):
        self.UpButton.Update(event)
        self.DownButton.Update(event)

        if self.UpButton.ButtonState == 2:
            self.ButtonState = 2

        if self.DownButton.ButtonState == 2:
            self.ButtonState = 1

    def Render(self, DISPLAY):
        self.UpButton.Render(DISPLAY)
        self.DownButton.Render(DISPLAY)

        if self.ButtonState == 2 or self.ButtonState == 1:
            self.BackStateWaitLoop += 1

            if self.BackStateWaitLoop >= 1:
                self.ButtonState = 0
                self.BackStateWaitLoop = 0

    def Get_Width(self):
        return mainScript.DefaultCnt.GetFont_width("/PressStart2P.ttf", self.TextSize, "\/") + 4 + mainScript.DefaultCnt.GetFont_width(
            "/PressStart2P.ttf", self.TextSize, "/\\") + 4

    def Get_Height(self):
        return mainScript.DefaultCnt.GetFont_height("/PressStart2P.ttf", self.TextSize, "\/") + 4 + mainScript.DefaultCnt.GetFont_height(
            "/PressStart2P.ttf", self.TextSize, "/\\") + 4

    def Set_X(self, NewXValue):
        self.UpButton.Set_X(NewXValue)
        self.DownButton.Set_X(NewXValue + mainScript.DefaultCnt.GetFont_width("/PressStart2P.ttf", self.TextSize, "\/") + 5)

    def Set_Y(self, NewYValue):
        self.UpButton.Set_Y(NewYValue)
        self.DownButton.Set_Y(NewYValue)

    def Set_Size(self, NewSize):
        self.UpButton.TextSize = NewSize
        self.DownButton.TextSize = NewSize

        self.UpButton.Set_X(self.X)
        self.DownButton.Set_X(
            self.X + mainScript.DefaultCnt.GetFont_width("/PressStart2P.ttf", self.TextSize, "\/") + 5)

class Window:
    def __init__(self, Rectangle, Title, Resiziable):
        self.WindowRectangle = Rectangle
        self.Title = Title
        self.TitleBarRectangle = pygame.Rect(self.WindowRectangle[0], self.WindowRectangle[1], self.WindowRectangle[2],
                                             20)
        self.ResizeRectangle = pygame.Rect(self.WindowRectangle[0] + self.WindowRectangle[3] - 16,
                                           self.WindowRectangle[1] + self.WindowRectangle[3] - 16, 16, 16)
        self.Cursor_Position = mainScript.Cursor_Position
        self.Window_IsBeingGrabbed = False
        self.Window_IsBeingResized = False
        self.Window_MinimunW = Rectangle[2]
        self.Window_MinimunH = Rectangle[3]
        self.Resiziable = Resiziable
        self.WindowOriginalRect = pygame.Rect(0, 0, 0, 0)
        self.OriginalMinumunHeight = 0
        self.OriginalResiziable = False
        self.WindowSurface_Rect = (0, 0, 200, 200)
        self.Minimizable = True
        self.SurfaceSizeFixed = False

    def Render(self, DISPLAY):
        # -- Window Rectangle -- #
        self.WindowRectangle[0] = self.TitleBarRectangle[0]
        self.WindowRectangle[1] = self.TitleBarRectangle[1]
        # -- Title Bar Rectangle -- #
        self.TitleBarRectangle = pygame.Rect(self.WindowRectangle[0], self.WindowRectangle[1], self.WindowRectangle[2], 20)

        # -- Resize Button Rectangle -- #
        if self.Resiziable:
            self.ResizeRectangle = pygame.Rect(self.WindowRectangle[0] + self.WindowRectangle[2] - 10,
                                               self.WindowRectangle[1] + self.WindowRectangle[3], 10, 10)
        # -- Update Window Surface Destination -- #
        self.WindowSurface_Rect = (self.WindowRectangle[0], self.WindowRectangle[1] + 20, self.WindowRectangle[2], self.WindowRectangle[3] - 20)

        # -- Update Window Border -- #
        if not self.Resiziable:
            WindowBorderRectangle = self.WindowRectangle
        else:
            WindowBorderRectangle = (self.WindowRectangle[0], self.WindowRectangle[1], self.WindowRectangle[2], self.WindowRectangle[3] + 12)

        # -- Draw the Window Blurred Background -- #
        if not self.Window_IsBeingGrabbed:
            IndicatorLineColor = (32, 164, 243)
        else:
            IndicatorLineColor = (255, 51, 102)
        WindowSurface = pygame.Surface((WindowBorderRectangle[2], WindowBorderRectangle[3]))
        WindowSurface.blit(DISPLAY, (0, 0), self.WindowRectangle)
        Draw_Panel(WindowSurface, (0, 0, WindowBorderRectangle[2], WindowBorderRectangle[3]))

        pygame.draw.line(WindowSurface, IndicatorLineColor, (0, self.TitleBarRectangle[3]), (self.TitleBarRectangle[2], self.TitleBarRectangle[3]), 2)

        # -- Draw the Resize Block -- #
        if self.Resiziable:
            mainScript.DefaultCnt.ImageRender(WindowSurface, "/window/resize.png", self.WindowRectangle[2] - 10, self.WindowRectangle[3], self.ResizeRectangle[2], self.ResizeRectangle[3], mainScript.DefaultCnt.Get_RegKey("/OPTIONS/sprite_aa"))

        # -- Draw the window title -- #
        mainScript.DefaultCnt.FontRender(WindowSurface, "/PressStart2P.ttf", 18, self.Title, (250, 250, 255), self.TitleBarRectangle[2] / 2 - mainScript.DefaultCnt.GetFont_width("/PressStart2P.ttf", 18, self.Title) / 2, 1, mainScript.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

        DISPLAY.blit(WindowSurface, (self.WindowRectangle[0], self.WindowRectangle[1]))

    def EventUpdate(self, event):
        # -- Grab the Window -- #
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.TitleBarRectangle.collidepoint(mainScript.Cursor_Position):
                self.Window_IsBeingGrabbed = True
                mainScript.Cursor_CurrentLevel = 2

            if self.ResizeRectangle.collidepoint(mainScript.Cursor_Position) and self.Resiziable:
                self.Window_IsBeingResized = True
                mainScript.Cursor_CurrentLevel = 1
        # -- Ungrab the Window -- #
        if event.type == pygame.MOUSEBUTTONUP:
            if self.Window_IsBeingResized:
                self.Window_IsBeingResized = False
                mainScript.Cursor_CurrentLevel = 0

            if self.Window_IsBeingGrabbed:
                self.Window_IsBeingGrabbed = False
                mainScript.Cursor_CurrentLevel = 0

        # -- Grab Window -- #
        if self.Window_IsBeingGrabbed:
            self.TitleBarRectangle[0] = mainScript.Cursor_Position[0] - self.WindowRectangle[2] / 2
            self.TitleBarRectangle[1] = mainScript.Cursor_Position[1] - self.TitleBarRectangle[3] / 2

        # -- Resize Window -- #
        if self.Window_IsBeingResized and self.Resiziable:
            # -- Limit Window Size -- #
            if self.WindowRectangle[2] >= self.Window_MinimunW:
                self.WindowRectangle[2] = mainScript.Cursor_Position[0] - self.WindowRectangle[0]

            if self.WindowRectangle[3] >= self.Window_MinimunH: # <- Resize the Window
                self.WindowRectangle[3] = mainScript.Cursor_Position[1] - self.WindowRectangle[1]

        # -- Dont Allow the Window to be resized lower than Minimum Size -- #
        if self.WindowRectangle[2] < self.Window_MinimunW:
            self.WindowRectangle[2] = self.Window_MinimunW

        if self.WindowRectangle[3] < self.Window_MinimunH:
            self.WindowRectangle[3] = self.Window_MinimunH

class VerticalListWithDescription:
    def __init__(self, Rectangle):
        self.Rectangle = Rectangle
        self.ItemsName = list()
        self.ItemsDescription = list()
        self.ItemOrderID = list()
        self.ItemSprite = list()
        self.ItemSelected = list()
        self.LastItemClicked = "null"
        self.LastItemOrderID = None
        self.ScrollY = 0
        self.ListSurface = pygame.Surface
        self.ClickedItem = ""
        self.ColisionXOffset = 0
        self.ColisionYOffset = 0
        self.ButtonUpRectangle = pygame.Rect(0, 0, 32, 32)
        self.ButtonDownRectangle = pygame.Rect(34, 0, 32, 32)
        self.Cursor_Position = mainScript.Cursor_Position
        self.ListSurfaceUpdated = False

    def Render(self,DISPLAY):
        self.ListSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)

        for i, itemNam in enumerate(self.ItemsName):
            ItemRect = (self.Rectangle[0], self.ScrollY + self.Rectangle[1] + 42 * i, self.Rectangle[2], 40)

            # -- When the item is not clicked -- #
            if not self.ItemSelected[i]:
                if self.LastItemClicked == itemNam:
                    # -- Background -- #
                    mainScript.shape.Shape_Rectangle(self.ListSurface, (20, 42, 59, 100), ItemRect)
                    # -- Indicator Bar -- #
                    mainScript.shape.Shape_Rectangle(self.ListSurface, (46, 196, 182), (ItemRect[0], ItemRect[1], ItemRect[2], 1))
                else:
                    # -- Background -- #
                    mainScript.shape.Shape_Rectangle(self.ListSurface, (20, 42, 59, 50), ItemRect)
                    # -- Indicator Bar -- #
                    mainScript.shape.Shape_Rectangle(self.ListSurface, (32, 164, 243), (ItemRect[0], ItemRect[1], ItemRect[2], 1))

            else:
                # -- Background -- #
                mainScript.shape.Shape_Rectangle(self.ListSurface, (30, 52, 69, 150), ItemRect)
                # -- Indicator Bar -- #
                mainScript.shape.Shape_Rectangle(self.ListSurface, (255, 51, 102), (ItemRect[0], ItemRect[1], ItemRect[2], 1))

            # -- Render the Item Name and Description -- #
            if not self.ItemSelected[i]:
                # -- Render Item Name -- #
                mainScript.DefaultCnt.FontRender(self.ListSurface, "/PressStart2P.ttf", 12, itemNam, (250, 250, 250), ItemRect[0] + 45, ItemRect[1] + 5, mainScript.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

                # -- Render Item Description -- #
                mainScript.DefaultCnt.FontRender(self.ListSurface, "/PressStart2P.ttf", 10, self.ItemsDescription[i], (250, 250, 250), ItemRect[0] + 45, ItemRect[1] + 30, mainScript.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

            else:
                # -- Render Item Name -- #
                mainScript.DefaultCnt.FontRender(self.ListSurface, "/PressStart2P.ttf", 12, itemNam, (255, 255, 255), ItemRect[0] + 45, ItemRect[1] + 5, mainScript.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

                # -- Render Item Description -- #
                mainScript.DefaultCnt.FontRender(self.ListSurface, "/PressStart2P.ttf", 10, self.ItemsDescription[i], (255, 255, 255), ItemRect[0] + 45, ItemRect[1] + 30, mainScript.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

            # -- Render the Item Sprite -- #
            if self.ItemSprite[i] != "null":
                mainScript.DefaultCnt.ImageRender(self.ListSurface, self.ItemSprite[i], ItemRect[0] + 4, ItemRect[1] + 4, 36, 32, mainScript.DefaultCnt.Get_RegKey("/OPTIONS/sprite_aa"))

        # -- Blit All Work to Screen -- #
        DISPLAY.blit(self.ListSurface,(self.Rectangle[0], self.Rectangle[1]))

    def Update(self, event):
        self.Cursor_Position = mainScript.Cursor_Position
        ColisionRect = pygame.Rect(self.ColisionXOffset + self.Rectangle[0], self.ColisionYOffset + self.Rectangle[1], self.Rectangle[2], self.Rectangle[3])

        if ColisionRect.collidepoint(self.Cursor_Position):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:
                    self.ScrollY += 5
                    return

                elif event.button == 4:
                    self.ScrollY -= 5
                    return

            # -- Select the Clicked Item -- #
            for i, itemNam in enumerate(self.ItemsName):
                ItemRect = pygame.Rect(self.ColisionXOffset + self.Rectangle[0], self.ColisionYOffset + self.ScrollY + self.Rectangle[1] + 42 * i, self.Rectangle[2], 40)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if ItemRect.collidepoint(self.Cursor_Position):
                        self.LastItemClicked = itemNam
                        self.ItemSelected[i] = True
                        self.LastItemOrderID = self.ItemOrderID[i]
                if event.type == pygame.MOUSEBUTTONUP:
                    self.ItemSelected[i] = False

    def Set_X(self, Value):
        self.Rectangle[0] = int(Value)

    def Set_Y(self, Value):
        self.Rectangle[1] = int(Value)

    def Set_W(self, Value):
        self.Rectangle[2] = int(Value)

    def Set_H(self, Value):
        self.Rectangle[3] = int(Value)

    def AddItem(self,ItemName, ItemDescription, ItemSprite="null"):
        self.ItemsName.append(ItemName)
        self.ItemsDescription.append(ItemDescription)
        self.ItemSprite.append(ItemSprite)
        self.ItemSelected.append(False)
        self.ItemOrderID.append((len(self.ItemOrderID) - 2) + 1)

    def ClearItems(self):
        self.ItemsName.clear()
        self.ItemsDescription.clear()
        self.ItemSprite.clear()
        self.ItemSelected.clear()
        self.ItemOrderID.clear()

class GameItemsView:
    def __init__(self, Rectangle):
        self.Rectangle = Rectangle
        self.ItemsID = list()

        self.ScrollX = 10
        self.ListSurface = pygame.Surface
        self.ButtonLeftRectangle = pygame.Rect(0, 0, 32, 32)
        self.ButtonRightRectangle = pygame.Rect(34, 0, 32, 32)
        self.ListSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)
        self.ListSurfaceUpdated = False

    def Render(self, DISPLAY):
        # -- Recreate Surface -- #
        self.ListSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)

        mainScript.shape.Shape_Rectangle(DISPLAY, (0, 12, 30), (self.Rectangle[0], self.Rectangle[1] - 16, self.Rectangle[2], 16), 0, 0, 2, 2)
        mainScript.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 10, mainScript.DefaultCnt.Get_RegKey("/strings/game/game_items_view"), (255, 255, 255), self.Rectangle[0] + self.Rectangle[2] / 2 - mainScript.DefaultCnt.GetFont_width("/PressStart2P.ttf", 10, mainScript.DefaultCnt.Get_RegKey("/strings/game/game_items_view")) / 2, self.Rectangle[1] - 13)

        Draw_Panel(DISPLAY, self.Rectangle)

        for i, itemID in enumerate(self.ItemsID):
            ItemName = mainScript.DefaultCnt.Get_RegKey("/ItemData/name/" + str(itemID))
            ItemWidth = 156

            ItemX = self.ScrollX + ItemWidth * i
            ItemRect = (ItemX, self.Rectangle[3] / 2 - 90 / 2, ItemWidth - 5, 90)

            # -- Draw the Background -- #
            Draw_Panel(self.ListSurface, ItemRect, True)

            # -- Render the Item Title -- #
            mainScript.DefaultCnt.FontRender(self.ListSurface, "/PressStart2P.ttf", 9, ItemName, (250, 250, 250), ItemRect[0] + ItemRect[2] / 2 - mainScript.DefaultCnt.GetFont_width("/PressStart2P.ttf", 9, ItemName) / 2, ItemRect[1] + 2, mainScript.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

            # -- Render the Item Sprite -- #
            mainScript.DefaultCnt.ImageRender(self.ListSurface, mainScript.DefaultCnt.Get_RegKey(gameItems.GetItemSprite_ByID(int(itemID))), ItemRect[0] + 3, ItemRect[1] + 15, 64, 64, mainScript.DefaultCnt.Get_RegKey("/OPTIONS/sprite_aa"))

            # -- Render the Item Info -- #
            LittleInfoText = mainScript.DefaultCnt.Get_RegKey("/strings/game/items_info").format(utils.FormatNumber(gameItems.GetItemCount_ByID(self.ItemsID[i])).replace(".00", ""), str(gameItems.GetItemLevel_ByID(self.ItemsID[i])))

            # -- Render Item Info -- #
            mainScript.DefaultCnt.FontRender(self.ListSurface, "/PressStart2P.ttf", 10, LittleInfoText, (250, 250, 250), ItemRect[0] + 70, ItemRect[1] + 12, mainScript.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

        DISPLAY.blit(self.ListSurface, (self.Rectangle[0], self.Rectangle[1]))

    def ClearItems(self):
        self.ItemsID.clear()

    def Update(self, event):
        # -- Scroll the List -- #
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.Rectangle.collidepoint(mainScript.Cursor_Position):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.ScrollX += 5

                    elif event.button == 5:
                        self.ScrollX -= 5

    def Set_X(self, Value):
        self.Rectangle[0] = float(Value)

    def Set_Y(self, Value):
        self.Rectangle[1] = float(Value)

    def Set_W(self, Value):
        self.Rectangle[2] = float(Value)

    def Set_H(self, Value):
        self.Rectangle[3] = float(Value)

    def AddItem(self, ItemID):
        try:
            Index = self.ItemsID.index(int(ItemID))
            return
        except ValueError:
            self.ItemsID.append(int(ItemID))

class ValuesView:
    def __init__(self, Rectangle, Active):
        self.Rectangle = Rectangle
        self.Active = Active
        self.ValueBlocksList = list()

    def ChangeValue(self, BlockText, NewValue):
        Index = -1
        for i, ValBlock in enumerate(self.ValueBlocksList):
            if ValBlock.Text == str(BlockText):
                Index = i

        # -- If item was not found, add it -- #
        if Index == -1:
            self.AddValue(BlockText, NewValue)
            return

        self.ValueBlocksList[Index].Value = str(NewValue)

    def AddValue(self, Text, Value):
        self.ValueBlocksList.append(ValueBlock(Text, Value))

    def Draw(self, DISPLAY):
        ValsBlockSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)

        for i, ValBlock in enumerate(self.ValueBlocksList):
            ValBlock.Index = i
            ValBlock.Ypos = mainScript.DefaultCnt.GetFont_height("/PressStart2P.ttf", 13, "H") * i

            ValBlock.Draw(ValsBlockSurface)

        DISPLAY.blit(ValsBlockSurface, (self.Rectangle[0], self.Rectangle[1]))


class ValueBlock:
    def __init__(self, Text, Value):
        self.Text = str(Text)
        self.Value = str(Value)
        self.Ypos = 0
        self.Index = 0

    def Draw(self, DISPLAY):
        TextXpos = mainScript.DefaultCnt.GetFont_width("/PressStart2P.ttf", 10, self.Text)
        #  Render Block Text
        mainScript.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 10, self.Text, ValueView_TextColor, 3, self.Ypos, mainScript.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))
        # Render Block Value
        mainScript.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 10, self.Value, ValueView_ValueColor, TextXpos + 5, self.Ypos, mainScript.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

    def ChangeValue(self, Text, Value):
        self.Text = str(Text)
        self.Value = str(Value)
