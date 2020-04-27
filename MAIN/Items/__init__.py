#!/usr/bin/ python3.6
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
from Fogoso import MAIN as mainScript
from ENGINE import REGISTRY as reg
import pygame
import random

print("FogosoItemsManagement version 1.0")


def GetItemID_ByName(ItemName):
    return reg.ReadKey("/ItemData/name/" + ItemName)

def GetItemPrice_ByID(ItemID):
    LastItemLevel = reg.ReadKey_int("/Save/item/last_level/" + str(ItemID))
    CorrectKeyName = "/ItemData/store/price/" + str(ItemID) + "_level_" + str(LastItemLevel)
    return reg.ReadKey_float(CorrectKeyName)

def GetItem_IsVisibleByID(ItemID):
    if ItemID != "":
        CorrectKeyName = "/ItemData/" + str(ItemID) + "/is_visible"
        return reg.ReadKey_bool(CorrectKeyName)