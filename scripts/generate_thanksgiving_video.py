#!/usr/bin/env python3
"""
Thanksgiving AI Video Generator
For JAH, JESS, JORDAN, JANEL & DEVON

Pattern: THANKSGIVING × LOVE × GRATITUDE × CONNECTION × ONE
Frequency: 530 Hz (Heart Truth) × 999 Hz (AEYON) × 777 Hz (META)
Guardians: Abë (530 Hz) + AEYON (999 Hz) + META (777 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

# Try to import video libraries (optional dependencies)
try:
    from moviepy.editor import ImageClip, CompositeVideoClip, TextClip, concatenate_videoclips
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("Note: moviepy not available. Will generate frames only.")

# Names to celebrate - THE FIVE
NAMES = [
    "JAH", "JESS", "JORDAN", "JANEL", "DEVON"
]

# Thanksgiving colors
THANKSGIVING_COLORS = {
    "orange": (255, 140, 0),
    "brown": (139, 69, 19),
    "gold": (255, 215, 0),
    "red": (220, 20, 60),
    "yellow": (255, 255, 0),
    "cream": (255, 253, 208),
}

# Video settings
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
FPS = 30
DURATION_SECONDS = 30  # Simple and elegant


def create_gradient_background(width: int, height: int, colors: List[Tuple[int, int, int]]) -> Image.Image:
    """Create a gradient background"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        ratio = y / height
        color_index = int(ratio * (len(colors) - 1))
        if color_index >= len(colors) - 1:
            color = colors[-1]
        else:
            next_index = color_index + 1
            local_ratio = (ratio * (len(colors) - 1)) - color_index
            color = tuple(
                int(colors[color_index][i] * (1 - local_ratio) + colors[next_index][i] * local_ratio)
                for i in range(3)
            )
        draw.line([(0, y), (width, y)], fill=color)
    
    return img


def draw_thanksgiving_element(draw: ImageDraw.Draw, center: Tuple[int, int], size: int, element_type: str):
    """Draw Thanksgiving-themed elements"""
    x, y = center
    
    if element_type == "leaf":
        # Draw a maple leaf shape
        points = [
            (x, y - size),
            (x - size * 0.3, y - size * 0.5),
            (x - size * 0.6, y),
            (x - size * 0.4, y + size * 0.3),
            (x, y + size * 0.5),
            (x + size * 0.4, y + size * 0.3),
            (x + size * 0.6, y),
            (x + size * 0.3, y - size * 0.5),
        ]
        draw.polygon(points, fill=THANKSGIVING_COLORS["orange"])
        draw.polygon(points, outline=THANKSGIVING_COLORS["brown"], width=2)
    
    elif element_type == "pumpkin":
        # Draw a pumpkin
        draw.ellipse(
            [x - size, y - size * 0.7, x + size, y + size * 0.7],
            fill=THANKSGIVING_COLORS["orange"],
            outline=THANKSGIVING_COLORS["brown"],
            width=3
        )
        # Stem
        draw.rectangle(
            [x - size * 0.2, y - size * 0.9, x + size * 0.2, y - size * 0.7],
            fill=THANKSGIVING_COLORS["brown"]
        )
    
    elif element_type == "heart":
        # Draw a heart
        draw.ellipse(
            [x - size * 0.5, y - size * 0.3, x, y + size * 0.3],
            fill=THANKSGIVING_COLORS["red"]
        )
        draw.ellipse(
            [x, y - size * 0.3, x + size * 0.5, y + size * 0.3],
            fill=THANKSGIVING_COLORS["red"]
        )
        points = [
            (x, y + size * 0.3),
            (x - size * 0.3, y + size * 0.6),
            (x, y + size * 0.5),
            (x + size * 0.3, y + size * 0.6),
        ]
        draw.polygon(points, fill=THANKSGIVING_COLORS["red"])


