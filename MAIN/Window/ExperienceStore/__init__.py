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

from ENGINE import APPDATA as reg
from ENGINE import UTILS as utils
from Fogoso.MAIN.Screens.Game import IncomingLog as IncomingLog
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso.MAIN import GameVariables as save
import pygame
from Fogoso import MAIN as gameMain
from Fogoso.MAIN import GameItems as gameItems

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
    WindowObject = gameObjs.Window(pygame.Rect(100,100,gameMain.DefaultCnt.Get_RegKey("/props/window/expecience_store/last_w", int), gameMain.DefaultCnt.Get_RegKey("/props/window/expecience_store/last_h", int)), gameMain.DefaultCnt.Get_RegKey("/strings/window/expecience_store/window_title"),True)
    WindowObject.Minimizable = False
    BuyButton = gameObjs.Button(pygame.Rect(20, 20, 50, 50), gameMain.DefaultCnt.Get_RegKey("/strings/window/expecience_store/buy_button"), 14)
    BuyButton.CustomColisionRectangle = True
    DrawnSurface = pygame.Surface((WindowObject.WindowSurface_Rect[2], WindowObject.WindowSurface_Rect[3]), pygame.SRCALPHA)

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
    DrawnSurface = pygame.Surface((WindowObject.WindowSurface_Rect[2], WindowObject.WindowSurface_Rect[3]), pygame.SRCALPHA)

    if not StoreLocked:
        # -- Draw the List -- #
        ListItems.Render(DrawnSurface)

        # -- Render the Selected Item Text -- #
        if ListItems.LastItemClicked != "null":
            if LastClickedItem != ListItems.LastItemClicked:
                DownBar_BuyPanelAnimEnabled = True
                DownBar_BuyPanelYOffset = 0
            LastClickedItem = ListItems.LastItemClicked

            # -- Set Item Price and ID -- #
            SelectedItemID = ListItems.LastItemOrderID - 1
            SelectedItemLevel = gameItems.GetItemLevel_ByID(SelectedItemID) + 1
            SelectedItemPrice = gameItems.GetItemUpgradePrice_ByID(SelectedItemID)

            # -- Down Panel Background -- #
            CONTENT_MANAGER.Shape_Rectangle(DrawnSurface, (0, 0, 0, 100), (0, DrawnSurface.get_height() - DownBar_BuyPanelYOffset, DrawnSurface.get_width(), DownBar_BuyPanelYOffset))
            CONTENT_MANAGER.Shape_Rectangle(DrawnSurface, (16, 166, 152), (0, DrawnSurface.get_height() - DownBar_BuyPanelYOffset - 1, DrawnSurface.get_width(), 1))

            # -- Draw the Buy Button -- #
            BuyButton.Render(DrawnSurface)

            # -- Draw the Item Title -- #
            CONTENT_MANAGER.FontRender(DrawnSurface, "/PressStart2P.ttf", 15, ListItems.LastItemClicked, (250, 250, 250), 10, DrawnSurface.get_height() - DownBar_BuyPanelYOffset + 5, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"))

            # -- Draw the Item Price -- #
            PriceTextOpacity = 255
            if save.Current_Experience < SelectedItemPrice:
                PriceTextOpacity = 100 - abs(save.Current_Experience - SelectedItemPrice)

                if PriceTextOpacity <= 100:
                    PriceTextOpacity = 100

            CONTENT_MANAGER.FontRender(DrawnSurface, "/PressStart2P.ttf", 8, "€xp" + str(utils.FormatNumber(SelectedItemPrice)), (PriceTextOpacity, PriceTextOpacity, PriceTextOpacity), 10, DrawnSurface.get_height() - DownBar_BuyPanelYOffset + 20, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"), Opacity=PriceTextOpacity)

    WindowObject.Render(DISPLAY) # -- Render Window Border
    DISPLAY.blit(DrawnSurface, (WindowObject.WindowSurface_Rect[0], WindowObject.WindowSurface_Rect[1]))  # -- Render Window Objects

def Update():
    global DownBar_BuyPanelYOffset
    global DownBar_BuyPanelAnimEnabled
    global DownBar_BuyPanelYOffsetAdder

    # -- Set the Buy Button Location -- #
    BuyButton.Set_X(WindowObject.WindowRectangle[2] - BuyButton.Rectangle[2] - 5)
    BuyButton.Set_Y(WindowObject.WindowRectangle[3] - BuyButton.Rectangle[3] - DownBar_BuyPanelYOffset + 5)
    # -- Set the Buy Button Collision -- #
    BuyButton.Set_ColisionX(WindowObject.WindowRectangle[0] + BuyButton.Rectangle[0])
    BuyButton.Set_ColisionY(WindowObject.WindowRectangle[1] + BuyButton.Rectangle[1] + BuyButton.Rectangle[3])

    if BuyButton .ButtonState == 2:
        BuyButton.ButtonState = "INATIVE"
        if save.Current_Experience >= gameItems.GetItemUpgradePrice_ByID(SelectedItemID):
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

def GetNextLevelByID(ItemID):
    CurrentLevel = gameItems.GetItemLevel_ByID(ItemID)
    CurrentLevel += 1

    return CurrentLevel

def BuyItem_ByID(ItemID):
    global SelectedItemLevel
    global LastClickedItem
    global SelectedItemPrice
    global SelectedItemID
    Price = gameItems.GetItemUpgradePrice_ByID(ItemID)

    print("BuyItemUpgrade : ItemID[{0}] Price[{1}]".format(str(ItemID), str(Price)))

    if save.Current_Experience >= Price:
        save.Current_Experience -= Price
        IncomingLog.AddMessageText(gameMain.DefaultCnt.Get_RegKey("/strings/window/expecience_store/item_upgrade"), False, (140, 240, 140))

        # -- Write item level Information -- #
        gameItems.IncreaseItemLevel_ByID(ItemID)

        ReloadItemsList()
    else:
        sound.PlaySound("/hit_2.wav", 0.5)

def ReloadItemsList():
    global ListItems
    global SelectedItemLevel
    global LastClickedItem
    global SelectedItemPrice
    global SelectedItemID
    ListItems = gameObjs.VerticalListWithDescription(pygame.Rect(0, 0, 350, 250))

    ListItems.ClearItems()
    print("ReloadItemsList : Add Store Items")
    for x in range(gameMain.DefaultCnt.Get_RegKey("/ItemData/minimum", int), gameMain.DefaultCnt.Get_RegKey("/ItemData/all", int) + 1):
        # -- Check if item is Visible -- #
        if gameMain.DefaultCnt.Get_RegKey("/ItemData/" + str(x) + "/is_upgradeable"):

            # -- Reg Keys Locations -- #
            CurrentItemRoot = "/ItemData/upgrade/" + str(x) + "_"
            CurrentItemLevel = gameItems.GetItemLevel_ByID(x) + 1
            CurrentItemSprite = gameItems.GetItemSprite_ByID(x)
            CurrentItemDescription = CurrentItemRoot + "description_" + str(CurrentItemLevel)
            CurrentItemName = CurrentItemRoot + "name_" + str(CurrentItemLevel)

            print("ReloadItemsList : CurrentItem[" + CurrentItemRoot + "]")
            ListItems.AddItem(gameMain.DefaultCnt.Get_RegKey(CurrentItemName), gameMain.DefaultCnt.Get_RegKey(CurrentItemDescription), gameMain.DefaultCnt.Get_RegKey(CurrentItemSprite))

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
