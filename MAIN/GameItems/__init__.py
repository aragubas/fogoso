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

from random import randint
from ENGINE import utils
from Fogoso import MAIN as gameMain
from ENGINE import appData
from Fogoso.MAIN.GameItems import AutoClicker
from Fogoso.MAIN import PlanetData as planets

# -- Game Items Variables -- #
ItemsList = list()
ItemsInitialized = False

# -- Items Levels -- #
Item_ExperienceStore_LastLevel = 0
Item_Shop_LastLevel = 0

# -- Items Count -- #
Item_ExperienceStore_Count = 0
Item_Shop_Count = 0

def LoadItemsLevels():
    global Item_ExperienceStore_LastLevel
    global Item_Shop_LastLevel

    AutoClicker.LastLevel = appData.ReadAppData_WithTry("item_level/0_level", int, "0")
    Item_ExperienceStore_LastLevel = appData.ReadAppData_WithTry("item_level/-1_level", int, "0")
    Item_Shop_LastLevel = appData.ReadAppData_WithTry("item_level/-2_level", int, "0")


# -- Get Item Sprite Name -- #
def GetItemSprite_ByID(ItemID):
    return "/ItemData/sprite/{0}_level_{1}".format(str(ItemID), str(GetItemLevel_ByID(ItemID)))

# -- Item Level -- #
def SaveItemsLevel():
    global Item_ExperienceStore_LastLevel
    global Item_Shop_LastLevel

    appData.WriteAppData("item_level/0_level", AutoClicker.LastLevel)
    appData.WriteAppData("item_level/-1_level", Item_ExperienceStore_LastLevel)
    appData.WriteAppData("item_level/-2_level", Item_Shop_LastLevel)

# -- Get Item Level -- #
def GetItemLevel_ByID(ItemID):
    global Item_ExperienceStore_LastLevel
    global Item_Shop_LastLevel

    if ItemID == -2:
        return Item_Shop_LastLevel

    elif ItemID == -1:
        return Item_ExperienceStore_LastLevel

    elif ItemID == 0:
        return AutoClicker.LastLevel

    else:
        print("Fogoso.GameItems.GetItemsLevelByID : ItemID[{0}] is invalid.".format(str(ItemID)))
        return 0

# -- Get the Maintenance Price -- #
def GetItem_MaintenancePrice(ItemID):
    RegDir = "/ItemData/{0}/lv_{1}_cost_maintenance".format(str(ItemID), str(GetItemLevel_ByID(int(ItemID))))

    return gameMain.DefaultCnt.Get_RegKey(RegDir, float) * GetItemCount_ByID(ItemID)

# -- Item Price -- #
def GetItemPrice_ByID(ItemID):
    RegDir = "/ItemData/{0}/lv_{1}_price".format(str(ItemID), str(GetItemLevel_ByID(int(ItemID))))

    return max(gameMain.DefaultCnt.Get_RegKey(RegDir, float), gameMain.DefaultCnt.Get_RegKey(RegDir, float) * GetItemCount_ByID(ItemID) + planets.GetPlanetInflation_ByID(gameMain.save.PlanetID))

# -- Item Upgrade -- #ura
def GetItemUpgradePrice_ByID(ItemID):
    RegDir = "/ItemData/{0}/lv_{1}_upgrade_price".format(str(ItemID), str(GetItemLevel_ByID(int(ItemID))))

    return gameMain.DefaultCnt.Get_RegKey(RegDir, float)


# -- Item Unlocker -- #
def GetItemIsUnlocker_ByID(ItemID):
    return gameMain.DefaultCnt.Get_RegKey("/ItemData/{0}/is_unlocker".format(str(ItemID)), bool)


# -- Item Object -- #
def CreateItemObject(ItemID):
    global ItemsList

    if ItemID == -2:
        ItemsList.append(Item_Shop())

    elif ItemID == -1:
        ItemsList.append(Item_ExperienceStore())


# -- Item Count -- #
def GetItemCount_ByID(ItemID):
    global Item_ExperienceStore_Count
    global Item_Shop_Count

    if ItemID == -2:
        return Item_Shop_Count

    elif ItemID == -1:
        return Item_ExperienceStore_Count

    elif ItemID == 0:
        return AutoClicker.Count

# -- Increase Item Level -- #
def IncreaseItemLevel_ByID(ItemID):
    global Item_ExperienceStore_LastLevel
    global Item_Shop_LastLevel

    if ItemID == -2:
        Item_Shop_LastLevel += 1

    elif ItemID == -1:
        Item_ExperienceStore_LastLevel += 1

    elif ItemID == 0:
        AutoClicker.LastLevel += 1

# -- Increase Item Count -- #
def IncreaseItemCount_ByID(ItemID, AddToItemDisplay=True):
    global Item_ExperienceStore_Count
    global Item_Shop_Count

    if ItemID == -2:
        Item_Shop_Count += 1

    elif ItemID == -1:
        Item_ExperienceStore_Count += 1

    elif ItemID == 0:
        AutoClicker.Count += 1

    # -- Add item to the Items View -- #
    if AddToItemDisplay:
        gameMain.ScreenGame.ItemsView.AddItem(int(ItemID))


def UnloadItems():
    global ItemsInitialized
    global ItemsList
    print("GameItems : Unloading Item Data...")
    RestartItemCount()

    ItemsInitialized = False
    RestartItemCount()
    ItemsList.clear()

    print("GameItems : Done!")


def RestartItemCount():
    global Item_ExperienceStore_Count
    global Item_Shop_Count

    Item_Shop_Count = 0
    Item_ExperienceStore_Count = 0
    AutoClicker.Count = 0