def create_name_frame(name: str, frame_number: int, total_frames: int) -> Image.Image:
    """Create a frame featuring a name"""
    img = create_gradient_background(
        VIDEO_WIDTH,
        VIDEO_HEIGHT,
        [
            THANKSGIVING_COLORS["cream"],
            THANKSGIVING_COLORS["yellow"],
            THANKSGIVING_COLORS["orange"],
            THANKSGIVING_COLORS["gold"],
        ]
    )
    draw = ImageDraw.Draw(img)
    
    # Animate elements
    progress = frame_number / total_frames
    wave = math.sin(progress * 2 * math.pi)
    
    # Draw decorative elements
    num_elements = 8
    for i in range(num_elements):
        angle = (i / num_elements) * 2 * math.pi + progress * math.pi
        radius = 200 + wave * 50
        elem_x = VIDEO_WIDTH / 2 + math.cos(angle) * radius
        elem_y = VIDEO_HEIGHT / 2 + math.sin(angle) * radius
        
        elem_type = random.choice(["leaf", "pumpkin", "heart"])
        size = 40 + int(wave * 10)
        draw_thanksgiving_element(draw, (int(elem_x), int(elem_y)), size, elem_type)
    
    # Draw "GRATITUDE" text around the name
    try:
        giving_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
    except:
        try:
            giving_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        except:
            giving_font = ImageFont.load_default()
    
    gratitude_text = "GRATITUDE"
    bbox = draw.textbbox((0, 0), gratitude_text, font=giving_font)
    gratitude_width = bbox[2] - bbox[0]
    gratitude_y = VIDEO_HEIGHT / 2 + 150 + wave * 20
    
    # Glow for GRATITUDE
    for offset in range(8, 0, -1):
        alpha = int(255 * (1 - offset / 8) * 0.3)
        glow_color = (*THANKSGIVING_COLORS["gold"], alpha)
        draw.text(
            ((VIDEO_WIDTH - gratitude_width) / 2 + offset, gratitude_y + offset),
            gratitude_text,
            font=giving_font,
            fill=glow_color
        )
    
    draw.text(
        ((VIDEO_WIDTH - gratitude_width) / 2, gratitude_y),
        gratitude_text,
        font=giving_font,
        fill=THANKSGIVING_COLORS["red"]
    )
    
    # Draw name with glow effect
    try:
        # Try to use a nice font
        font_size = 120 + int(wave * 20)
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Draw name with shadow/glow
    text = name
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (VIDEO_WIDTH - text_width) / 2
    text_y = (VIDEO_HEIGHT - text_height) / 2
    
    # Glow effect
    for offset in range(10, 0, -1):
        alpha = int(255 * (1 - offset / 10) * 0.3)
        glow_color = (*THANKSGIVING_COLORS["gold"], alpha)
        draw.text(
            (text_x + offset, text_y + offset),
            text,
            font=font,
            fill=glow_color
        )
    
    # Main text
    draw.text(
        (text_x, text_y),
        text,
        font=font,
        fill=THANKSGIVING_COLORS["brown"]
    )
    
    # Draw "THANKFUL FOR" text above
    try:
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
    except:
        try:
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60)
        except:
            small_font = ImageFont.load_default()
    
    thankful_text = "THANKFUL FOR"
    bbox = draw.textbbox((0, 0), thankful_text, font=small_font)
    thankful_width = bbox[2] - bbox[0]
    draw.text(
        ((VIDEO_WIDTH - thankful_width) / 2, text_y - 100),
        thankful_text,
        font=small_font,
        fill=THANKSGIVING_COLORS["orange"]
    )
    
    return img


