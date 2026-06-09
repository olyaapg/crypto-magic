import struct
import secrets
from PIL import Image
import matplotlib.pyplot as plt

# =====================================================
# TEA
# TEA является блочным шифром и работает с любыми байтами. 
# Для наглядности шифруются только пиксельные данные BMP, а заголовок BMP (54 байта) 
# оставляется без изменений, чтобы файл оставался открываемым как изображение.
# =====================================================

DELTA = 0x9E3779B9 # предотвращает возникновение симметрий в ключе
ROUNDS = 32
BLOCK_SIZE = 8

def tea_encrypt_block(block, key):
    v0, v1 = struct.unpack(">2I", block) # блок разбивается на две части (v0 — первые 32 бита, v1 — вторые)
    k0, k1, k2, k3 = key
    total = 0
    for _ in range(ROUNDS):
        total = (total + DELTA) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) + k0) ^ (v1 + total) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
        v1 = (v1 + (((v0 << 4) + k2) ^ (v0 + total) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
    return struct.pack(">2I", v0, v1)

def tea_decrypt_block(block, key):
    v0, v1 = struct.unpack(">2I", block)
    k0, k1, k2, k3 = key
    total = (DELTA * ROUNDS) & 0xFFFFFFFF
    for _ in range(ROUNDS):
        v1 = (v1 - (((v0 << 4) + k2) ^ (v0 + total) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
        v0 = (v0 - (((v1 << 4) + k0) ^ (v1 + total) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
        total = (total - DELTA) & 0xFFFFFFFF
    return struct.pack(">2I", v0, v1)

# PKCS7
def add_padding(data):
    pad = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    if pad == 0:
        pad = BLOCK_SIZE
    return data + bytes([pad]) * pad

def remove_padding(data):
    pad = data[-1]
    return data[:-pad]

# BMP ENCRYPTION
def encrypt_bmp(input_file, output_file, key):
    with open(input_file, "rb") as file:
        data = file.read()
    # заголовок не шифруем, чтобы открыть нормально шифрованное изобр-е
    header = data[:54]
    pixels = data[54:]
    pixels = add_padding(pixels) # Если количество пиксельных данных не кратно BLOCK_SIZE, дополняем
    encrypted = bytearray()
    for i in range(0, len(pixels), BLOCK_SIZE):
        block = pixels[i:i + BLOCK_SIZE]
        encrypted.extend(tea_encrypt_block(block, key))
    with open(output_file, "wb") as file:
        file.write(header)
        file.write(encrypted)

# BMP DECRYPTION
def decrypt_bmp(input_file, output_file, key):
    with open(input_file, "rb") as file:
        data = file.read()
    header = data[:54]
    pixels = data[54:]
    decrypted = bytearray()
    for i in range(0, len(pixels), BLOCK_SIZE):
        block = pixels[i:i + BLOCK_SIZE]
        decrypted.extend(tea_decrypt_block(block, key))
    decrypted = remove_padding(decrypted)
    with open(output_file, "wb") as file:
        file.write(header)
        file.write(decrypted)

# CHECK
def files_equal(file1, file2):
    with open(file1, "rb") as f1:
        with open(file2, "rb") as f2:
            return f1.read() == f2.read()

def show_images(images):
  plt.figure(figsize=(18,6))
  for i, (title, path) in enumerate(images, start=1):
      plt.subplot(1, 3, i)
      img = Image.open(path)
      plt.imshow(img)
      plt.title(title)
      plt.axis("off")
  plt.tight_layout()
  plt.show()
