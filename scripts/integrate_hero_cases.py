#!/usr/bin/env python3
"""
1) products.html: 4 个案例 -> 旧官网 6 个典型案例（内容结合旧站原文重新生成）
2) index.html: hero 区改为全宽轮播（hero-1-tech / hero-3-port / hero-4-command，跳过已过时冬奥 banner）
"""
import os

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ══════════════════════════════════════════════════════════════
# 1) products.html 案例
# ══════════════════════════════════════════════════════════════
PROD = os.path.join(SITE, 'products.html')
with open(PROD, encoding='utf-8') as f:
    prod = f.read()

# 更新 section 头部描述
prod = prod.replace(
    '<h2 class="section__title">真实落地，见证价值</h2>',
    '<h2 class="section__title">六大典型案例，真实落地见证价值</h2>'
)
prod = prod.replace(
    '<p class="section__desc">汇特讯已在多个行业实现规模化部署，以下为部分典型合作案例。</p>',
    '<p class="section__desc">从冬奥保障到城市治理，汇特讯在多个行业实现规模化部署，以下为六大典型合作案例。</p>'
)

CASES_GRID_START = '<div class="cases-grid">'
CASES_GRID_END = '    </div>\n  </div>\n</section>'
start = prod.index(CASES_GRID_START)
end = prod.index(CASES_GRID_END, start)

def case(gradient, icon, alt, tag_cls, tag_text, title, desc, metrics):
    items = ''.join(
        f'<div class="case-result-item"><div class="case-result-item__num">{n}</div><div class="case-result-item__lbl">{l}</div></div>'
        for n, l in metrics
    )
    return (
        f'      <div class="case-card">\n'
        f'        <div class="case-card__cover" style="background:linear-gradient(135deg,{gradient});"><img src="img/industry/{icon}" alt="{alt}" class="case-card__cover-img"/></div>\n'
        f'        <div class="case-card__body">\n'
        f'          <div class="case-card__industry tag {tag_cls}">{tag_text}</div>\n'
        f'          <div class="case-card__title">{title}</div>\n'
        f'          <p class="case-card__desc">{desc}</p>\n'
        f'          <div class="case-card__result">{items}</div>\n'
        f'        </div>\n'
        f'      </div>'
    )

cases = []
cases.append(case(
    '#E3F2FD,#BBDEFB', 'yingji.png', '应急指挥', 'tag--blue', '🚨 应急指挥',
    '北京冬奥会 · 指挥调度平台',
    '覆盖 13 个比赛场馆、18 个配套场所，为 1.5 万名赛事组织与运输保障人员及 500 名医疗急救人员提供专项指挥调度，实现集群对讲、视频会商、人员/车辆定位与移动视频回传一体化。',
    [('1.5万', '保障人员'), ('13', '比赛场馆'), ('500+', '医疗急救')]
))
cases.append(case(
    '#FFF3E0,#FFE0B2', 'anquan.png', '安全生产', 'tag--warn', '🏗️ 安全生产',
    'AI 智慧家装 · 工地管理平台',
    '面向 10000+ 同时施工的家庭装修工地，通过 AI 摄像机实现远程监理、人员考勤、智慧监管与业主服务，施工计划、工地文明与工人考勤全程数字化。',
    [('10000+', '家装工地'), ('AI', '远程监理'), ('5 大', '业务模块')]
))
cases.append(case(
    '#E8F5E9,#C8E6C9', 'zhifa.png', '安全监管', 'tag--green', '🛡️ 安全监管',
    '室外施工 · 安全生产远程审核',
    '落实新版《安全生产法》，为集团工程部建设安全施工远程审核与监管系统，实现远程审核、审核模版、施工过程监管与记录查询全流程数字化。',
    [('全流程', '远程审核'), ('100%', '记录存档'), ('AI', '自动告警')]
))
cases.append(case(
    '#E0F7FA,#B2EBF2', '5g.png', '5G集群', 'tag--cyan', '📶 5G集群',
    '5G 集群调度通信系统',
    '基于 5G 核心网 UPF 下沉与 MEC 技术，替代传统 800M/TETRA 数字集群，实现集群对讲、音视频多媒体调度、GIS 可视化调度与 AR 增强现实应用。',
    [('5G', '核心网'), ('4 大', '业务能力'), ('1Gbps+', '峰值速率')]
))
cases.append(case(
    '#F3E5F5,#E1BEE7', 'yanglao.png', '智慧养老', 'tag--blue', '👴 智慧养老',
    '社会养老 · 即时调度系统',
    '为居家老人提供一键呼叫、例行广播提醒与个性化关怀，调度社区服务站与志愿者上门服务，并通过智能手表实时监测心率、血压、血氧，向家属推送健康信息。',
    [('一键', '呼叫求助'), ('7×24', '值班调度'), ('实时', '健康监测')]
))
cases.append(case(
    '#EDE7F6,#D1C4E9', 'anfang.png', '城市治理', 'tag--cyan', '🏙️ 城市治理',
    '智慧城市 · 网格化基层治理',
    '为区政府网格化基层治理提供移动信息化工具，支撑 7000 名网格员视频会议与即时通信，2 万个城市监控摄像头实时入会，实现"一事一群、事毕群闭"。',
    [('7000', '网格员'), ('2万+', '监控接入'), ('一事一群', '事件处置')]
))