# -- Load Items Data -- #
def LoadItems():
    global Item_ExperienceStore_Count
    global ItemsList
    global ItemsInitialized
    AllKeys = 0
    SavedItemsData = appData.ReadAppData_WithTry("Items", str, "-2").splitlines()

    # -- Load Items Level -- #
    LoadItemsLevels()

    for i, x in enumerate(SavedItemsData):
        print("LoadItems ; Loading ItemID: " + x)

        # -- Increase item Count -- #
        IncreaseItemCount_ByID(int(x))

        # -- Create the Item Object -- #
        CreateItemObject(int(x))

        # -- Add item to the Items View -- #
        gameMain.ScreenGame.ItemsView.AddItem(int(x))

    ItemsInitialized = True
    print("LoadItems ; AllItemsLoaded: " + str(AllKeys))

    # -- Load the Items2 List --
    Items2List = appData.ReadAppData_WithTry("Items2", str, "").splitlines()

    for i, x in enumerate(Items2List):
        x = x.rstrip()
        SplitLine = x.split(":")

        ItemIDs = int(SplitLine[0])
        ItemCount = int(SplitLine[1])

        for _ in range(ItemCount):
            IncreaseItemCount_ByID(ItemIDs)

# -- Save Items Data -- #
def SaveItems():
    global ItemsList
    SaveItemsLevel()
    print("SaveItem : Saving Items Data...")

    print(ItemsList)
    AllItemsData = ""
    for i in range(0, len(ItemsList)):
        print("SaveItem : id:" + str(i))
        if i >= 1:
            AllItemsData += "\n" + str(ItemsList[i].ItemID)
        else:
            AllItemsData += str(ItemsList[i].ItemID)

    # -- Write Items1 File -- #
    appData.WriteAppData("Items", AllItemsData)

    # -- Write Items2 File -- #
    Items2List = ""

    if GetItemCount_ByID(0) >= 1:
        Items2List += "0:{0}".format(GetItemCount_ByID(0))

    # -- Write Save File -- #
    appData.WriteAppData("Items2", Items2List)

def UpdateItems():
    global ItemsList
    global ItemsInitialized

    if ItemsInitialized:
        for i, x in enumerate(ItemsList):
            x.InstanceID = i
            x.Update()

    # -- Update AutoClicker Instance -- #
    if GetItemCount_ByID(0) >= 1:
        AutoClicker.Run()

# -- Restart Items Data -- #
def RestartItems():
    global ItemsInitialized
    global ItemsList
    print("RestartItems : Clear Item Data...")
    ItemsInitialized = False
    RestartItemCount()
    ItemsList.clear()
    gameMain.ScreenGame.ItemsView.ClearItems()

    LoadItems()

class Item_ExperienceStore:
    def __init__(self):
        self.ItemID = -1
        self.DeltaTime = 0
        self.InstanceID = 0
        self.DeltaTimeAction = 0
        self.ItemIsActivated = False
        self.ItemRoll = 0

        # -- Item Statistics -- #
        self.ItemLevel = GetItemLevel_ByID(self.ItemID)
        self.ItemExpPerSecound = gameMain.DefaultCnt.Get_RegKey("/ItemData/-1/lv_" + str(self.ItemLevel) + "_exp_click", int)
        self.SecoundTimeAction = gameMain.DefaultCnt.Get_RegKey("/ItemData/-1/lv_" + str(self.ItemLevel) + "_activation_sec", int)
        self.maintenance_cost = gameMain.DefaultCnt.Get_RegKey("/ItemData/-1/lv_" + str(self.ItemLevel) + "_cost_maintenance", float)

    def Update(self):
        if self.ItemRoll == 1:
            if gameMain.save.CurrentDate_Second == 0:
                self.ItemRoll = 0

        if self.ItemRoll == 0:
            if gameMain.save.CurrentDate_Second >= int(self.SecoundTimeAction):
                self.ItemIsActivated = True
                self.DeltaTimeAction = self.InstanceID + 5

        if self.ItemIsActivated:
            self.DeltaTime += 1

            if self.DeltaTime >= self.DeltaTimeAction:
                self.DeltaTime = 0
                self.DeltaTimeAction = 0
                self.ItemIsActivated = False
                self.ItemRoll += 1

                self.ItemAction()

    def ReloadStatus(self):
        # -- Item Statistics -- #
        self.ItemLevel = GetItemLevel_ByID(self.ItemID)
        self.ItemExpPerSecound = gameMain.DefaultCnt.Get_RegKey("/ItemData/-1/lv_" + str(self.ItemLevel) + "_exp_click", int)
        self.SecoundTimeAction = gameMain.DefaultCnt.Get_RegKey("/ItemData/-1/lv_" + str(self.ItemLevel) + "_activation_sec", int)
        self.maintenance_cost = gameMain.DefaultCnt.Get_RegKey("/ItemData/-1/lv_" + str(self.ItemLevel) + "_cost_maintenance", float)

    def ItemAction(self):
        gameMain.ScreenGame.IncomingLog.AddMessageText("€+{0}".format(str(self.ItemExpPerSecound)), False, (55, 45, 60))
        gameMain.save.Current_Experience += self.ItemExpPerSecound

        self.ReloadStatus()

class Item_Shop:
    def __init__(self):
        self.ItemID = -2
        self.InstanceID = 0

        self.ItemLevel = GetItemLevel_ByID(self.ItemID)
        self.maintenance_cost = gameMain.DefaultCnt.Get_RegKey("/ItemData/-2/lv_" + str(self.ItemLevel) + "_cost_maintenance", float)

    def Update(self):
        pass
