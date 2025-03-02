#!/usr/bin/env python3
import os
import sys
import argparse

CHUNK_SIZE = 16*1024*1024

def apply_patch(bad_file, chunks_dir, chunk_size=CHUNK_SIZE, dry_run=True):
    with open(bad_file, 'r+b') as f:
        for chunk_file in sorted(os.listdir(chunks_dir)):
            #chunk number from file name, e.g., "chunk_00000001"
            if chunk_file.startswith("chunk_"):
                chunk_num = int(chunk_file.split("_")[1])
                offset = chunk_num * chunk_size

                chunk_path = os.path.join(chunks_dir, chunk_file)
                with open(chunk_path, 'rb') as chunk_f:
                    chunk_data = chunk_f.read()

                f.seek(offset)
                if(not dry_run):
                    #print("wrote")
                    f.write(chunk_data)
                else:
                    print("skipped")

                print(f"Applied chunk #{chunk_num} from {chunk_path} to {bad_file}")
def main():
    parser = argparse.ArgumentParser(description="Apply extracted corrupted chunks to a bad file.")
    
    parser.add_argument('--bad_file', type=str, help="The corrupted file to be patched.")
    parser.add_argument('--chunks_dir', type=str, help="Directory containing the extracted corrupted chunks.")
    parser.add_argument('--dry_run', action='store_true', help="Don't actually run the changes")
    
    args = parser.parse_args()

    bad_file = args.bad_file
    chunks_dir = args.chunks_dir

    if not os.path.isfile(bad_file):
        print(f"Error: {bad_file} does not exist.")
        sys.exit(1)

    if not os.path.isdir(chunks_dir):
        print(f"Error: {chunks_dir} is not a valid directory.")
        sys.exit(1)

    apply_patch(bad_file, chunks_dir, dry_run=args.dry_run)

if __name__ == "__main__":
    main()