new_grid = CASES_GRID_START + '\n' + '\n'.join(cases) + '\n    </div>'
prod = prod[:start] + new_grid + prod[end:]
with open(PROD, 'w', encoding='utf-8') as f:
    f.write(prod)
print(f'products.html: 案例 4 -> 6 ✅')

# ══════════════════════════════════════════════════════════════
# 2) index.html hero 轮播
# ══════════════════════════════════════════════════════════════
IDX = os.path.join(SITE, 'index.html')
with open(IDX, encoding='utf-8') as f:
    idx = f.read()

HERO_CSS = '''/* ── HERO SLIDER ── */
.hero {
  position: relative;
  height: clamp(460px, 74vh, 640px);
  min-height: 480px;
  overflow: hidden;
  padding: 0;
  background: #0D3B7A;
}
.hero__slide {
  position: absolute; inset: 0;
  background-size: cover;
  background-position: center;
  opacity: 0;
  transition: opacity 1.1s ease;
  z-index: 0;
}
.hero__slide.active { opacity: 1; }
.hero__scrim {
  position: absolute; inset: 0;
  background: linear-gradient(90deg, rgba(8,36,77,.94) 0%, rgba(13,59,122,.78) 42%, rgba(13,59,122,.28) 100%);
  z-index: 1;
}
.hero__content {
  position: relative; z-index: 2;
  height: 100%;
  display: flex; flex-direction: column; justify-content: center;
  color: #fff;
}
.hero__eyebrow {
  display:inline-flex; align-items:center; gap:7px;
  background:rgba(255,255,255,.12); color:#fff;
  font-size:12px; font-weight:700;
  padding:5px 14px; border-radius:99px;
  border:1px solid rgba(255,255,255,.25);
  margin-bottom:20px; width: fit-content;
}
.hero__dot {
  width:7px;height:7px;border-radius:50%;
  background:var(--c-accent2);
  animation:blink 2s infinite;
}
@keyframes blink{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(1.5)}}
.hero__title {
  font-size:clamp(28px,4vw,50px);
  font-weight:800; line-height:1.2;
  color:#fff; margin-bottom:18px;
  text-shadow: 0 2px 24px rgba(0,0,0,.35);
}
.hero__title em {
  font-style:normal;
  background:linear-gradient(90deg, #4FC3F7, #00E5FF);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
}
.hero__desc {
  font-size:16px; color:rgba(255,255,255,.85);
  line-height:1.85; margin-bottom:36px;
  max-width:520px;
  text-shadow: 0 1px 12px rgba(0,0,0,.3);
}
.hero__btns { display:flex; gap:14px; flex-wrap:wrap; }
.hero__btns .btn--outline {
  background:rgba(255,255,255,.08);
  color:#fff;
  border:1.5px solid rgba(255,255,255,.4);
}
.hero__btns .btn--outline:hover { background:rgba(255,255,255,.18); }
.hero__dots {
  position:absolute; bottom:26px; left:50%; transform:translateX(-50%);
  z-index:3; display:flex; gap:9px;
}
.hero__dot-btn {
  width:10px; height:10px; border-radius:99px;
  background:rgba(255,255,255,.35); border:none; cursor:pointer;
  transition:all var(--transition); padding:0;
}
.hero__dot-btn.active { width:30px; background:#fff; }
.hero__arrow {
  position:absolute; top:50%; transform:translateY(-50%);
  z-index:3; width:46px; height:46px; border-radius:50%;
  background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.3);
  color:#fff; font-size:24px; cursor:pointer; line-height:1;
  display:flex; align-items:center; justify-content:center;
  transition:all var(--transition);
}
.hero__arrow:hover { background:rgba(255,255,255,.3); }
.hero__arrow--prev { left:22px; }
.hero__arrow--next { right:22px; }

'''

