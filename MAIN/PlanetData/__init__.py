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
from Fogoso import MAIN as Game
from ENGINE import appData
from random import randint

Aragubas_Inflation = 0.0

def LoadPlanetsData():
    global Aragubas_Inflation

    Aragubas_Inflation = appData.ReadAppData_WithTry("planets/aragubas/inflation", float, float("{0}.{0}".format(randint(0, 5), randint(0, 5))))

def GetPlanetName_ByID(PlanetID):
    if PlanetID == 0:
        return "Aragubas"

def GetPlanetInflation_ByID(PlanetID):
    global Aragubas_Inflation

    if PlanetID == 0:
        return Aragubas_Inflation

    raise IndexError("Invalid Planet ID\n [{0}]".format(PlanetID))