#!/usr/bin/env python3
"""Batch generate Spanish SEO blogs for comprimefotos.com using DeepSeek API."""
import json
import urllib.request
import os
import re
from pathlib import Path

# Configuration
DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]  # 密钥走环境变量，不入库
BLOG_DIR = Path(r"E:\网站项目\comprimefotos\blog")
SITE_URL = "https://comprimefotos.com"

# 20 long-tail blog topics (Spanish)
BLOG_TOPICS = [
    {
        "slug": "comprimir-imagenes-a-tamano-exacto",
        "title": "Cómo comprimir imágenes a un tamaño exacto (KB o MB)",
        "meta": "Aprende a comprimir imágenes a un tamaño exacto en KB o MB. Guía paso a paso para reducir fotos al peso que necesitas sin perder calidad.",
        "keywords": "comprimir imagenes a tamano exacto, reducir imagen a kb, comprimir foto a mb, tamano especifico imagen",
        "topic": "Cómo comprimir imágenes a un tamaño exacto específico (ej: 100KB, 500KB, 1MB)",
        "related_tool": "/tools/comprimir-imagenes",
        "related_tool_name": "Comprimir imágenes online"
    },
    {
        "slug": "jpg-vs-png-cual-ocupa-menos",
        "title": "JPG vs PNG: ¿Cuál ocupa menos espacio?",
        "meta": "Comparativa entre JPG y PNG. Descubre cuál formato ocupa menos espacio y cuál debes usar según el tipo de imagen.",
        "keywords": "jpg vs png cual ocupa menos, diferencia jpg png, cual es mas ligero jpg o png, cuando usar jpg png",
        "topic": "JPG vs PNG: comparativa detallada de tamaño, calidad y cuándo usar cada uno",
        "related_tool": "/tools/convertir-formato",
        "related_tool_name": "Convertir formato de imagen"
    },
    {
        "slug": "comprimir-fotos-sin-perder-calidad",
        "title": "Cómo comprimir fotos sin perder calidad visible",
        "meta": "Guía para comprimir fotos sin que se vean borrosas ni pixeladas. Aprende los ajustes óptimos para mantener la calidad.",
        "keywords": "comprimir fotos sin perder calidad, reducir tamano imagen sin perder calidad, compresion sin perdida",
        "topic": "Cómo comprimir imágenes sin perder calidad visible, ajustes óptimos",
        "related_tool": "/tools/comprimir-imagenes",
        "related_tool_name": "Comprimir imágenes online"
    },
    {
        "slug": "comprimir-imagenes-en-movil",
        "title": "Cómo comprimir imágenes en el móvil (Android e iPhone)",
        "meta": "Trucos para comprimir fotos directamente desde tu móvil. Apps y métodos nativos para Android e iOS sin perder calidad.",
        "keywords": "comprimir fotos en movil, comprimir imagenes android, comprimir fotos iphone, reducir tamano foto celular",
        "topic": "Cómo comprimir imágenes directamente desde el móvil, métodos nativos y apps recomendadas",
        "related_tool": "/tools/comprimir-imagenes",
        "related_tool_name": "Comprimir imágenes online"
    },
    {
        "slug": "comprimir-imagenes-para-correo",
        "title": "Cómo comprimir imágenes para enviar por correo electrónico",
        "meta": "Aprende a reducir el peso de tus fotos para enviarlas por email sin problemas de límite de adjuntos. Tamaños ideales para Gmail, Outlook y más.",
        "keywords": "comprimir fotos para correo, enviar imagenes por email, tamano adjunto correo, reducir fotos para gmail",
        "topic": "Cómo comprimir imágenes para enviar por correo electrónico, límites de Gmail/Outlook",
        "related_tool": "/tools/comprimir-imagenes",
        "related_tool_name": "Comprimir imágenes online"
    },
    {
        "slug": "webp-vs-jpg-2026",
        "title": "WebP vs JPG en 2026: ¿Cuál es mejor?",
        "meta": "Comparativa actualizada 2026 entre WebP y JPG. Ventajas, desventajas y cuál formato elegir para web, redes sociales y fotografía.",
        "keywords": "webp vs jpg 2026, ventajas webp, cuando usar webp, webp mejor que jpg",
        "topic": "WebP vs JPG en 2026: comparativa actualizada, ventajas de WebP y compatibilidad",
        "related_tool": "/tools/convertir-formato",
        "related_tool_name": "Convertir formato de imagen"
    },
    {
        "slug": "comprimir-imagenes-lote",
        "title": "Cómo comprimir varias imágenes a la vez (procesamiento por lotes)",
        "meta": "Guía para comprimir decenas o cientos de fotos de una sola vez. Métodos online y programas de escritorio para procesar por lotes.",
        "keywords": "comprimir imagenes por lotes, comprimir varias fotos a la vez, procesamiento masivo imagenes",
        "topic": "Cómo comprimir múltiples imágenes a la vez, herramientas de procesamiento por lotes",
        "related_tool": "/tools/procesador-por-lotes",
        "related_tool_name": "Procesador por lotes"
    },
    {
        "slug": "comprimir-imagenes-afecta-calidad",
        "title": "¿Comprimir imágenes afecta la calidad? Todo lo que debes saber",
        "meta": "Descubre cómo afecta la compresión a la calidad de tus fotos. Compresión con pérdida vs sin pérdida, cuánto puedes comprimir sin notarlo.",
        "keywords": "comprimir imagenes afecta calidad, compresion con perdida, compresion sin perdida, cuanto se degrada imagen",
        "topic": "¿La compresión de imágenes afecta la calidad? Explicación técnica con pérdida vs sin pérdida",
        "related_tool": "/tools/comprimir-imagenes",
        "related_tool_name": "Comprimir imágenes online"
    },
    {
        "slug": "comprimir-imagenes-para-instagram",
        "title": "Tamaño ideal de imágenes para Instagram en 2026",
        "meta": "Guía de tamaños de imagen para Instagram 2026: posts, stories, reels y perfil. Cómo subir fotos sin que Instagram las arruine.",
        "keywords": "tamano imagen instagram 2026, tamano ideal foto instagram, como subir fotos a instagram sin perder calidad",
        "topic": "Tamaños ideales de imagen para Instagram 2026 y cómo evitar que la app comprima demasiado",
        "related_tool": "/tools/redimensionar-redes-sociales",
        "related_tool_name": "Redimensionar para redes sociales"
    },
    {
        "slug": "heic-a-jpg-gratis",
        "title": "Cómo convertir HEIC a JPG gratis (iPhone y Windows)",
        "meta": "Convierte fotos HEIC de tu iPhone a JPG gratis online. Métodos para Windows, Mac y móvil sin instalar programas.",
        "keywords": "heic a jpg gratis, convertir heic iphone, como abrir heic en windows, convertir fotos iphone a jpg",
        "topic": "Cómo convertir fotos HEIC de iPhone a JPG, métodos online y nativos",
        "related_tool": "/tools/convertir-formato",
        "related_tool_name": "Convertir formato de imagen"
    },
]

