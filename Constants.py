from dataclasses import dataclass
from math import pi
from anki import TrackPieceType

@dataclass(slots=True)
class Constants:
    StaightLength: int = 550
    IntersectionLength: int = 550
    FinishLength: int = 35
    StartLength: int = 20
    
    def curveRadius(roadOffset:int) -> int:
        return 0.5*pi*(roadOffset+280)
    
    def pieceLength(vehicle: "VehicleEmulation") -> int:
        match vehicle.current_track_piece.type:
            case TrackPieceType.START:
                return Constants.StaightLength
            case TrackPieceType.FINISH:
                return Constants.FinishLength
            case TrackPieceType.INTERSECTION:
                return Constants.IntersectionLength
            case TrackPieceType.CURVE:
                return Constants.curveRadius(vehicle.road_offset)

    
    def timeUntilTrackpieceChange(vehicle: "VehicleEmulation", distance:int) -> float:
        if vehicle.speed == 0:
            return float("inf")
        return distance / vehicle.speed