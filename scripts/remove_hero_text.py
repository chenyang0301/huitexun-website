#!/usr/bin/env python3
"""
去掉 hero banner 上烧进去的文字：
- hero-1-tech.png: 左上区域 "赋能千行百业/助力数智化转型" -> 克隆上方蓝色渐变覆盖
- hero-3-port.png: 底部居中 "5G集群调度通信系统" -> 克隆上方场景覆盖
技术：crop(src_y0-h..y0) -> paste(y0..y0+h) -> 高斯模糊缝合带
"""
import os
from PIL import Image, ImageFilter

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def remove_text_clone_above(im, box, seam_blur=12, seam_h=None):
    """用 box 正上方等高区域的内容覆盖 box，再模糊缝合带消除接缝。"""
    x0, y0, x1, y1 = box
    h = y1 - y0
    w = x1 - x0
    if seam_h is None:
        seam_h = min(22, h // 3)
    sx0, sy0, sx1, sy1 = x0, y0 - h, x1, y0
    if sy0 < 0:
        raise ValueError(f"上方没有足够空间克隆: y0={y0}, need h={h}")
    src = im.crop((sx0, sy0, sx1, sy1))
    if src.size != (w, h):
        src = src.resize((w, h))
    im.paste(src, (x0, y0))
    # 模糊顶边缝合（y0 处）
    t0 = max(0, y0 - seam_h)
    t1 = min(im.height, y0 + seam_h)
    band = im.crop((x0, t0, x1, t1))
    im.paste(band.filter(ImageFilter.GaussianBlur(seam_blur)), (x0, t0))
    return im

# ── hero-1-tech: 左上文字 (40,240)-(720,480) ──
p1 = os.path.join(SITE, 'img/hero/hero-1-tech.png')
im1 = Image.open(p1).convert('RGB')
print(f'hero-1-tech size: {im1.size}')
remove_text_clone_above(im1, (40, 240, 720, 480))
im1.save(p1, optimize=True)
print('hero-1-tech.png: 文字已去除 ✅')

# ── hero-3-port: 底部文字 (580,640)-(1340,780) ──
p3 = os.path.join(SITE, 'img/hero/hero-3-port.png')
im3 = Image.open(p3).convert('RGB')
print(f'hero-3-port size: {im3.size}')
remove_text_clone_above(im3, (580, 640, 1340, 780))
im3.save(p3, optimize=True)
print('hero-3-port.png: 文字已去除 ✅')

print('\n完成 ✅')