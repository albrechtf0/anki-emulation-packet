from anki import Vehicle, TrackPiece, errors
from anki.control.controller import Controller
from anki.control.vehicle import BatteryState, _call_all_soon
from anki.misc import msg_protocol, const
import asyncio
import struct
from threading import Thread
from bleak import BleakClient
from bleak.backends.device import BLEDevice
from time import sleep
from PacketEncoder import encodePacket


class VehicleEmulation(Vehicle):
    def __init__(self, id: int, device: BLEDevice, client: BleakClient | None = None, controller: Controller | None = None,internalPosition:int = 0 , *, battery: BatteryState):
        super().__init__(id, device, client, controller, battery=battery)
        self._internalPosition = internalPosition
        self._simThread = Thread(target=vehicleTread,daemon=True,args=(self,))
        self._simThread.start
    
    async def _Vehicle__send_package(self, payload: bytes):#Overrides Vehicle.__send_package
        """Send a payload to the supercar"""
        #if self._write_chara is None:
        #    raise RuntimeError("A command was sent to a vehicle that has not been connected.")
        try:
            packetType, content =  msg_protocol.disassemble_packet(payload)
            match packetType:
                case const.ControllerMsg.SET_SPEED:
                    speed, accel = struct.unpack_from("<ii",payload)
                    self._speed = speed
                case const.ControllerMsg.CHANGE_LANE:
                    (
                        horizontalSpeed,
                        horizontalAcceleration,
                        roadCenterOffset,
                        _hopIntent,
                        _tag
                    ) = struct.unpack_from("<HHfBB",payload)
                    self._road_offset = roadCenterOffset
                case const.ControllerMsg.TURN_180:
                    raise NotImplementedError("Turn_180 is not supported jet")
                    pass#TODO: add support
                case _:
                    pass
        except OSError as e:
            raise RuntimeError(
                "A command was sent to a vehicle that is already disconnected"
            ) from e


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
        self._is_connected = True
        self._ping_task = asyncio.create_task(self._auto_ping())
    
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
        self._is_connected = False
        return self._is_connected


def vehicleTread(vehicle: VehicleEmulation):
    while True:
        sleep(2)
        vehicle._internalPosition = (vehicle._internalPosition+1)%(len(vehicle._controller._simmulatedTrack)-1) 
        payload = encodePacket(vehicle,const.VehicleMsg.TRACK_PIECE_UPDATE)
        vehicle._notify_handler(None,payload)