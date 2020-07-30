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
from ENGINE import REGISTRY as reg
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
import os

print("Fogoso Variables Management, version 1.6")

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

    print("Fogoso.SaveManager : Loading Save Data...")

    # -- Load Money and Click Variables -- #
    Current_Money = reg.ReadAppData_WithTry("money", float, 0.0)
    Current_MoneyValuePerClick = reg.ReadAppData_WithTry("money_per_click", float, 0.50)
    Current_MoneyMinimun = reg.ReadAppData_WithTry("money_minimun", float, -5000)
    Current_Experience = reg.ReadAppData_WithTry("experience", int, 0)
    Current_TotalClicks = reg.ReadAppData_WithTry("total_clicks", int, 0)
    Current_TotalClicksForEach = reg.ReadAppData_WithTry("total_clicks_for_each", int, 35)
    Current_ExperiencePerEach = reg.ReadAppData_WithTry("total_experience_per_each", int, 15)
    Current_MoneyPerClickBest = reg.ReadAppData_WithTry("click_last_best", float, 0)

    # -- Calculate the Total Clicks Next -- #
    Current_TotalClicksNext = Current_TotalClicks + Current_TotalClicksForEach

    # -- Load the Current Date -- #
    CurrentDate_Year = reg.ReadAppData_WithTry("date/year", int, 0)
    CurrentDate_Month = reg.ReadAppData_WithTry("date/month", int, 0)
    CurrentDate_Day = reg.ReadAppData_WithTry("date/day", int, 0)
    CurrentDate_Second = reg.ReadAppData_WithTry("date/second", int, 0)
    CurrentDate_Minute = reg.ReadAppData_WithTry("date/minute", int, 0)
    CurrentDate_Microseconds = reg.ReadAppData_WithTry("date/microsecond", int, 0)

    # -- Load the Date Limiters -- #
    CurrentDate_MinuteLimiter = reg.ReadAppData_WithTry("date/limiter/minute", int, 60)
    CurrentDate_SecondLimiter = reg.ReadAppData_WithTry("date/limiter/second", int, 50)
    CurrentDate_DayLimiter = reg.ReadAppData_WithTry("date/limiter/day", int, 5)
    CurrentDate_MonthLimiter = reg.ReadAppData_WithTry("date/limiter/month", int, 7)
    CurrentDate_YearLimiter = reg.ReadAppData_WithTry("date/limiter/year", int, 5)

    # -- Load Last Maintenance -- #
    maintenance.DayTrigger = reg.ReadAppData_WithTry("maintenance_day_trigger", int, 1)
    maintenance.PerDayValue = reg.ReadAppData_WithTry("maintenance_per_day_value", int, 1)
    maintenance.BaseMaintenance = reg.ReadAppData_WithTry("maintenance_base_price", float, 15.0)

    # -- ETC -- #
    WelcomeMessageTriggered = reg.ReadAppData_WithTry("welcome_message_triggered",bool, False)

    # -- Load Passed Tutorials -- #
    try:
        FileData = reg.ReadAppData_WithTry("tutorials_triggered", str, "")
        SplitedData = FileData.split('%n')
        for tutorial in SplitedData:
            try:
                Index = triggered_tutorials.index(str(tutorial))

            except ValueError:
                triggered_tutorials.append(str(tutorial))
    except AttributeError:
        reg.WriteAppData("tutorials_triggered", "")

    gameItems.LoadItems()
    print("Fogoso.SaveManager : Loading Store Items...")

    storeWindow.ReloadItemsList()
    expStoreWindow.ReloadItemsList()

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

    # -- Money and Click Vars -- #
    reg.WriteAppData("money", Current_Money)
    reg.WriteAppData("experience", Current_Experience)
    reg.WriteAppData("money_per_click", Current_MoneyValuePerClick)
    reg.WriteAppData("total_clicks", Current_TotalClicks)
    reg.WriteAppData("total_clicks_for_each", Current_TotalClicksForEach)
    reg.WriteAppData("total_experience_per_each", Current_ExperiencePerEach)
    reg.WriteAppData("money_minimun", Current_MoneyMinimun)
    reg.WriteAppData("click_last_best", Current_MoneyPerClickBest)

    # -- ETC -- #
    reg.WriteAppData("welcome_message_triggered", WelcomeMessageTriggered)

    # -- Maintenance Variables -- #
    reg.WriteAppData("maintenance_day_trigger", maintenance.DayTrigger)
    reg.WriteAppData("maintenance_per_day_value", maintenance.PerDayValue)
    reg.WriteAppData("maintenance_base_price", maintenance.BaseMaintenance)

    # -- Save Date -- #
    reg.WriteAppData("date/day", CurrentDate_Day)
    reg.WriteAppData("date/month", CurrentDate_Month)
    reg.WriteAppData("date/year", CurrentDate_Year)
    reg.WriteAppData("date/minute", CurrentDate_Minute)
    reg.WriteAppData("date/second", CurrentDate_Second)
    reg.WriteAppData("date/microseconds", CurrentDate_Microseconds)

    # -- Save Date Limiter -- #
    reg.WriteAppData("date/limiter/day", CurrentDate_DayLimiter)
    reg.WriteAppData("date/limiter/month", CurrentDate_MonthLimiter)
    reg.WriteAppData("date/limiter/year", CurrentDate_YearLimiter)
    reg.WriteAppData("date/limiter/minute", CurrentDate_MinuteLimiter)
    reg.WriteAppData("date/limiter/second", CurrentDate_SecondLimiter)

    # -- Save Passed Tutorials -- #
    FileData = ""
    for i, tutorial in enumerate(triggered_tutorials):
        if not tutorial == "":
            FileData += "%n" + str(tutorial)

    reg.WriteAppData("tutorials_triggered", FileData)

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
        if reg.ReadKey_bool("/OPTIONS/format_numbers"):
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
BankruptWarningType = 0
def TriggerBankrupt():
    global LowerMoneyWarning
    global Current_MoneyMinimun
    global BankruptWarningType

    # -- Bankrupt Warning 0 -- #
    if not LowerMoneyWarning and Current_Money <= -10.00 and not Current_Money <= Current_MoneyMinimun:
        BankruptWarningType = 0
        LowerMoneyWarning = True
        OverlayDialog.subscreen1.SetMessage(reg.ReadKey("/strings/game/bankrupt_0_title"), reg.ReadKey("/strings/game/bankrupt_0_text").format(utils.FormatNumber(Current_MoneyMinimun)), typeDelay=0)

    # -- Bankrupt Warning 1 -- #
    if Current_Money <= Current_MoneyMinimun and not LowerMoneyWarning:
        BankruptWarningType = 1
        LowerMoneyWarning = True
        OverlayDialog.subscreen1.SetMessage(reg.ReadKey("/strings/game/bankrupt_1_title"), reg.ReadKey("/strings/game/bankrupt_1_text").format(utils.FormatNumber(Current_Money)), typeDelay=0)

    if LowerMoneyWarning and Current_Money >= 1 and BankruptWarningType == 0:
        if OverlayDialog.subscreen1.ResponseTrigger:
            LowerMoneyWarning = False
            OverlayDialog.subscreen1.ResponseTrigger = False

    # -- Go Bankrupt -- #
    if LowerMoneyWarning and BankruptWarningType == 1:
        LowerMoneyWarning = False
        RestartSaveGame()

def TutorialTrigger(Action):
    global triggered_tutorials

    try:
        Index = triggered_tutorials.index(str(Action))
        return

    except ValueError:
        triggered_tutorials.append(Action)
        OverlayDialog.subscreen1.SetMessage(reg.ReadKey("/strings/tutorial/title_{0}".format(str(Action))), reg.ReadKey("/strings/tutorial/{0}".format(str(Action))), typeDelay=0, wordStep=2)

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
