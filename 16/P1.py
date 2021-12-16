from __future__ import annotations
from typing import Deque, List
from enum import Enum
from collections import deque
from dataclasses import dataclass, field
from sys import maxsize


class AnyPacketSegment(Enum):
    VERSION = 0
    TYPE = 1

    def next(self) -> AnyPacketSegment:
        return AnyPacketSegment(
            (self.value + 1) % len(AnyPacketSegment.__members__.items())
        )


@dataclass
class BasePacket:
    version: int
    type: int


@dataclass
class LiteralPacket(BasePacket):
    number: int


@dataclass
class OperatorPacket(BasePacket):
    packets: List[BasePacket] = field(default_factory=list)


def decode_operator_packet(version: int, type: int, data: Deque[str]) -> OperatorPacket:
    packet = OperatorPacket(version=version, type=type)
    lenght_type = data.popleft()
    if lenght_type == "0":
        number_of_bits_data = []
        for _ in range(15):
            number_of_bits_data.append(data.popleft())
        number_of_bits = int("".join(number_of_bits_data), 2)
        while number_of_bits > 0:
            previous_data_length = len(data)
            sub_packet = decode_next_packet(data)
            packet.packets.append(sub_packet)
            number_of_bits -= previous_data_length - len(data)
    else:
        number_of_sub_packets_data = []
        for _ in range(11):
            number_of_sub_packets_data.append(data.popleft())
        number_of_sub_packets = int("".join(number_of_sub_packets_data), 2)
        while number_of_sub_packets > 0:
            sub_packet = decode_next_packet(data)
            packet.packets.append(sub_packet)
            number_of_sub_packets -= 1

    return packet


def decode_literal_packet(version: int, type: int, data: Deque[str]) -> LiteralPacket:
    current_data: Deque[str] = deque()
    number_data: List[str] = []
    while True:
        current_data.append(data.popleft())
        if len(current_data) == 5:
            is_last_group = current_data.popleft() == "0"
            number_data += current_data
            current_data.clear()
            if is_last_group:
                break
    packet = LiteralPacket(
        version=version, type=type, number=int("".join(number_data), 2)
    )
    return packet


def decode_next_packet(data: Deque[str]) -> BasePacket:
    current_data: Deque[str] = deque()

    current_packet_segment = AnyPacketSegment.VERSION
    current_version = maxsize
    current_packet_type_id = maxsize

    packet: BasePacket
    while data:
        current_data.append(data.popleft())
        if current_packet_segment == AnyPacketSegment.VERSION:
            if len(current_data) == 3:
                current_version = int("".join(current_data), 2)
                current_data.clear()
                current_packet_segment = current_packet_segment.next()
        if current_packet_segment == AnyPacketSegment.TYPE:
            if len(current_data) == 3:
                current_packet_type_id = int("".join(current_data), 2)
                if current_packet_type_id == 4:
                    packet = decode_literal_packet(
                        current_version, current_packet_type_id, data
                    )
                else:
                    packet = decode_operator_packet(
                        current_version, current_packet_type_id, data
                    )
                break
    return packet


def solve() -> int:
    input = open("input.txt", "r").readline().strip()

    data: Deque[str] = deque()
    for c in input:
        data += bin(int(c, 16))[2:].zfill(4)

    packet = decode_next_packet(data)

    to_visit: Deque[BasePacket] = deque()
    to_visit.append(packet)
    versions_total = 0
    while to_visit:
        current_packet = to_visit.popleft()
        versions_total += current_packet.version
        if isinstance(current_packet, OperatorPacket):
            to_visit += current_packet.packets

    return versions_total


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
