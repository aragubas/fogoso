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

from ENGINE import REGISTRY as reg
from Fogoso import MAIN as gameMain
from random import randint

# -- Game Items Variables -- #
ItemsList = list()
ItemsInitialized = False

# -- Items Levels -- #
Item_AutoClicker_LastLevel = 0
Item_ExperienceStore_LastLevel = 0

# -- Items Count -- #
Item_ExperienceStore_Count = 0
Item_AutoClicker_Count = 0


def LoadItemsLevels():
    global Item_AutoClicker_LastLevel
    global Item_ExperienceStore_LastLevel

    Item_AutoClicker_LastLevel = reg.ReadAppData_WithTry("savegame/item_level/0_level", int, "0")
    Item_ExperienceStore_LastLevel = reg.ReadAppData_WithTry("savegame/item_level/-1_level", int, "0")


# -- Get Item Sprite Name -- #
def GetItemSprite_ByID(ItemID):
    global Item_AutoClicker_LastLevel
    global Item_ExperienceStore_LastLevel

    # -- The Root Folder -- #
    RootFolder = "/ItemData/sprite/"

    return RootFolder + str(ItemID) + "_level_" + str(GetItemLevel_ByID(ItemID))



# -- Item Level -- #
def SaveItemsLevel():
    global Item_AutoClicker_LastLevel
    global Item_ExperienceStore_LastLevel

    reg.WriteAppData("savegame/item_level/0_level", Item_AutoClicker_LastLevel)
    reg.WriteAppData("savegame/item_level/-1_level", Item_ExperienceStore_LastLevel)

# -- Get Item Level -- #
def GetItemLevel_ByID(ItemID):
    global Item_AutoClicker_LastLevel
    global Item_ExperienceStore_LastLevel

    if ItemID == -1:
        return Item_ExperienceStore_LastLevel
    elif ItemID == 0:
        return Item_AutoClicker_LastLevel
    else:
        return None

# -- Item Price -- #
def GetItemPrice_ByID(ItemID):
    RegDir = "/ItemData/store/price/" + str(ItemID) + "_level_" + str(GetItemLevel_ByID(int(ItemID)))

    return max(reg.ReadKey_float(RegDir), reg.ReadKey_float(RegDir) * GetItemCount_ByID(ItemID))

# -- Item Price -- #
def GetItemIsUnlocker_ByID(ItemID):
    RegDir = "/ItemData/" + str(ItemID) + "/is_unlocker"

    return reg.ReadKey_bool(RegDir)


# -- Item Object -- #
def CreateItemObject(ItemID):
    global ItemsList
    if ItemID == -1:
        ItemsList.append(Item_ExperienceStore())

    if ItemID == 0:
        ItemsList.append(Item_AutoClicker())


# -- Item Count -- #
def GetItemCount_ByID(ItemID):
    global Item_ExperienceStore_Count
    global Item_AutoClicker_Count
    if ItemID == -1:
        return Item_ExperienceStore_Count

    if ItemID == 0:
        return Item_AutoClicker_Count

# -- Increase Item Level -- #
def IncreaseItemLevel_ByID(ItemID):
    global Item_ExperienceStore_LastLevel
    global Item_AutoClicker_LastLevel
    if ItemID == -1:
        Item_ExperienceStore_LastLevel += 1

    if ItemID == 0:
        Item_AutoClicker_LastLevel += 1

# -- Increase Item Count -- #
def IncreaseItemCount_ByID(ItemID):
    global Item_ExperienceStore_Count
    global Item_AutoClicker_Count
    if ItemID == -1:
        Item_ExperienceStore_Count += 1

    if ItemID == 0:
        Item_AutoClicker_Count += 1

def UnloadItems():
    global ItemsInitialized
    global ItemsList
    print("GameItems : Unloading Item Data")
    RestartItemCount()

    ItemsInitialized = False
    RestartItemCount()
    ItemsList.clear()


def RestartItemCount():
    global Item_ExperienceStore_Count
    global Item_AutoClicker_Count

    Item_ExperienceStore_Count = 0
    Item_AutoClicker_Count = 0


