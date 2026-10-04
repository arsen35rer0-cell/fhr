# build_icon.py
from PIL import Image, ImageDraw

def generate():
    size = 256
    img = Image.new('RGBA', (size, size), (10, 10, 15, 255))
    draw = ImageDraw.Draw(img)
    c = size // 2
    
    # Неоновое кольцо
    draw.ellipse([c-100, c-100, c+100, c+100], outline=(0, 200, 255), width=8)
    # Внутренний "глаз" анализа
    draw.ellipse([c-35, c-35, c+35, c+35], fill=(255, 40, 40))
    # Сканирующие линии
    for i in range(3):
        y = c - 70 + i * 70
        draw.line([(c-90, y), (c+90, y)], fill=(0, 255, 150, 120), width=2)
    
    img.save('app_icon.ico', format='ICO', sizes=[(256, 256)])
    print("✅ Icon generated")

if __name__ == "__main__":
    generate()
