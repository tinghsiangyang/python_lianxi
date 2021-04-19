from PIL import Image
import argparse

# 创建对象用于接收命令行参数
parser = argparse.ArgumentParser()

# 定义输入文件、输出文件、输出字符画的宽和高
parser.add_argument('file') # 接收文件参数
parser.add_argument('-o', '--output') # 接收字符输出文件参数
parser.add_argument('--width', type=int, default=80) # 接收输出字符图宽参数
parser.add_argument('--height', type=int, default=80) # 接收输出字符图高参数

# 获取命令行参数
args = parser.parse_args()

IMG = args.file # 文件赋予IMG
WIDTH = args.width # 字符图宽赋予WIDTH
HEIGHT = args.height # 字符图高赋予HEIGHT
OUTPUT = args.output # 字符图输出文件赋予OUTPUT

# print(IMG, WIDTH, HEIGHT, OUTPUT)
# python3 imgtochar.py ascii_dora.png， 输出结果：ascii_dora.png 80 80 None

# 字符图使用的字符，赋予ascii_char列表
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

def get_char(r, g, b, alpha=256):
    # 将灰度值和字符对应，返回一个灰度值对应的字符

    if alpha == 0:
        return ' '
    
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0772 * b)
    unit = (256.0 + 1)/length 

    return ascii_char[int(gray/unit)]

if __name__ == '__main__':
    # 打开IMG文件
    im = Image.open(IMG)
    
    # print(im)
    # 调整文件宽高
    im = im.resize((WIDTH, HEIGHT), Image.NEAREST)
    
    print(im.getpixel((12, 24)))

    txt = ''

    for i in range(HEIGHT):
        for j in range(WIDTH):
            txt += get_char(*im.getpixel((j, i)))
            # 元组解码？对，时元组的解码
            # 将一行每个字符添加到txt中
            
        txt += '\n' # 啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊！！！！！！！！！！！，txt='\n'了，淦
        # 一行完成，换行

    print(txt)

    if OUTPUT:
        with open(OUTPUT, 'w') as f:
            f.write(txt)
    else:
        with open('output1.txt', 'w') as f: # 如果打开的文件不存在，则新建文件
            f.write(txt)