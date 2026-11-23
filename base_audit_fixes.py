#!/usr/bin/env python3
"""Conservative Beautywithin Aesthetics website changes; run in cloned repository root."""
from pathlib import Path
from xml.etree import ElementTree as ET
import re
import sys

ROOT = Path.cwd()
DRY_RUN = '--dry-run' in sys.argv


def replace_once(text, old, new, where):
    if old not in text:
        if new in text:
            return text
        raise ValueError(f'{where}: expected content not found; no changes saved')
    if text.count(old) != 1:
        raise ValueError(f'{where}: expected exactly one match; no changes saved')
    return text.replace(old, new)


def generate():
    for name in ('index.html', 'faq.html', 'sitemap.xml'):
        if not (ROOT / name).is_file():
            raise FileNotFoundError(f'{name} not found. Run inside the Beautywithinsalon repository folder.')

    index = (ROOT / 'index.html').read_text(encoding='utf-8')
    faq = (ROOT / 'faq.html').read_text(encoding='utf-8')

    index = replace_once(index,
        '<h1 class="vh">Aesthetics Clinic in Woodkirk (WF12) – Wrinkle Softening, Dermal Fillers & Skin Treatments near Leeds & Dewsbury</h1>\n',
        '', 'Remove redundant hidden H1')

    index = replace_once(index,
        '@media (max-width: 380px){ .logo-img{ height:36px; } }',
        '@media (max-width: 420px){ .logo-img{height:34px} .logo{gap:6px;font-size:13px} .nav.container{padding-left:14px;padding-right:14px} }\n'
        '     @media (prefers-reduced-motion: reduce){ .glow,.whatsapp-fab.glow{animation:none} }',
        'Small-screen logo and reduced-motion preference')

    index = replace_once(index,
        'id="mobileMenu" class="mobile-menu" role="dialog" aria-modal="true" aria-label="Mobile menu"',
        'id="mobileMenu" class="mobile-menu" role="dialog" aria-modal="true" aria-label="Mobile menu" inert',
        'Prevent keyboard focus in closed mobile menu')

    index = replace_once(index,
        "function closeMenu(){ panel.classList.remove('open'); backdrop.classList.remove('open'); btn.setAttribute('aria-expanded','false'); }",
        "function closeMenu(){ panel.classList.remove('open'); backdrop.classList.remove('open'); panel.inert = true; btn.setAttribute('aria-expanded','false'); btn.setAttribute('aria-label','Open menu'); }",
        'Update closed menu accessibility')

    index = replace_once(index,
        "function toggleMenu(){ const isOpen = panel.classList.toggle('open'); backdrop.classList.toggle('open', isOpen); btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false'); }",
        "function toggleMenu(){ const isOpen = panel.classList.toggle('open'); backdrop.classList.toggle('open', isOpen); panel.inert = !isOpen; btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false'); btn.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu'); }",
        'Update menu open/close accessibility')

    index = re.sub(r'<img src="((?:before|after)[1-4]\.jpg)"(?! loading=)',
                   r'<img src="\1" loading="lazy" decoding="async"', index)
    index = replace_once(index,
        '<img src="joanne.jpg?v=2" alt="Joanne Burley, Beautywithin Aesthetics">',
        '<img src="joanne.jpg?v=2" alt="Joanne Burley, Beautywithin Aesthetics" loading="lazy" decoding="async">',
        'Lazy load below-the-fold practitioner image')

    faq = replace_once(faq,
        '<title>FAQ | Beautywithin Aesthetics Woodkirk</title>',
        '<title>FAQ | Beautywithin Aesthetics Woodkirk</title>\n  <link rel="canonical" href="https://aestheticsnearme.co.uk/faq.html" />',
        'Add FAQ canonical')

    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://aestheticsnearme.co.uk/</loc></url>
  <url><loc>https://aestheticsnearme.co.uk/blog.html</loc></url>
  <url><loc>https://aestheticsnearme.co.uk/faq.html</loc></url>
</urlset>
'''

    ET.fromstring(sitemap)
    assert index.count('<h1') == 1, 'Homepage should contain exactly one H1 after repair'
    assert index.count('loading="lazy" decoding="async"') == 9
    assert 'wa.me/447714201913' in index
    assert 'from £200' in index
    assert 'https://aestheticsnearme.co.uk/faq.html' in faq
    return {'index.html': index, 'faq.html': faq, 'sitemap.xml': sitemap}


def main():
    changes = generate()  # All checks run before any file is changed
    for name, content in changes.items():
        target = ROOT / name
        current = target.read_text(encoding='utf-8')
        if current == content:
            print(f'Already up to date: {name}')
            continue
        if DRY_RUN:
            print(f'Would update: {name}')
            continue
        backup = ROOT / f'{name}.before-audit.bak'
        if not backup.exists():
            backup.write_text(current, encoding='utf-8')
        target.write_text(content, encoding='utf-8')
        print(f'Updated: {name} (backup: {backup.name})')
    print('Done. Review the diff and publish only after approving the changes.')


if __name__ == '__main__':
    main()
