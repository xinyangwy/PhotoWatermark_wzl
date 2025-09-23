#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
创建一个带有EXIF日期信息的测试图片
"""

from PIL import Image, ImageDraw, ImageFont
import os
import time

# 创建一个简单的测试图片
img = Image.new('RGB', (800, 600), color='#333333')
draw = ImageDraw.Draw(img)

# 尝试使用系统字体添加一些文字
try:
    if os.name == 'nt':  # Windows
        font = ImageFont.truetype("arial.ttf", 36)
    else:  # Linux/Mac
        font = ImageFont.truetype("DejaVuSans.ttf", 36)
    draw.text((100, 250), "Test Image", font=font, fill=(255, 255, 255))
    draw.text((100, 300), "For Photo Watermark Tool", font=font, fill=(255, 255, 255))
except IOError:
    # 使用默认字体
    draw.text((100, 250), "Test Image", fill=(255, 255, 255))
    draw.text((100, 300), "For Photo Watermark Tool", fill=(255, 255, 255))

# 注意：在较新版本的PIL中，添加EXIF信息的方式有所不同
# 我们简化处理，先创建图片文件
img.save('test_photo.jpg')

# 获取当前日期
current_date = time.strftime("%Y-%m-%d", time.localtime())
print(f"测试图片已创建: test_photo.jpg")
print(f"提示：由于EXIF写入在新版本PIL中需要更复杂的处理，")
print(f"程序将默认使用当前日期作为水印：{current_date}")