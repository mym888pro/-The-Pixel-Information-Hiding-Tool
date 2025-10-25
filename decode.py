from PIL import Image

def rgb_to_bits(rgb_list):
    # 将所有RGB值转为二进制字符串
    bits = ''
    for r, g, b in rgb_list:
        bits += format(r, '08b') + format(g, '08b') + format(b, '08b')
    return bits

def bits_to_message(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        char = chr(int(byte, 2))
        # 可选：遇到终止符(如0)则结束
        if char == '\x00':
            break
        chars.append(char)
    return ''.join(chars)

def decode_message_from_image(img_path, message_len=None, pixel_count=None):
    img = Image.open(img_path)
    img = img.convert('RGB')
    pixels = img.load()
    width, height = img.size

    # 计算需要读取多少像素点
    if message_len:
        # 每字符8位，每像素24位
        count = (message_len * 8 + 23) // 24
    elif pixel_count:
        count = pixel_count
    else:
        raise ValueError("必须指定 message_len 或 pixel_count！")

    rgb_list = []
    idx = 0
    for y in range(height):
        for x in range(width):
            if idx < count:
                rgb_list.append(pixels[x, y])
                idx += 1
            else:
                break
        if idx >= count:
            break

    bits = rgb_to_bits(rgb_list)
    message = bits_to_message(bits)
    print(f"恢复的信息：{message}")
    return message

if __name__ == "__main__":
    # 示例用法：已知原信息长度为13
    decode_message_from_image(
        img_path="output.png",
        message_len=13  # 与编码时一致
    )
