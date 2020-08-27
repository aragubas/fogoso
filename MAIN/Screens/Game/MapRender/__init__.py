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

# -- Imports -- #
from ENGINE import APPDATA as reg
from ENGINE import UTILS as utils
from ENGINE import shape
import ENGINE as tge

from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso.MAIN.Screens import Settings as ScreenSettings
from Fogoso import MAIN as gameMain

from Fogoso.MAIN.Window import StoreWindow as storeWindow
from Fogoso.MAIN.Window import ExperienceStore as expStoreWindow
from Fogoso.MAIN.Window import InfosWindow as infosWindow
from random import randint
import pygame, os
import importlib
import time
from math import *

MapData = list()
MapTileset = 0
MapSizeW = 0
MapSizeH = 0
MapTileSize = 0
MapCamX = 0
MapCamY = 0


class Player:
    def __init__(self, TileX, TileY):
        self.Rectangle = pygame.Rect(TileX * MapTileSize, TileY * MapTileSize,MapTileSize,MapTileSize)
        self.SpriteInd = 0
        self.MoveXEnabled = True
        self.MoveXDest = self.Rectangle[0]
        self.MoveYEnabled = True
        self.MoveYDest = self.Rectangle[1]
        self.MoveDelay = 0
        self.MoveDelayLimit = 1

    def Draw(self, DISPLAY):
        shape.Shape_Rectangle(DISPLAY, (255, 0, 0), pygame.Rect(MapCamX + self.Rectangle[0], MapCamY + self.Rectangle[1], self.Rectangle[2], self.Rectangle[3]))

    def Update(self):
        PlayerMovA = False
        PlayerMovD = False
        PlayerMovW = False
        PlayerMovS = False
        PressedKeys = pygame.key.get_pressed()

        if PressedKeys[pygame.K_a]:
            PlayerMovA = True
            self.MoveDelay += 1

        if PressedKeys[pygame.K_d]:
            PlayerMovD = True
            self.MoveDelay += 1

        if PressedKeys[pygame.K_w]:
            PlayerMovW = True
            self.MoveDelay += 1

        if PressedKeys[pygame.K_s]:
            PlayerMovS = True
            self.MoveDelay += 1

        if PlayerMovW:
            if self.MoveDelay > self.MoveDelayLimit:
                self.MoveDelay = 0
                return

            PlayerTileAfront = pygame.Rect(self.Rectangle[0], self.Rectangle[1] - MapTileSize, self.Rectangle[2],self.Rectangle[3])

            if GetTile(PlayerTileAfront) == 0:
                self.Rectangle[1] -= MapTileSize
                self.MoveYEnabled = True
                self.MoveYDest = self.Rectangle[1]

        if PlayerMovS:
            if self.MoveDelay > self.MoveDelayLimit:
                self.MoveDelay = 0
                return

            PlayerTileAfront = pygame.Rect(self.Rectangle[0], self.Rectangle[1] + MapTileSize, self.Rectangle[2],self.Rectangle[3])

            if GetTile(PlayerTileAfront) == 0:
                self.Rectangle[1] += MapTileSize
                self.MoveYEnabled = True
                self.MoveYDest = self.Rectangle[1]

        if PlayerMovA:
            if self.MoveDelay > self.MoveDelayLimit:
                self.MoveDelay = 0
                return

            PlayerTileAfront = pygame.Rect(self.Rectangle[0] - MapTileSize, self.Rectangle[1], self.Rectangle[2], self.Rectangle[3])

            if GetTile(PlayerTileAfront) == 0:
                self.Rectangle[0] -= MapTileSize
                self.MoveXEnabled = True
                self.MoveXDest = self.Rectangle[0]

        if PlayerMovD:
            if self.MoveDelay > self.MoveDelayLimit:
                self.MoveDelay = 0
                return

            PlayerTileAfront = pygame.Rect(self.Rectangle[0] + MapTileSize, self.Rectangle[1], self.Rectangle[2], self.Rectangle[3])
            if GetTile(PlayerTileAfront) == 0:
                self.Rectangle[0] += MapTileSize
                self.MoveXEnabled = True
                self.MoveXDest = self.Rectangle[0]


PlayerObj = Player

def Initialize():
    global PlayerRect
    global MapTileSize
    global PlayerObj
    LoadGameMap("Fogoso/SOURCE/MAP/intro_001.map")
    PlayerRect = pygame.Rect(0,0,MapTileSize,MapTileSize)
    PlayerObj = Player(15,12)


def LoadGameMap(mapName):
    global MapData
    global MapTileset
    global MapTileSize
    global MapSizeW
    global MapSizeH
    global CurrentMessage

    try:
        f = open(mapName, "r")

        IsInitializationLines = True
        InfosLoaded = 0
        for line in f:
            line = line.rstrip()
            print(line)

            if line.startswith(";"):
                IsInitializationLines = True

            if not IsInitializationLines:
                if not line.startswith("#"):
                    SplitedData = line.split(',')
                    print("Fill Map Data:")
                    MapData[int(SplitedData[0])][int(SplitedData[1])] = int(SplitedData[2])

            if IsInitializationLines:
                SplitedParameters = line.split(':')

                if SplitedParameters[0] == "tileset":
                    InfosLoaded += 1
                    MapTileset = int(SplitedParameters[1])
                    print("Tileset set to: [{0}].".format(MapTileset))

                if SplitedParameters[0] == "tile_size":
                    InfosLoaded += 1
                    MapTileSize = int(SplitedParameters[1])
                    print("Tilesize set to: [{0}].".format(MapTileSize))

                if SplitedParameters[0] == "map_width":
                    InfosLoaded += 1
                    MapSizeW = int(SplitedParameters[1])
                    print("Map Width set to: [{0}].".format(MapSizeW))

                if SplitedParameters[0] == "map_height":
                    InfosLoaded += 1
                    MapSizeH = int(SplitedParameters[1])
                    print("Map Height set to: [{0}].".format(MapSizeH))

                if InfosLoaded >= 4:
                    IsInitializationLines = False
                    w, h = MapSizeW, MapSizeH
                    MapData = [[0 for x in range(w)] for y in range(h)]

                    print("Map Info Loaded, Loading Map Data...")
    except Exception as ex:
        CurrentMessage = str(ex)
        print("Error while loading map-data:\n" + str(ex))


def GameDraw(DISPLAY):
    global MapData
    global MapSizeW
    global MapSizeH
    global MapTileSize
    global MapTileset
    global MapCamX
    global MapCamY
    global PlayerObj
    for x, row in enumerate(MapData):
        for y, data in enumerate(row):
            gameMain.DefaultCnt.ImageRender(DISPLAY, "/map/{0}/{1}.png".format(str(MapTileset), data), MapCamX + x * MapTileSize, MapCamY + y * MapTileSize, MapTileSize, MapTileSize)

    PlayerObj.Draw(DISPLAY)

def GetTile(Rectangle):
    global MapData

    for x, row in enumerate(MapData):
        for y, data in enumerate(row):
            ColisionRect = pygame.Rect(x * MapTileSize, y * MapTileSize, MapTileSize, MapTileSize)

            if Rectangle.colliderect(ColisionRect):
                return data

def Update():
    global PlayerObj
    global MapCamY
    global MapCamX

    PlayerObj.Update()

    MapCamX = 1024 / 2 - PlayerObj.Rectangle[0]
    MapCamY = 480 / 2 - PlayerObj.Rectangle[1]

def EventUpdate(event):
    global MapData
    global MapCamY
    global MapCamX
