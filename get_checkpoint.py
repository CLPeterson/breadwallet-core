#!/usr/bin/env python
"""
Given a block height, return the checkpoint hash information data that consist of:

- block hash
- timestamp
- bits

Usage (default network is mainnet):
    get_checkpoint.py <height> [network]

Example:
    get_checkpoint.py 624960
    { 624960, uint256("00000000000000000010a34de0c20440b6804f61549e1c1b18d0b80afb\
    589d6e"), 1586336046, 0x171320bc }
"""

from sys import argv

import httpx


def main():
    network = "mainnet"
    if len(argv) <= 1:
        print(__doc__)
        exit(1)

    if len(argv) > 2:
        network = argv[2]
    else:
        network = "mainnet"

    height: str = argv[1]

    url: str = "https://blockstream.info"

    if network == "mainnet":
        url += f"/api/block-height/{height}"
    else:
        url += f"/{network}/api/block-height/{height}"

    hash: str = httpx.get(url).read().decode("utf-8")

    url = "https://blockstream.info"

    if network == "mainnet":
        url += f"/api/block/{hash}"
    else:
        url += f"/{network}/api/block/{hash}"

    data: dict = httpx.get(url).json()

    timestamp = data["timestamp"]
    bits = data["bits"]

    print(checkpoint_str(int(height), hash, timestamp, bits))


def checkpoint_str(height: int, hash: str, timestamp: int, bits: int) -> str:
    return f'{{ {height}, uint256("{hash}"), {timestamp}, 0x{bits:2x} }}'


if __name__ == "__main__":
    main()
