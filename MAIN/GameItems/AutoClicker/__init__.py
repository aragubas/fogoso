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
# -- Import -- #
from Fogoso.MAIN import GameItems as items
from ENGINE import utils
from Fogoso import MAIN as gameMain

# -- Variables -- #
LastLevel = 0
Count = 0


DeltaTime = 0

def Run():
    global DeltaTime

    DeltaTime += 1

    if DeltaTime > 2:
        DeltaTime = 0
        # -- ItemID is 0
        ItemLevel = items.GetItemLevel_ByID(0)
        ItemClickPerSecound = gameMain.DefaultCnt.Get_RegKey("/ItemData/0/lv_{0}_click".format(ItemLevel), float)

        TotalValue = (ItemClickPerSecound * gameMain.save.Current_MoneyMultiplier) * items.GetItemCount_ByID(0)
        AdderText = "+{0}".format(utils.FormatNumber(TotalValue))

        try:  # -- Items exists -- #
            Index = gameMain.ScreenGame.IncomingLog.TextGrind_Text.index(AdderText)

            gameMain.save.Current_Money += TotalValue

        except ValueError: # -- Item Does not Exist -- #
            gameMain.ScreenGame.IncomingLog.AddMessageText(AdderText, True, (150, 220, 150), TotalValue)
