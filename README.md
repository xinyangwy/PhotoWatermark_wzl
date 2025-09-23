# Photo Watermark Tool

一个命令行工具，用于给照片添加基于EXIF信息的日期水印。

## 功能特点

- 读取图片的EXIF信息，提取拍摄日期（年月日）作为水印
- 支持自定义水印的字体大小、颜色和位置
- 将水印添加到图片上并保存到原目录下的新子目录中
- 支持处理单张图片或整个目录中的所有图片
- 在无法获取EXIF信息时，使用当前日期作为水印

## 安装要求

- Python 3.6 或更高版本
- Pillow 库 (9.0.0 或更高版本)

## 安装步骤

1. 确保已安装 Python
2. 安装依赖库：

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
python photo_watermark.py [图片路径或目录路径]
```

### 高级选项

```bash
python photo_watermark.py [图片路径或目录路径] [选项]
```

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

### 示例

为单张图片添加水印：
```bash
python photo_watermark.py path/to/image.jpg
```

为整个目录的图片添加水印：
```bash
python photo_watermark.py path/to/directory
```

自定义水印样式：
```bash
python photo_watermark.py path/to/image.jpg --font-size 48 --color 255,0,0,200 --position center
```

## 输出

程序会将处理后的图片保存在原目录下的"原目录名_watermark"子目录中，保持原始文件名不变。