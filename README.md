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

## 安装步骤

1. 确保已安装 Python 3.6 或更高版本

2. 克隆或下载本项目代码到本地

3. 安装项目依赖库：

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

自定义水印样式（红色半透明水印，字体大小48，居中显示）：
```bash
python photo_watermark.py path/to/image.jpg --font-size 48 --color 255,0,0,200 --position center
```

## 输出

程序会将处理后的图片保存在原目录下的"原目录名_watermark"子目录中，保持原始文件名不变。

例如：如果输入路径是`images/photo.jpg`，那么输出路径将是`images/images_watermark/photo.jpg`。

## 测试图片

项目包含一个`test_image.py`脚本，可以用来生成测试图片：

```bash
python test_image.py
```

这将在当前目录下生成一个名为`test_photo.jpg`的测试图片，您可以使用这个图片来测试水印功能。

## 常见问题解答 (FAQ)

**Q: 为什么有些图片没有显示拍摄日期水印？**
**A:** 这可能是因为图片的EXIF信息中没有包含拍摄日期，或者EXIF信息已被删除。在这种情况下，程序会自动使用当前日期作为水印。

**Q: 支持哪些图片格式？**
**A:** 程序支持多种常见图片格式，包括但不限于JPG、JPEG、PNG、TIFF和BMP。

**Q: 如何调整水印的透明度？**
**A:** 可以通过`--color`选项设置RGBA颜色的第四个值（Alpha通道）来调整透明度，值范围为0-255，其中0表示完全透明，255表示完全不透明。

**Q: 程序会覆盖原始图片吗？**
**A:** 不会。程序总是将处理后的图片保存到新的目录中，原始图片不会被修改。

## 项目结构

```
PhotoWatermark_wzl/
├── photo_watermark.py  # 主程序文件
├── test_image.py       # 测试图片生成脚本
├── requirements.txt    # 项目依赖
├── README.md           # 项目文档
├── LICENSE             # 许可证文件
└── images/             # 示例图片目录
    ├── [示例图片文件]
    └── images_watermark/  # 处理后的示例图片目录
```

## 贡献指南

欢迎提交问题和改进建议。如果您想贡献代码，请遵循以下步骤：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个Pull Request

## 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件。

## 致谢

- 感谢[Pillow](https://python-pillow.org/)库提供的图像处理功能
- 感谢所有为本项目做出贡献的开发者和用户