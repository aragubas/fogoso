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
from Fogoso.MAIN.Screens import Settings as ScreenSettings
from Fogoso import MAIN as gameMain
from Fogoso.MAIN.Window import StoreWindow as storeWindow
from Fogoso.MAIN.Window import ExperienceStore as expStoreWindow
from Fogoso.MAIN.Window import InfosWindow as infosWindow
from ENGINE import SPRITE as sprite
from Fogoso.MAIN import GameVariables as save
from Fogoso.MAIN.Screens.Game import IncomingLog
from Fogoso.MAIN.Screens.Game import Maintenance as maintenance
from Fogoso.MAIN import GameItems as gameItems
from Fogoso.MAIN import ScreenTransition as transition
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
ItemsView = gameObjs.HorizontalItemsView

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
    # -- Save Items Data -- #
    gameItems.SaveItems()

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

    # -- Copy the Screen -- #
    if not SavingScreen_DISPLAYCopied:
        SavingScreen_DISPLAYCopied = True
        SavingScreenCopyOfScreen = HUD_Surface.copy()

    SavingSurfaceBackground = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()))
    SavingSurfaceBackground.blit(sprite.Surface_Blur(SavingScreenCopyOfScreen, BackgroundAnim_Numb), (0,0))
    DISPLAY.blit(SavingSurfaceBackground, (0, 0))

    TextsSurface = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()), pygame.SRCALPHA)
    TextsSurface.fill((0,0,0, 0))
    TextsSurface.set_alpha(BackgroundAnim_Numb * 8.5)

    SavingText = reg.ReadKey("/strings/game/save_screen/title")
    SavingStatusText = reg.ReadKey("/strings/game/save_screen/message")

    TextSavingX = DISPLAY.get_width() / 2 - sprite.GetFont_width("/PressStart2P.ttf", 50, SavingText) / 2
    TextSavingY = DISPLAY.get_height() / 2 - sprite.GetFont_height("/PressStart2P.ttf", 50, SavingText) / 2 - 100

    sprite.FontRender(TextsSurface, "/PressStart2P.ttf", 50, SavingText, (250, 250, 255), TextSavingX, TextSavingY, reg.ReadKey_bool("/OPTIONS/font_aa"))
    sprite.FontRender(TextsSurface, "/PressStart2P.ttf", 35, SavingStatusText, (250, 250, 255), DISPLAY.get_width() / 2 - sprite.GetFont_width("/PressStart2P.ttf", 35, SavingStatusText) / 2, TextSavingY + 100, reg.ReadKey_bool("/OPTIONS/font_aa"))

    DISPLAY.blit(TextsSurface, (0,0))

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
        if GrindButton.ButtonState == "UP":
            GrindClick()
        # -- Game Options Button -- #
        if GameOptionsButton.ButtonState == "UP":
            transition.Run()
            ScreenSettings.ScreenToReturn = gameMain.CurrentScreen
            ScreenSettings.Initialize()
            storeWindow.RestartAnimation()
            gameMain.CurrentScreen += 1

        # -- Save Buttons -- #
        if SaveButton.ButtonState == "UP":
            SavingScreenEnabled = True
            IsControlsEnabled = False

        # -- Back to Main Menu Button -- #
        if BackToMainMenuButton.ButtonState == "UP":
            transition.Run()
            BackToMainMenu = True

        if BackToMainMenu:
            BackToMainMenu_Delay += 1

            if BackToMainMenu_Delay >= 5:
                gameMain.CurrentScreen -= 1

                # -- Reset Variables -- #
                BackToMainMenu_Delay = 0
                BackToMainMenu = False

        # -- Open Store Button -- #
        if OpenStoreButton.ButtonState == "UP":
            if StoreWindow_Enabled:
                StoreWindow_Enabled = False
                storeWindow.RestartAnimation()
            else:
                StoreWindow_Enabled = True
                InfosWindow_Enabled = False
                ExperienceStore_Enabled = False

        # -- Open Infos Button -- #
        if OpenInfosWindowButton.ButtonState == "UP":
            if InfosWindow_Enabled:
                InfosWindow_Enabled = False
                storeWindow.RestartAnimation()
            else:
                InfosWindow_Enabled = True
                StoreWindow_Enabled = False
                ExperienceStore_Enabled = False

        # -- Open Experience Store Button -- #
        if OpenExperienceWindowButton.ButtonState == "UP" and gameItems.GetItemCount_ByID(-1) >= 1:
            if ExperienceStore_Enabled:
                ExperienceStore_Enabled = False
                storeWindow.RestartAnimation()
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
        if gameItems.GetItemCount_ByID(-1) >= 1:
            OpenExperienceWindowButton.Set_X(OpenInfosWindowButton.Rectangle[0] + OpenInfosWindowButton.Rectangle[2] + 5)
            OpenExperienceWindowButton.Set_Y(OpenInfosWindowButton.Rectangle[1])

        IncomingLog.Update()