def call_deepseek(prompt, max_tokens=2000):
    """Call DeepSeek API to generate content."""
    url = "https://api.deepseek.com/v1/chat/completions"
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Eres un experto en fotografía y edición de imágenes. Escribes artículos en español natural, optimizados para SEO, sin sonar a IA. Usa títulos claros, listas y ejemplos prácticos."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  API Error: {e}")
        return None

def generate_blog_content(topic_info):
    """Generate full blog content using DeepSeek."""
    prompt = f"""Escribe un artículo de blog completo en español sobre: {topic_info['topic']}

Requisitos:
- Al menos 1200 palabras
- Estructura con título principal, introducción, 4-6 secciones con H2, conclusión
- Incluye 4-5 preguntas frecuentes (FAQ) al final
- Tono natural, útil, como un blog de fotografía
- Optimizado para SEO: incluye la palabra clave principal de forma natural
- Termina con una sección de conclusión
- NO uses markdown, usa texto plano con saltos de línea
- NO incluyas el título principal en el cuerpo, ya lo pondremos en el HTML

Estructura que debes seguir:
[Introducción de 2-3 párrafos]
[Sección 1: H2]
[Párrafos y listas]
[Sección 2: H2]
[Párrafos y listas]
[Sección 3: H2]
[Párrafos y listas]
[Sección 4: H2]
[Párrafos y listas]
[Consejos prácticos]
[Conclusión de 1-2 párrafos]
[PREGUNTAS FRECUENTES]
Pregunta 1: ...
Respuesta: ...
Pregunta 2: ...
Respuesta: ...
Pregunta 3: ...
Respuesta: ...
Pregunta 4: ...
Respuesta: ...
"""
    return call_deepseek(prompt, max_tokens=2500)

