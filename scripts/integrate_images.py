#!/usr/bin/env python3
"""
将 16 个页面的导航栏 logo 从 '汇' 字文字块换成 img/brand/logo.png 真 logo。
同时为 products.html 案例卡封面换上 4 张行业图标。
"""
import re, os, sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1) shared.css: 新增 .nav__logo-img 样式
SHARED = os.path.join(SITE, 'shared.css')
with open(SHARED, encoding='utf-8') as f:
    css = f.read()
if '.nav__logo-img' not in css:
    insertion = (
        "\n/* Real brand logo image (overrides the '汇' text mark) */\n"
        ".nav__logo-img {\n"
        "  height: 40px;\n"
        "  width: auto;\n"
        "  display: block;\n"
        "  flex-shrink: 0;\n"
        "  /* logo.png has a white opaque background; blends with the light nav */\n"
        "  border-radius: 4px;\n"
        "}\n"
    )
    # 插在 /* Logo */ 段，nav__logo-tag 之后
    css = css.replace(
        ".nav__logo-tag {\n  font-size: 10.5px; color: var(--c-text-pale);\n  margin-top: -2px; letter-spacing: .5px;\n}\n",
        ".nav__logo-tag {\n  font-size: 10.5px; color: var(--c-text-pale);\n  margin-top: -2px; letter-spacing: .5px;\n}\n" + insertion
    )
    with open(SHARED, 'w', encoding='utf-8') as f:
        f.write(css)
    print('shared.css: + .nav__logo-img 样式已添加')
else:
    print('shared.css: .nav__logo-img 已存在，跳过')

# 2) 替换 16 个页面的导航 logo
LOGO_RE = re.compile(
    r'<div class="nav__logo-mark">汇</div>\s*<div>\s*<div class="nav__logo-name">汇特讯</div>\s*<div class="nav__logo-tag">([^<]+)</div>\s*</div>'
)
LOGO_NEW = (
    r'<img src="img/brand/logo.png" alt="汇特讯" class="nav__logo-img"/>\n'
    r'      <div><div class="nav__logo-tag">\1</div></div>'
)

nav_files = [
    'index.html','products.html','5g-cluster.html','support.html',
    'docs.html','demo.html','contact.html',
    'ai-travel.html','ai-travel-premium.html','ai-travel-pure.html',
    'ai-travel-premium-guide.html','ai-travel-premium-guide-zh.html','ai-travel-premium-guide-en.html',
    'ai-travel-pure-guide.html','ai-travel-pure-guide-zh.html','ai-travel-pure-guide-en.html',
]
nav_changed = 0
for fn in nav_files:
    p = os.path.join(SITE, fn)
    if not os.path.exists(p):
        print(f'  [SKIP] {fn} not found'); continue
    with open(p, encoding='utf-8') as f:
        html = f.read()
    if 'nav__logo-img' in html:
        print(f'  [SKIP] {fn} already updated'); continue
    new_html, n = LOGO_RE.subn(LOGO_NEW, html)
    if n == 0:
        print(f'  [WARN] {fn} pattern not matched'); continue
    with open(p, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f'  [OK]   {fn}  替换 {n} 处')
    nav_changed += n
print(f'导航 logo: 共替换 {nav_changed} 处')

# 3) products.html 案例卡封面：4 张 emoji 换行业图标
PROD = os.path.join(SITE, 'products.html')
with open(PROD, encoding='utf-8') as f:
    prod = f.read()

# 添加 case-card__cover-img 样式
if '.case-card__cover-img' not in prod:
    prod = prod.replace(
        ".case-card__cover {\n  height:160px;\n  display:flex; align-items:center;justify-content:center;\n  font-size:48px;\n  position:relative;\n}\n",
        ".case-card__cover {\n  height:160px;\n  display:flex; align-items:center;justify-content:center;\n  font-size:48px;\n  position:relative;\n}\n.case-card__cover-img { width:100px; height:100px; object-fit:contain; }\n"
    )

# 案例映射：emoji -> 行业图标
cases_map = [
    ('⚖️', 'img/industry/zhifa.png',  '智慧执法'),
    ('🏗️', 'img/industry/anquan.png', '安全生产'),
    ('🚨', 'img/industry/yingji.png', '应急指挥'),
    ('👴', 'img/industry/yanglao.png','智慧养老'),
]
case_changed = 0
for emoji, icon, alt in cases_map:
    old = f'>{emoji}</div>'
    new = f'><img src="{icon}" alt="{alt}" class="case-card__cover-img"/></div>'
    if old in prod:
        prod = prod.replace(old, new, 1)
        case_changed += 1
        print(f'  products.html: {emoji} -> {icon}')
    else:
        print(f'  [WARN] products.html 未找到 emoji {emoji}')

with open(PROD, 'w', encoding='utf-8') as f:
    f.write(prod)
print(f'案例封面: 共替换 {case_changed} 处')

print('\n完成 ✅')
