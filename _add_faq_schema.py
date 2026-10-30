#!/usr/bin/env python3
"""Add FAQPage JSON-LD to all blog posts in comprimefotos."""
import re
import json
import os
from pathlib import Path

BLOG_DIR = Path(r"E:\网站项目\comprimefotos\blog")

def extract_faq(html_content):
    """Extract FAQ questions and answers from HTML."""
    # Match faq-item divs
    pattern = r'<div class="faq-item">\s*<button class="faq-question">(.*?)</button>\s*<div class="faq-answer">\s*<p>(.*?)</p>\s*</div>\s*</div>'
    matches = re.findall(pattern, html_content, re.DOTALL)
    
    faqs = []
    for q, a in matches:
        # Strip HTML tags from question and answer
        q_clean = re.sub(r'<[^>]+>', '', q).strip()
        a_clean = re.sub(r'<[^>]+>', '', a).strip()
        # Decode HTML entities
        q_clean = q_clean.replace('&aacute;', 'á').replace('&eacute;', 'é').replace('&iacute;', 'í').replace('&oacute;', 'ó').replace('&uacute;', 'ú').replace('&ntilde;', 'ñ').replace('&Aacute;', 'Á').replace('&Eacute;', 'É').replace('&Iacute;', 'Í').replace('&Oacute;', 'Ó').replace('&Uacute;', 'Ú').replace('&Ntilde;', 'Ñ').replace('&iquest;', '¿').replace('&iexcl;', '¡').replace('&amp;', '&').replace('&quot;', '"')
        a_clean = a_clean.replace('&aacute;', 'á').replace('&eacute;', 'é').replace('&iacute;', 'í').replace('&oacute;', 'ó').replace('&uacute;', 'ú').replace('&ntilde;', 'ñ').replace('&Aacute;', 'Á').replace('&Eacute;', 'É').replace('&Iacute;', 'Í').replace('&Oacute;', 'Ó').replace('&Uacute;', 'Ú').replace('&Ntilde;', 'Ñ').replace('&iquest;', '¿').replace('&iexcl;', '¡').replace('&amp;', '&').replace('&quot;', '"')
        faqs.append({"question": q_clean, "answer": a_clean})
    return faqs

def make_faq_jsonld(faqs, page_url):
    """Generate FAQPage JSON-LD."""
    main_entity = []
    for faq in faqs:
        main_entity.append({
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"]
            }
        })
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main_entity
    }

def process_blog(html_file):
    """Process a single blog file."""
    content = html_file.read_text(encoding='utf-8')
    
    # Skip if already has FAQPage
    if '"@type": "FAQPage"' in content:
        print(f"  SKIP (already has FAQPage): {html_file.name}")
        return False
    
    # Extract FAQ
    faqs = extract_faq(content)
    if not faqs:
        print(f"  NO FAQ FOUND: {html_file.name}")
        return False
    
    # Build page URL
    slug = html_file.stem
    page_url = f"https://comprimefotos.com/blog/{slug}"
    
    # Generate JSON-LD
    faq_jsonld = make_faq_jsonld(faqs, page_url)
    json_ld_script = f'\n<script type="application/ld+json">\n{json.dumps(faq_jsonld, ensure_ascii=False, indent=2)}\n</script>\n'
    
    # Insert before </head>
    content = content.replace('</head>', json_ld_script + '</head>')
    
    # Write back
    html_file.write_text(content, encoding='utf-8')
    print(f"  OK ({len(faqs)} FAQs): {html_file.name}")
    return True

# Main
print("=" * 60)
print("Adding FAQPage JSON-LD to comprimefotos blogs")
print("=" * 60)

blog_files = list(BLOG_DIR.glob("*.html"))
blog_files = [f for f in blog_files if f.name != "index.html"]

success = 0
for bf in blog_files:
    print(f"\nProcessing: {bf.name}")
    if process_blog(bf):
        success += 1

print(f"\n{'=' * 60}")
print(f"Done: {success}/{len(blog_files)} blogs updated")