def build_blog_html(topic_info, content, faqs):
    """Build complete HTML blog page."""
    slug = topic_info["slug"]
    title = topic_info["title"]
    meta_desc = topic_info["meta"]
    keywords = topic_info["keywords"]
    tool_path = topic_info["related_tool"]
    tool_name = topic_info["related_tool_name"]
    
    # Convert plain text content to HTML
    # Split into sections
    lines = content.split('\n')
    body_html = ""
    in_faq = False
    faq_items = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if we're entering FAQ section
        if "PREGUNTAS FRECUENTES" in line.upper() or "PREGUNTAS FRECUENTES" in line:
            in_faq = True
            continue
        
        # Parse FAQ
        if in_faq:
            if line.startswith("Pregunta"):
                q = re.sub(r'^Pregunta \d+:\s*', '', line)
                faq_items.append({"q": q, "a": ""})
            elif line.startswith("Respuesta:"):
                a = re.sub(r'^Respuesta:\s*', '', line)
                if faq_items:
                    faq_items[-1]["a"] = a
            continue
        
        # Regular content
        if len(line) > 100 and not line.startswith(('•', '-', '1.', '2.', '3.', '4.', '5.')):
            body_html += f"      <p>{line}</p>\n"
        elif line.startswith('•') or line.startswith('-'):
            body_html += f"        <li>{line[1:].strip()}</li>\n"
        elif re.match(r'^\d+\.', line):
            body_html += f"        <li>{line}</li>\n"
    
    # Build FAQ HTML
    faq_html = '      <h2 id="faq">Preguntas frecuentes</h2>\n'
    for faq in faq_items:
        faq_html += f'      <div class="faq-item"><button class="faq-question">{faq["q"]}</button><div class="faq-answer"><p>{faq["a"]}</p></div></div>\n'
    
    # Build FAQPage JSON-LD
    faq_jsonld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }
    for faq in faq_items:
        faq_jsonld["mainEntity"].append({
            "@type": "Question",
            "name": faq["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["a"]
            }
        })
    
    # Article JSON-LD
    article_jsonld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": meta_desc,
        "author": {"@type": "Organization", "name": "ComprimeFotos"},
        "publisher": {
            "@type": "Organization",
            "name": "ComprimeFotos",
            "url": "https://comprimefotos.com",
            "logo": {"@type": "ImageObject", "url": "https://comprimefotos.com/favicon.svg"}
        },
        "datePublished": "2026-09-18",
        "dateModified": "2026-09-18",
        "mainEntityOfPage": f"{SITE_URL}/blog/{slug}"
    }
    
    # Breadcrumb JSON-LD
    breadcrumb_jsonld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE_URL}/blog/"},
            {"@type": "ListItem", "position": 3, "name": title}
        ]
    }
    
    # Related section
    related_html = f'''
    <div class="related-section" style="margin-top: 48px; padding: 24px; background: #f8f9fa; border-radius: 12px;">
      <h3 style="margin-top: 0; color: #1a6b52; font-size: 1.2rem;">Herramienta recomendada</h3>
      <p style="margin: 12px 0;">Prueba nuestra herramienta gratuita para esto:</p>
      <p style="margin: 12px 0;"><a href="{tool_path}" style="color: #1a6b52; font-weight: 600;">→ {tool_name}</a></p>
      <h3 style="margin-top: 24px; color: #1a6b52; font-size: 1.2rem;">Artículos relacionados</h3>
      <ul style="list-style: none; padding: 0; margin: 12px 0;">
        <li style="margin: 8px 0;"><a href="/blog/como-comprimir-imagenes-para-whatsapp" style="color: #1a6b52; text-decoration: none;">→ Comprimir imágenes para WhatsApp</a></li>
        <li style="margin: 8px 0;"><a href="/blog/jpg-vs-png-vs-webp-formatos-imagen" style="color: #1a6b52; text-decoration: none;">→ JPG vs PNG vs WebP: ¿Qué formato usar?</a></li>
      </ul>
    </div>
'''
    
    # Full HTML
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="robots" content="index,follow">
<title>{title} | ComprimeFotos</title>
<meta name="description" content="{meta_desc}">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="{SITE_URL}/blog/{slug}">
<meta name="theme-color" content="#1a6b52">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="{SITE_URL}/blog/{slug}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ComprimeFotos">
<meta property="og:locale" content="es_ES">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="stylesheet" href="../css/style.css?v=3">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap" rel="stylesheet">
<script type="application/ld+json">
{json.dumps(article_jsonld, ensure_ascii=False, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(breadcrumb_jsonld, ensure_ascii=False, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(faq_jsonld, ensure_ascii=False, indent=2)}
</script>
</head>
<body>
<header class="site-header">
  <div class="container">
    <a href="/" class="logo"><span class="logo-icon">📷</span><span class="logo-text">ComprimeFotos</span></a>
    <nav class="main-nav">
      <a href="/">Inicio</a>
      <a href="/tools/comprimir-imagenes">Comprimir</a>
      <a href="/tools/comprimir-imagenes-whatsapp">WhatsApp</a>
      <a href="/tools/quitar-fondo">Quitar fondo</a>
      <a href="/blog/" class="active">Blog</a>
      <a href="/about">Sobre nosotros</a>
    </nav>
  </div>
</header>
<main class="container">
  <nav class="breadcrumb">
    <a href="/">Inicio</a> — <a href="/blog/">Blog</a> — <span>{title}</span>
  </nav>
  <article class="blog-post">
    <h1>{title}</h1>
    <div class="blog-meta">
      <span class="blog-date">18 septiembre, 2026</span>
      <span class="blog-tag">Guía</span>
      <span class="blog-readtime">7 min de lectura</span>
    </div>
    <div class="blog-post-content">
{body_html}
{faq_html}
{related_html}
    </div>
  </article>
</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" class="logo"><span class="logo-icon">📷</span><span class="logo-text">ComprimeFotos</span></a>
        <p>Herramientas gratuitas para comprimir y editar imágenes online.</p>
      </div>
      <div class="footer-links">
        <h4>Herramientas</h4>
        <a href="/tools/comprimir-imagenes">Comprimir imágenes</a>
        <a href="/tools/comprimir-imagenes-whatsapp">Comprimir para WhatsApp</a>
        <a href="/tools/quitar-fondo">Quitar fondo</a>
      </div>
      <div class="footer-links">
        <h4>Legal</h4>
        <a href="/about">Sobre nosotros</a>
        <a href="/contacto">Contacto</a>
        <a href="/privacy">Privacidad</a>
        <a href="/blog/">Blog</a>
      </div>
    </div>
  </div>
</footer>
</body>
</html>'''
    return html

# Main
print("=" * 60)
print("Generating Spanish SEO blogs for comprimefotos.com")
print("=" * 60)

success = 0
for i, topic in enumerate(BLOG_TOPICS[3:10]):  # Next 7 blogs
    print(f"\n[{i+1}/3] Generando: {topic['slug']}")
    
    # Check if already exists
    filepath = BLOG_DIR / f"{topic['slug']}.html"
    if filepath.exists():
        print(f"  SKIP (already exists)")
        continue
    
    # Generate content
    content = generate_blog_content(topic)
    if not content:
        print(f"  FAILED (API error)")
        continue
    
    # Parse FAQs
    lines = content.split('\n')
    faqs = []
    in_faq = False
    current_q = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "PREGUNTAS FRECUENTES" in line.upper():
            in_faq = True
            continue
        if in_faq:
            if line.startswith("Pregunta"):
                current_q = re.sub(r'^Pregunta \d+:\s*', '', line)
            elif line.startswith("Respuesta:"):
                a = re.sub(r'^Respuesta:\s*', '', line)
                faqs.append({"q": current_q, "a": a})
    
    # Build HTML
    html = build_blog_html(topic, content, faqs)
    
    # Save
    filepath.write_text(html, encoding='utf-8')
    word_count = len(re.findall(r'\b\w+\b', content))
    print(f"  OK ({word_count} words, {len(faqs)} FAQs)")
    success += 1

print(f"\n{'=' * 60}")
print(f"Done: {success}/3 blogs generated")
