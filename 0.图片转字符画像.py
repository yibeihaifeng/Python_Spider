'''
需要的环境：python3  Pillow  argparse
'''

from PIL import Image
# 命令行输入参数处理
import argparse

#首先，构建命令行输入参数处理 ArgumentParser实例
parser = argparse.ArgumentParser()


# 定义输入文件、输出文件、输出字符画的宽和高
parser.add_argument('file')     #输入文件
parser.add_argument('-o', '--output')   #输出文件
parser.add_argument('--width', type = int, default = 80) #输出字符画宽
parser.add_argument('--height', type = int, default = 80) #输出字符画高

#解析并获取参数
args = parser.parse_args()

# 输入的图片文件路径
IMG = args.file

# 输出字符画的宽度和高度
WIDTH = args.width
HEIGHT = args.height

# 输出字符画的路径
OUTPUT = args.output

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

# 将256灰度映射到70个字符上
def get_char(r,g,b,alpha = 256):
    # 判断 alpha的值
    if alpha == 0:
        return ' '
    # 获取字符集的长度
    length = len(ascii_char)
    # 将RGB的值转为灰度值gray，灰度值范围为0-255
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    # 灰度值范围为0-255，而字符集只有70
    # 需要进行如下处理才能将灰度值映射到指定的字符上
    unit = (256.0 + 1)/length
    # 返回灰度值对应的字符
    return ascii_char[int(gray/unit)]


# 对图片进行处理
if __name__ == '__main__':  # 表示：如果该文件被当做python模块import的时候，这部分代码不会被执行


# 1.首先使用PIL的image.OPEN打开图片文件，获得对象im
    im = Image.open(IMG)
# 2.使用PIL库的im.resize（）调整图片大小对应到输出的字符画的宽度和高度
    im = im.resize((WIDTH,HEIGHT), Image.NEAREST)

# 将所有的像素对应的字符拼接在一起成为一个字符串txt
    txt = ""

# 3.遍历提取图片中每行的像素的RGB值，调用getchar转成对应的字符

    for i in range(HEIGHT): # 遍历每行
        for j in range(WIDTH): # 遍历每列

            # 其中im.getpixel((j,i))获取得到坐标（j，i）位置的RGB像素值（有时候包含alpha值）  返回元祖
            # *可以将元祖作为参数传递给get_char，同时元祖中的每个元素都对应到get_char函数的每个元素
            txt += get_char(*im.getpixel((j,i)))
        # 遍历完一行 需要增加换行符
        txt += '\n'
    # 输出到屏幕
    print(txt)
    
    #字符画输出到文件，如果执行时配置了输出文件，将打开文件将txt输出到文件，如果没有，则默认输出到output.txt
    if OUTPUT:
        with open(OUTPUT,'w') as f:
            f.write(txt)
    else:
        with open("output.txt",'w') as f:
            f.write(txt)


'''
最后，使用刚刚编写的 ascii.py 来将下载的 ascii_dora.png 转换成字符画，
此时执行过程没有指定其他的参数，比如输出文件、输出文件的宽和高，这些参数都将使用默认的参数值：
使用命令  python 文件.py  图片名  
'''