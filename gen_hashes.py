#!/usr/bin/env python3
import hashlib
import argparse

CHUNK_SIZE = 16*1024*1024

def generate_hashes(file_path, chunk_size=CHUNK_SIZE):
    hashes = list()
    with open(file_path, 'rb') as f:
        chunk_number = 0
        chunk = f.read(chunk_size)
        while (chunk):
            hash_obj = hashlib.sha256()
            hash_obj.update(chunk)
            hashes.append((chunk_number, hash_obj.hexdigest()))
            print(hashes[chunk_number])
            chunk_number += 1
            chunk = f.read(chunk_size)
    return hashes

def main():
    parser = argparse.ArgumentParser(description="Generate hash file for blocks of data.")
    
    parser.add_argument('--file', type=str, help="The file to read for blocks")
    parser.add_argument('--out', type=str, help="The output file of <block#> <hash>")
    
    args = parser.parse_args()

    base_file = args.file
    out_file = args.out
    hashes = generate_hashes(base_file)

    with open(out_file, "w") as f:
        for chunk_num, hash_val in hashes:
            f.write(f"{chunk_num} {hash_val}\n")

if __name__ == "__main__":
    main()
