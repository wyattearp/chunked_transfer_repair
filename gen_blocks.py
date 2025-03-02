#!/usr/bin/env python3
import os
import argparse

CHUNK_SIZE = 16*1024*1024

def compare_hashes(good_hashes, bad_hashes):
    bad_chunks = []
    for chunk_num, good_hash in good_hashes.items():
        bad_hash = bad_hashes.get(chunk_num)
        if bad_hash is None:
            print(f"Chunk {chunk_num} is missing in the bad file.")
            bad_chunks.append(chunk_num)
        elif good_hash != bad_hash:
            print(f"Chunk {chunk_num} is corrupted.")
            bad_chunks.append(chunk_num)
    return bad_chunks


def extract_and_save_chunks(base_file, bad_chunks, output_dir, chunk_size=CHUNK_SIZE):
    os.makedirs(output_dir, exist_ok=True)
    with open(base_file, 'rb') as f:
        for chunk_num in bad_chunks:
            f.seek(chunk_num * chunk_size)
            chunk = f.read(chunk_size)
            output_file = os.path.join(output_dir, f"chunk_{chunk_num:08d}")
            with open(output_file, 'wb') as out:
                out.write(chunk)
            print(f"Extracted chunk #{chunk_num} to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Generate chunks for patching based on comparing two hash lists.")
    
    parser.add_argument('--file', type=str, help="The original (good) file to read for blocks")
    parser.add_argument('--good', type=str, help="The hashes.good list of good <block#> <hash>")
    parser.add_argument('--bad', type=str, help="The hashes.bad list of bad <block#> <hash>")
    parser.add_argument('--out', type=str, help="The directory where good chunks to patch will be stored, 'corrupted_chunks'", default="corrupted_chunks")
    
    args = parser.parse_args()
    base_file = args.file
    hashes_good_file = args.good
    hashes_bad_file = args.bad
    output_dir = args.out

    with open(hashes_good_file, 'r') as f:
        good_hashes = {int(line.split()[0]): line.split()[1] for line in f.readlines()}

    with open(hashes_bad_file, 'r') as f:
        bad_hashes = {int(line.split()[0]): line.split()[1] for line in f.readlines()}

    bad_chunks = compare_hashes(good_hashes, bad_hashes)

    if bad_chunks:
        print(f"Identified corrupted chunks: {bad_chunks}")
        extract_and_save_chunks(base_file, bad_chunks, output_dir)
    else:
        print("No corrupted chunks found.")

