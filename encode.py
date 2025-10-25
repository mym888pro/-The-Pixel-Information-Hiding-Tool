from PIL import Image

def message_to_bits(message):
    # 将字符串转为二进制
    return ''.join([format(ord(c), '08b') for c in message])

def bits_to_rgb(bits):
    # 每组8*3=24bit，分别分配给RGB通道
    rgb = []
    for i in range(0, len(bits), 24):
        chunk = bits[i:i+24].ljust(24, '0')
        r = int(chunk[0:8], 2)
        g = int(chunk[8:16], 2)
        b = int(chunk[16:24], 2)
        rgb.append((r, g, b))
    return rgb

def encode_message_to_image(img_path, message, output_path):
    img = Image.open(img_path)
    img = img.convert('RGB')
    pixels = img.load()
    width, height = img.size

    bits = message_to_bits(message)
    rgb_list = bits_to_rgb(bits)

    # 选前几个像素点（从左上角开始）
    if len(rgb_list) > width * height:
        raise ValueError('信息太长，像素点不够！')

    idx = 0
    for y in range(height):
        for x in range(width):
            if idx < len(rgb_list):
                pixels[x, y] = rgb_list[idx]
                idx += 1
            else:
                break
        if idx >= len(rgb_list):
            break

    img.save(output_path)
    print(f'信息已编码，保存为 {output_path}')

if __name__ == "__main__":
    # 示例用法
    encode_message_to_image(
        img_path="input.png",
        message="Hello, world!",
        output_path="output.png"
    )
