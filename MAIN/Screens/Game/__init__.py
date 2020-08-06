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

from ENGINE import MAIN as taiyouMain
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso.MAIN.Screens import Settings as ScreenSettings
from Fogoso import MAIN as gameMain
from Fogoso.MAIN.Window import StoreWindow as storeWindow
from Fogoso.MAIN.Window import ExperienceStore as expStoreWindow
from Fogoso.MAIN.Window import InfosWindow as infosWindow
from Fogoso.MAIN import GameVariables as save
from Fogoso.MAIN.Screens.Game import IncomingLog
from Fogoso.MAIN.Screens.Game import Maintenance as maintenance
from Fogoso.MAIN import GameItems as gameItems
from Fogoso.MAIN import ScreenTransition as transition
from Fogoso.MAIN.Screens.Game import GameClock as gameClock
import ENGINE as tge
import pygame

# -- Objects Definition -- #
GrindButton = gameObjs.Button
GameOptionsButton = gameObjs.Button
SaveButton = gameObjs.Button
BackToMainMenuButton = gameObjs.Button
OpenStoreButton = gameObjs.Button
OpenInfosWindowButton = gameObjs.Button
OpenExperienceWindowButton = gameObjs.Button

# -- Game Items View -- #
ItemsView = gameObjs.GameItemsView

# -- Store Window -- #
StoreWindow_Enabled = False

# -- Infos Window -- #
InfosWindow_Enabled = True

# -- Experience Store Windows -- #
ExperienceStore_Enabled = False

# -- Unload -- #
BackToMainMenu = False
BackToMainMenu_Delay = 0

# -- Saving Screen Variables -- #
IsControlsEnabled = True
SavingScreenEnabled = False
SavingScreen_DISPLAYCopied = False
SavingSurfaceBackground = pygame.Surface
SavingScreenCopyOfScreen = pygame.Surface

Current_Maintenance = 0.0

# -- Background Animation -- #
BackgroundAnim_Type = 0
BackgroundAnim_Enabled = True
BackgroundAnim_Numb = 1.0

# -- HUD -- #
HUD_Surface = pygame.Surface

# -- Load/Save Functions -- #
def LoadGame():
    global ItemsView
    print("LoadGame : Init")
    transition.Run()

    save.LoadSaveData()

    print("LoadGame : Game Loaded Sucefully")

def SaveGame():
    global SavingScreenEnabled
    global IsControlsEnabled
    global BackgroundAnim_Type
    global BackgroundAnim_Enabled
    global BackgroundAnim_Numb

    # -- Save Game Data -- #
    save.SaveData()

    BackgroundAnim_Type = 1
    BackgroundAnim_Enabled = True

def UpdateSavingScreen(DISPLAY):
    global SavingScreenEnabled
    global IsControlsEnabled
    global BackgroundAnim_Type
    global BackgroundAnim_Enabled
    global BackgroundAnim_Numb
    global SavingScreen_DISPLAYCopied
    global SavingSurfaceBackground
    global SavingScreenCopyOfScreen
    global HUD_Surface

    # -- Copy the Screen -- #
    if not SavingScreen_DISPLAYCopied:
        SavingScreenCopyOfScreen = HUD_Surface.copy()
        SavingScreen_DISPLAYCopied = True

    # -- Draw the Blurred Background -- #
    DISPLAY.blit(gameMain.fx.Surface_Blur(SavingScreenCopyOfScreen, BackgroundAnim_Numb * 9), (0, 0))

    SavingText = gameMain.DefaultCnt.Get_RegKey("/strings/game/save_screen/title")
    SavingStatusText = gameMain.DefaultCnt.Get_RegKey("/strings/game/save_screen/message")
    TextsOpacity = BackgroundAnim_Numb * 8.5

    TextSavingX = DISPLAY.get_width() / 2 - gameMain.DefaultCnt.GetFont_width("/PressStart2P.ttf", 50, SavingText) / 2
    TextSavingY = DISPLAY.get_height() / 2 - gameMain.DefaultCnt.GetFont_height("/PressStart2P.ttf", 50, SavingText) / 2 - 100

    gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 50, SavingText, (250, 250, 255), TextSavingX, TextSavingY, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa"), Opacity=TextsOpacity)
    gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 35, SavingStatusText, (250, 250, 255), DISPLAY.get_width() / 2 - gameMain.DefaultCnt.GetFont_width("/PressStart2P.ttf", 35, SavingStatusText) / 2, TextSavingY + 100, gameMain.DefaultCnt.Get_RegKey("/OPTIONS/font_aa", bool), Opacity=TextsOpacity)

    # -- Run the Animation -- #
    if BackgroundAnim_Enabled:
        if BackgroundAnim_Type == 0:
            BackgroundAnim_Numb += 0.5
            if BackgroundAnim_Numb >= 30.5:
                BackgroundAnim_Enabled = False
                BackgroundAnim_Type = 1
                BackgroundAnim_Numb = 30.5
                SaveGame()

        if BackgroundAnim_Type == 1:
            BackgroundAnim_Numb -= 0.5
            if BackgroundAnim_Numb <= 1.1:
                BackgroundAnim_Numb = 1.0
                BackgroundAnim_Enabled = True
                BackgroundAnim_Type = 0

                SavingScreenEnabled = False
                IsControlsEnabled = True
                SavingScreen_DISPLAYCopied = False
                SavingScreenCopyOfScreen.fill((0, 0, 0))

