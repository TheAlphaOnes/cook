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
  # Ensure output_folder exists
  os.makedirs(output_folder, exist_ok=True)

  temp_tar_path = os.path.join(output_folder, '__temp__.tar')

  # Decompress the .tar.zst file with zstd
  dctx = zstd.ZstdDecompressor()
  with open(compressed_file, 'rb') as zstd_file, open(temp_tar_path, 'wb') as tar_file:
    tar_file.write(dctx.decompress(zstd_file.read()))

  # Extract the contents of the .tar file to the output folder
  with tarfile.open(temp_tar_path, 'r') as tar:
    tar.extractall(output_folder)

  # Clean up the temporary .tar file
  os.remove(temp_tar_path)

  # If only one top-level folder exists, move its contents up
  extracted_items = [item for item in os.listdir(output_folder) if item != '__temp__.tar']
  if len(extracted_items) == 1:
    single_folder = os.path.join(output_folder, extracted_items[0])
    if os.path.isdir(single_folder):
      for item in os.listdir(single_folder):
        src = os.path.join(single_folder, item)
        dst = os.path.join(output_folder, item)
        os.rename(src, dst)
      os.rmdir(single_folder)

  return os.path.abspath(output_folder)
