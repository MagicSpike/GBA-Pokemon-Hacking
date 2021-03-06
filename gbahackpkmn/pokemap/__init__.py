"""This tool contains some functionality for GBA Pokemon map manipulation.
Don't expect full advance map functionality. However expect easy map elements
modification, such as headers, scripts, etc. This can be usefull for running
automated jobs. For example when you update a script, automatically update the
script reference."""

from gbahack.gbabin.datastruct import DataStruct, RomDataType as RT
from gbahackpkmn.pokemap.scripts import MapScriptStruct
from gbahackpkmn.pokemap.events import *
from gbahackpkmn.pokemap.mapscripts import MapScripts

class PokeMapManager():
    def __init__(self, rom):
        self.tablepointer = rom.metadata['maptable']
        self.rom = rom
    
    def getBank(self, bankid):
        #The tablepointer contains a list of pointers to the banks. This list is not
        # ended with an end of list.
        # TODO: Maybe the 02 00 00 00 00 00 00 00 at the end is the end of list
        #       Then a warning can be raised if searching too far.
        _, bankpointer = self.rom.readPointer(self.tablepointer + 4*bankid)
        return PokeMapBank(self.rom, bankpointer)
    
    def getMap(self, bankid, mapid):
        bank = self.getBank(bankid)
        return bank.getMap(mapid)

    
class PokeMapBank():
    '''Pokemap bank, is a list of all maps on this bank. This bank is completely
    rom-aware, since it is just a lookup table, to map-header pointers.
  
    NOTE: In ROM there is no length defined for this bank! There is also no end of
          bank notion.'''
    def __init__(self, rom, pointer):
        self.rom = rom
        self.pointer = pointer
    
    def getMap(self, mapid):
        _, mapheaderpointer  = self.rom.readPointer(self.pointer + 4 * mapid)
        return PokeMap(self.rom, mapheaderpointer)
  
    
class PokeMap():
    '''Representation of a map. It is aware of its map location.
    Current implementation is read-only.'''
    def __init__(self, rom, p):
        self.header = p
        p, self.pointerfooter      = rom.readPointer(p)
        p, self.pointerevents      = rom.readPointer(p)
        p, self.pointermapscripts  = rom.readPointer(p)
        p, self.pointerconnections = rom.readPointer(p)
        #TODO: 3 x 4 bytes to read with additional map data
        
        self.events = PokeMapEvents(rom, self.pointerevents)
        self.mapscripts = MapScripts(rom, self.pointermapscripts)