def Update():
    global GameOptionsButton
    global BackToMainMenuButton
    global OpenStoreButton
    global StoreWindow_Enabled
    global ItemsView
    global BackToMainMenu_Delay
    global BackToMainMenu
    global IsControlsEnabled
    global SavingScreenEnabled
    global ExperienceStore_Enabled
    global InfosWindow_Enabled

    if IsControlsEnabled:
        # -- Update Save -- #
        save.Update()

        # -- Update Experience Blink -- #
        UpdateExperienceBlink()

        ItemsView.Set_X(5)
        ItemsView.Set_Y(gameMain.DefaultDisplay.get_height() - 130)

        # -- Update General Maintenance -- #
        maintenance.Update()

        # -- Update Buttons Click -- #
        if GrindButton .ButtonState == 2:
            save.TutorialTrigger("clicking_button")
            save.GrindClick()

        # -- Game Options Button -- #
        if GameOptionsButton .ButtonState == 2:
            transition.Run()
            ScreenSettings.ScreenToReturn = 1
            ScreenSettings.Initialize()
            storeWindow.RestartAnimation()
            gameMain.SetScreen_ByID(2)

        # -- Save Buttons -- #
        if SaveButton .ButtonState == 2:
            SavingScreenEnabled = True
            IsControlsEnabled = False

        # -- Back to Main Menu Button -- #
        if BackToMainMenuButton .ButtonState == 2:
            transition.Run()
            BackToMainMenu = True

        if BackToMainMenu:
            BackToMainMenu_Delay += 1

            if BackToMainMenu_Delay >= 5:
                gameMain.SetScreen_ByID(0)
                # -- Reset Variables -- #
                BackToMainMenu_Delay = 0
                BackToMainMenu = False

                SaveGame()

        # -- Store Button -- #
        if OpenStoreButton .ButtonState == 2:
            save.TutorialTrigger("store_window_button")

            if StoreWindow_Enabled:
                StoreWindow_Enabled = False
                storeWindow.RestartAnimation()
            else:
                StoreWindow_Enabled = True
                InfosWindow_Enabled = False
                ExperienceStore_Enabled = False

        # -- Infos Button -- #
        elif OpenInfosWindowButton .ButtonState == 2:
            save.TutorialTrigger("infos_window_button")

            if InfosWindow_Enabled:
                InfosWindow_Enabled = False
            else:
                InfosWindow_Enabled = True
                StoreWindow_Enabled = False
                ExperienceStore_Enabled = False

        # -- Experience Store Button -- #
        elif OpenExperienceWindowButton .ButtonState == 2 and gameItems.GetItemCount_ByID(-1) >= 1:
            save.TutorialTrigger("expstore_window_button")

            if ExperienceStore_Enabled:
                ExperienceStore_Enabled = False
                expStoreWindow.RestartAnimation()

            else:
                ExperienceStore_Enabled = True
                StoreWindow_Enabled = False
                InfosWindow_Enabled = False

        # -- Update Buttons Location -- #
        GameOptionsButton.Set_X(gameMain.DefaultDisplay.get_width() - 120)
        SaveButton.Set_X(gameMain.DefaultDisplay.get_width() - 120)
        BackToMainMenuButton.Set_X(gameMain.DefaultDisplay.get_width() - 120)
        GrindButton.Rectangle[2] = 130
        GrindButton.Rectangle[3] = 150
        OpenStoreButton.Set_X(5)
        OpenStoreButton.Set_Y(gameMain.DefaultDisplay.get_height() - OpenStoreButton.Rectangle[3] - 5)
        OpenInfosWindowButton.Set_X(OpenStoreButton.Rectangle[0] + OpenStoreButton.Rectangle[2] + 5)
        OpenInfosWindowButton.Set_Y(OpenStoreButton.Rectangle[1])
        OpenExperienceWindowButton.Set_X(OpenInfosWindowButton.Rectangle[0] + OpenInfosWindowButton.Rectangle[2] + 5)
        OpenExperienceWindowButton.Set_Y(OpenInfosWindowButton.Rectangle[1])

        # -- Update Windows -- #
        WindowsUpdate()

        # -- Update Objects -- #
        IncomingLog.Update()
        gameClock.Update()

