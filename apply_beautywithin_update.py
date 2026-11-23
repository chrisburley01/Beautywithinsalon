#!/usr/bin/env python3
"""Prepare compliant website HTML, women's SMP and a privacy notice, preserving design.

Run in the extracted GitHub repository folder with base_audit_fixes.py and privacy.html
beside this script. Dry run first. A .bak backup is made for modified files.
"""
from pathlib import Path
import json
import re
import sys
from xml.etree import ElementTree as ET

# Read-only importer of the previous SEO/accessibility audit fixes.
import base_audit_fixes

ROOT=Path.cwd()
PACK=Path(__file__).resolve().parent
DRY='--dry-run' in sys.argv


def one(s, old, new, label):
    if s.count(old)!=1:
        raise ValueError(f'{label}: expected one occurrence, found {s.count(old)}. Nothing written.')
    return s.replace(old,new)


def article(s, headline, html):
    pattern = r'<article class="card">\s*<h2>' + re.escape(headline) + r'</h2>.*?</article>'
    result,count = re.subn(pattern,lambda m:html,s,flags=re.S)
    if count!=1:
        raise ValueError(f'Blog post {headline}: found {count} entries, expected one')
    return result


def update_schema(page, transform):
    count=0
    def change(match):
        nonlocal count
        try: data=json.loads(match.group(1))
        except (ValueError,TypeError): return match.group(0)
        replacement=transform(data)
        if replacement is None:return match.group(0)
        count+=1
        return '<script type="application/ld+json">\n'+json.dumps(replacement,ensure_ascii=False,indent=2)+'\n</script>'
    page=re.sub(r'<script type="application/ld\+json">\s*(.*?)\s*</script>',change,page,flags=re.S)
    return page,count


