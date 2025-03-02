# overview
sometimes when you're transferring data across air-gapped systems, stuff goes wrong and massive (2-3TB) files get corrupted.
rather than redo the whole transfer again because air-gapped systems make that hard, we just want the deltas of the files...
but that's hard because tools like `rsync` `xdelta3` and `bsdiff` all need the bad file next to the good file (which we sometimes can't make happen).

this set of tools is designed to address the brain dead paradigm of 'just give me the bad blocks to transfer if i know where they are'
which would be again easier if it was on the same system.
to address this we take the following brain dead CS 101 approach:

* chunk both the `file.good` and the `file.bad` up
* create a hash of every chunk (`hashes.good` and `hashes.bad`)
* transfer (sneaker net) the hash files and create the comparison
* from the compared hashes, generate the blocks of chunks that were corrupted from the good file
* transfer the `corrupted_blocks` back to the location of `file.bad`
* apply the patch of the chunks against the `file.bad`
* `file.bad` should now be corrected into `file.good`

the problem with chunking is that we need to have storage space for a duplicate copy in each location and this becomes hard with really large files.
instead, we just create the `hashes.good` and the `hashes.bad` from each file using `gen_hashes.py`.
each of these files should be easier to transfer, potentially even printable if you're having a bad day.

once we have the hashes, which are generally megabytes of data, we can use `gen_blocks.py` with the `hashes.good`, `hashes.bad`, and the original file.
if life is good, the result should be something significantly smaller (hopefully GBs vs TBs).

all files are written to try and stay under 100 lines of code in case you have to retype it from scratch and use only the build in python libraries to minimize dependencies.

tested with "it works for my horrible problem", verified twice, YMMV.

make sure your block size matches across everything (obviously)
