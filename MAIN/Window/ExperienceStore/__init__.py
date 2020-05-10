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

from ENGINE import SPRITE as sprite
from ENGINE import REGISTRY as reg
from ENGINE import UTILS as utils
from Fogoso.MAIN.Screens.Game import IncomingLog as IncomingLog
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso.MAIN import GameVariables as save
import pygame

print("Fogoso Experience Store Window, Version 1.0")

# -- Field -- #
WindowObject = gameObjs.Window
BuyButton = gameObjs.Button
DrawnSurface = pygame.Surface((0,0))
ListItems = gameObjs.VerticalListWithDescription
SelectedItemPrice = 0
SelectedItemID = 0
SelectedItemLevel = 0
DownBar_BuyPanelYOffset = 0
DownBar_BuyPanelYOffsetAdder = 0
DownBar_BuyPanelAnimEnabled = True
LastClickedItem = "null"
StoreLocked = False

def Initialize():
    global WindowObject
    global BuyButton
    global DrawnSurface
    global ListItems
    global BuyAmout
    WindowObject = gameObjs.Window(pygame.Rect(100,100,reg.ReadKey_int("/props/window/expecience_store/last_w"),reg.ReadKey_int("/props/window/expecience_store/last_h")), reg.ReadKey("/strings/window/expecience_store/window_title"),True)
    WindowObject.Minimizable = False
    BuyButton = gameObjs.Button(pygame.Rect(20, 20, 50, 50), reg.ReadKey("/strings/window/expecience_store/buy_button"), 14)
    BuyButton.CustomColisionRectangle = True
    DrawnSurface = WindowObject.WindowSurface
    ReloadItemsList()

def Render(DISPLAY):
    global WindowObject
    global DrawnSurface
    global BuyButton
    global ListItems
    global DownBar_BuyPanelAnimEnabled
    global DownBar_BuyPanelYOffset
    global LastClickedItem
    global SelectedItemID
    global SelectedItemPrice
    global SelectedItemLevel
    global StoreLocked
    # -- Update the Surface -- #
    DrawnSurface = WindowObject.WindowSurface

    if not StoreLocked:
        # -- Update Controls -- #
        UpdateControls()

        # -- Draw the List -- #
        ListItems.Render(DrawnSurface)

        # -- Render the Selected Item Text -- #
        if ListItems.LastItemClicked != "null":
            if LastClickedItem != ListItems.LastItemClicked:
                DownBar_BuyPanelAnimEnabled = True
                DownBar_BuyPanelYOffset = 0
            LastClickedItem = ListItems.LastItemClicked

            # -- Set Item Price and ID -- #
            SelectedItemID = GetItemID_ByName(ListItems.LastItemClicked)
            SelectedItemLevel = GetNextLevelByID(SelectedItemID)
            SelectedItemPrice = GetItemPrice_ByID(SelectedItemID)
            
            # -- Down Panel Background -- #
            sprite.RenderRectangle(DrawnSurface, (0, 0, 0, 100), (0, DrawnSurface.get_height() - DownBar_BuyPanelYOffset, DrawnSurface.get_width(), DownBar_BuyPanelYOffset))
            sprite.RenderRectangle(DrawnSurface, (16, 166, 152), (0, DrawnSurface.get_height() - DownBar_BuyPanelYOffset - 1, DrawnSurface.get_width(), 1))
            # -- Draw the Buy Button -- #
            BuyButton.Render(DrawnSurface)
            # -- Draw the Item Title -- #
            sprite.RenderFont(DrawnSurface, "/PressStart2P.ttf", 15, ListItems.LastItemClicked,(250,250,250),10,DrawnSurface.get_height() - DownBar_BuyPanelYOffset + 5, reg.ReadKey_bool("/OPTIONS/font_aa"))
            # -- Draw the Item Price -- #
            sprite.RenderFont(DrawnSurface,"/PressStart2P.ttf",8, "€xp" + str(utils.FormatNumber(SelectedItemPrice)),(250,250,250),10,DrawnSurface.get_height() - DownBar_BuyPanelYOffset + 20, reg.ReadKey_bool("/OPTIONS/font_aa"))

    WindowObject.Render(DISPLAY)
    DISPLAY.blit(DrawnSurface, WindowObject.WindowSurface_Dest)