# -- Load Items Data -- #
def LoadItems():
    global Item_ExperienceStore_Count
    global Item_AutoClicker_Count
    global ItemsList
    global ItemsInitialized
    AllKeys = 0
    SavedItemsData = reg.ReadAppData_WithTry("savegame/Items", str, "").splitlines()

    # -- Load Items Level -- #
    LoadItemsLevels()

    for i, x in enumerate(SavedItemsData):
        print("LoadItems ; Loading ItemID: " + x)

        # -- Add item to the Items View -- #
        gameMain.ScreenGame.ItemsView.AddItem(x)

        # -- Increase item Count -- #
        IncreaseItemCount_ByID(int(x))

        # -- Add Game item -- #
        CreateItemObject(int(x))

    ItemsInitialized = True
    print("LoadItems ; AllItemsLoaded: " + str(AllKeys))

# -- Save Items Data -- #
def SaveItems():
    global ItemsList
    AllItemsData = ""
    for i in range(0, len(ItemsList)):
        print("SaveItem : id:" + str(i))
        if i >= 1:
            AllItemsData += "\n" + str(ItemsList[i].ItemID)
        else:
            AllItemsData += str(ItemsList[i].ItemID)
        print("SaveItem : Item saved.")

    # -- Write Files -- #
    reg.WriteAppData("savegame/Items", AllItemsData)

    SaveItemsLevel()


def UpdateItems():
    global ItemsList
    global ItemsInitialized

    if ItemsInitialized:
        for i, x in enumerate(ItemsList):
            x.InstanceID = i
            x.Update()


# -- Restart Items Data -- #
def RestartItems():
    global ItemsInitialized
    global ItemsList
    print("RestartItems : Clear Item Data...")
    ItemsInitialized = False
    RestartItemCount()
    ItemsList.clear()

    LoadItems()


class Item_AutoClicker:
    def __init__(self):
        self.DeltaTime = 0
        self.DeltaTimeAction = 0
        self.ItemIsActivated = False
        self.InstanceID = 0
        self.ItemRoll = 0
        self.ItemID = 0

        # -- Item Statistics -- #
        self.ItemLevel = GetItemLevel_ByID(self.ItemID)
        self.ItemClickPerSecound = reg.ReadKey("/ItemData/0/lv_" + str(self.ItemLevel) + "_click")
        self.SecoundTimeAction = int(reg.ReadKey("/ItemData/0/lv_" + str(self.ItemLevel) + "_activation_sec"))
        self.maintenance_cost = reg.ReadKey_float("/ItemData/0/lv_" + str(self.ItemLevel) + "_cost_maintenance")
        self.ExpMiningTotal = reg.ReadKey_int("/ItemData/0/lv_" + str(self.ItemLevel) + "_exp")

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

                # -- Reload Item Statistics -- #
                self.ItemLevel = GetItemLevel_ByID(self.ItemID)
                self.ItemClickPerSecound = reg.ReadKey("/ItemData/0/lv_" + str(self.ItemLevel) + "_click")
                self.SecoundTimeAction = int(reg.ReadKey("/ItemData/0/lv_" + str(self.ItemLevel) + "_activation_sec"))
                self.maintenance_cost = reg.ReadKey_float("/ItemData/0/lv_" + str(self.ItemLevel) + "_cost_maintenance")
                self.ExpMiningTotal = reg.ReadKey_int("/ItemData/0/lv_" + str(self.ItemLevel) + "_exp")

                gameMain.ScreenGame.IncomingLog.AddMessageText("+" + str(self.ItemClickPerSecound), True, (100, 210, 100), self.ItemClickPerSecound)
                if self.ExpMiningTotal > 0:
                    gameMain.ScreenGame.save.Current_Experience += self.ExpMiningTotal
                    gameMain.ScreenGame.IncomingLog.AddMessageText("€+" + str(self.ItemClickPerSecound), True, (100, 110, 100), self.ItemClickPerSecound)


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
        self.ItemExpPerSecound = reg.ReadKey_int("/ItemData/-1/lv_" + str(self.ItemLevel) + "_exp_click")
        self.SecoundTimeAction = int(reg.ReadKey("/ItemData/-1/lv_" + str(self.ItemLevel) + "_activation_sec"))
        self.maintenance_cost = reg.ReadKey_float("/ItemData/-1/lv_" + str(self.ItemLevel) + "_cost_maintenance")

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

                gameMain.ScreenGame.IncomingLog.AddMessageText("€+" + str(self.ItemExpPerSecound), False, (55, 45, 60))
                gameMain.save.Current_Experience += self.ItemExpPerSecound

