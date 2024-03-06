from Vehicle import VehicleEmulation
from Controller import ControllerEmulation
from Constants import Constants
import asyncio
import anki_ui_access as ankiUi
from anki import TrackPiece, TrackPieceType
from MapPiece import MapPiece

async def main():
    map = [
        MapPiece(TrackPiece(0,TrackPieceType.START,False)),
        MapPiece(TrackPiece(0,TrackPieceType.CURVE,False)),
        MapPiece(TrackPiece(0,TrackPieceType.CURVE,False)),
        MapPiece(TrackPiece(0,TrackPieceType.STRAIGHT,False)),
        MapPiece(TrackPiece(0,TrackPieceType.CURVE,False)),
        MapPiece(TrackPiece(0,TrackPieceType.CURVE,False)),
        MapPiece(TrackPiece(0,TrackPieceType.FINISH,False))
    ]
    async with ControllerEmulation(map) as control:
        vehicles = await control.connect_many(3)
        await control.scan()
        with ankiUi.Ui(vehicles,control.map,(0,1)) as Ui:
            await vehicles[0].set_speed(200)
            while True:
                await asyncio.sleep(1)

asyncio.run(main())