HERO_HTML = '''<!-- HERO -->
<section class="hero" id="heroSlider">
  <div class="hero__slide active" style="background-image:url('img/hero/hero-1-tech.png');"></div>
  <div class="hero__slide" style="background-image:url('img/hero/hero-3-port.png');"></div>
  <div class="hero__slide" style="background-image:url('img/hero/hero-4-command.png');"></div>
  <div class="hero__scrim"></div>
  <div class="container hero__content">
    <div class="hero__eyebrow"><span class="hero__dot"></span>5G · AIoT · 云计算 · SaaS</div>
    <h1 class="hero__title">面向未来的<br><em>融合通信</em><br>调度平台</h1>
    <p class="hero__desc">汇特讯依托 5G/4G 宽带无线网络，整合多媒体指挥调度、视觉 AI 识别、高精定位等核心技术，为政企行业提供一体化数智融合通信解决方案。</p>
    <div class="hero__btns">
      <a href="5g-cluster.html" class="btn btn--primary btn--lg">
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
        了解5G集群
      </a>
      <a href="products.html" class="btn btn--outline btn--lg">查看产品方案</a>
    </div>
  </div>
  <button class="hero__arrow hero__arrow--prev" onclick="heroPrev()" aria-label="上一张">‹</button>
  <button class="hero__arrow hero__arrow--next" onclick="heroNext()" aria-label="下一张">›</button>
  <div class="hero__dots" id="heroDots"></div>
</section>

'''

# 替换 CSS
css_start = idx.index('/* ── HERO ── */')
css_end = idx.index('/* ── MODULES GRID ── */')
idx = idx[:css_start] + HERO_CSS + idx[css_end:]

# 替换 HTML
html_start = idx.index('<!-- HERO -->')
html_end = idx.index('<!-- STATS -->')
idx = idx[:html_start] + HERO_HTML + idx[html_end:]

# 更新 responsive 块（去掉 .hero__inner / .hero__visual 引用）
old_resp = '''@media(max-width:900px){
  .hero__inner,.modules__grid{grid-template-columns:1fr;}
  .hero__visual{display:none;}
  .stats-bar__grid{grid-template-columns:repeat(2,1fr);}
}'''
new_resp = '''@media(max-width:900px){
  .modules__grid{grid-template-columns:1fr;}
  .hero{height:480px;}
  .hero__scrim{background:linear-gradient(90deg,rgba(8,36,77,.96) 0%,rgba(13,59,122,.88) 100%);}
  .hero__arrow{display:none;}
  .stats-bar__grid{grid-template-columns:repeat(2,1fr);}
}'''
if old_resp in idx:
    idx = idx.replace(old_resp, new_resp)
else:
    print('[WARN] responsive block 未匹配')

# 追加轮播 JS 到 script
SLIDER_JS = '''
// hero slider
const heroSlides = document.querySelectorAll('.hero__slide');
const heroDots = document.getElementById('heroDots');
let heroIdx = 0, heroTimer = null;
if (heroSlides.length && heroDots) {
  heroSlides.forEach((_, i) => {
    const b = document.createElement('button');
    b.className = 'hero__dot-btn' + (i === 0 ? ' active' : '');
    b.onclick = () => heroGo(i);
    heroDots.appendChild(b);
  });
  function heroGo(i) {
    heroSlides[heroIdx].classList.remove('active');
    heroDots.children[heroIdx].classList.remove('active');
    heroIdx = (i + heroSlides.length) % heroSlides.length;
    heroSlides[heroIdx].classList.add('active');
    heroDots.children[heroIdx].classList.add('active');
    heroRestart();
  }
  window.heroNext = () => heroGo(heroIdx + 1);
  window.heroPrev = () => heroGo(heroIdx - 1);
  function heroRestart() { clearInterval(heroTimer); heroTimer = setInterval(() => heroGo(heroIdx + 1), 6000); }
  heroRestart();
}
'''
# 插入到 script 末尾
script_marker = 'document.addEventListener(\'click\',()=>{document.querySelectorAll(\'.nav__links > li.dropdown-open\').forEach(el=>el.classList.remove(\'dropdown-open\'));});'
if script_marker in idx:
    idx = idx.replace(script_marker, script_marker + SLIDER_JS)
else:
    print('[WARN] script marker 未匹配')

with open(IDX, 'w', encoding='utf-8') as f:
    f.write(idx)
print('index.html: hero 轮播 ✅')

print('\n完成 ✅')
