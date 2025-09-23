# 照片水印工具 (Photo Watermark Tool)

一个简单易用的命令行工具，用于自动给照片添加基于EXIF信息的日期水印。

## 项目简介

照片水印工具是一个轻量级Python脚本，专门设计用于批量处理照片并添加日期水印。工具会自动读取照片的EXIF信息，提取拍摄日期，并以可自定义的样式将日期添加为水印，帮助用户在保留照片原始信息的同时，也能在视觉上直观地了解照片的拍摄时间。

## 功能特点

- 自动读取图片的EXIF信息，提取拍摄日期（年月日）作为水印
- 支持自定义水印的字体大小、颜色和位置
- 将水印添加到图片上并保存到原目录下的新子目录中
- 支持处理单张图片或批量处理整个目录中的所有图片
- 在无法获取EXIF信息时，默认使用当前日期作为水印
- 支持多种常见图片格式（JPG、PNG、TIFF、BMP等）

## 安装要求

- Python 3.6 或更高版本
- Pillow 库 (9.0.0 或更高版本)

## 安装项目依赖库

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

为单张图片添加水印：
```bash
python photo_watermark.py path/to/image.jpg
```

为整个目录的图片添加水印：
```bash
python photo_watermark.py path/to/directory
```

### 高级选项

自定义水印样式（红色半透明水印，字体大小48，居中显示）：
```bash
python photo_watermark.py path/to/image.jpg --font-size 96 --color 255,0,0,200 --position center
```
运行举例：
![image](https://github.com/xinyangwy/PhotoWatermark_wzl/blob/main/readmePng.png)

可用选项：

- `--font-size`, `-s`：设置水印字体大小（默认：36）
- `--color`, `-c`：设置水印颜色，格式为r,g,b,a（默认：255,255,255,128）
- `--position`, `-p`：设置水印位置，可选值：
  - `left_top`：左上角
  - `center_top`：顶部居中
  - `right_top`：右上角
  - `left_center`：左侧居中
  - `center`：正中央
  - `right_center`：右侧居中
  - `left_bottom`：左下角
  - `center_bottom`：底部居中
  - `right_bottom`：右下角（默认）

## 输出

程序会将处理后的图片保存在原目录下的"原目录名_watermark"子目录中，保持原始文件名不变。

例如：如果输入路径是`images/photo.jpg`，那么输出路径将是`images/images_watermark/photo.jpg`。

## 生成测试用的图片

项目包含一个`test_image.py`脚本，可以用来生成测试图片：

```bash
python test_image.py
```

这将在当前目录下生成一个名为`test_photo.jpg`的测试图片，您可以使用这个图片来测试水印功能。



## 项目结构

```
PhotoWatermark_wzl/
├── photo_watermark.py  # 主程序文件
├── test_image.py       # 测试脚本，用于生成测试图片
├── requirements.txt    # 项目依赖
├── README.md           # 项目文档
├── LICENSE             # 许可证文件
└── images/             # 示例图片目录
    ├── [示例图片文件]
    └── images_watermark/  # 处理后的示例图片目录
```

## 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件。
