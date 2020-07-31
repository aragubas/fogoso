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
from ENGINE import APPDATA as reg
from Fogoso.MAIN.Screens import Game as gameScr
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso.MAIN import GameItems as gameItems
from Fogoso.MAIN import GameVariables as save
from Fogoso.MAIN.Screens.Game import IncomingLog
from ENGINE import UTILS as utils
from random import randint

print("Fogoso Maintenance , version 1.3")

# -- Variables -- #
ItemsMaintenance = 0.0
BaseMaintenance = 25.0
LastMaintenancePrice = 0.0

DayTrigger = 1
PerDayValue = 1
NextMaintenanceDay = 0

def Unload():
    global LastMaintenancePrice
    global DayTrigger
    global PerDayValue
    global NextMaintenanceDay
    global ItemsMaintenance

    LastMaintenancePrice = 0.0
    DayTrigger = 1
    PerDayValue = 1
    ItemsMaintenance = 0.0

def Update():
    global ItemsMaintenance
    global BaseMaintenance
    global LastMaintenancePrice
    global DayTrigger
    global NextMaintenanceDay

    if save.CurrentDate_Day == DayTrigger:
        # -- Dont let the Maintenance Day to the Day Limit -- #
        if save.CurrentDate_Day + 1 >= save.CurrentDate_MonthLimiter:
            DayTrigger = 0

        else:
            DayTrigger = save.CurrentDate_Day + PerDayValue

        # -- Calculate Maintenance of All Items -- #
        TotalItems = 0

        for item in gameItems.ItemsList:
            TotalItems += 1
            ItemsMaintenance = ItemsMaintenance + item.maintenance_cost + randint(1, TotalItems)

        # -- Add Maintenance of Auto Clicker -- #
        if gameItems.GetItemCount_ByID(0) > 1:
            ItemsMaintenance += (gameItems.GetItem_MaintenancePrice(0) * gameItems.GetItemCount_ByID(0))

        # -- Calculate the Maintenance -- #
        MaintenancePrice = BaseMaintenance + ItemsMaintenance

        # -- Decrease Money -- #
        IncomingLog.AddMessageText(utils.FormatNumber(-MaintenancePrice, 2) , True, (250, 150, 150, ), -MaintenancePrice)

        # -- Set Variables -- #
        LastMaintenancePrice = MaintenancePrice