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
from ENGINE import appData
import ENGINE as tge
from Fogoso.MAIN.Screens import Game as gameScr
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso.MAIN import GameItems as gameItems
from Fogoso.MAIN.Screens.Game import Maintenance as maintenance
from Fogoso.MAIN.Window import StoreWindow as storeWindow
from Fogoso.MAIN.Window import ExperienceStore as expStoreWindow
from Fogoso.MAIN.Screens.Game import IncomingLog
from ENGINE import UTILS as utils
from random import randint
from Fogoso.MAIN import OverlayDialog
from Fogoso import MAIN as gameMain
from Fogoso.MAIN import PlanetData as planets

import os

print("Fogoso Variables Management, version 1.7")

# -- Money -- #
Current_Money = 0.0
Current_MoneyValuePerClick = 0.2
Current_MoneyMultiplier = 1
Current_MoneyMinimun = -15000.0
SaveDataLoaded = False
WelcomeMessageTriggered = False

# -- Experience -- #
Current_Experience = 250
Current_TotalClicks = 0
Current_TotalClicksNext = 0
Current_TotalClicksForEach = 0
Current_ExperiencePerEach = 20

# -- Formated Money Strings -- #
Current_MoneyPerSecond = 0.0
Current_MoneyFormated = "UNDEFINED"
Current_MoneyPerSecondFormatted = "UNDEFINED"
Current_ExperienceFormated = "0"
Current_MoneyPerClickBest = 0.0

# -- Money Per Secound -- #
MoneyPerSecond_Delta = 0
MoneyPerSecond_Last = 0.0

# -- Current Date -- #
CurrentDate_Day = 0
CurrentDate_Month = 0
CurrentDate_Year = 0
CurrentDate_Minute = 0
CurrentDate_Second = 0
CurrentDate_Microseconds = 0

# -- Date Limiters -- #
CurrentDate_DayLimiter = 0
CurrentDate_MonthLimiter = 0
CurrentDate_MinuteLimiter = 0
CurrentDate_SecondLimiter = 0
CurrentDate_YearLimiter = 0

# -- Tutoriais -- #
triggered_tutorials = list()

# -- Planet Data -- #
PlanetName = "Aragubas"
PlanetID = 0

# -- Load Saved Data -- #
def LoadSaveData():
    global CurrentDate_Day
    global CurrentDate_Month
    global CurrentDate_Year
    global CurrentDate_Minute
    global CurrentDate_Second
    global CurrentDate_Microseconds
    global Current_TotalClicks
    global Current_TotalClicksNext
    global Current_TotalClicksForEach
    global Current_ExperiencePerEach
    global Current_MoneyPerClickBest
    global Current_Experience
    global Current_Money
    global Current_MoneyValuePerClick
    global CurrentDate_DayLimiter
    global CurrentDate_MonthLimiter
    global CurrentDate_MinuteLimiter
    global CurrentDate_SecondLimiter
    global CurrentDate_YearLimiter
    global Current_MoneyMinimun
    global SaveDataLoaded
    global triggered_tutorials
    global WelcomeMessageTriggered
    global LowerMoneyWarning
    global PlanetID
    global PlanetName

    print("Fogoso.SaveManager : Loading Save Data...")

    # -- Load Money and Click Variables -- #
    Current_Money = appData.ReadAppData_WithTry("money", float, 0.0)
    Current_MoneyValuePerClick = appData.ReadAppData_WithTry("money_per_click", float, 0.50)
    Current_MoneyMinimun = appData.ReadAppData_WithTry("money_minimun", float, -5000)
    Current_Experience = appData.ReadAppData_WithTry("experience", int, 0)
    Current_TotalClicks = appData.ReadAppData_WithTry("total_clicks", int, 0)
    Current_TotalClicksForEach = appData.ReadAppData_WithTry("total_clicks_for_each", int, 35)
    Current_ExperiencePerEach = appData.ReadAppData_WithTry("total_experience_per_each", int, 15)
    Current_MoneyPerClickBest = appData.ReadAppData_WithTry("click_last_best", float, 0)

    # -- Calculate the Total Clicks Next -- #
    Current_TotalClicksNext = Current_TotalClicks + Current_TotalClicksForEach

    # -- Load the Current Date -- #
    CurrentDate_Year = appData.ReadAppData_WithTry("date/year", int, 0)
    CurrentDate_Month = appData.ReadAppData_WithTry("date/month", int, 0)
    CurrentDate_Day = appData.ReadAppData_WithTry("date/day", int, 0)
    CurrentDate_Second = appData.ReadAppData_WithTry("date/second", int, 0)
    CurrentDate_Minute = appData.ReadAppData_WithTry("date/minute", int, 0)
    CurrentDate_Microseconds = appData.ReadAppData_WithTry("date/microsecond", int, 0)

    # -- Load the Date Limiters -- #
    CurrentDate_MinuteLimiter = appData.ReadAppData_WithTry("date/limiter/minute", int, 60)
    CurrentDate_SecondLimiter = appData.ReadAppData_WithTry("date/limiter/second", int, 50)
    CurrentDate_DayLimiter = appData.ReadAppData_WithTry("date/limiter/day", int, 5)
    CurrentDate_MonthLimiter = appData.ReadAppData_WithTry("date/limiter/month", int, 7)
    CurrentDate_YearLimiter = appData.ReadAppData_WithTry("date/limiter/year", int, 5)

    # -- Load Last Maintenance -- #
    maintenance.DayTrigger = appData.ReadAppData_WithTry("maintenance_day_trigger", int, 1)
    maintenance.PerDayValue = appData.ReadAppData_WithTry("maintenance_per_day_value", int, 1)
    maintenance.BaseMaintenance = appData.ReadAppData_WithTry("maintenance_base_price", float, 15.0)

    # -- ETC -- #
    WelcomeMessageTriggered = appData.ReadAppData_WithTry("welcome_message_triggered",bool, False)
    LowerMoneyWarning = appData.ReadAppData_WithTry("lower_money_warning", bool, False)

    # -- Load Passed Tutorials -- #
    try:
        FileData = appData.ReadAppData_WithTry("tutorials_triggered", str, "")
        SplitedData = FileData.split('%n')
        for tutorial in SplitedData:
            try:
                Index = triggered_tutorials.index(str(tutorial))

            except ValueError:
                triggered_tutorials.append(str(tutorial))
    except AttributeError:
        appData.WriteAppData("tutorials_triggered", "")

    gameItems.LoadItems()
    print("Fogoso.SaveManager : Loading Store Items...")

    storeWindow.ReloadItemsList()
    expStoreWindow.ReloadItemsList()

    # -- Load the Planet Data -- #
    PlanetName = appData.ReadAppData_WithTry("planet_name", str, "Aragubas")
    PlanetID = appData.ReadAppData_WithTry("planet_id", int, 0)

    planets.LoadPlanetsData()

    print("Fogoso.SaveManager : Operation Completed!")
    SaveDataLoaded = True

