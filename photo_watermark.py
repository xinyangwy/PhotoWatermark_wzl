#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo Watermark Tool
This script adds a watermark to photos based on their EXIF date information.
"""

import os
import sys
import argparse
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ExifTags

class PhotoWatermark:
    """Photo watermark processor class"""
    
    def __init__(self, font_size=36, font_color=(255, 255, 255, 128), position="right_bottom"):
        """
        Initialize the watermark processor
        
        Args:
            font_size (int): Size of the watermark font
            font_color (tuple): RGBA color of the watermark text
            position (str): Position of the watermark on the image
                            (left_top, center, right_bottom, etc.)
        """
        self.font_size = font_size
        self.font_color = font_color
        self.position = position
        
        # Try to find a suitable font
        try:
            # Try to use a system font
            if os.name == 'nt':  # Windows
                self.font = ImageFont.truetype("arial.ttf", self.font_size)
            else:  # Linux/Mac
                self.font = ImageFont.truetype("DejaVuSans.ttf", self.font_size)
        except IOError:
            # Fallback to default font
            self.font = ImageFont.load_default()
    
    def get_exif_date(self, image_path):
        """
        Extract the date from image EXIF data
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            str: Date string in YYYY-MM-DD format
        """
        try:
            with Image.open(image_path) as img:
                exif_data = img._getexif()
                
                if exif_data:
                    # Find the date tag in EXIF data
                    date_time = None
                    for tag, tag_value in ExifTags.TAGS.items():
                        if tag_value == 'DateTimeOriginal':
                            if tag in exif_data:
                                date_time = exif_data[tag]
                                break
                    
                    if date_time:
                        # Parse the date (format: YYYY:MM:DD HH:MM:SS)
                        try:
                            dt = datetime.strptime(date_time, "%Y:%m:%d %H:%M:%S")
                            return dt.strftime("%Y-%m-%d")
                        except ValueError:
                            pass
                
                # Fallback to current date if EXIF not available
                current_date = datetime.now().strftime("%Y-%m-%d")
                print(f"No EXIF date found for {image_path}, using current date: {current_date}")
                return current_date
        except Exception as e:
            print(f"Error reading EXIF data: {e}")
            # Fallback to current date on error
            return datetime.now().strftime("%Y-%m-%d")
    
    def calculate_position(self, img_width, img_height, text_width, text_height):
        """
        Calculate the position of the watermark text
        
        Args:
            img_width (int): Width of the image
            img_height (int): Height of the image
            text_width (int): Width of the watermark text
            text_height (int): Height of the watermark text
            
        Returns:
            tuple: (x, y) coordinates for the watermark
        """
        padding = 20  # Padding from the edge
        
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
            # Default to right bottom
            return (img_width - text_width - padding, img_height - text_height - padding)
    
    def add_watermark(self, image_path, output_path):
        """
        Add watermark to an image and save it
        
        Args:
            image_path (str): Path to the source image
            output_path (str): Path to save the watermarked image
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get the date from EXIF or use current date
            date_text = self.get_exif_date(image_path)
            
            # Open the image
            with Image.open(image_path) as img:
                # Create a copy to draw on
                watermarked = img.copy()
                draw = ImageDraw.Draw(watermarked)
                
                # Calculate text size
                try:
                    # For newer Pillow versions
                    text_bbox = draw.textbbox((0, 0), date_text, font=self.font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                except AttributeError:
                    # For older Pillow versions
                    text_width, text_height = draw.textsize(date_text, font=self.font)
                
                # Calculate position
                position = self.calculate_position(
                    watermarked.width, watermarked.height, text_width, text_height
                )
                
                # Draw the watermark
                draw.text(position, date_text, font=self.font, fill=self.font_color)
                
                # Ensure the output directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Save the watermarked image
                watermarked.save(output_path)
                
                print(f"Watermarked image saved to {output_path}")
                return True
                
        except Exception as e:
            print(f"Error adding watermark: {e}")
            return False
    
    def process_directory(self, input_dir):
        """
        Process all images in a directory
        
        Args:
            input_dir (str): Path to the directory containing images
            
        Returns:
            int: Number of successfully processed images
        """
        if not os.path.isdir(input_dir):
            print(f"Error: {input_dir} is not a directory")
            return 0
        
        # Create output directory
        output_dir = os.path.join(input_dir, os.path.basename(input_dir) + "_watermark")
        os.makedirs(output_dir, exist_ok=True)
        
        # Supported image extensions
        image_extensions = ('.jpg', '.jpeg', '.png', '.tiff', '.bmp')
        
        # Process each image
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
    Parse color string to RGBA tuple
    
    Args:
        color_str (str): Color string in format "r,g,b,a" or "r,g,b"
        
    Returns:
        tuple: RGBA color tuple
    """
    try:
        components = [int(c.strip()) for c in color_str.split(',')]
        if len(components) == 3:
            # Add default alpha
            components.append(128)
        elif len(components) != 4:
            raise ValueError("Color must have 3 or 4 components")
        
        # Validate ranges
        for i, val in enumerate(components):
            if val < 0 or val > 255:
                raise ValueError(f"Color component {i+1} out of range (0-255)")
        
        return tuple(components)
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Invalid color format: {e}")


def main():
    """Main function to parse arguments and run the watermark process"""
    parser = argparse.ArgumentParser(
        description="Add date watermark to photos based on EXIF information"
    )
    
    parser.add_argument(
        "input_path",
        help="Path to the image file or directory containing images"
    )
    
    parser.add_argument(
        "--font-size", "-s",
        type=int,
        default=36,
        help="Font size for the watermark (default: 36)"
    )
    
    parser.add_argument(
        "--color", "-c",
        type=parse_color,
        default="255,255,255,128",
        help="Watermark color in r,g,b,a format (0-255, default: 255,255,255,128)"
    )
    
    parser.add_argument(
        "--position", "-p",
        choices=[
            "left_top", "center_top", "right_top",
            "left_center", "center", "right_center",
            "left_bottom", "center_bottom", "right_bottom"
        ],
        default="right_bottom",
        help="Position of the watermark on the image (default: right_bottom)"
    )
    
    args = parser.parse_args()
    
    # Create watermark processor
    watermark = PhotoWatermark(
        font_size=args.font_size,
        font_color=args.color,
        position=args.position
    )
    
    # Process input path
    if os.path.isdir(args.input_path):
        # Process directory
        count = watermark.process_directory(args.input_path)
        print(f"Successfully processed {count} images")
    elif os.path.isfile(args.input_path):
        # Process single file
        filename = os.path.basename(args.input_path)
        dir_path = os.path.dirname(args.input_path) or "."
        
        # Create output directory
        output_dir = os.path.join(dir_path, os.path.basename(dir_path) + "_watermark")
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, filename)
        
        if watermark.add_watermark(args.input_path, output_path):
            print("Watermark added successfully")
        else:
            print("Failed to add watermark")
    else:
        print(f"Error: {args.input_path} does not exist")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())