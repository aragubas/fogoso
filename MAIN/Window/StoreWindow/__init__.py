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
from Fogoso.MAIN.Screens import Game as GameScreen 
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso.MAIN import GameItems as gameItems
from Fogoso.MAIN import GameVariables as save
from ENGINE import UTILS as utils
from Fogoso.MAIN.Screens.Game import IncomingLog as IncomingLog
from ENGINE import SOUND as sound
import pygame

print("Fogoso Store Window, Version 1.2")

# -- Field -- #
WindowObject = gameObjs.Window
BuyButton = gameObjs.Button
DrawnSurface = pygame.Surface((0,0))
ListItems = gameObjs.VerticalListWithDescription
SelectedItemPrice = 0
SelectedItemID = 0
DownBar_BuyPanelYOffset = 0
DownBar_BuyPanelYOffsetAdder = 0
DownBar_BuyPanelAnimEnabled = True
LastClickedItem = "null"
StoreLocked = False
BuyAmountButton = gameObjs.UpDownButton
LastItemIDSelected = None

def Initialize():
    global WindowObject
    global BuyButton
    global DrawnSurface
    global ListItems
    WindowObject = gameObjs.Window(pygame.Rect(100,100,430,285), reg.ReadKey("/strings/window/store/window_title"), True)
    WindowObject.Minimizable = False
    BuyButton = gameObjs.Button(pygame.Rect(20, 20, 50, 50), reg.ReadKey("/strings/window/store/buy_button"), 14)
    BuyButton.CustomColisionRectangle = True
    DrawnSurface = pygame.Surface((WindowObject.WindowSurface_Rect[2], WindowObject.WindowSurface_Rect[3]), pygame.SRCALPHA)
    ListItems = gameObjs.VerticalListWithDescription(pygame.Rect(0, 0, 350, 250))

def ReloadItemsList():
    global ListItems

    # -- Load Items -- #
    for x in range(reg.ReadKey_int("/ItemData/minimum"), reg.ReadKey_int("/ItemData/all") + 1):
        # -- Check if item is Visible -- #
        if reg.ReadKey_bool("/ItemData/" + str(x) + "/is_buyable"):
            CurrentItemRoot = "/ItemData/store/" + str(x) + "_"
            ItemSprite = gameItems.GetItemSprite_ByID(x)
            ListItems.AddItem(reg.ReadKey(CurrentItemRoot + "name"), reg.ReadKey(CurrentItemRoot + "description"), reg.ReadKey(ItemSprite))

def Render(DISPLAY):
    global WindowObject
    global DrawnSurface
    global BuyButton
    global ListItems
    global DownBar_BuyPanelAnimEnabled
    global DownBar_BuyPanelYOffset
    global LastClickedItem
    global SelectedItemID
    global StoreLocked
    global SelectedItemPrice

    if not StoreLocked:
        # -- Update the Surface -- #
        DrawnSurface = pygame.Surface((WindowObject.WindowSurface_Rect[2], WindowObject.WindowSurface_Rect[3]), pygame.SRCALPHA)

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

            # -- Down Panel Background -- #
            sprite.Shape_Rectangle(DrawnSurface, (0, 0, 0, 100), (0, DrawnSurface.get_height() - DownBar_BuyPanelYOffset, DrawnSurface.get_width(), DownBar_BuyPanelYOffset))
            sprite.Shape_Rectangle(DrawnSurface, (16, 166, 152), (0, DrawnSurface.get_height() - DownBar_BuyPanelYOffset - 1, DrawnSurface.get_width(), 1))

            # -- Draw the Buy Button -- #
            BuyButton.Render(DrawnSurface)

            # -- Draw the Item Title -- #
            sprite.FontRender(DrawnSurface, "/PressStart2P.ttf", 15, ListItems.LastItemClicked, (250, 250, 250), 10, DrawnSurface.get_height() - DownBar_BuyPanelYOffset + 5, reg.ReadKey_bool("/OPTIONS/font_aa"))

            # -- Draw the Item Price -- #
            PriceTextOpacity = 255
            if save.Current_Money < SelectedItemPrice:
                PriceTextOpacity = 100 - abs(save.Current_Money - SelectedItemPrice)

                if PriceTextOpacity <= 100:
                    PriceTextOpacity = 100

            sprite.FontRender(DrawnSurface, "/PressStart2P.ttf", 8, "$" + str(utils.FormatNumber(SelectedItemPrice)), (PriceTextOpacity, PriceTextOpacity, PriceTextOpacity), 10, DrawnSurface.get_height() - DownBar_BuyPanelYOffset + 20, reg.ReadKey_bool("/OPTIONS/font_aa"), Opacity=PriceTextOpacity)

    WindowObject.Render(DISPLAY)
    DISPLAY.blit(DrawnSurface, (WindowObject.WindowSurface_Rect[0], WindowObject.WindowSurface_Rect[1]))


