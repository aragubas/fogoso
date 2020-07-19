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
from ENGINE import UTILS as utils

# -- Game Items Variables -- #
ItemsList = list()
ItemsInitialized = False

# -- Items Levels -- #
Item_AutoClicker_LastLevel = 0
Item_ExperienceStore_LastLevel = 0
Item_Shop_LastLevel = 0

# -- Items Count -- #
Item_ExperienceStore_Count = 0
Item_AutoClicker_Count = 0
Item_Shop_Count = 0

def LoadItemsLevels():
    global Item_AutoClicker_LastLevel
    global Item_ExperienceStore_LastLevel
    global Item_Shop_LastLevel

    Item_AutoClicker_LastLevel = reg.ReadAppData_WithTry("item_level/0_level", int, "0")
    Item_ExperienceStore_LastLevel = reg.ReadAppData_WithTry("item_level/-1_level", int, "0")
    Item_Shop_LastLevel = reg.ReadAppData_WithTry("item_level/-2_level", int, "0")


# -- Get Item Sprite Name -- #
def GetItemSprite_ByID(ItemID):
    return "/ItemData/sprite/{0}_level_{1}".format(str(ItemID), str(GetItemLevel_ByID(ItemID)))


# -- Item Level -- #
def SaveItemsLevel():
    global Item_AutoClicker_LastLevel
    global Item_ExperienceStore_LastLevel
    global Item_Shop_LastLevel

    reg.WriteAppData("item_level/0_level", Item_AutoClicker_LastLevel)
    reg.WriteAppData("item_level/-1_level", Item_ExperienceStore_LastLevel)
    reg.WriteAppData("item_level/-2_level", Item_Shop_LastLevel)

# -- Get Item Level -- #
def GetItemLevel_ByID(ItemID):
    global Item_AutoClicker_LastLevel
    global Item_ExperienceStore_LastLevel
    global Item_Shop_LastLevel

    if ItemID == -2:
        return Item_Shop_LastLevel

    elif ItemID == -1:
        return Item_ExperienceStore_LastLevel

    elif ItemID == 0:
        return Item_AutoClicker_LastLevel

    else:
        print("Fogoso.GameItems.GetItemsLevelByID : ItemID[{0}] is invalid.".format(str(ItemID)))
        return 0

# -- Item Price -- #
def GetItemPrice_ByID(ItemID):
    RegDir = "/ItemData/{0}/lv_{1}_price".format(str(ItemID), str(GetItemLevel_ByID(int(ItemID))))

    return max(reg.ReadKey_float(RegDir), reg.ReadKey_float(RegDir) * GetItemCount_ByID(ItemID))

# -- Item Upgrade -- #
def GetItemUpgradePrice_ByID(ItemID):
    RegDir = "/ItemData/{0}/lv_{1}_upgrade_price".format(str(ItemID), str(GetItemLevel_ByID(int(ItemID))))

    return reg.ReadKey_int(RegDir)


# -- Item Unlocker -- #
def GetItemIsUnlocker_ByID(ItemID):
    return reg.ReadKey_bool("/ItemData/{0}/is_unlocker".format(str(ItemID)))


# -- Item Object -- #
def CreateItemObject(ItemID):
    global ItemsList

    if ItemID == -2:
        ItemsList.append(Item_Shop())

    elif ItemID == -1:
        ItemsList.append(Item_ExperienceStore())

    elif ItemID == 0:
        ItemsList.append(Item_AutoClicker())


# -- Item Count -- #
def GetItemCount_ByID(ItemID):
    global Item_ExperienceStore_Count
    global Item_AutoClicker_Count
    global Item_Shop_Count

    if ItemID == -2:
        return Item_Shop_Count

    elif ItemID == -1:
        return Item_ExperienceStore_Count

    elif ItemID == 0:
        return Item_AutoClicker_Count

# -- Increase Item Level -- #
def IncreaseItemLevel_ByID(ItemID):
    global Item_ExperienceStore_LastLevel
    global Item_AutoClicker_LastLevel
    global Item_Shop_LastLevel

    if ItemID == -2:
        Item_Shop_LastLevel += 1

    elif ItemID == -1:
        Item_ExperienceStore_LastLevel += 1

    elif ItemID == 0:
        Item_AutoClicker_LastLevel += 1

# -- Increase Item Count -- #
def IncreaseItemCount_ByID(ItemID):
    global Item_ExperienceStore_Count
    global Item_AutoClicker_Count
    global Item_Shop_Count

    if ItemID == -2:
        Item_Shop_Count += 1

    elif ItemID == -1:
        Item_ExperienceStore_Count += 1

    elif ItemID == 0:
        Item_AutoClicker_Count += 1

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
    global Item_AutoClicker_Count
    global Item_Shop_Count

    Item_Shop_Count = 0
    Item_ExperienceStore_Count = 0
    Item_AutoClicker_Count = 0

