from anki.misc import msg_protocol, const
from anki.misc.track_pieces import TrackPieceType
import struct

def encodePacket(vehicle: "VehicleEmulation",packetType: int) -> bytes:
    control:"ControllerEmulation" = vehicle._controller
    match packetType:
        case const.VehicleMsg.CHARGER_INFO:
            payload = struct.pack(
                "<????",
                False, 
                vehicle.battery_state.on_charger,
                vehicle.battery_state.charging,
                vehicle.battery_state.full_battery
                )
            return msg_protocol.assemble_packet(packetType.to_bytes(1,"little"),payload)
        case const.VehicleMsg.TRACK_PIECE_UPDATE:
            payload = struct.pack(
                "<BBfHB",
                control._simmulatedTrack[vehicle._internalPosition].trackPiece.loc, 
                control._simmulatedTrack[vehicle._internalPosition].trackPiece.type, 
                vehicle.road_offset, 
                vehicle.speed, 
                control._simmulatedTrack[vehicle._internalPosition].trackPiece.clockwise
            )
            return msg_protocol.assemble_packet(packetType.to_bytes(1,"little"),payload)
        case const.VehicleMsg.TRACK_PIECE_CHANGE:
            payload = struct.pack(
                "<bbfBBHbBBBBB",
                0,
                0,
                vehicle.road_offset,
                0,
                0,
                0,
                0,
                0,
                control._simmulatedTrack[vehicle._internalPosition].uphill_count, 
                control._simmulatedTrack[vehicle._internalPosition].downhill_count,
                0,
                0
            )
            return msg_protocol.assemble_packet(packetType.to_bytes(1,"little"),payload)