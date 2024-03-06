from anki import TrackPiece

class MapPiece:
    def __init__(self, trackpiece: TrackPiece, uphill_count: int = 0, downhill_count:int = 0) -> None:
        self.trackPiece = trackpiece
        self.uphill_count = uphill_count
        self.downhill_count = downhill_count