# -- Load Items Data -- #
def LoadItems():
    global Item_ExperienceStore_Count
    global Item_AutoClicker_Count
    global ItemsList
    global ItemsInitialized
    AllKeys = 0
    SavedItemsData = reg.ReadAppData_WithTry("Items", str, "-2").splitlines()

    # -- Load Items Level -- #
    LoadItemsLevels()

    for i, x in enumerate(SavedItemsData):
        print("LoadItems ; Loading ItemID: " + x)

        # -- Increase item Count -- #
        IncreaseItemCount_ByID(int(x))

        # -- Add Game item -- #
        CreateItemObject(int(x))

        # -- Add item to the Items View -- #
        gameMain.ScreenGame.ItemsView.AddItem(int(x))

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
    reg.WriteAppData("Items", AllItemsData)

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
        self.ItemClickPerSecound = reg.ReadKey_float("/ItemData/0/lv_" + str(self.ItemLevel) + "_click")
        self.SecoundTimeAction = int(reg.ReadKey("/ItemData/0/lv_" + str(self.ItemLevel) + "_activation_sec"))
        self.maintenance_cost = reg.ReadKey_float("/ItemData/0/lv_" + str(self.ItemLevel) + "_cost_maintenance")
        self.ExpMiningTotal = reg.ReadKey_int("/ItemData/0/lv_" + str(self.ItemLevel) + "_exp")
        self.ActivationType = reg.ReadKey_int("/ItemData/0/lv_" + str(self.ItemLevel) + "_activation_type")

    def Update(self):
        if self.ActivationType == 0:
            self.ActivationPerSecound()

        elif self.ActivationType == 1:
            self.ActivationPerConstantFlux()

    def ActivationPerSecound(self):
        if self.ItemRoll == 1:
            if gameMain.save.CurrentDate_Second == 0:
                self.ItemRoll = 0

        elif self.ItemRoll == 0:
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

                gameMain.ScreenGame.IncomingLog.AddMessageText("+" + str(self.ItemClickPerSecound), True, (100, 210, 100), self.ItemClickPerSecound)
                if self.ExpMiningTotal > 0:
                    gameMain.ScreenGame.save.Current_Experience += self.ExpMiningTotal
                    gameMain.ScreenGame.IncomingLog.AddMessageText("€+" + str(self.ExpMiningTotal), False, (100, 110, 100))

                self.ReloadStatus()

    def ActivationPerConstantFlux(self):
        if self.ItemRoll == 1:
            self.ItemRoll = 0

        if self.ItemRoll == 0:
            self.ItemIsActivated = True
            self.DeltaTimeAction = self.InstanceID + 5

        if self.ItemIsActivated:
            self.DeltaTime += 1

            if self.DeltaTime >= self.DeltaTimeAction:
                self.DeltaTime = 0
                self.DeltaTimeAction = 0
                self.ItemIsActivated = False
                self.ItemRoll += 1

                TotalValue = self.ItemClickPerSecound * GetItemCount_ByID(self.ItemID)
                AdderText = "+" + utils.FormatNumber(TotalValue)
                ExpValue = self.ExpMiningTotal * GetItemCount_ByID(self.ItemID)

                # -- Check if item is already on the Receiving Log -- #
                try:
                    IndexTest = gameMain.ScreenGame.IncomingLog.TextGrind_Text.index(AdderText)

                    self.ReloadStatus()

                except ValueError:  # -- IF not, Execute Item Mining -- #
                    gameMain.ScreenGame.IncomingLog.AddMessageText(AdderText, True, (150, 220, 150), TotalValue)
                    gameMain.ScreenGame.IncomingLog.AddMessageText("€+" + str(ExpValue), True, (100, 110, 100))
                    gameMain.save.Current_Experience += ExpValue

    def ReloadStatus(self):
        self.ItemLevel = GetItemLevel_ByID(self.ItemID)
        self.ItemClickPerSecound = reg.ReadKey_float("/ItemData/0/lv_" + str(self.ItemLevel) + "_click")
        self.SecoundTimeAction = int(reg.ReadKey("/ItemData/0/lv_" + str(self.ItemLevel) + "_activation_sec"))
        self.maintenance_cost = reg.ReadKey_float("/ItemData/0/lv_" + str(self.ItemLevel) + "_cost_maintenance")
        self.ExpMiningTotal = reg.ReadKey_int("/ItemData/0/lv_" + str(self.ItemLevel) + "_exp")
        self.ActivationType = reg.ReadKey_int("/ItemData/0/lv_" + str(self.ItemLevel) + "_activation_type")

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

                self.ItemAction()

    def ReloadStatus(self):
        # -- Item Statistics -- #
        self.ItemLevel = GetItemLevel_ByID(self.ItemID)
        self.ItemExpPerSecound = reg.ReadKey_int("/ItemData/-1/lv_" + str(self.ItemLevel) + "_exp_click")
        self.SecoundTimeAction = int(reg.ReadKey("/ItemData/-1/lv_" + str(self.ItemLevel) + "_activation_sec"))
        self.maintenance_cost = reg.ReadKey_float("/ItemData/-1/lv_" + str(self.ItemLevel) + "_cost_maintenance")

    def ItemAction(self):
        gameMain.ScreenGame.IncomingLog.AddMessageText("€+" + str(self.ItemExpPerSecound), False, (55, 45, 60))
        gameMain.save.Current_Experience += self.ItemExpPerSecound

        self.ReloadStatus()

class Item_Shop:
    def __init__(self):
        self.ItemID = -2
        self.InstanceID = 0

        self.ItemLevel = GetItemLevel_ByID(self.ItemID)
        self.maintenance_cost = reg.ReadKey_float("/ItemData/-2/lv_" + str(self.ItemLevel) + "_cost_maintenance")


    def Update(self):
        pass
