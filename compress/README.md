# Compression Tool

Implementation of Huffman Encoding & Decoding

# Usage

* Compress a file (this will save a `test.txt.compressed` in the same directory)
```shell
$ uv run compress test/test.txt
```

* Decompress a file to a filepath
```shell
$ uv run compress -d test/test.txt.compressed -o test/test.txt.decompressed
```

* (For testing) Compare the original file with the file after compression + decompression
```shell
$ diff test/test.txt test/test.txt.decompressed
```