BlinkExperienceEnabled = False
BlinkExperienceValue = 0
LastExperience = 0
def UpdateExperienceBlink():
    global BlinkExperienceEnabled
    global BlinkExperienceValue
    global LastExperience

    # -- Check if Experience has changed. -- #
    if not save.CUrrent_Experience == LastExperience:
        LastExperience = save.CUrrent_Experience
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
        HUD_Surface.fill((5, 13, 17))

        # -- Draw the Grind Text -- #
        IncomingLog.Draw(HUD_Surface)
        # -- Draw the Grind Button -- #
        GrindButton.Render(HUD_Surface)
        # -- Draw the Options Button -- #
        GameOptionsButton.Render(HUD_Surface)
        # -- Draw the Save Button -- #
        SaveButton.Render(HUD_Surface)
        # -- Draw the BackToMenu button -- #
        BackToMainMenuButton.Render(HUD_Surface)
        # -- Draw the Store Button -- #
        OpenStoreButton.Render(HUD_Surface)
        # -- Draw the Items View -- #
        ItemsView.Render(HUD_Surface)
        # -- Draw the OpenInfosWindow -- #
        OpenInfosWindowButton.Render(HUD_Surface)
        # -- Draw the OpenExperience -- #
        if gameItems.GetItemCount_ByID(-1) == 1:
            OpenExperienceWindowButton.Render(HUD_Surface)

        # -- Render Money Text -- #
        MoneyColor = (250,250,255)
        PerSecoundColor = (220, 220, 220)
        if save.Current_Money > 0.1:
            MoneyColor = (120, 220, 120)
        elif save.Current_Money <= 0:
            MoneyColor = (220, 10, 10)
        if save.Current_MoneyPerSecound > 0.1:
            PerSecoundColor = (50, 200, 50)
        elif save.Current_MoneyPerSecound <= 0:
            PerSecoundColor = (120, 10, 10)

        # -- Render Current Money, at Top -- #
        MoneyText = reg.ReadKey("/strings/game/money") + save.Current_MoneyFormated
        sprite.FontRender(HUD_Surface, "/PressStart2P.ttf", 18, reg.ReadKey("/strings/game/money") + save.Current_MoneyFormated, (0, 0, 0), 12, 22)
        sprite.FontRender(HUD_Surface, "/PressStart2P.ttf", 18, MoneyText, MoneyColor, 10, 20)

        # -- Render Money per Secound -- #
        MoneyPerSecoundText = reg.ReadKey("/strings/game/money_per_secound") + save.Current_MoneyPerSecoundFormatted
        sprite.FontRender(HUD_Surface, "/PressStart2P.ttf", 18, MoneyPerSecoundText, (0, 0, 0), 12, 52)
        sprite.FontRender(HUD_Surface, "/PressStart2P.ttf", 18, MoneyPerSecoundText, PerSecoundColor, 10, 50)

        # -- Render Experience -- #
        ExperienceText = reg.ReadKey("/strings/game/experience") + str(save.CUrrent_ExperienceFormated) + "/" + str(save.Current_TotalClicks - save.Current_TotalClicksNext) + "=" + str(save.Current_ExperiencePerEach)
        sprite.FontRender(HUD_Surface, "/PressStart2P.ttf", 18, ExperienceText, (BlinkExperienceValue, BlinkExperienceValue, BlinkExperienceValue), 12, 82)
        sprite.FontRender(HUD_Surface, "/PressStart2P.ttf", 18, ExperienceText, (140 + BlinkExperienceValue, 130 + BlinkExperienceValue, 120 + BlinkExperienceValue), 10, 80)

        # -- Render the Clock -- #
        # -- Time -- #
        SecoundsText = reg.ReadKey("/strings/game/clock").format(str(save.CurrentDate_Minute), str(save.CurrentDate_Secound), str(save.CurrentDate_DayLimiter), str(save.CurrentDate_MinuteLimiter))
        sprite.FontRender(HUD_Surface, "/PressStart2P.ttf", 10, SecoundsText, (0, 0, 0), HUD_Surface.get_width() / 2 - sprite.GetFont_width("/PressStart2P.ttf", 10, SecoundsText) / 2 + 2, 7, reg.ReadKey_bool("/OPTIONS/font_aa"))
        sprite.FontRender(HUD_Surface, "/PressStart2P.ttf", 10, SecoundsText, (230, 230, 230), HUD_Surface.get_width() / 2 - sprite.GetFont_width("/PressStart2P.ttf", 10, SecoundsText) / 2, 5, reg.ReadKey_bool("/OPTIONS/font_aa"))

        # -- Day -- #
        DateText = reg.ReadKey("/strings/game/calendar").format(str(save.CurrentDate_Day), str(save.CurrentDate_Month), str(save.CurrentDate_Year), str(save.CurrentDate_MonthLimiter), str(save.CurrentDate_YearLimiter))
        sprite.FontRender(HUD_Surface, "/PressStart2P.ttf", 10, DateText, (0, 0, 0), HUD_Surface.get_width() / 2 - sprite.GetFont_width("/PressStart2P.ttf", 10, DateText) / 2 + 2, sprite.GetFont_height("/PressStart2P.ttf", 10, SecoundsText) + 12, reg.ReadKey_bool("/OPTIONS/font_aa"))
        sprite.FontRender(HUD_Surface, "/PressStart2P.ttf", 10, DateText, (230, 230, 230), HUD_Surface.get_width() / 2 - sprite.GetFont_width("/PressStart2P.ttf", 10, DateText) / 2, sprite.GetFont_height("/PressStart2P.ttf", 10, SecoundsText) + 10, reg.ReadKey_bool("/OPTIONS/font_aa"))

        # -- Draw the Store Window -- #
        if StoreWindow_Enabled:
            storeWindow.Render(HUD_Surface)

        # -- Draw the Infos Window -- #
        if InfosWindow_Enabled:
            infosWindow.Render(HUD_Surface)

        # -- Draw the Exp Store Window -- #
        if ExperienceStore_Enabled and gameItems.GetItemCount_ByID(-1) >= 1:
            expStoreWindow.Render(HUD_Surface)

        DISPLAY.blit(HUD_Surface, (0, 0))

        # -- Update Surface Size -- #
        if not HUD_Surface.get_width() == DISPLAY.get_width() or not HUD_Surface.get_height() == DISPLAY.get_height():
            print("GameRenderMain : HUD_Surface has been updated.")
            HUD_Surface = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()), pygame.SRCALPHA)

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
    GrindButton = gameObjs.Button(pygame.rect.Rect(15, 115, 130, 150), "Loremk ipsum dolor sit amet...", 18)
    GrindButton.WhiteButton = True
    GameOptionsButton = gameObjs.Button(pygame.rect.Rect(DISPLAY.get_width() - 120, 5, 0, 0), reg.ReadKey("/strings/button/game/options"), 12)
    SaveButton = gameObjs.Button(pygame.rect.Rect(DISPLAY.get_width() - 120, 20, 0, 0), reg.ReadKey("/strings/button/game/save"), 12)
    BackToMainMenuButton = gameObjs.Button(pygame.Rect(DISPLAY.get_width() - 120,35,0,0),reg.ReadKey("/strings/button/game/main_menu"),12)
    OpenStoreButton = gameObjs.Button(pygame.Rect(5,DISPLAY.get_height() - 25,0,0),reg.ReadKey("/strings/button/game/store"),14)
    OpenInfosWindowButton = gameObjs.Button(pygame.Rect(0, 0, 0, 0), reg.ReadKey("/strings/button/game/infos"), 14)
    OpenExperienceWindowButton = gameObjs.Button(pygame.Rect(0,0,0,0), reg.ReadKey("/strings/button/game/experience_store"), 14)
    ItemsView = gameObjs.HorizontalItemsView(pygame.Rect(5, 500, 430, 100))

    IncomingLog.Initialize()

    # -- Load Saved Values -- #
    LoadGame()
    print("GameScreen : All objects initialized.")

    # -- Initialize Objects -- #
    storeWindow.Initialize()
    expStoreWindow.Initialize()
    infosWindow.Initialize()
    gameMain.ClearColor = (5, 20, 14)

    # -- Initialize the Screen -- #
    HUD_Surface = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()))

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
        GrindClick()

    if event.type == pygame.KEYUP and event.key == pygame.K_m:
        GrindClick()


def GrindClick():
    save.Current_TotalClicks += 1

    # -- €xp Mining -- #
    if save.Current_TotalClicks == save.Current_TotalClicksNext:
        save.Current_TotalClicksNext = save.Current_TotalClicks + save.Current_TotalClicksForEach
        save.CUrrent_Experience += save.Current_ExperiencePerEach
        IncomingLog.AddMessageText("€+" + str(save.Current_ExperiencePerEach), False, (150,150,150))

    IncomingLog.AddMessageText("+" + str(save.Current_MoneyValuePerClick), True, (20, 150, 25), save.Current_MoneyValuePerClick)

