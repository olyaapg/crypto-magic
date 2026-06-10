import struct

# внедрение иноформации в BMP (LSB-replacement)
def embed_lsb_replacement(input_bmp, output_bmp, message):
    with open(input_bmp, "rb") as f:
        data = bytearray(f.read())
    # проверка, что BMP
    if data[:2] != b"BM":
        raise ValueError("Not BMP-file")
    # смещение до пикселей
    pixel_offset = struct.unpack_from("<I", data, 0x0A)[0]
    # размер всего файла
    file_size = struct.unpack_from("<I", data, 0x02)[0]
    pixel_data_size = file_size - pixel_offset
    # байты сообщения
    message_bytes = message.encode("utf-8")
    # длина сообщения в байтах
    print("Message length:", len(message_bytes), "bytes")
    print("Image size:", pixel_data_size, "bytes")
    message_length_bytes = struct.pack("<I", len(message_bytes))
    # сначала биты длины, потом биты сообщения
    bit_stream = (message_length_bytes + message_bytes)
    # проверка, что не превысили размер (1 байт текста умещается в 8 байт картинки)
    max_bytes = pixel_data_size // 8
    if len(bit_stream) > max_bytes:
        raise ValueError(f"Message is too long. Max: {max_bytes - 4} bytes")
    for i in range(len(bit_stream)):
        byte_val = bit_stream[i]
        for bit_pos in range(8):
            bit = (byte_val >> (7 - bit_pos)) & 1
            idx = i * 8 + bit_pos
            data[pixel_offset + idx] = (data[pixel_offset + idx] & 0xFE) | bit
    
    with open(output_bmp, "wb") as f:
        f.write(data)


# собираем информацию из байтов
def extract_lsb_replacement_from_bytes(data, offset, message_length):
    message_bits = []
    for i in range(offset, offset + message_length * 8):
        message_bits.append(data[i] & 1)
    message_bytes = bytearray()
    for i in range(message_length):
        byte_val = 0
        for j in range(8):
            byte_val = (byte_val << 1) | message_bits[i * 8 + j]
        message_bytes.append(byte_val)
    return message_bytes

# извлечение информации из BMP
def extract_lsb_replacement(stego_bmp):
    with open(stego_bmp, "rb") as f:
        data = f.read()
    if data[:2] != b"BM":
        raise ValueError("Not BMP-file")
    pixel_offset = struct.unpack_from("<I", data, 0x0A)[0]
    file_size = struct.unpack_from("<I", data, 0x02)[0]
    pixel_data = data[pixel_offset:file_size]
    # 4 байта длины сообщения
    length_bytes = extract_lsb_replacement_from_bytes(pixel_data, 0, 4)
    message_length = struct.unpack("<I", length_bytes)[0]
    print("Message length:", message_length)
    # длина собщения >0 и не вылазит за картинку
    if message_length <= 0 or message_length > (len(pixel_data) // 8) - 4:
        raise ValueError(f"Incorrect message length: {message_length}")
    # байты сообщения
    message_bytes = extract_lsb_replacement_from_bytes(pixel_data, 4 * 8, message_length)
    return message_bytes.decode("utf-8")

if __name__ == "__main__":
    embed_lsb_replacement("original.bmp", "stego.bmp", "Юстас — Центру. Приём, приём...")
    secret = extract_lsb_replacement("stego.bmp")
    print("Message:", secret)
