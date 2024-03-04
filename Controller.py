from anki import Controller, TrackPiece
from typing import Collection, Optional
from anki.control.scanner import BaseScanner
import asyncio
from Vehicle import VehicleEmulation
from Scanner import DummyScanner


class ControllerEmulation(Controller):
    def __init__(self, *, timeout: float=10):
        self.timeout: float = timeout
        self.vehicles: set[VehicleEmulation] = set()
        self.map: Optional[list[TrackPiece]] = None
    
    async def connect_one(self,vehicle_id: Optional[int]=None) -> VehicleEmulation:
        """Connect to one non-charging Supercar and return the Vehicle instance

        :param vehicle_id: :class:`Optional[int]`
            The id given to the :class:`Vehicle` instance on connection


        Returns
        -------
        :class:`Vehicle`
            The connected supercar


        Raises
        ------
        :class:`VehicleNotFound`
            No supercar was found in the set timeout
        
        :class:`ConnectionTimedoutException`
            The connection attempt to the supercar did not succeed within the set timeout
        
        :class:`ConnectionDatabusException`
            A databus error occured whilst connecting to the supercar
        
        :class:`ConnectionFailedException`
            A generic error occured whilst connection to the supercar

        :class:`RuntimeError`
            A vehicle with the specified id already exists.
            This will only be raised when using a custom id.
        """
        vehicle = VehicleEmulation(self._check_vehicle_id(vehicle_id),self)
        vehicle._road_offset = 0
        self.vehicles.add(vehicle)
        return vehicle
    
    async def connect_specific(
            self, 
            address: str, 
            vehicle_id: Optional[int]=None
        ) -> VehicleEmulation:
        """Connect to a supercar with a specified MAC address
        
        :param address: :class:`str`
            The MAC-address of the vehicle to connect to. Needs to be uppercase seperated by colons
        :param vehicle_id: :class:`int`
            The id passed to the :class:`Vehicle` object on its creation

        Returns
        -------
        :class:`Vehicle`
            The connected supercar
        
        Raises
        ------
        :class:`VehicleNotFound`
            No supercar was found in the set timeout
        
        :class:`ConnectionTimedoutException`
            The connection attempt to the supercar did not succeed within the set timeout
        
        :class:`ConnectionDatabusException`
            A databus error occured whilst connecting to the supercar
        
        :class:`ConnectionFailedException`
            A generic error occured whilst connection to the supercar

        :class:`RuntimeError`
            A vehicle with the specified id already exists.
            This will only be raised when using a custom id.
        """
        return await self.connect_one(vehicle_id)
    
    async def connect_many(
            self,
            amount: int,
            vehicle_ids: Collection[int|None]|None=None
    ) -> tuple[VehicleEmulation, ...]:
        """Connect to <amount> non-charging Supercars
        
        :param amount: :class:`int`
            The amount of vehicles to connect to
        :param vehicle_ids: :class:`Optional[Iterable[int]]`
            The vehicle ids passed to the :class:`Vehicle` instances

        Returns
        -------
        :class:`tuple[Vehicle]`
            The connected supercars

        Raises
        ------
        :class:`ValueError`
            The amount of requested supercars does not match the length of :param vehicle_ids:

        :class:`VehicleNotFound`
            No supercar was found in the set timeout

        :class:`ConnectionTimedoutException`
            A connection attempt to one of the supercars timed out

        :class:`ConnectionDatabusException`
            A databus error occured whilst connecting to a supercar

        :class:`ConnectionFailedException`
            A generic error occured whilst connecting to a supercar
        
        :class:`RuntimeError`
            A vehicle with the specified id already exists.
            This will only be raised when using a custom id.
        """
        if vehicle_ids == None:
            vehicle_ids = []
        while len(vehicle_ids) < amount:
            vehicle_ids.append(None)

        return tuple([await self.connect_one(id) for id in vehicle_ids])
    
    async def scan(
            self,
            scan_vehicle: VehicleEmulation|None=None,
            /,
            align_pre_scan: bool=True,
            scanner_class: type[BaseScanner] = DummyScanner
    ) -> list[TrackPiece]:
        """Assembles a digital copy of the map and adds it to every connected vehicle.
        
        :param scan_vehicle: :class:`Optional[Vehicle]`
            When passed a Vehicle object, this Vehicle will be used as a scanner. Otherwise one
            will be selected automatically.
        :param align_pre_scan: :class:`bool`
            When set to True, the supercars can start from any position on the map and align
            automatically before scanning. Disabling this means your supercars need to start
            between START and FINISH
        :param scanner_class: :class:`type`
            The type of scanner used

        Returns
        -------
        :class:`list[TrackPiece]`
            The resulting map

        Raises
        ------
        :class:`DuplicateScanWarning`
            The map was already scanned in. This scan will be skipped.
        """
        scanner = scanner_class(scan_vehicle)
        
        if align_pre_scan:
            # Aligning before scanning if enabled.
            # This allows the vehicles to be placed anywhere on the map
            await asyncio.gather(*[scanner.align(v) for v in self.vehicles])
            # Since we're aligning BEFORE scan, we need the piece before
            # the one we want to align in front of
            await asyncio.sleep(1)
        await asyncio.sleep(1)#Todo: add dalay
        for v in self.vehicles:
            v._map = self.map
            v._position = len(self.map) - 1 if v in self.vehicles else 0
            # Scanner is always one piece ahead
        return self.map

    
    def _check_vehicle_id(self, vehicle_id: int| None):
        vehicle_ids = {v.id for v in self.vehicles}
        if vehicle_id == None:
            vehicle_id = 1024
            while vehicle_id in vehicle_ids:
                vehicle_id += 1
        elif vehicle_id in vehicle_ids:
            raise RuntimeError(f"Duplicate id for vehicle. Id {vehicle_id} already in use.")
        return vehicle_id