def UpdateControls():
    global DownBar_BuyPanelYOffset
    global DownBar_BuyPanelAnimEnabled
    global DownBar_BuyPanelYOffsetAdder
    global BuyAmout
    # -- Set the Buy Button Location -- #
    BuyButton.Set_X(WindowObject.WindowRectangle[2] - BuyButton.Rectangle[2] - 5)
    BuyButton.Set_Y(WindowObject.WindowRectangle[3] - BuyButton.Rectangle[3] - DownBar_BuyPanelYOffset + 5)
    # -- Set the Buy Button Collision -- #
    BuyButton.Set_ColisionX(WindowObject.WindowRectangle[0] + BuyButton.Rectangle[0])
    BuyButton.Set_ColisionY(WindowObject.WindowRectangle[1] + BuyButton.Rectangle[1] + BuyButton.Rectangle[3])

    if BuyButton.ButtonState == "UP":
        if save.CUrrent_Experience >= GetItemPrice_ByID(SelectedItemID):
            BuyItem_ByID(SelectedItemID)

    # -- Set Items List Size -- #
    ListItems.Set_W(DrawnSurface.get_width())
    ListItems.Set_H(DrawnSurface.get_height())
    ListItems.ColisionXOffset = WindowObject.WindowRectangle[0]
    ListItems.ColisionYOffset = WindowObject.WindowRectangle[1] + 20

    # -- Buy Panel -- #
    if DownBar_BuyPanelAnimEnabled:
        DownBar_BuyPanelYOffsetAdder += 1
        DownBar_BuyPanelYOffset += DownBar_BuyPanelYOffsetAdder

        if DownBar_BuyPanelYOffset >= 30:
            DownBar_BuyPanelYOffset = 30
            DownBar_BuyPanelAnimEnabled = False
            DownBar_BuyPanelYOffsetAdder = 0

def GetItemID_ByName(ItemName):
    global SelectedItemLevel
    return reg.ReadKey("/ItemData/upgrade/name/" + ItemName)

def GetNextLevelByID(ItemID):
    CurrentLevel = reg.ReadKey_int("/Save/item/last_level/" + ItemID)
    CurrentLevel = CurrentLevel + 1
    return CurrentLevel

def GetItemPrice_ByID(ItemID):
    global SelectedItemLevel
    CorrectKeyName = "/ItemData/upgrade/price/" + str(ItemID) + "_" + str(SelectedItemLevel)
    return reg.ReadKey_int(CorrectKeyName)

def BuyItem_ByID(ItemID):
    global SelectedItemLevel
    global LastClickedItem
    global SelectedItemPrice
    global SelectedItemID
    Price = GetItemPrice_ByID(ItemID)

    if Price < 0.0:
        IncomingLog.AddMessageText(reg.ReadKey("/strings/window/expecience_store/item_not_upgradable"), False, (250, 140, 140))
    else:
        save.CUrrent_Experience -= Price
        ItemLevelKey = "/Save/item/last_level/" + str(SelectedItemID)
        reg.WriteKey(ItemLevelKey, str(SelectedItemLevel))
        IncomingLog.AddMessageText(reg.ReadKey("/strings/window/expecience_store/item_upgrade"), False, (140, 240, 140))
        ReloadItemsList()
        
        # -- Reload Items Data -- #
        save.SaveItems()
        save.RestartItems()



def ReloadItemsList():
    global ListItems
    global SelectedItemLevel
    global LastClickedItem
    global SelectedItemPrice
    global SelectedItemID
    ListItems = gameObjs.VerticalListWithDescription(pygame.Rect(0, 0, 350, 250))

    print("ReloadItemsList : Add Store Items")
    for x in range(-1, reg.ReadKey_int("/ItemData/upgrade/all") + 1):
        CurrentItemRoot = "/ItemData/upgrade/" + str(x) + "_"
        CurrentItemLevel = reg.ReadKey_int("/Save/item/last_level/" + str(x)) + 1
        print("ReloadItemsList : CurrentItem[" + CurrentItemRoot + "]")
        ListItems.AddItem(reg.ReadKey(CurrentItemRoot + "name_" + str(CurrentItemLevel)), reg.ReadKey(CurrentItemRoot + "description_" + str(CurrentItemLevel)), reg.ReadKey(CurrentItemRoot + "sprite"))
    print("ReloadItemsList : Add Store Items")

    RestartAnimation()


def RestartAnimation():
    global DownBar_BuyPanelAnimEnabled
    global DownBar_BuyPanelYOffset
    global LastClickedItem
    DownBar_BuyPanelAnimEnabled = False
    DownBar_BuyPanelYOffset = 0
    LastClickedItem = "null"


def EventUpdate(event):
    global StoreLocked
    WindowObject.EventUpdate(event)

    if not StoreLocked:
        BuyButton.Update(event)
        ListItems.Update(event)
