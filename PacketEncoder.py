from anki.misc import msg_protocol, const
from anki.misc.track_pieces import TrackPieceType
from Vehicle import VehicleEmulation
import struct

class PacketDecoder:
    def encodePacket(vehicle: VehicleEmulation,packetType: int) -> bytes:
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
                    vehicle.current_track_piece.loc, 
                    vehicle.current_track_piece.type, 
                    vehicle.road_offset, 
                    vehicle.speed, 
                    vehicle.current_track_piece.clockwise
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
                    uphill_count, 
                    downhill_count,
                    0,
                    0
                )
                return msg_protocol.assemble_packet(packetType.to_bytes(1,"little"),payload)