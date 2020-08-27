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
from ENGINE import MAIN as taiyouMain
from ENGINE import APPDATA as reg
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso.MAIN import ScreenTransition as transition
from Fogoso import MAIN as gameMain

class ChangeableValueBlock:
    def __init__(self, Text, Value, ValueType, ID):
        self.Text = str(Text)
        self.Value = str(Value)
        self.ValueType = ValueType
        self.Ypos = 0
        self.Index = 0
        self.ChangeButton = gameObjs.Button((0, 0, 0, 0), "Toggle", 8)
        self.Xoffset = 0
        self.Yoffset = 0
        self.Response = -1002
        self.ID = ID

        # -- Set the Button Type -- #
        if ValueType == int or float:
            self.ChangeButton = gameObjs.UpDownButton(5, 5, 8)

            self.ChangeButton.UpButton.CustomColisionRectangle = True
            self.ChangeButton.DownButton.CustomColisionRectangle = True

        self.ChangeButton.CustomColisionRectangle = True

    def Draw(self, DISPLAY):
        # Render the Change Button
        ButtonSize = 0
        if self.ValueType == bool:
            ButtonSize = self.ChangeButton.Rectangle[2]

        elif self.ValueType == int or self.ValueType == float:
            ButtonSize = self.ChangeButton.UpButton.Rectangle[2] * 2

        TextXpos = ButtonSize + gameMain.DefaultCnt.GetFont_width("/PressStart2P.ttf", 10, self.Text)
        #  Render Block Text
        gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 10, self.Text, gameObjs.ValueView_TextColor, ButtonSize + 3, self.Ypos, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

        # Render Block Value
        gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 10, self.Value, gameObjs.ValueView_ValueColor, TextXpos + 15, self.Ypos, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

        self.ChangeButton.Render(DISPLAY)

    def Update(self, event):
        self.ChangeButton.Update(event)
        self.ChangeButton.Set_X(0)
        self.ChangeButton.Set_Y(self.Ypos + 1)

        if self.ValueType == int or self.ValueType == float:
            self.ChangeButton.UpButton.Set_ColisionX(self.Xoffset)
            self.ChangeButton.UpButton.Set_ColisionY(self.Yoffset)

            self.ChangeButton.DownButton.Set_ColisionX(self.ChangeButton.UpButton.ColisionRectangle[0] + self.ChangeButton.DownButton.ColisionRectangle[2])
            self.ChangeButton.DownButton.Set_ColisionY(self.ChangeButton.UpButton.ColisionRectangle[1])

            if self.ChangeButton.ButtonState == 1:
                self.Response == "ADD"
            elif self.ChangeButton.ButtonState == 2:
                self.Response == "DOWN"

        elif self.ValueType == bool:

            self.ChangeButton.Set_ColisionX(self.Xoffset)
            self.ChangeButton.Set_ColisionY(self.Yoffset)



    def ChangeValue(self, Text, Value):
        self.Text = str(Text)
        self.Value = str(Value)

class ChangeableValuesView:
    def __init__(self, Rectangle, Active):
        self.Rectangle = Rectangle
        self.Active = Active
        self.ValueBlocksList = list()
        self.ResponseID = 0
        self.ResponseControl = 0

    def ChangeValue(self, BlockText, NewValue, ValueType, ID):
        Index = -1
        for i, ValBlock in enumerate(self.ValueBlocksList):
            if ValBlock.ID == int(ID):
                Index = i
                break

        # -- If item was not found, add it -- #
        if Index == -1:
            self.AddValue(BlockText, NewValue, ValueType, int(ID))
            return

        self.ValueBlocksList[Index].Value = str(NewValue)

    def EventUpdate(self, event):
        for ValBlocks in self.ValueBlocksList:
            ValBlocks.Update(event)

    def AddValue(self, Text, Value, ValueType, ID):
        self.ValueBlocksList.append(ChangeableValueBlock(Text, Value, ValueType, ID))

    def Draw(self, DISPLAY):
        ValsBlockSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)

        for i, ValBlock in enumerate(self.ValueBlocksList):
            ValBlock.Index = i
            ValBlock.Ypos = gameMain.DefaultCnt.GetFont_height("/PressStart2P.ttf", 13, "H") * i + 5

            ValBlock.Draw(ValsBlockSurface)
            ValBlock.Xoffset = self.Rectangle[0]
            ValBlock.Yoffset = self.Rectangle[1] + gameMain.DefaultCnt.GetFont_height("/PressStart2P.ttf", 13, "H") * i

        DISPLAY.blit(ValsBlockSurface, (self.Rectangle[0], self.Rectangle[1]))

        # -- CLear the Response -- #
        if not self.ResponseID == "":
            self.ResponseID = -1
            self.ResponseControl = "NULL"

    def Update(self):
        for block in self.ValueBlocksList:
            if not block.Response == -1002:
                self.ResponseID = block.ID
                self.ResponseControl = block.Response
                block.Response = -1002
                print("REPOSTA ACHADA")
                break


ElementsX = 0
ElementsY = 0
changeable_values_view = ChangeableValuesView

def Initialize():
    global changeable_values_view

    changeable_values_view = ChangeableValuesView((120, 120, 500, 400), True)

def EventUpdate(event):
    global changeable_values_view

    changeable_values_view.EventUpdate(event)

def Update():
    global changeable_values_view

    changeable_values_view.ChangeValue("MaxFPS", str(gameMain.Engine_MaxFPS), int, 0)
    changeable_values_view.ChangeValue("FlashAnimationSpeed", str(gameMain.DefaultCnt.Get_RegKey("/OPTIONS/fade_flash_speed", int)), int, 1)
    changeable_values_view.Rectangle = pygame.Rect(ElementsX + 15, ElementsY + 50, 558, 258)
    changeable_values_view.Update()

    print(changeable_values_view.ResponseID)
    print(changeable_values_view.ResponseControl)

    if changeable_values_view.ResponseID == 0:
        if changeable_values_view.ResponseControl == "ADD":
            print("MaxFPS is [" + str(gameMain.Engine_MaxFPS) + "]")
            gameMain.Engine_MaxFPS += 5

            if gameMain.Engine_MaxFPS >= 75:
                gameMain.Engine_MaxFPS = 50

            taiyouMain.ReceiveCommand(0, gameMain.Engine_MaxFPS)
            gameMain.DefaultCnt.Write_RegKey("/OPTIONS/maxFPS", str(gameMain.Engine_MaxFPS))
            print("MaxFPS is now set to[" + str(gameMain.Engine_MaxFPS) + "]")

    """
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
    """

def Render(DISPLAY):
    global changeable_values_view

    changeable_values_view.Draw(DISPLAY)
