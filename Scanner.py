from anki.control.scanner import BaseScanner
from anki import TrackPiece, TrackPieceType
from     Vehicle import VehicleEmulation

class DummyScanner(BaseScanner):
    def __init__(self, vehicle: VehicleEmulation):
        self.vehicle = vehicle
        self.map: list[TrackPiece] = []
        print("Created scanner")
    
    
    async def scan(self) -> list[TrackPiece]:
        """
        This method should scan in the map using various functionalities.
        The returned list of track pieces should begin with a type of
        `TrackPieceType.START` and end with `TrackPieceType.FINISH`.

        Returns
        -------
        :class:`list[TrackPiece]`
            The scanned map
        
        Raises
        ------
        """
        return None
    
    
    async def align(
        self,
        vehicle: VehicleEmulation,
        *,
        target_previous_track_piece_type: TrackPieceType=TrackPieceType.FINISH
    ) -> None:
        await vehicle.align()