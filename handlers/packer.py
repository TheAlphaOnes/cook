import os
import tarfile
import zstandard as zstd


def compress_folder(folder_path, output_file):

    # Create a .tar file from the folder
    with tarfile.open(output_file + '.tar', 'w') as tar:
        tar.add(folder_path, arcname=os.path.basename(folder_path))

    # Compress the .tar file with zstd
    # You can adjust the compression level (1-22) as needed
    cctx = zstd.ZstdCompressor(level=3)
    with open(output_file + '.tar', 'rb') as tar_file:
        with open(output_file + '.tar.zst', 'wb') as zstd_file:
            zstd_file.write(cctx.compress(tar_file.read()))

    # Clean up the temporary .tar file
    os.remove(output_file + '.tar')


def decompress_folder(compressed_file, output_folder):
    # Decompress the .tar.zst file with zstd
    dctx = zstd.ZstdDecompressor()
    with open(compressed_file, 'rb') as zstd_file:
        with open(output_folder + '.tar', 'wb') as tar_file:
            tar_file.write(dctx.decompress(zstd_file.read()))

    # Extract the contents of the .tar file to the output folder
    with tarfile.open(output_folder + '.tar', 'r') as tar:
        tar.extractall(output_folder)

    # Clean up the temporary .tar file
    os.remove(output_folder + '.tar')