def generate():
    for name in ('index.html','blog.html','faq.html','sitemap.xml'):
        if not (ROOT/name).is_file():
            raise FileNotFoundError(f'Cannot find {name}; run inside the extracted Beautywithinsalon repository folder')
    for name in ('base_audit_fixes.py','privacy.html'):
        if not (PACK/name).is_file():
            raise FileNotFoundError(f'Missing kit file: {name}')
    # Earlier tested base fixes are computed without changing any local files.
    base_audit_fixes.ROOT=ROOT
    stage=base_audit_fixes.generate()
    idx, faq, sm = stage['index.html'],stage['faq.html'],stage['sitemap.xml']
    blog=(ROOT/'blog.html').read_text(encoding='utf-8')

    # Keep design, logo, navigation, existing non-POM price cards and contact details.
    idx=one(idx,'<title>Beautywithin Aesthetics Woodkirk | Wrinkle Softening, Fillers & Skin Boosters Near Leeds</title>',
        '<title>Beautywithin Aesthetics Woodkirk | Skin Treatments, Facials & Women’s SMP</title>','Homepage title')
    idx=one(idx,
        'Beautywithin Aesthetics by Joanne Burley — aesthetics in Woodkirk (WF12) serving Leeds, Dewsbury & Wakefield. Wrinkle softening from £200, fillers, and skin boosters. Call 07714 201913.',
        'Beautywithin Aesthetics in Woodkirk (WF12) offers skin boosters, dermal fillers, facial care and women’s SMP for female pattern hair loss. Book a consultation with Joanne.','Homepage meta description')
    idx=one(idx,'Aesthetics in Woodkirk (WF12) serving Leeds & Dewsbury — wrinkle softening, fillers & skin boosters. Call 07714 201913.',
        'Skin boosters, facials, dermal fillers and women’s SMP. Contact Joanne.','Social description')
    idx=one(idx,'Wrinkle softening, fillers & skin boosters in Woodkirk (WF12). Serving Leeds & Dewsbury.',
        'Skin care, fillers, facials and women’s SMP in Woodkirk (WF12). Serving Leeds & Dewsbury.',
        'Social Twitter description')
    idx=one(idx,
        '<article class="card"><h3>Wrinkle Softening</h3><p class="muted">Gentle softening of lines while keeping natural movement and expression.</p></article>',
        '<article class="card"><h3>Fine Lines &amp; Facial Care</h3><p class="muted">Explore non-prescription options for skin texture and fine lines, including facial massage, facials and tailored skin care. Results vary by treatment.</p></article>',
        'Treatments: fine lines')
    idx=one(idx,
        '<article class="card"><h3>Consultations</h3><p class="muted">Friendly, no-obligation chats to plan your journey and answer questions.</p></article>',
        '<article class="card"><h3>Women’s Scalp Micropigmentation (SMP)</h3><p class="muted">Specialist cosmetic scalp pigmentation for women experiencing female pattern hair loss (female pattern baldness). Creates the appearance of fuller-looking hair; it does not stimulate new hair growth. Suitability is assessed in consultation.</p></article>\n    <article class="card"><h3>Consultations</h3><p class="muted">Friendly, no-obligation chats to plan your journey and answer questions.</p></article>',
        'Treatments: womens SMP')
    idx=one(idx,
        '''    <article class="card">
      <h3>Wrinkle Softening</h3>
      <ul class="small"><li>1 area — <strong>from £200</strong></li><li>2 areas — <strong>from £240</strong></li><li>3 areas — <strong>from £280</strong></li></ul>
    </article>''',
        '''    <article class="card">
      <h3>Facial Care &amp; Fine Lines</h3>
      <ul class="small"><li>Facials, massage and other non-prescription skin-care options</li><li><strong>Price confirmed during consultation</strong></li></ul>
    </article>''',
        'Remove area-priced POM promotion')
    idx=one(idx,
        '''    <article class="card">
      <h3>Consultation</h3>
      <ul class="small"><li>New client consult — <strong>£0</strong> (redeemable)</li><li>Review & top-up — <strong>as advised</strong></li></ul>
    </article>''',
        '''    <article class="card">
      <h3>Women’s SMP — Female Pattern Hair Loss</h3>
      <ul class="small"><li>Cosmetic scalp-density enhancement for women</li><li><strong>Personal quote following consultation</strong></li></ul>
    </article>
    <article class="card">
      <h3>Consultation</h3>
      <ul class="small"><li>New client consult — <strong>£0</strong> (redeemable)</li><li>Review &amp; follow-up — <strong>as advised</strong></li></ul>
    </article>''',
        'SMP price and existing consultation')
    # Remove a gallery pair which may depict a POM result. Keep assets in repository.
    idx=one(idx,
        '''    <div class="ba"><div class="ba-head">Wrinkle Softening</div><div class="ba-body"><div class="ba-half"><img src="before2.jpg" loading="lazy" decoding="async" alt="Before wrinkle softening"></div><div class="ba-half"><img src="after2.jpg" loading="lazy" decoding="async" alt="After wrinkle softening"></div></div><div class="ba-foot">Softer lines, natural movement maintained.</div></div>''',
        '', 'Remove potentially POM-related before-after pair')
    idx=one(idx,'<a class="cta-btn glow" href="#contact">Book a consult</a>',
        '<a class="cta-btn glow" href="#contact">Book a consultation</a>', 'Consultation CTA')
    idx=one(idx,
        '<a href="/privacy.html">Privacy Policy</a> · <a href="/blog.html">Blog</a> · <a href="/faq.html">FAQ</a>',
        '<a href="/privacy.html">Privacy Policy</a> · <a href="/blog.html">Blog</a> · <a href="/faq.html">FAQ</a>',
        'Existing privacy link') if False else idx

    def homepage_json(data):
        if data.get('@type')=='MedicalBusiness':
            # BeautySalon avoids claiming a regulated medical status not established by source.
            data['@type']='BeautySalon'
            # Remove unverified hours and potentially approximate coordinate data.
            data.pop('openingHoursSpecification',None)
            data.pop('geo',None)
            return data
        if data.get('@type')=='ItemList':
            data['itemListElement']=[
                {'@type':'Service','name':'Facial Care & Fine Lines','description':'Facials, facial massage and non-prescription skin care to support cosmetic skin appearance.'},
                {'@type':'Service','name':'Dermal Fillers','description':'Cosmetic volume and contour options, subject to consultation.'},
                {'@type':'Service','name':'Skin Boosters','description':'Consultation-led skin booster options.'},
                {'@type':'Service','name':'Skin Health','description':'Microneedling, peels and facials.'},
                {'@type':'Service','name':'Women’s Scalp Micropigmentation','description':'Cosmetic scalp micropigmentation specifically for women with female pattern hair loss; does not regrow hair.'}
            ]
            return data
        if data.get('@type')=='FAQPage':
            data['mainEntity']=[
                {'@type':'Question','name':'Which treatments can help the appearance of fine lines?','acceptedAnswer':{'@type':'Answer','text':'Facials, massage and skin-care options may help improve the appearance of skin, depending on suitability. Joanne can explain non-prescription options at a consultation.'}},
                {'@type':'Question','name':'Do you offer consultations?','acceptedAnswer':{'@type':'Answer','text':'Yes — friendly, no-obligation consultations to discuss options.'}},
                {'@type':'Question','name':'Is SMP available for women with female pattern hair loss?','acceptedAnswer':{'@type':'Answer','text':'Yes. SMP is a cosmetic scalp pigmentation service for women with female pattern hair loss. It creates the look of greater hair density rather than regrowing hair.'}}
            ]
            return data
        return None
    idx,num=update_schema(idx,homepage_json)
    if num!=3:raise ValueError(f'Expected 3 homepage schema updates, found {num}')

    # FAQ: readable and marked-up answers must agree.
    faq=one(faq,
        '''  <details open>
    <summary>How much does wrinkle softening cost?</summary>
    <p>Wrinkle softening starts from £200 depending on area and consultation. We’ll assess suitability and tailor a plan during your visit.</p>
  </details>''',
        '''  <details open>
    <summary>What can help the appearance of fine lines?</summary>
    <p>Depending on your skin, facial massage, facials, skin care and other non-prescription options may help improve the skin’s appearance. Joanne can discuss realistic options and pricing at a consultation.</p>
  </details>''','FAQ fine lines')
    faq=one(faq,
        '''  <details>
    <summary>How long do dermal fillers and wrinkle softening last?</summary>
    <p>Wrinkle softening typically lasts 3–4 months. Dermal fillers usually last 6–12 months depending on the product and area treated.</p>
  </details>''',
        '''  <details>
    <summary>How long do dermal fillers last?</summary>
    <p>Results vary by product, treatment area and individual circumstances. Joanne can explain expected longevity, aftercare and potential risks at your consultation.</p>
  </details>''','FAQ dermal fillers')
    faq=one(faq,
        '''  <details>
    <summary>Do you treat men?</summary>
    <p>Yes. Treatments are personalised for all clients.</p>
  </details>''',
        '''  <details>
    <summary>Do you treat men?</summary>
    <p>Yes, other aesthetic and skin-care treatments are available to clients of all genders. The scalp micropigmentation service listed here is specifically for women experiencing female pattern hair loss.</p>
  </details>

  <details>
    <summary>What is SMP for female pattern hair loss?</summary>
    <p>Scalp micropigmentation (SMP) uses cosmetic pigmentation to make thinning scalp areas appear denser. It is a visual cosmetic treatment, not a treatment that stops hair loss or grows new hair. Joanne offers this service for women with female pattern hair loss only, subject to consultation.</p>
  </details>''','FAQ SMP')
    def faq_json(data):
        if data.get('@type')!='FAQPage':return None
        data['mainEntity']=[
            {'@type':'Question','name':'What can help the appearance of fine lines?','acceptedAnswer':{'@type':'Answer','text':'Facials, facial massage and other non-prescription skin care may help improve skin appearance depending on individual suitability.'}},
            {'@type':'Question','name':'How long do dermal fillers last?','acceptedAnswer':{'@type':'Answer','text':'Duration varies depending on product, treatment area and individual circumstances; a consultation covers expected outcomes and risks.'}},
            {'@type':'Question','name':'What are skin boosters and who are they for?','acceptedAnswer':{'@type':'Answer','text':'Skin booster suitability is assessed during a consultation based on individual skin needs.'}},
            {'@type':'Question','name':'Do you treat men?','acceptedAnswer':{'@type':'Answer','text':'Other aesthetic and skin-care services may be available to all genders; women’s SMP is specifically for female pattern hair loss.'}},
            {'@type':'Question','name':'What is SMP for female pattern hair loss?','acceptedAnswer':{'@type':'Answer','text':'Women’s SMP uses cosmetic scalp pigmentation to make thinning areas look denser; it does not regrow hair.'}},
            {'@type':'Question','name':'Where are you based?','acceptedAnswer':{'@type':'Answer','text':'We are based in Woodkirk (WF12), near Leeds, Dewsbury and Wakefield.'}}
        ]
        return data
    faq,n=update_schema(faq,faq_json)
    if n!=1:raise ValueError(f'Expected FAQ schema change once, got {n}')
    faq=one(faq,'· <a href="/blog.html">Blog</a></p>',
               '· <a href="/blog.html">Blog</a> · <a href="/privacy.html">Privacy Policy</a></p>','FAQ privacy footer')

    blog=article(blog,'Don’t Be Scared of Your Skin This Halloween!',
        '''<article class="card">
      <h2>Comfortable Skin Through the Colder Months</h2>
      <p>Cool weather and indoor heating can leave skin feeling dry. Consistent, gentle routines are often more useful than chasing quick fixes.</p>
      <ul class="small"><li><strong>Hydration:</strong> Choose a moisturiser that suits your skin.</li><li><strong>Daily sun protection:</strong> Consider appropriate SPF throughout the year.</li><li><strong>Facial care:</strong> Ask Joanne about suitable non-prescription facial and skin-care options.</li></ul>
      <p><a href="/#contact">Book a consultation</a> to discuss a suitable plan.</p>
    </article>''')
    blog=article(blog,'Top Skin Boosters for Autumn Radiance (2025)',
        '''<article class="card">
      <h2>Skin Boosters: Questions to Ask Before Treatment</h2>
      <p>There are different cosmetic skin treatments marketed as skin boosters. Suitability, ingredients, contraindications, aftercare and results should be discussed before booking.</p>
      <ul class="small"><li>Ask what product is proposed and why.</li><li>Discuss risks, expected results and the number of visits.</li><li>Understand alternative options, including non-injectable skin care.</li></ul>
      <p><a href="/#contact">Talk to Joanne</a> about your individual skin-care goals.</p>
    </article>''')
    blog=article(blog,'Wrinkle Softening vs Fillers — What’s Right for Me?',
        '''<article class="card">
      <h2>Facial Care and Dermal Fillers: Different Options</h2>
      <p>Facial massage and skin-care treatments can support comfort and the skin’s appearance. Dermal fillers are a different cosmetic procedure used to change the appearance of volume or contour. They have different benefits, costs and risks.</p>
      <p>A consultation is the right place to discuss expectations and find out whether any treatment is suitable.</p>
      <p><a href="/#contact">Ask Joanne about a consultation</a>.</p>
    </article>''')
    # Add an SMP article with carefully limited cosmetic claims, ahead of old aftercare posts.
    blog=one(blog,'      <h2>Aftercare Tips: Make Your Results Last</h2>',
        '''      <h2>Aftercare Tips: Make Your Results Last</h2>''','Aftercare anchor') if False else blog
    anchor='''    <article class="card">
      <h2>Aftercare Tips: Make Your Results Last</h2>'''
    blog=one(blog,anchor,
        '''    <article class="card">
      <h2>Women’s SMP for Female Pattern Hair Loss: What to Know</h2>
      <p>Scalp micropigmentation uses tiny cosmetic pigment deposits to create the appearance of more scalp coverage in thinning areas. Beautywithin offers this service to women experiencing female pattern hair loss only.</p>
      <p>SMP is not a hair-growth treatment and does not stop the cause of thinning. A consultation is needed to discuss suitability, appearance, aftercare and maintenance.</p>
      <p><a href="/#contact">Ask Joanne about women’s SMP</a>.</p>
    </article>

'''+anchor,'Women SMP new blog post')
    def blog_json(data):
        if data.get('@type')!='Blog':return None
        posts=data.get('blogPost',[])
        posts[0]['headline']='Comfortable Skin Through the Colder Months'
        posts[0]['dateModified']='2026-11-23'
        posts[1]['headline']='Skin Boosters: Questions to Ask Before Treatment'
        posts[2]['headline']='Facial Care and Dermal Fillers: Different Options'
        posts.insert(3,{'@type':'BlogPosting','headline':'Women’s SMP for Female Pattern Hair Loss: What to Know','datePublished':'2026-11-23','author':{'@type':'Person','name':'Joanne Burley'}})
        return data
    blog,n=update_schema(blog,blog_json)
    if n!=1:raise ValueError(f'Expected one blog structured data update, found {n}')
    blog=one(blog,'<a href="/faq.html">FAQ</a>','<a href="/faq.html">FAQ</a> · <a href="/privacy.html">Privacy Policy</a>', 'Blog footer')

    # Sitemap includes every real public page; do not invent lastmod dates.
    sm='''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://aestheticsnearme.co.uk/</loc></url>
  <url><loc>https://aestheticsnearme.co.uk/blog.html</loc></url>
  <url><loc>https://aestheticsnearme.co.uk/faq.html</loc></url>
  <url><loc>https://aestheticsnearme.co.uk/privacy.html</loc></url>
</urlset>
'''
    ET.fromstring(sm)
    privacy=(PACK/'privacy.html').read_text(encoding='utf-8')
    privacy=privacy.replace('When you choose to load the location map or open an external link,',
                            'When the embedded location map loads or you open an external link,')

    # Prepublication assertions: verify no leftover potentially POM-specific promotion.
    for name, content in (('index.html',idx),('faq.html',faq),('blog.html',blog)):
        if re.search(r'wrinkle softening|anti.wrinkle injections|botox',content,re.I):
            raise AssertionError(f'{name} still contains POM-associated promotional wording')
        if content.lower().count('<h1')!=1: raise AssertionError(f'{name} should have exactly one H1')
        if '447714201913' not in content and name=='index.html':raise AssertionError('Contact changed unexpectedly')
        if 'female pattern hair loss' not in content.lower():raise AssertionError(f'{name} missing women SMP context')
    for p in (idx,faq,blog,privacy):
        for m in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>',p,re.S):json.loads(m)
    assert '<loc>https://aestheticsnearme.co.uk/privacy.html</loc>' in sm
    return {'index.html':idx,'faq.html':faq,'blog.html':blog,'sitemap.xml':sm,'privacy.html':privacy}


def main():
    changes=generate()
    for name,contents in changes.items():
        path=ROOT/name
        old=path.read_text(encoding='utf-8') if path.exists() else None
        if old==contents:
            print('Already current:',name);continue
        if DRY:
            print('Would '+('create' if old is None else 'update')+':',name);continue
        if old is not None:
            backup=ROOT/(name+'.before-beautywithin-2026.bak')
            if not backup.exists():backup.write_text(old,encoding='utf-8')
        path.write_text(contents,encoding='utf-8')
        print(('Created' if old is None else 'Updated')+':',name)
    print('Ready for a code review. Nothing automatically uploaded to GitHub.')

if __name__=='__main__':main()
