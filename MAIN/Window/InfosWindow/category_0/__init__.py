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
from ENGINE import sprite
from ENGINE import reg
from ENGINE import utils

# -- Fogoso Imports -- #
from Fogoso.MAIN import GameVariables as save
from Fogoso.MAIN.Screens.Game import Maintenance as maintenance


import pygame


def Initialize():
    pass

def Render(DISPLAY):
    sprite.FontRender(DISPLAY, "/PressStart2P.ttf", 10, reg.ReadKey("/strings/window/infos/txt_maintenance") + utils.FormatNumber(maintenance.LastMaintenancePrice), (240, 240, 240), 5, 30, reg.ReadKey_bool("/OPTIONS/font_aa"))
    sprite.FontRender(DISPLAY, "/PressStart2P.ttf", 10, reg.ReadKey("/strings/window/infos/txt_maintenance_delay") + str(maintenance.DayTrigger), (220, 220, 220), 5, 45, reg.ReadKey_bool("/OPTIONS/font_aa"))
    sprite.FontRender(DISPLAY, "/PressStart2P.ttf", 10, reg.ReadKey("/strings/window/infos/txt_maintenance_base") + utils.FormatNumber(maintenance.BaseMaintenance), (200, 200, 200), 5, 60, reg.ReadKey_bool("/OPTIONS/font_aa"))
    sprite.FontRender(DISPLAY, "/PressStart2P.ttf", 10, reg.ReadKey("/strings/window/infos/txt_items_maintenance") + utils.FormatNumber(maintenance.ItemsMaintenance), (200, 200, 200), 5, 75, reg.ReadKey_bool("/OPTIONS/font_aa"))


def Update():
    pass

def EventUpdate(event):
    pass