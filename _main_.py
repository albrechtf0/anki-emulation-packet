from Vehicle import VehicleEmulation
from Controller import ControllerEmulation
from Constants import Constants
import asyncio
import anki_ui_access as ankiUi
from anki import TrackPiece, TrackPieceType

async def main():
    map = [
        TrackPiece(0,TrackPieceType.START,False),
        TrackPiece(0,TrackPieceType.CURVE,False),
        TrackPiece(0,TrackPieceType.CURVE,False),
        TrackPiece(0,TrackPieceType.STRAIGHT,False),
        TrackPiece(0,TrackPieceType.CURVE,False),
        TrackPiece(0,TrackPieceType.CURVE,False),
        TrackPiece(0,TrackPieceType.FINISH,False)
    ]
    async with ControllerEmulation() as control:
        vehicles = await control.connect_many(3)
        control.map = map
        await control.scan()
        with ankiUi.Ui(vehicles,control.map,(0,1)) as Ui:
            await vehicles[0].set_speed(200)
            while True:
                await asyncio.sleep(1)

asyncio.run(main())