def Unload():
    global CurrentDate_Day
    global CurrentDate_Month
    global CurrentDate_Year
    global CurrentDate_Minute
    global CurrentDate_Second
    global CurrentDate_Microseconds
    global Current_TotalClicks
    global Current_TotalClicksNext
    global Current_TotalClicksForEach
    global Current_ExperiencePerEach
    global Current_MoneyPerClickBest
    global Current_Experience
    global Current_Money
    global Current_MoneyValuePerClick
    global CurrentDate_DayLimiter
    global CurrentDate_MonthLimiter
    global CurrentDate_MinuteLimiter
    global CurrentDate_SecondLimiter
    global CurrentDate_YearLimiter
    global Current_MoneyMinimun
    global SaveDataLoaded
    global triggered_tutorials
    global WelcomeMessageTriggered
    global LowerMoneyWarning
    global BankruptWarning
    global PlanetID
    global PlanetName

    CurrentDate_Day = None
    CurrentDate_Month = None
    CurrentDate_Year = None
    CurrentDate_Minute = None
    CurrentDate_Second = None
    CurrentDate_Microseconds = None
    Current_TotalClicks = None
    Current_TotalClicksNext = None
    Current_TotalClicksForEach = None
    Current_ExperiencePerEach = None
    Current_MoneyPerClickBest = None
    Current_Experience = None
    Current_Money = None
    Current_MoneyValuePerClick = None
    CurrentDate_DayLimiter = None
    CurrentDate_MonthLimiter = None
    CurrentDate_MinuteLimiter = None
    CurrentDate_SecondLimiter = None
    CurrentDate_YearLimiter = None
    Current_MoneyMinimun = None
    SaveDataLoaded = None
    triggered_tutorials = list()
    WelcomeMessageTriggered = None
    BankruptWarning = None
    LowerMoneyWarning = None
    PlanetID = None
    PlanetName = None

    storeWindow.ReloadItemsList()
    expStoreWindow.ReloadItemsList()
    gameItems.RestartItems()
    gameScr.IncomingLog.Unload()
    maintenance.Unload()

