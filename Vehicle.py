from warnings import warn
from anki import Vehicle, TrackPiece, BaseLane, TrackPieceType
from anki.control.vehicle import BatteryState
import asyncio
from typing import Optional, Callable
from Constants import Constants
from threading import Event, Thread
from time import sleep, perf_counter

_Callback = Callable[[], None]

def waitingTask(time: int):
    if time == float("inf"):
        while(True):
            sleep(100)
    else:
        sleep(time)

def interuptTask(changedEvent:Event):
    changedEvent.wait()
    changedEvent.clear()

class VehicleEmulation(Vehicle):
    def __init__(
            self,
            id: int,
            controller: Optional["ControllerEmulatior"]=None,  # Inconsistent, but fixes failing docs
            *,
            battery: BatteryState | None = None
    ):
        super().__init__(id,None,None,controller,battery=BatteryState)
        self._is_connected = True
        
        self._pieceDistanceLeft = 0
        self._changedEvent = Event()
        self._VehicleThread = Thread(target=vehicleThread,daemon=True,args=(self,))
        self._VehicleThread.start()
    
    async def wait_for_track_change(self) -> Optional[TrackPiece]:
        """Waits until the current track piece changes.
        
        Returns
        -------
        :class:`TrackPiece`
            The new track piece. `None` if :func:`Vehicle.map` is None
            (for example if the map has not been scanned yet)
        """
        await self._track_piece_future
        # Wait on a new track piece (See _notify_handler)
        return self.current_track_piece

    async def connect(self):
        """Connect to the Supercar
        **Don't forget to call Vehicle.disconnect on program exit!**
        
        Raises
        ------
        :class:`ConnectionTimedoutException`
            The connection attempt to the supercar did not succeed within the set timeout
        :class:`ConnectionDatabusException`
            A databus error occured whilst connecting to the supercar
        :class:`ConnectionFailedException`
            A generic error occured whilst connection to the supercar
        """
        await asyncio.sleep(1)#TODO add delay
        self._is_connected = True
    
    async def disconnect(self) -> bool:
        """Disconnect from the Supercar

        .. note::
            Remember to execute this for every connected :class:`Vehicle` once the program exits.
            Not doing so will result in your supercars not connecting sometimes
            as they still think they are connected.

        Returns
        -------
        :class:`bool`
        The connection state of the :class:`Vehicle` instance. This should always be `False`

        Raises
        ------
        :class:`DisconnectTimedoutException`
            The attempt to disconnect from the supercar timed out
        :class:`DisconnectFailedException`
            The attempt to disconnect from the supercar failed for an unspecified reason
        """
        asyncio.sleep(1)#TODO: add delay
        self._is_connected = False
        return True

    async def set_speed(self, speed: int, acceleration: int = 500):
        """Set the speed of the Supercar in mm/s

        :param speed: :class:`int`
            The speed in mm/s
        :param acceleration: :class:`Optional[int]`
            The acceleration in mm/s²
        """
        self._speed = speed
        self._changedEvent.set()
    
    async def stop(self):
        """Stops the Supercar"""
        self._speed = 0
    
    async def change_position(
            self,
            roadCenterOffset: float,
            horizontalSpeed: int = 300,
            horizontalAcceleration: int = 300,
            *,
            _hopIntent: int = 0x0,
            _tag: int = 0x0
        ):
        self._road_offset = roadCenterOffset
    
    #TODO make this do something 
    async def turn(self, type: int = 3, trigger: int = 0):
        # type and trigger don't work correcty
        """
        .. warning::
            This does not yet function properly. It is advised not to use this method
        """
        if self.map is not None:
            warn(
                "Turning around with a map! This will cause a desync!",
                UserWarning
            )
    
    async def align(
            self,
            speed: int=300,
            *,
            target_previous_track_piece_type: TrackPieceType = TrackPieceType.FINISH
        ):
        await asyncio.sleep(1)#TODO add delay
        self._position = 0
        await self.stop()
    
    async def ping(self):
        """
        .. warning::
            Due to a bug in the firmware, supercars will never respond to pings!
        
        Send a ping to the vehicle
        """

def vehicleThread(vehicle: VehicleEmulation):
    while(vehicle.is_connected):
        time = perf_counter()
        oldSpeed = vehicle.speed
        tasks = (waitingTask(Constants.timeUntilTrackpieceChange(vehicle,vehicle._pieceDistanceLeft)),interuptTask())
        done, _ = asyncio.wait(tasks,return_when=asyncio.FIRST_COMPLETED)
        print("vehicle action")
        if done is tasks[0]:
            vehicle.map_position = (vehicle.map_position + 1)%len(vehicle.map)
            vehicle._pieceDistanceLeft = Constants.pieceLength()
        else:
            passedTime = perf_counter - time
            vehicle._pieceDistanceLeft -= oldSpeed*passedTime