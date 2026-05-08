"""
Copyright 2025 Cypress Semiconductor Corporation (an Infineon company)
or an affiliate of Cypress Semiconductor Corporation. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import argparse
import secrets


def ror_u32(val: int, n: int) -> int:
    return ((val >> n) | (val << (32 - n))) & 0xFFFFFFFF


def parse_hex_string(s: str) -> bytes:
    return bytes.fromhex(s)


def parse_bin_file(s: str) -> bytes:
    with open(s, 'rb') as f:
        return f.read()


def parse_random(size: int) -> bytes:
    return secrets.token_bytes(size)


def parse_input(s: str, size=0) -> bytes:
    if s == "random":
        parsed = parse_random(size)
    else:
        try:
            parsed = parse_bin_file(s)
        except (FileNotFoundError, ValueError, OSError):
            try:
                parsed = parse_hex_string(s)
            except ValueError as e:
                raise ValueError(f"Invalid input: {s}. "
                                 f"Must be a hex string "
                                 f"or a binary file.") from e
    return parsed


def words_from_bytes(parsed: bytes) -> list:
    length = len(parsed)
    if length % 4 != 0:
        raise ValueError(f'{parsed.hex()} is not properly aligned')
    words = [
        int.from_bytes(parsed[i:i+4], byteorder='little')
        for i in range(0, length, 4)
    ]
    return words


def bytes_from_words(words: list) -> bytes:
    return b''.join(
        int.to_bytes(word, length=4, byteorder='little')
        for word in words
    )


def hex_string_from_words(words: list) -> str:
    return bytes_from_words(words).hex()


def obfuscate(root_secret, key_modifier):
    num_words = len(root_secret)
    share_1 = [secrets.randbits(32) for _ in range(num_words)]
    share_2 = [secrets.randbits(32) for _ in range(num_words)]
    share_0 = []
    for i in range(num_words):
        s0 = root_secret[i] ^ key_modifier[i]
        s0 ^= ror_u32(share_1[i], 1) ^ ror_u32(share_2[i], 2)
        share_0.append(s0)
    return share_0, share_1, share_2


def deobfuscate(share_0, share_1, share_2, key_modifier):
    num_words = len(share_0)
    root_secret = []
    for i in range(num_words):
        val = share_0[i] ^ ror_u32(share_1[i], 1) ^ ror_u32(share_2[i], 2)
        val ^= key_modifier[i]
        root_secret.append(val)
    return root_secret


def process_obfuscate(input_data: bytes, key_modifier: bytes) -> bytes:
    share_0, share_1, share_2 = obfuscate(
        words_from_bytes(input_data),
        words_from_bytes(key_modifier)
    )
    return bytes_from_words(share_0 + share_1 + share_2)


def process_deobfuscate(input_data: bytes, key_modifier: bytes) -> bytes:
    if len(input_data) % 3 != 0:
        raise ValueError("Input data must be a concatenation of share_0, "
                         "share_1, and share_2")

    share_length = len(input_data) // 3
    share_0 = input_data[:share_length]
    share_1 = input_data[share_length:share_length * 2]
    share_2 = input_data[share_length * 2:]

    return bytes_from_words(
        deobfuscate(
            words_from_bytes(share_0),
            words_from_bytes(share_1),
            words_from_bytes(share_2),
            words_from_bytes(key_modifier)
        )
    )


def main():
    parser = argparse.ArgumentParser(
        description="Obfuscation tool")
    subparsers = parser.add_subparsers(dest='command', required=True)

    obf = subparsers.add_parser('obfuscate')
    obf.add_argument('--input', required=True,
                     help="Hex string (e.g. 123456789abcdef0), "
                          "binary file (e.g. data.bin) or 'random'")
    obf.add_argument('--size', default=32,
                     help="Size for random generation "
                          "of input or key-modifier data (default: 32)")
    obf.add_argument('--key-modifier', required=True,
                     help="Hex string (e.g. 123456789abcdef0), "
                          "binary file (e.g. data.bin) or 'random'")
    obf.add_argument('--key-modifier-output',
                     help="Output file to save the key-modifier data "
                          "(e.g. key-modifier.bin)")
    obf.add_argument('--output',
                     help="Output file to save the obfuscated data "
                          "(e.g. output.bin)")

    deobf = subparsers.add_parser('deobfuscate')
    deobf.add_argument('--input', required=True,
                       help="Hex string (e.g. 123456789abcdef0), "
                            "binary file (e.g. data.bin) or 'random'")
    deobf.add_argument('--size', help="Size for truncating output data")
    deobf.add_argument('--key-modifier', required=True,
                       help="Hex string (e.g. 123456789abcdef0), "
                            "binary file (e.g. data.bin)")
    deobf.add_argument('--output',
                       help="Output file to save the deobfuscated data "
                            "(e.g. output.bin)")

    args = parser.parse_args()

    if args.command == 'obfuscate':
        size = int(args.size) if args.size else 32
        root_secret = parse_input(args.input, size=size)
        key_modifier = parse_input(args.key_modifier, size=size)

        data = process_obfuscate(root_secret, key_modifier)

        print("input_data:", root_secret.hex())
        print("key_modifier:", key_modifier.hex())
        print("output_data:", data.hex())

        if args.key_modifier_output:
            with open(args.key_modifier_output, 'wb') as f:
                f.write(key_modifier)
            print(f'Key modifier saved to "{args.key_modifier_output}"')

        if args.output:
            with open(args.output, 'wb') as f:
                f.write(data)
            print(f'Obfuscated data saved to "{args.output}"')

    elif args.command == 'deobfuscate':
        share = parse_input(args.input)
        key_modifier = parse_input(args.key_modifier)

        data = process_deobfuscate(share, key_modifier)
        size = int(args.size) if args.size else len(data)

        print("input_data:", share.hex())
        print("key_modifier:", key_modifier.hex())
        print("output_data:", data[:size].hex())

        if args.output:
            with open(args.output, 'wb') as f:
                f.write(data[:size])
            print(f'Deobfuscated data saved to "{args.output}"')


if __name__ == '__main__':
    main()