def SaveData():
    global CurrentDate_Day
    global CurrentDate_Month
    global CurrentDate_Year
    global CurrentDate_Minute
    global CurrentDate_Second
    global CurrentDate_Microseconds
    global Current_TotalClicks
    global Current_TotalClicksNext
    global Current_TotalClicksForEach
    global Current_ExperiencePerEach
    global Current_Experience
    global Current_Money
    global Current_MoneyValuePerClick
    global CurrentDate_DayLimiter
    global CurrentDate_MonthLimiter
    global CurrentDate_MinuteLimiter
    global CurrentDate_SecondLimiter
    global CurrentDate_YearLimiter
    global Current_MoneyMinimun
    global triggered_tutorials
    global Current_MoneyPerClickBest
    global WelcomeMessageTriggered
    global LowerMoneyWarning
    global PlanetID
    global PlanetName

    # -- Money and Click Vars -- #
    appData.WriteAppData("money", Current_Money)
    appData.WriteAppData("experience", Current_Experience)
    appData.WriteAppData("money_per_click", Current_MoneyValuePerClick)
    appData.WriteAppData("total_clicks", Current_TotalClicks)
    appData.WriteAppData("total_clicks_for_each", Current_TotalClicksForEach)
    appData.WriteAppData("total_experience_per_each", Current_ExperiencePerEach)
    appData.WriteAppData("money_minimun", Current_MoneyMinimun)
    appData.WriteAppData("click_last_best", Current_MoneyPerClickBest)

    # -- ETC -- #
    appData.WriteAppData("welcome_message_triggered", WelcomeMessageTriggered)
    appData.WriteAppData("lower_money_warning", LowerMoneyWarning)

    # -- Maintenance Variables -- #
    appData.WriteAppData("maintenance_day_trigger", maintenance.DayTrigger)
    appData.WriteAppData("maintenance_per_day_value", maintenance.PerDayValue)
    appData.WriteAppData("maintenance_base_price", maintenance.BaseMaintenance)

    # -- Save Date -- #
    appData.WriteAppData("date/day", CurrentDate_Day)
    appData.WriteAppData("date/month", CurrentDate_Month)
    appData.WriteAppData("date/year", CurrentDate_Year)
    appData.WriteAppData("date/minute", CurrentDate_Minute)
    appData.WriteAppData("date/second", CurrentDate_Second)
    appData.WriteAppData("date/microseconds", CurrentDate_Microseconds)

    # -- Save Date Limiter -- #
    appData.WriteAppData("date/limiter/day", CurrentDate_DayLimiter)
    appData.WriteAppData("date/limiter/month", CurrentDate_MonthLimiter)
    appData.WriteAppData("date/limiter/year", CurrentDate_YearLimiter)
    appData.WriteAppData("date/limiter/minute", CurrentDate_MinuteLimiter)
    appData.WriteAppData("date/limiter/second", CurrentDate_SecondLimiter)

    # -- Save Passed Tutorials -- #
    FileData = ""
    for i, tutorial in enumerate(triggered_tutorials):
        if not tutorial == "":
            FileData += "%n" + str(tutorial)

    appData.WriteAppData("tutorials_triggered", FileData)

    # -- Planet Data -- #
    appData.WriteAppData("planet_name", PlanetName)
    appData.WriteAppData("planet_id", PlanetID)

    # -- Save Items Data -- #
    gameItems.SaveItems()

def UpdateClock():
    global CurrentDate_Day
    global CurrentDate_Month
    global CurrentDate_Year
    global CurrentDate_Minute
    global CurrentDate_Second
    global CurrentDate_Microseconds
    global CurrentDate_DayLimiter
    global CurrentDate_MonthLimiter
    global CurrentDate_MinuteLimiter
    global CurrentDate_SecondLimiter
    global CurrentDate_YearLimiter

    CurrentDate_Microseconds += 1

    if CurrentDate_Microseconds >= CurrentDate_SecondLimiter:  # -- 1 Second Passed
        CurrentDate_Microseconds = 0
        CurrentDate_Second += 1

    if CurrentDate_Second >= CurrentDate_MinuteLimiter:  # -- 1 Minute Passed
        CurrentDate_Second = 0
        CurrentDate_Minute += 1

    if CurrentDate_Minute >= CurrentDate_DayLimiter:  # -- 1 Day Passed
        CurrentDate_Minute = 0
        CurrentDate_Day += 1

    if CurrentDate_Day >= CurrentDate_MonthLimiter:  # -- 1 Month Passed
        CurrentDate_Day = 0
        CurrentDate_Month += 1

    if CurrentDate_Month >= CurrentDate_YearLimiter:  # -- 1 Year Passed
        CurrentDate_Month = 0
        CurrentDate_Year += 1