def WindowsUpdate():
    if StoreWindow_Enabled:
        storeWindow.Update()

    elif ExperienceStore_Enabled:
        expStoreWindow.Update()

    elif InfosWindow_Enabled:
        infosWindow.Update()

BlinkExperienceEnabled = False
BlinkExperienceValue = 0
LastExperience = 0
def UpdateExperienceBlink():
    global BlinkExperienceEnabled
    global BlinkExperienceValue
    global LastExperience

    # -- Check if Experience has changed. -- #
    if not save.Current_Experience == LastExperience:
        LastExperience = save.Current_Experience
        BlinkExperienceEnabled = True

    # -- Do Animation -- #
    if BlinkExperienceEnabled:
        if BlinkExperienceValue < 100:
            BlinkExperienceValue += 5

        if BlinkExperienceValue >= 100:
            BlinkExperienceValue = 0
            BlinkExperienceEnabled = False

def GameDraw(DISPLAY):
    global BackToMainMenuButton
    global OpenStoreButton
    global OpenInfosWindowButton
    global OpenExperienceWindowButton
    global StoreWindow_Enabled
    global ItemsView
    global SavingScreenEnabled
    global BlinkExperienceValue
    global HUD_Surface

    if SavingScreenEnabled:
        UpdateSavingScreen(DISPLAY)

    if not SavingScreenEnabled:
        # -- Draw the Grind Text -- #
        IncomingLog.Draw(DISPLAY)
        # -- Draw the Grind Button -- #
        GrindButton.Render(DISPLAY)
        # -- Draw the Options Button -- #
        GameOptionsButton.Render(DISPLAY)
        # -- Draw the Save Button -- #
        SaveButton.Render(DISPLAY)
        # -- Draw the BackToMenu button -- #
        BackToMainMenuButton.Render(DISPLAY)
        # -- Draw the Store Button -- #
        OpenStoreButton.Render(DISPLAY)
        # -- Draw the Items View -- #
        ItemsView.Render(DISPLAY)
        # -- Draw the OpenInfosWindow -- #
        OpenInfosWindowButton.Render(DISPLAY)
        # -- Draw the OpenExperience -- #
        if gameItems.GetItemCount_ByID(-1) == 1:
            OpenExperienceWindowButton.Render(DISPLAY)

        # -- Render Money Text -- #
        MoneyColor = (250, 250, 255)
        PerSecoundColor = (220, 220, 220)
        if save.Current_Money > 0.1:
            MoneyColor = (120, 220, 120)
        elif save.Current_Money <= 0:
            MoneyColor = (220, 10, 10)
        if save.Current_MoneyPerSecond > 0.1:
            PerSecoundColor = (50, 200, 50)
        elif save.Current_MoneyPerSecond <= 0:
            PerSecoundColor = (120, 10, 10)

        # -- Render Current Money, at Top -- #
        MoneyText = gameMain.DefaultCnt.Get_RegKey("/strings/game/money") + save.Current_MoneyFormated
        gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 18, gameMain.DefaultCnt.Get_RegKey("/strings/game/money") + save.Current_MoneyFormated, (0, 0, 0), 12, 22)
        gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 18, MoneyText, MoneyColor, 10, 20)

        # -- Render Money per Second -- #
        MoneyPerSecoundText = gameMain.DefaultCnt.Get_RegKey("/strings/game/money_per_secound") + save.Current_MoneyPerSecondFormatted
        gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 18, MoneyPerSecoundText, (0, 0, 0), 12, 52)
        gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 18, MoneyPerSecoundText, PerSecoundColor, 10, 50)

        # -- Render Experience -- #
        ExperienceText = gameMain.DefaultCnt.Get_RegKey("/strings/game/experience") + str(save.Current_ExperienceFormated) + "/" + str(save.Current_TotalClicks - save.Current_TotalClicksNext) + "=" + str(save.Current_ExperiencePerEach)
        gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 18, ExperienceText, (BlinkExperienceValue, BlinkExperienceValue, BlinkExperienceValue), 12, 82)
        gameMain.DefaultCnt.FontRender(DISPLAY, "/PressStart2P.ttf", 18, ExperienceText, (140 + BlinkExperienceValue, 130 + BlinkExperienceValue, 120 + BlinkExperienceValue), 10, 80)

        # -- Render the Clock -- #
        gameClock.Draw(DISPLAY)

        # -- Draw the Store Window -- #
        if StoreWindow_Enabled:
            storeWindow.Render(DISPLAY)

        # -- Draw the Infos Window -- #
        if InfosWindow_Enabled:
            infosWindow.Render(DISPLAY)

        # -- Draw the Exp Store Window -- #
        if ExperienceStore_Enabled and gameItems.GetItemCount_ByID(-1) >= 1:
            expStoreWindow.Render(DISPLAY)

        HUD_Surface = DISPLAY.copy()

