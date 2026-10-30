#!/usr/bin/env python3
"""Add related posts section to all blog posts."""
import re
from pathlib import Path

BLOG_DIR = Path(r"E:\网站项目\comprimefotos\blog")

# Blog metadata: slug -> (title, related_blogs, related_tools)
BLOG_META = {
    "como-comprimir-imagenes-para-whatsapp": {
        "title": "Cómo comprimir imágenes para WhatsApp",
        "related_blogs": [
            ("guia-completa-compresion-imagenes", "Guía completa de compresión de imágenes"),
            ("jpg-vs-png-vs-webp-formatos-imagen", "JPG vs PNG vs WebP: ¿Qué formato usar?"),
        ],
        "related_tools": [
            ("/tools/comprimir-imagenes-whatsapp", "Comprimir imágenes para WhatsApp"),
            ("/tools/comprimir-imagenes", "Comprimir imágenes online"),
        ]
    },
    "guia-completa-compresion-imagenes": {
        "title": "Guía completa de compresión de imágenes",
        "related_blogs": [
            ("como-comprimir-imagenes-para-whatsapp", "Comprimir imágenes para WhatsApp"),
            ("jpg-vs-png-vs-webp-formatos-imagen", "JPG vs PNG vs WebP: ¿Qué formato usar?"),
        ],
        "related_tools": [
            ("/tools/comprimir-imagenes", "Comprimir imágenes online"),
            ("/tools/convertir-formato", "Convertir formato de imagen"),
        ]
    },
    "imagen-a-texto": {
        "title": "Imagen a texto: OCR online gratis",
        "related_blogs": [
            ("como-quitar-fondo-imagenes-online", "Cómo quitar fondo de imágenes online"),
            ("guia-completa-compresion-imagenes", "Guía completa de compresión de imágenes"),
        ],
        "related_tools": [
            ("/tools/imagen-a-texto", "Imagen a texto (OCR)"),
            ("/tools/pdf-a-imagen", "PDF a imagen"),
        ]
    },
    "como-quitar-fondo-imagenes-online": {
        "title": "Cómo quitar fondo de imágenes online",
        "related_blogs": [
            ("imagen-a-texto", "Imagen a texto: OCR online gratis"),
            ("jpg-vs-png-vs-webp-formatos-imagen", "JPG vs PNG vs WebP: ¿Qué formato usar?"),
        ],
        "related_tools": [
            ("/tools/quitar-fondo", "Quitar fondo de imagen"),
            ("/tools/fondo-blanco-producto", "Fondo blanco para producto"),
        ]
    },
    "jpg-vs-png-vs-webp-formatos-imagen": {
        "title": "JPG vs PNG vs WebP: ¿Qué formato usar?",
        "related_blogs": [
            ("guia-completa-compresion-imagenes", "Guía completa de compresión de imágenes"),
            ("como-comprimir-imagenes-para-whatsapp", "Comprimir imágenes para WhatsApp"),
        ],
        "related_tools": [
            ("/tools/convertir-formato", "Convertir formato de imagen"),
            ("/tools/comprimir-imagenes", "Comprimir imágenes online"),
        ]
    },
}

def build_related_section(meta):
    """Build HTML for related posts and tools section."""
    html = '\n<div class="related-section" style="margin-top: 48px; padding: 24px; background: #f8f9fa; border-radius: 12px;">\n'
    html += '  <h3 style="margin-top: 0; color: #2563eb; font-size: 1.2rem;">Artículos relacionados</h3>\n'
    html += '  <ul style="list-style: none; padding: 0; margin: 12px 0;">\n'
    for slug, title in meta["related_blogs"]:
        html += f'    <li style="margin: 8px 0;"><a href="/blog/{slug}" style="color: #2563eb; text-decoration: none;">→ {title}</a></li>\n'
    html += '  </ul>\n'
    html += '  <h3 style="margin-top: 24px; color: #2563eb; font-size: 1.2rem;">Herramientas recomendadas</h3>\n'
    html += '  <ul style="list-style: none; padding: 0; margin: 12px 0;">\n'
    for path, title in meta["related_tools"]:
        html += f'    <li style="margin: 8px 0;"><a href="{path}" style="color: #2563eb; text-decoration: none;">→ {title}</a></li>\n'
    html += '  </ul>\n'
    html += '</div>\n'
    return html

def process_blog(slug, meta):
    """Add related section to a blog post."""
    filepath = BLOG_DIR / f"{slug}.html"
    if not filepath.exists():
        print(f"  NOT FOUND: {slug}.html")
        return False
    
    content = filepath.read_text(encoding='utf-8')
    
    # Skip if already has related section
    if 'class="related-section"' in content:
        print(f"  SKIP (already has related section): {slug}")
        return False
    
    # Build related section HTML
    related_html = build_related_section(meta)
    
    # Insert before </article>
    content = content.replace('</article>', related_html + '</article>')
    
    filepath.write_text(content, encoding='utf-8')
    print(f"  OK: {slug}")
    return True

# Main
print("=" * 60)
print("Adding related posts section to blogs")
print("=" * 60)

success = 0
for slug, meta in BLOG_META.items():
    print(f"\nProcessing: {slug}")
    if process_blog(slug, meta):
        success += 1

print(f"\n{'=' * 60}")
print(f"Done: {success}/{len(BLOG_META)} blogs updated")