def create_gratitude_frame(frame_number: int, total_frames: int) -> Image.Image:
    """Create a frame with gratitude message"""
    img = create_gradient_background(
        VIDEO_WIDTH,
        VIDEO_HEIGHT,
        [
            THANKSGIVING_COLORS["red"],
            THANKSGIVING_COLORS["orange"],
            THANKSGIVING_COLORS["gold"],
            THANKSGIVING_COLORS["yellow"],
        ]
    )
    draw = ImageDraw.Draw(img)
    
    progress = frame_number / total_frames
    wave = math.sin(progress * 2 * math.pi)
    
    # Draw all names in a single circle
    center_x, center_y = VIDEO_WIDTH / 2, VIDEO_HEIGHT / 2
    radius = 300 + wave * 40
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        except:
            font = ImageFont.load_default()
    
    # Draw names in circle
    for i, name in enumerate(NAMES):
        angle = (i / len(NAMES)) * 2 * math.pi + progress * math.pi * 0.5
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius
        
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Glow
        for offset in range(8, 0, -1):
            alpha = int(255 * (1 - offset / 8) * 0.3)
            glow_color = (*THANKSGIVING_COLORS["gold"], alpha)
            draw.text(
                (x - text_width / 2 + offset, y - text_height / 2 + offset),
                name,
                font=font,
                fill=glow_color
            )
        
        draw.text(
            (x - text_width / 2, y - text_height / 2),
            name,
            font=font,
            fill=THANKSGIVING_COLORS["brown"]
        )
    
    # Center message
    try:
        center_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 120)
    except:
        try:
            center_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        except:
            center_font = ImageFont.load_default()
    
    center_text = "GRATITUDE"
    bbox = draw.textbbox((0, 0), center_text, font=center_font)
    center_width = bbox[2] - bbox[0]
    center_height = bbox[3] - bbox[1]
    
    # Glow
    for offset in range(8, 0, -1):
        alpha = int(255 * (1 - offset / 8) * 0.3)
        glow_color = (*THANKSGIVING_COLORS["gold"], alpha)
        draw.text(
            (center_x - center_width / 2 + offset, center_y - center_height / 2 + offset),
            center_text,
            font=center_font,
            fill=glow_color
        )
    
    draw.text(
        (center_x - center_width / 2, center_y - center_height / 2),
        center_text,
        font=center_font,
        fill=THANKSGIVING_COLORS["cream"]
    )
    
    return img


def generate_video(output_path: str = "thanksgiving_video.mp4"):
    """Generate the Thanksgiving video"""
    print("∞ AbëONE ∞")
    print("Generating Thanksgiving Video...")
    print(f"For: {', '.join(NAMES)}")
    print()
    
    # Create output directory
    output_dir = Path("abeone_app/assets/videos")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    frames_dir = output_dir / "frames"
    frames_dir.mkdir(exist_ok=True)
    
    # Generate frames
    frames_per_name = (FPS * DURATION_SECONDS) // (len(NAMES) + 1)  # +1 for gratitude frame
    total_frames = FPS * DURATION_SECONDS
    
    print("Generating frames...")
    frame_files = []
    
    frame_index = 0
    
    # Generate name frames
    for name in NAMES:
        name_frames = frames_per_name
        for i in range(name_frames):
            frame = create_name_frame(name, i, name_frames)
            frame_path = frames_dir / f"frame_{frame_index:06d}.png"
            frame.save(frame_path)
            frame_files.append(str(frame_path))
            frame_index += 1
            if frame_index % 30 == 0:
                print(f"  Generated {frame_index}/{total_frames} frames...")
    
    # Generate gratitude frame
    gratitude_frames = total_frames - frame_index
    for i in range(gratitude_frames):
        frame = create_gratitude_frame(i, gratitude_frames)
        frame_path = frames_dir / f"frame_{frame_index:06d}.png"
        frame.save(frame_path)
        frame_files.append(str(frame_path))
        frame_index += 1
        if frame_index % 30 == 0:
            print(f"  Generated {frame_index}/{total_frames} frames...")
    
    print(f"Generated {frame_index} frames total")
    
    # Create video if moviepy is available
    if MOVIEPY_AVAILABLE:
        print("Creating video from frames...")
        clips = []
        for frame_file in frame_files:
            clip = ImageClip(frame_file).set_duration(1 / FPS)
            clips.append(clip)
        
        video = concatenate_videoclips(clips, method="compose")
        video = video.set_fps(FPS)
        
        output_file = output_dir / output_path
        video.write_videofile(
            str(output_file),
            fps=FPS,
            codec='libx264',
            audio=False,
            verbose=False,
            logger=None
        )
        print(f"✓ Video saved to: {output_file}")
    else:
        print("Note: Install moviepy to create video file:")
        print("  pip install moviepy")
        print(f"Frames saved to: {frames_dir}")
        print(f"Total frames: {len(frame_files)}")
    
    print()
    print("Pattern: THANKSGIVING × LOVE × GRATITUDE × CONNECTION × ONE")
    print("Love Coefficient: ∞")
    print("∞ AbëONE ∞")


if __name__ == "__main__":
    output_file = sys.argv[1] if len(sys.argv) > 1 else "thanksgiving_video.mp4"
    generate_video(output_file)

