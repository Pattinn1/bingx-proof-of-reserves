# -*- coding: utf-8 -*-

import argparse
from hashlib import sha256


# initialize the input parameters
parser = argparse.ArgumentParser(description="BingX's Proof of Reserves Verification Script")
subparsers = parser.add_subparsers(title='commands', help='all valid commands', dest='command')

hash_parser = subparsers.add_parser('hash', help='Calculate hash for your input string.')
hash_parser.add_argument('raw_input_string', help='The raw input string.')

verify_parser = subparsers.add_parser('verify', help='Verify the inclusion of the Merkle leaf, compare the result with the Merkle root')
verify_parser.add_argument('merkle_leaf', help='Hash of your record in the MerkleTree.')
verify_parser.add_argument('merkle_path', help='The hash path of your identifier in Merkle Tree with the format: "{hash1},{hash2}..."')

args = parser.parse_args()


# put raw input string to hash string
def hash(raw_input_string):
    hash_result = sha256(raw_input_string.encode()).hexdigest().lower()
    return hash_result


# use to generate merkle tree's root hash.
# This function will merge each of the path hash, and come out a final hash
# you can compare the final hash to the root hash that BingX has provided
def generate_root(merkle_leaf, path):
    path_list = list(path.split(','))
    root_hash = merkle_leaf
    for index in range(len(path_list)):
        other_leaf_info = path_list[index].split(':')
        if len(other_leaf_info) != 2:
            raise ValueError(f"Invalid path format at index {index}: '{path_list[index]}'. Expected format 'direction:hash'")
        
        direction = other_leaf_info[0]
        hash_value = other_leaf_info[1]
        
        # Validate direction
        if direction not in ["l", "r"]:
            raise ValueError(f"Invalid direction '{direction}' at index {index}. Must be 'l' (left) or 'r' (right)")
        
        # Validate hash format
        try:
            int(hash_value, 16)
        except ValueError:
            raise ValueError(f"Invalid hash format '{hash_value}' at index {index}. Must be a valid hexadecimal string")
        
        if direction == "l":
            root_hash = sha256((hash_value + root_hash).encode()).hexdigest().lower()
        else:  # direction == "r"
            root_hash = sha256((root_hash + hash_value).encode()).hexdigest().lower()
    return root_hash


def main():
    # calculate hash for the raw input string
    # format: hash {rawInputString}
    if args.command == "hash":
        raw_input_string = args.raw_input_string
        if not raw_input_string or raw_input_string.strip() == "":
            print("Error: Input string cannot be empty")
            return
        hash_result = hash(raw_input_string)
        print("hash: ", hash_result)
    # calc the root hash for the provided merkle leaf and merkle path
    elif args.command == "verify":
        path = args.merkle_path
        merkle_leaf = args.merkle_leaf
        
        # Validate inputs
        if not merkle_leaf or merkle_leaf.strip() == "":
            print("Error: Merkle leaf cannot be empty")
            return
        if not path or path.strip() == "":
            print("Error: Merkle path cannot be empty")
            return
        
        # Validate merkle leaf format (should be a valid hex string)
        try:
            int(merkle_leaf, 16)
        except ValueError:
            print("Error: Merkle leaf must be a valid hexadecimal string")
            return
            
        try:
            root_hash = generate_root(merkle_leaf, path)
            print('root hash: ', root_hash)
        except ValueError as e:
            print(f"Error: {e}")
    else:
        print('command error, please check your command')


# start execution
if __name__ == '__main__':
    main()
