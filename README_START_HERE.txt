BEAUTYWITHIN AESTHETICS — WEBSITE UPDATE KIT
Prepared 23 November 2026 for https://aestheticsnearme.co.uk
Website repository: https://github.com/chrisburley01/Beautywithinsalon

WHAT IS INCLUDED
  privacy.html                 New privacy notice — review the business details before publication.
  apply_beautywithin_update.py Updates existing files without redesigning the site.
  base_audit_fixes.py         
Preserves original audit's SEO, small mobile and accessibility fixes.

CHANGES
1) Add women's scalp micropigmentation (SMP) specifically for female pattern hair loss, without hair regrowth claims.
2) Add non-prescription facial care / facial massage / fine-lines options; no invented prices.
3) Remove 1/2/3-area pricing, POM-related wording and potentially Botox-linked before/after gallery card.
   Original before2.jpg and after2.jpg files remain in the repository; they are not deleted.
4) Update linked FAQ, blog and JSON-LD to the same wording and add a women’s SMP explanation.
5) Update the outdated Halloween 2025 blog article; preserve original site styling.
6) Add privacy.html, update sitemap to FOUR URLs, link Privacy Policy from blog and FAQ.
7) Apply previously tested canonical, mobile menu, reduced-motion and 
lazy-loading improvements.

IMPORTANT — VERIFY BEFORE PUBLISHING
The privacy page is a thorough working draft, not a certified compliance document. Confirm:
 [ ] The business controller/contact address is correct and clients can make privacy requests by phone.
 [ ] What information Joanne actually collects, where it is stored, and suppliers involved.
 [ ] How she obtains any required explicit consent for special-category health records, 
or the lawful Article 9 condition actually relied upon.
 [ ] How long appointment and treatment records are retained (actual written retention schedule).
 [ ] Whether consultation photos are taken; proof of separate consent for public before/after photographs.
 [ ] No unsupported claims about insurance, medical titles, practitioner qualifications or SMP outcomes.
 [ ] Whether third-party Google Map embedding/cookies needs a consent control under current 
UK PECR rules.
 [ ] Whether the original wrinkle-softening before/after photo actually depicts POM results (the patch hides it by default).
 [ ] Treatment availability — facial massage and women-only SMP have been explicitly requested by the site owner; confirm they are presently delivered/insured.

ASA/CAP advice for prescription-only medicines:
 https://www.asa.org.uk/advice-online/health-prescription-only
-medicines-websites.html
 https://www.asa.org.uk/advice-online/beauty-and-cosmetics-botulinum-toxin-products.html
ICO advice on special-category data and notices:
 https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/special-category-data/

GITHUB PUBLISHING (ON A PC OR MAC)
1) Visit https://github.com/chrisburley01/Beautywithinsalon and select Code > Download ZIP.
2) Extract the repository. Keep ALL its existing images and HTML files.
3) Copy the three files in this update kit into the extracted repository folder.
4) Open a terminal inside that folder and run:
     python3 apply_beautywithin_update.py --dry-run
   You should see five files listed for change.
5) After reviewing the compliance checklist, run:
     python3 apply_beautywithin_update.py
   It creates .bak copies for existing HTML/XML files.
6) Upload the updated index.html, blog.html, faq.html and sitemap.xml and new privacy.html
   using GitHub's Add file > Upload files (or via a Git client). Upload only these FIVE files.
   Avoid uploading the backup files or scripts to the live site.
7) Wait for GitHub Pages deployment and verify the site. Submit sitemap.xml in Search Console.

STATUS
GitHub integration allowed READ, but branch creation returned 403 (Resource not accessible by integration).
No repository or live website files have been changed by this kit.