def Initialize(DISPLAY):
    # -- Set Buttons -- #
    global SaveButton
    global GameOptionsButton
    global GrindButton
    global BackToMainMenuButton
    global OpenStoreButton
    global ItemsView
    global OpenInfosWindowButton
    global OpenExperienceWindowButton
    global HUD_Surface

    # -- Initialize Buttons -- #
    GrindButton = gameObjs.Button(pygame.rect.Rect(15, 115, 130, 150), "Lorem", 18)
    GrindButton.WhiteButton = True
    GameOptionsButton = gameObjs.Button(pygame.rect.Rect(DISPLAY.get_width() - 120, 5, 0, 0), gameMain.DefaultCnt.Get_RegKey("/strings/button/game/options"), 12)
    SaveButton = gameObjs.Button(pygame.rect.Rect(DISPLAY.get_width() - 120, 20, 0, 0), gameMain.DefaultCnt.Get_RegKey("/strings/button/game/save"), 12)
    BackToMainMenuButton = gameObjs.Button(pygame.Rect(DISPLAY.get_width() - 120,35,0,0),gameMain.DefaultCnt.Get_RegKey("/strings/button/game/main_menu"),12)
    OpenStoreButton = gameObjs.Button(pygame.Rect(5,DISPLAY.get_height() - 25,0,0),gameMain.DefaultCnt.Get_RegKey("/strings/button/game/store"),14)
    OpenInfosWindowButton = gameObjs.Button(pygame.Rect(0, 0, 0, 0), gameMain.DefaultCnt.Get_RegKey("/strings/button/game/infos"), 14)
    OpenExperienceWindowButton = gameObjs.Button(pygame.Rect(0,0,0,0), gameMain.DefaultCnt.Get_RegKey("/strings/button/game/experience_store"), 14)
    ItemsView = gameObjs.GameItemsView(pygame.Rect(5, 500, 430, 100))

    IncomingLog.Initialize()

    # -- Initialize Objects -- #
    storeWindow.Initialize()
    expStoreWindow.Initialize()
    infosWindow.Initialize()
    gameMain.ClearColor = (5, 20, 14)

    # -- Initialize the Screen -- #
    HUD_Surface = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()))

#    # -- Load the Save Game -- #
    LoadGame()

def EventUpdate(event):
    # -- Update all buttons -- #
    global GrindButton
    global GameOptionsButton
    global SaveButton
    global BackToMainMenuButton
    global OpenStoreButton
    global StoreWindow_Enabled
    global ItemsView
    global IsControlsEnabled
    global OpenExperienceWindowButton
    global OpenInfosWindowButton
    global BlinkExperienceEnabled
    global HUD_Surface

    if IsControlsEnabled:
        GrindButton.Update(event)
        GameOptionsButton.Update(event)
        SaveButton.Update(event)
        BackToMainMenuButton.Update(event)
        OpenStoreButton.Update(event)
        ItemsView.Update(event)
        IncomingLog.EventUpdate(event)
        OpenInfosWindowButton.Update(event)

        if gameItems.GetItemCount_ByID(-1) == 1:
            OpenExperienceWindowButton.Update(event)

        # -- Update store Window -- #
        if StoreWindow_Enabled:
            storeWindow.EventUpdate(event)

        # -- Update Infos Window -- #
        if InfosWindow_Enabled:
            infosWindow.EventUpdate(event)

        if ExperienceStore_Enabled:
            expStoreWindow.EventUpdate(event)

    if event.type == pygame.KEYUP and event.key == pygame.K_z:
        save.GrindClick()

    if event.type == pygame.KEYUP and event.key == pygame.K_m:
        save.GrindClick()

