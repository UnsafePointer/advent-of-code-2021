from __future__ import annotations
import operator
from typing import Deque, List
from enum import Enum
from collections import deque
from dataclasses import dataclass, field
from sys import maxsize
from functools import reduce
from operator import mul


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


def calculate_packet(packet: BasePacket) -> int:
    if isinstance(packet, LiteralPacket):
        return packet.number
    else:
        operator_packet: OperatorPacket = eval(
            repr(packet)
        )  # Python sins to shut up mypy
        sub_packet_values = [calculate_packet(sp) for sp in operator_packet.packets]
        if operator_packet.type == 0:
            return sum(sub_packet_values)
        elif operator_packet.type == 1:
            return reduce(mul, sub_packet_values, 1)
        elif operator_packet.type == 2:
            return min(sub_packet_values)
        elif operator_packet.type == 3:
            return max(sub_packet_values)
        elif operator_packet.type == 5:
            return 1 if sub_packet_values[0] > sub_packet_values[-1] else 0
        elif operator_packet.type == 6:
            return 1 if sub_packet_values[0] < sub_packet_values[-1] else 0
        elif operator_packet.type == 7:
            return 1 if sub_packet_values[0] == sub_packet_values[-1] else 0
        else:
            raise RuntimeError(
                f"Invalid operator packet with type: {operator_packet.type}"
            )


def solve() -> int:
    input = open("input.txt", "r").readline().strip()

    data: Deque[str] = deque()
    for c in input:
        data += bin(int(c, 16))[2:].zfill(4)

    packet = decode_next_packet(data)
    return calculate_packet(packet)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