def UpdateControls():
    global DownBar_BuyPanelYOffset
    global DownBar_BuyPanelAnimEnabled
    global DownBar_BuyPanelYOffsetAdder
    global BuyAmout
    global LastItemIDSelected
    global SelectedItemPrice
    global SelectedItemID

    # -- Set Item Price and ID -- #
    if not LastItemIDSelected == ListItems.LastItemOrderID:  # -- Only Update when needed
        SelectedItemPrice = gameItems.GetItemPrice_ByID(ListItems.LastItemOrderID)
        SelectedItemID = ListItems.LastItemOrderID

        LastItemIDSelected = ListItems.LastItemOrderID

    # -- Set the Buy Button Location -- #
    BuyButton.Set_X(WindowObject.WindowRectangle[2] - BuyButton.Rectangle[2] - 5)
    BuyButton.Set_Y(WindowObject.WindowRectangle[3] - BuyButton.Rectangle[3] - DownBar_BuyPanelYOffset + 5)

    # -- Set the Buy Button Collision -- #
    BuyButton.Set_ColisionX(WindowObject.WindowRectangle[0] + BuyButton.Rectangle[0])
    BuyButton.Set_ColisionY(WindowObject.WindowRectangle[1] + BuyButton.Rectangle[1] + BuyButton.Rectangle[3])

    # -- Update Buy Button -- #
    if BuyButton .ButtonState == 2:
        # -- Update Item Price -- #
        SelectedItemPrice = gameItems.GetItemPrice_ByID(ListItems.LastItemOrderID)

        if save.Current_Money >= SelectedItemPrice:  # -- If you can buy the Item -- #
            BuyItem_ByID(SelectedItemID)

        else:  # -- Notify that you can't buy that item
            IncomingLog.AddMessageText(reg.ReadKey("/strings/window/store/cant_buy_item"), False, (250, 150, 150))
            sound.PlaySound("/hit_2.wav", 0.5)

    # -- Update the Items List -- #
    ListItems.Set_W(DrawnSurface.get_width())
    ListItems.Set_H(DrawnSurface.get_height())
    ListItems.ColisionXOffset = WindowObject.WindowRectangle[0]
    ListItems.ColisionYOffset = WindowObject.WindowRectangle[1] + 20

    # -- Update Buy Panel Animation -- #
    if DownBar_BuyPanelAnimEnabled:
        DownBar_BuyPanelYOffsetAdder += 1
        DownBar_BuyPanelYOffset += DownBar_BuyPanelYOffsetAdder

        if DownBar_BuyPanelYOffset >= 30:
            DownBar_BuyPanelYOffset = 30
            DownBar_BuyPanelAnimEnabled = False
            DownBar_BuyPanelYOffsetAdder = 0

def RestartAnimation():
    global DownBar_BuyPanelAnimEnabled
    global DownBar_BuyPanelYOffset
    global LastClickedItem
    DownBar_BuyPanelAnimEnabled = False
    DownBar_BuyPanelYOffset = 0
    LastClickedItem = "null"

def BuyItem_ByID(ItemID):
    ItemID = int(ItemID)
    ItemPrice = gameItems.GetItemPrice_ByID(ItemID)
    ItemCount = gameItems.GetItemCount_ByID(ItemID)
    ItemIsUnlocker = gameItems.GetItemIsUnlocker_ByID(ItemID)
    BuySucefully = False

    if ItemIsUnlocker:  # -- Buy Unlocker Items
        if not ItemCount >= 1:
            # -- Increase Item Count -- #
            gameItems.IncreaseItemCount_ByID(ItemID)

            # -- Create Item Object -- #
            gameItems.CreateItemObject(ItemID)

            BuySucefully = True

    else:  # -- Buy Common Items -- #
        # -- Increase Item Count -- #
        gameItems.IncreaseItemCount_ByID(ItemID)

        # -- Create Item Object -- #
        gameItems.CreateItemObject(ItemID)

        BuySucefully = True

    if BuySucefully:
        # -- Subtract the Money -- #
        IncomingLog.AddMessageText(utils.FormatNumber(-ItemPrice, 2), True, (250, 150, 150), -ItemPrice)

        # -- Add Item to the Item View on Game Screen -- #
        GameScreen.ItemsView.AddItem(str(ItemID))
    else:
        # -- Subtract the Money -- #
        IncomingLog.AddMessageText(reg.ReadKey("/strings/window/store/cant_buy_item"), False, (250, 150, 150))
        sound.PlaySound("/hit_2.wav", 0.5)


def EventUpdate(event):
    global StoreLocked
    WindowObject.EventUpdate(event)

    if not StoreLocked:
        BuyButton.Update(event)
        ListItems.Update(event)
