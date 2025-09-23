#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
照片水印工具
此脚本根据照片的EXIF日期信息为照片添加水印。
"""

import os
import sys
import argparse
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ExifTags

class PhotoWatermark:
    """照片水印处理器类"""
    
    def __init__(self, font_size=36, font_color=(255, 255, 255, 128), position="right_bottom"):
        """
        初始化水印处理器
        
        参数:
            font_size (int): 水印字体大小
            font_color (tuple): 水印文本的RGBA颜色
            position (str): 水印在图像上的位置
                            (left_top, center, right_bottom等)
        """
        self.font_size = font_size
        self.font_color = font_color
        self.position = position
        
        # 尝试找到合适的字体
        try:
            # 尝试使用系统字体
            if os.name == 'nt':  # Windows
                self.font = ImageFont.truetype("arial.ttf", self.font_size)
            else:  # Linux/Mac
                self.font = ImageFont.truetype("DejaVuSans.ttf", self.font_size)
        except IOError:
            # 回退到默认字体
            self.font = ImageFont.load_default()
    
    def get_exif_date(self, image_path):
        """
        从图像EXIF数据中提取日期
        
        参数:
            image_path (str): 图像文件路径
            
        返回:
            str: YYYY-MM-DD格式的日期字符串
        """
        try:
            with Image.open(image_path) as img:
                exif_data = img._getexif()
                
                if exif_data:
                    # 在EXIF数据中查找日期标签
                    date_time = None
                    for tag, tag_value in ExifTags.TAGS.items():
                        if tag_value == 'DateTimeOriginal':
                            if tag in exif_data:
                                date_time = exif_data[tag]
                                break
                    
                    if date_time:
                        # 解析日期（格式：YYYY:MM:DD HH:MM:SS）
                        try:
                            dt = datetime.strptime(date_time, "%Y:%m:%d %H:%M:%S")
                            return dt.strftime("%Y-%m-%d")
                        except ValueError:
                            pass
                
                # 如果EXIF不可用，回退到当前日期
                current_date = datetime.now().strftime("%Y-%m-%d")
                print(f"未找到{image_path}的EXIF日期，使用当前日期：{current_date}")
                return current_date
        except Exception as e:
            print(f"读取EXIF数据时出错：{e}")
            # 出错时回退到当前日期
            return datetime.now().strftime("%Y-%m-%d")
    
    def calculate_position(self, img_width, img_height, text_width, text_height):
        """
        计算水印文本的位置
        
        参数:
            img_width (int): 图像宽度
            img_height (int): 图像高度
            text_width (int): 水印文本宽度
            text_height (int): 水印文本高度
            
        返回:
            tuple: 水印的(x, y)坐标
        """
        padding = 20  # 边缘填充
        
        if self.position == "left_top":
            return (padding, padding)
        elif self.position == "center_top":
            return ((img_width - text_width) // 2, padding)
        elif self.position == "right_top":
            return (img_width - text_width - padding, padding)
        elif self.position == "left_center":
            return (padding, (img_height - text_height) // 2)
        elif self.position == "center":
            return ((img_width - text_width) // 2, (img_height - text_height) // 2)
        elif self.position == "right_center":
            return (img_width - text_width - padding, (img_height - text_height) // 2)
        elif self.position == "left_bottom":
            return (padding, img_height - text_height - padding)
        elif self.position == "center_bottom":
            return ((img_width - text_width) // 2, img_height - text_height - padding)
        elif self.position == "right_bottom":
            return (img_width - text_width - padding, img_height - text_height - padding)
        else:
            # 默认为右下角
            return (img_width - text_width - padding, img_height - text_height - padding)
    
    def add_watermark(self, image_path, output_path):
        """
        为图像添加水印并保存
        
        参数:
            image_path (str): 源图像路径
            output_path (str): 保存水印图像的路径
            
        返回:
            bool: 成功返回True，否则返回False
        """
        try:
            # 从EXIF获取日期或使用当前日期
            date_text = self.get_exif_date(image_path)
            
            # 打开图像
            with Image.open(image_path) as img:
                # 创建副本用于绘制
                watermarked = img.copy()
                draw = ImageDraw.Draw(watermarked)
                
                # 计算文本大小
                try:
                    # 对于较新的Pillow版本
                    text_bbox = draw.textbbox((0, 0), date_text, font=self.font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                except AttributeError:
                    # 对于较旧的Pillow版本
                    text_width, text_height = draw.textsize(date_text, font=self.font)
                
                # 计算位置
                position = self.calculate_position(
                    watermarked.width, watermarked.height, text_width, text_height
                )
                
                # 绘制水印
                draw.text(position, date_text, font=self.font, fill=self.font_color)
                
                # 确保输出目录存在
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # 保存水印图像
                watermarked.save(output_path)
                
                print(f"水印图像已保存到 {output_path}")
                return True
                
        except Exception as e:
            print(f"添加水印时出错：{e}")
            return False
    
    def process_directory(self, input_dir):
        """
        处理目录中的所有图像
        
        参数:
            input_dir (str): 包含图像的目录路径
            
        返回:
            int: 成功处理的图像数量
        """
        if not os.path.isdir(input_dir):
            print(f"错误：{input_dir}不是一个目录")
            return 0
        
        # 创建输出目录
        output_dir = os.path.join(input_dir, os.path.basename(input_dir) + "_watermark")
        os.makedirs(output_dir, exist_ok=True)
        
        # 支持的图像扩展名
        image_extensions = ('.jpg', '.jpeg', '.png', '.tiff', '.bmp')
        
        # 处理每张图像
        success_count = 0
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(image_extensions):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                
                if self.add_watermark(input_path, output_path):
                    success_count += 1
        
        return success_count


def parse_color(color_str):
    """
    解析颜色字符串为RGBA元组
    
    参数:
        color_str (str): "r,g,b,a"或"r,g,b"格式的颜色字符串
        
    返回:
        tuple: RGBA颜色元组
    """
    try:
        components = [int(c.strip()) for c in color_str.split(',')]
        if len(components) == 3:
            # 添加默认透明度
            components.append(128)
        elif len(components) != 4:
            raise ValueError("颜色必须有3或4个组件")
        
        # 验证范围
        for i, val in enumerate(components):
            if val < 0 or val > 255:
                raise ValueError(f"颜色组件{i+1}超出范围(0-255)")
        
        return tuple(components)
    except Exception as e:
        raise argparse.ArgumentTypeError(f"无效的颜色格式：{e}")


def main():
    """解析参数并运行水印处理的主函数"""
    parser = argparse.ArgumentParser(
        description="根据EXIF信息为照片添加日期水印"
    )
    
    parser.add_argument(
        "input_path",
        help="图像文件或包含图像的目录的路径"
    )
    
    parser.add_argument(
        "--font-size", "-s",
        type=int,
        default=36,
        help="水印的字体大小（默认：36）"
    )
    
    parser.add_argument(
        "--color", "-c",
        type=parse_color,
        default="255,255,255,128",
        help="水印颜色，格式为r,g,b,a（0-255，默认：255,255,255,128）"
    )
    
    parser.add_argument(
        "--position", "-p",
        choices=[
            "left_top", "center_top", "right_top",
            "left_center", "center", "right_center",
            "left_bottom", "center_bottom", "right_bottom"
        ],
        default="right_bottom",
        help="水印在图像上的位置（默认：right_bottom）"
    )
    
    args = parser.parse_args()
    
    # 创建水印处理器
    watermark = PhotoWatermark(
        font_size=args.font_size,
        font_color=args.color,
        position=args.position
    )
    
    # 处理输入路径
    if os.path.isdir(args.input_path):
        # 处理目录
        count = watermark.process_directory(args.input_path)
        print(f"成功处理了{count}张图像")
    elif os.path.isfile(args.input_path):
        # 处理单个文件
        filename = os.path.basename(args.input_path)
        dir_path = os.path.dirname(args.input_path) or "."
        
        # 创建输出目录
        output_dir = os.path.join(dir_path, os.path.basename(dir_path) + "_watermark")
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, filename)
        
        if watermark.add_watermark(args.input_path, output_path):
            print("水印添加成功")
        else:
            print("添加水印失败")
    else:
        print(f"错误：{args.input_path}不存在")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())