from pathlib import Path
from PIL import Image
from bs4 import BeautifulSoup
import re, csv, zipfile
root=Path('/mnt/data/serum_refresh'); assets=root/'assets'
im=Image.open('/mnt/data/a_clean_bright_high_resolution_collage_advertisi.png').convert('RGB')
im.crop((22,553,520,877)).save(assets/'hon_texture_illustration.webp',quality=88)
# Three separate motifs, without bottles or implied actual product texture
specs=[('shiny','F8F3DE','E7EFDA','D5BC74','花と光','<g fill="#d5c78f" opacity=".6"><circle cx="590" cy="125" r="7"/><circle cx="630" cy="115" r="6"/><circle cx="560" cy="150" r="4"/></g><g transform="translate(520 225)" fill="#fffaf0" stroke="#d9c997" stroke-width="2"><ellipse rx="26" ry="75" transform="rotate(0)"/><ellipse rx="26" ry="75" transform="rotate(60)"/><ellipse rx="26" ry="75" transform="rotate(120)"/><circle r="13" fill="#f1d68b"/></g>'),('rempli','E9F5F3','DCECF9','8EB7B3','水のゆらぎ','<g fill="none" stroke="#ffffff" stroke-width="5" opacity=".85"><circle cx="565" cy="180" r="93"/><circle cx="565" cy="180" r="65"/><circle cx="565" cy="180" r="36"/></g><path d="M355 310 Q480 270 640 335 T880 330" stroke="#b8d8dd" stroke-width="13" fill="none" opacity=".5"/>'),('hon','FFF2E8','F8E8E1','D8B7A0','やわらかな光','<g fill="none" stroke="#d6b39c" stroke-width="3" opacity=".6"><ellipse cx="620" cy="170" rx="104" ry="104"/><ellipse cx="620" cy="170" rx="135" ry="135"/></g><g fill="#fff" opacity=".8"><circle cx="540" cy="115" r="10"/><circle cx="700" cy="190" r="13"/><circle cx="590" cy="275" r="5"/></g>')]
for name,a,b,c,label,motif in specs:
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 540"><defs><linearGradient id="g" x2="1" y2="1"><stop stop-color="#{a}"/><stop offset="1" stop-color="#{b}"/></linearGradient><radialGradient id="light"><stop stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs><rect width="900" height="540" fill="url(#g)"/><circle cx="690" cy="100" r="260" fill="url(#light)"/><g fill="none" stroke="#{c}" stroke-width="5" stroke-linecap="round" opacity=".6"><path d="M75 550 Q240 330 270 85"/><path d="M173 398 Q85 340 90 280 Q175 272 205 346"/><path d="M207 315 Q295 265 312 199 Q224 209 207 315"/><path d="M247 178 Q177 138 184 80 Q262 101 247 178"/></g>{motif}<path d="M0 470 Q200 400 400 478 T900 435 L900 540 L0 540Z" fill="#fff" opacity=".36"/></svg>'''
 (assets/f'{name}_editorial_background.svg').write_text(svg)
html=(root/'index.html').read_text()
soup=BeautifulSoup(html,'html.parser')
for section_id,name in [('shiny','shiny'),('rempli','rempli'),('horn','hon')]:
 section=soup.find(id=section_id)
 section['class']=list(set(section.get('class',[])+['art-directed',f'art-directed-{name}']))
 photo=section.select_one('.photo')
 art=soup.new_tag('img',attrs={'class':'editorial-backdrop','src':f'assets/{name}_editorial_background.svg','alt':'','aria-hidden':'true','loading':'lazy'})
 photo.insert(0,art)
 badge=soup.new_tag('span',attrs={'class':'art-note'})
 badge.string={'shiny':'BOTANICAL LIGHT','rempli':'AQUA & MOISTURE','hon':'GENTLE FOCUS'}[name]
 photo.append(badge)
texture=soup.select_one('.texture-illustrated')
drop=texture.select_one('.drop-composition')
new=soup.new_tag('img',attrs={'src':'assets/hon_texture_illustration.webp','loading':'lazy','alt':'無色透明の美容液をイメージした生成画像。ホニオールⅡの実物撮影ではありません。','class':'hon-texture-generated'})
drop.replace_with(new)
texture.select_one('figcaption span').string='無色透明の液をイメージした生成画像です。実際の粘度・使用感を示す実物写真ではありません。'
section=soup.find(id='texture');section.select_one('.section-head p',recursive=False) if False else None
p=section.select_one('.section-head p:not(.num)')
if p: p.string='実物写真2点と、ホニオールⅡの透明液を表現した生成イメージでご紹介。'
(root/'index.html').write_text(str(soup),encoding='utf-8')
css='''\n/* 2026-10-29 individual art direction */\n.art-directed .photo {position:relative;isolation:isolate;overflow:hidden;min-height:430px;background:#f8f6f0;}\n.art-directed .photo .editorial-backdrop {position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-1;opacity:1;}\n.art-directed .photo > img:not(.editorial-backdrop) {position:relative;z-index:1;object-fit:contain;max-width:70%;max-height:350px;filter:drop-shadow(0 18px 14px rgba(55,40,20,.12));}\n.art-directed-hon .photo > img:not(.editorial-backdrop) {max-height:235px;max-width:55%;}\n.art-directed .photo-label{z-index:2;}\n.art-note{position:absolute;top:17px;left:22px;font-size:11px;letter-spacing:.22em;color:#725f50;font-weight:600;z-index:2;}\n.hon-texture-generated{display:block;width:100%;height:270px;object-fit:cover;object-position:center 38%;border-radius:16px;}\n@media(max-width:700px){.art-directed .photo{min-height:340px}.art-directed .photo > img:not(.editorial-backdrop){max-height:245px}.art-directed-hon .photo > img:not(.editorial-backdrop){max-height:165px}.hon-texture-generated{height:230px}}\n'''
with (root/'style.css').open('a') as f:f.write(css)
(root/'README_追加画像と確認事項.txt').write_text('''今回の更新：商品別に独立した背景アートSVG×3を制作・組込。ホニオールⅡ透明液イメージを生成し、容器を含まない部分だけを切り出し掲載。\n重要：ホニオールⅡの液画像は生成イメージであり、実物写真・実際の粘性や使用感の証拠ではありません。社内で実物と照合し問題なければ使用を承認してください。\nホニオールⅡは10mL・スポイト式ではありません。シャイニーブラン／リンプルは30mLです。既存商品の写真は公式URLを外部参照しています。\n外部画像の可用性、GitHub Pagesでの実表示・スマートフォン実機検証、薬事表現・最新価格の確認は未完了です。\n''')
with (root/'image_and_link_map.csv').open('a') as f:
 for n in ['shiny','rempli','hon']: f.write(f'\nassets/{n}_editorial_background.svg,独立生成SVG背景,商品容器は描写しない装飾素材')
 f.write('\nassets/hon_texture_illustration.webp,ホニオールⅡ透明液イメージ,生成画像・実物写真ではない')
with zipfile.ZipFile('/mnt/data/EPORASHE_美容液LP_独立背景_ホニオール透明液_更新版.zip','w',zipfile.ZIP_DEFLATED) as z:
 for file in root.rglob('*'):
  if file.is_file() and file.name not in ['patch.py','hon_texture_preview.png']:
   z.write(file,file.relative_to(root))
print('done')