def Update():
    global Current_Money
    global Current_MoneyValuePerClick
    global Current_MoneyPerSecond
    global Current_MoneyFormated
    global Current_MoneyPerSecondFormatted
    global MoneyPerSecond_Delta
    global MoneyPerSecond_Last
    global Current_ExperienceFormated
    global Current_MoneyPerClickBest
    global SaveDataLoaded
    global WelcomeMessageTriggered

    if SaveDataLoaded:
        # -- Update the Clock -- #
        UpdateClock()

        # -- Say the Initial Message -- #
        if not WelcomeMessageTriggered:
            WelcomeMessageTriggered = True
            TutorialTrigger("new_savegame")

        # -- Updated Formated Strings -- #
        if gameMain.DefaultCnt.Get_RegKey("/OPTIONS/format_numbers"):
            Current_MoneyFormated = utils.FormatNumber(Current_Money, 2)
            Current_MoneyPerSecondFormatted = utils.FormatNumber(Current_MoneyPerSecond, 2)
            Current_ExperienceFormated = utils.FormatNumber(Current_Experience, 2)
        else:
            Current_MoneyFormated = str(Current_Money)
            Current_MoneyPerSecondFormatted = str(Current_MoneyPerSecond)
            Current_ExperienceFormated = str(Current_Experience)

        # -- Update Money Per Second -- #
        MoneyPerSecond_Delta += 1
        if MoneyPerSecond_Delta == 1000:
            Current_MoneyPerSecond = Current_Money - MoneyPerSecond_Last
            MoneyPerSecond_Last = Current_Money
            MoneyPerSecond_Delta = 0

            # -- Set Best Click -- #
            if Current_MoneyPerClickBest < Current_MoneyPerSecond:
                Current_MoneyPerClickBest = Current_MoneyPerSecond

        # -- Update All Loaded Items -- #
        gameItems.UpdateItems()

        # -- Triggers Bankrupt -- #
        TriggerBankrupt()

def RestartSaveGame():
    Unload()
    print("RestartSaveGame : Deleting Save Folder...")
    utils.Directory_Remove(tge.TaiyouPath_AppDataFolder)
    print(tge.TaiyouPath_AppDataFolder)

    print("RestartSaveGame : Loading Null Data...")
    LoadSaveData()

    print("RestartSaveGame : Saving Null Data")
    SaveData()

    print("RestartSaveGame : Done!")

LowerMoneyWarning = False
BankruptWarning = False
def TriggerBankrupt():
    global LowerMoneyWarning
    global Current_MoneyMinimun
    global BankruptWarning

    # -- Bankrupt Warning -- #
    if Current_Money <= Current_MoneyMinimun and not BankruptWarning:
        BankruptWarning = True
        LowerMoneyWarning = False
        OverlayDialog.subscreen1.SetMessage(gameMain.DefaultCnt.Get_RegKey("/strings/game/bankrupt_1_title"), gameMain.DefaultCnt.Get_RegKey("/strings/game/bankrupt_1_text").format(utils.FormatNumber(Current_Money)), typeDelay=0)

    # -- Lower Money Warning -- #
    elif not LowerMoneyWarning and Current_Money <= -10.00 and not BankruptWarning:
        LowerMoneyWarning = True
        OverlayDialog.subscreen1.SetMessage(gameMain.DefaultCnt.Get_RegKey("/strings/game/bankrupt_0_title"), gameMain.DefaultCnt.Get_RegKey("/strings/game/bankrupt_0_text").format(utils.FormatNumber(Current_MoneyMinimun)), typeDelay=0)

    if LowerMoneyWarning:
        if Current_Money >= 0.1:
            LowerMoneyWarning = False

    # -- Go Bankrupt -- #
    if BankruptWarning:
        BankruptWarning = False
        RestartSaveGame()

def TutorialTrigger(Action):
    if not gameMain.DefaultCnt.Get_RegKey("/OPTIONS/tutorial_enabled", bool):
        return
    global triggered_tutorials

    try:
        Index = triggered_tutorials.index(str(Action))
        return

    except ValueError:
        triggered_tutorials.append(Action)
        OverlayDialog.subscreen1.SetMessage(gameMain.DefaultCnt.Get_RegKey("/strings/tutorial/title_{0}".format(str(Action))), gameMain.DefaultCnt.Get_RegKey("/strings/tutorial/{0}".format(str(Action))), typeDelay=0, wordStep=2)

# -- Action when grinding -- #
def GrindClick():
    global Current_TotalClicks
    global Current_TotalClicksNext
    global Current_Experience
    global Current_MoneyValuePerClick
    global Current_ExperiencePerEach
    global CurrentDate_Microseconds

    Current_TotalClicks += 1
    CurrentDate_Microseconds += Current_TotalClicks

    # -- €xp Mining -- #
    if Current_TotalClicks == Current_TotalClicksNext:
        Current_TotalClicksNext = Current_TotalClicks + Current_TotalClicksForEach
        Current_Experience += Current_ExperiencePerEach
        IncomingLog.AddMessageText("€+{0}".format(str(Current_ExperiencePerEach)), False, (150,150,150))

    IncomingLog.AddMessageText("+{0}".format(str(Current_MoneyValuePerClick)), True, (20, 150, 25), Current_MoneyValuePerClick * Current_MoneyMultiplier)
