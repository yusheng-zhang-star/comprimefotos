#!/usr/bin/env python3
"""Generate blogs 11-20 for comprimefotos.com."""
import json
import urllib.request
import os
import re
from pathlib import Path

DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]  # 密钥走环境变量，不入库
BLOG_DIR = Path(r"E:\网站项目\comprimefotos\blog")
SITE_URL = "https://comprimefotos.com"

# Blogs 11-20
BLOG_TOPICS = [
    {
        "slug": "comprimir-png-transparente",
        "title": "Cómo comprimir PNG con fondo transparente",
        "meta": "Aprende a reducir el tamaño de imágenes PNG con fondo transparente sin perder la transparencia. Métodos online y consejos prácticos.",
        "keywords": "comprimir png transparente, reducir tamano png fondo transparente, comprimir png sin perder transparencia",
        "topic": "Cómo comprimir imágenes PNG con fondo transparente manteniendo la transparencia",
        "related_tool": "/tools/comprimir-imagenes",
        "related_tool_name": "Comprimir imágenes online"
    },
    {
        "slug": "comprimir-imagenes-para-web",
        "title": "Cómo optimizar imágenes para web (guía 2026)",
        "meta": "Guía completa para optimizar imágenes para tu sitio web. Tamaños, formatos y compresión para que tu web cargue más rápido.",
        "keywords": "optimizar imagenes para web, comprimir fotos para pagina web, imagenes para web tamano, velocidad web",
        "topic": "Cómo optimizar imágenes para web, mejorar velocidad de carga de tu sitio",
        "related_tool": "/tools/comprimir-imagenes",
        "related_tool_name": "Comprimir imágenes online"
    },
    {
        "slug": "comprimir-imagenes-facebook",
        "title": "Cómo subir fotos a Facebook sin que pierdan calidad",
        "meta": "Trucos para subir fotos a Facebook sin que la red social las comprima demasiado. Configuración y tamaños ideales.",
        "keywords": "subir fotos a facebook sin perder calidad, facebook comprime fotos, tamano ideal facebook",
        "topic": "Cómo evitar que Facebook comprima tus fotos y subirlas en calidad máxima",
        "related_tool": "/tools/redimensionar-redes-sociales",
        "related_tool_name": "Redimensionar para redes sociales"
    },
    {
        "slug": "comprimir-imagenes-resolucion",
        "title": "Resolución de imagen vs tamaño de archivo: qué relación hay",
        "meta": "Explicación clara sobre resolución de imágenes y tamaño de archivo. Cuántos DPI necesitas para web, impresión o redes sociales.",
        "keywords": "resolucion imagen vs tamano archivo, dpi para impresion, resolucion web, cuanto pesa una foto",
        "topic": "Resolución de imágenes (DPI) vs tamaño de archivo: relación práctica según uso",
        "related_tool": "/tools/redimensionar-imagen",
        "related_tool_name": "Redimensionar imagen"
    },
    {
        "slug": "comprimir-screenshots",
        "title": "Cómo comprimir capturas de pantalla grandes",
        "meta": "Aprende a reducir el tamaño de capturas de pantalla sin que se vean borrosas. Especial para tutoriales y documentación.",
        "keywords": "comprimir capturas de pantalla, reducir tamano screenshot, comprimir capturas windows, comprimir pantallazos",
        "topic": "Cómo comprimir capturas de pantalla grandes manteniendo la legibilidad del texto",
        "related_tool": "/tools/comprimir-imagenes",
        "related_tool_name": "Comprimir imágenes online"
    },
    {
        "slug": "comprimir-gif",
        "title": "Cómo comprimir GIF animados sin perder calidad",
        "meta": "Guía para reducir el tamaño de GIFs animados online. Métodos gratuitos para que tus GIFs carguen más rápido.",
        "keywords": "comprimir gif animado, reducir tamano gif, optimizar gif online, gif mas ligero",
        "topic": "Cómo comprimir GIFs animados manteniendo la animación y calidad",
        "related_tool": "/tools/comprimir-imagenes",
        "related_tool_name": "Comprimir imágenes online"
    },
    {
        "slug": "tamano-fotos-imprimir",
        "title": "¿Qué tamaño de imagen necesito para imprimir?",
        "meta": "Guía de resolución necesaria para imprimir fotos en diferentes tamaños. Evita fotos borrosas o pixeladas al imprimir.",
        "keywords": "tamano imagen para imprimir, resolucion para imprimir fotos, dpi impresion fotografica, que resolucion necesito para imprimir",
        "topic": "Tamaños de resolución necesarios para imprimir fotos en diferentes formatos",
        "related_tool": "/tools/redimensionar-imagen",
        "related_tool_name": "Redimensionar imagen"
    },
    {
        "slug": "convertir-pdf-a-jpg",
        "title": "Cómo convertir PDF a JPG gratis online",
        "meta": "Convierte páginas de PDF a imágenes JPG gratis online. Métodos rápidos sin instalar programas, para Windows, Mac y móvil.",
        "keywords": "convertir pdf a jpg gratis, pdf a imagen online, extraer imagenes de pdf, pdf a jpeg",
        "topic": "Cómo convertir archivos PDF a imágenes JPG gratis online, métodos rápidos",
        "related_tool": "/tools/pdf-a-imagen",
        "related_tool_name": "PDF a imagen"
    },
    {
        "slug": "comprimir-imagenes-para-linkedin",
        "title": "Tamaño ideal de imágenes para LinkedIn 2026",
        "meta": "Guía completa de tamaños de imagen para LinkedIn 2026: perfil, portada, posts y artículos. Optimiza tu presencia profesional.",
        "keywords": "tamano imagen linkedin 2026, tamano foto perfil linkedin, tamano portada linkedin, imagenes linkedin",
        "topic": "Tamaños ideales de imagen para LinkedIn en 2026 para perfil, portada y posts",
        "related_tool": "/tools/redimensionar-redes-sociales",
        "related_tool_name": "Redimensionar para redes sociales"
    },
    {
        "slug": "por-que-mis-fotos-pesan-mucho",
        "title": "¿Por qué mis fotos pesan tanto? Causas y soluciones",
        "meta": "Descubre por qué tus fotos ocupan tanto espacio y cómo reducir su tamaño sin perder calidad. Causas comunes y soluciones rápidas.",
        "keywords": "por que mis fotos pesan tanto, fotos muy pesadas, como reducir peso de fotos, por que mis imagenes ocupan mucho",
        "topic": "¿Por qué tus fotos pesan tanto? Causas comunes y soluciones prácticas",
        "related_tool": "/tools/comprimir-imagenes",
        "related_tool_name": "Comprimir imágenes online"
    },
]

def call_deepseek(prompt, max_tokens=2500):
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

def build_blog_html(topic_info, content, faqs):
    slug = topic_info["slug"]
    title = topic_info["title"]
    meta_desc = topic_info["meta"]
    keywords = topic_info["keywords"]
    tool_path = topic_info["related_tool"]
    tool_name = topic_info["related_tool_name"]
    
    lines = content.split('\n')
    body_html = ""
    in_faq = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "PREGUNTAS FRECUENTES" in line.upper():
            in_faq = True
            continue
        if in_faq:
            continue
        if len(line) > 80 and not line.startswith(('•', '-', '1.', '2.', '3.', '4.', '5.')):
            body_html += f"      <p>{line}</p>\n"
        elif line.startswith('•') or line.startswith('-'):
            body_html += f"        <li>{line[1:].strip()}</li>\n"
    
    # FAQ HTML
    faq_html = '      <h2 id="faq">Preguntas frecuentes</h2>\n'
    for faq in faqs:
        faq_html += f'      <div class="faq-item"><button class="faq-question">{faq["q"]}</button><div class="faq-answer"><p>{faq["a"]}</p></div></div>\n'
    
    # JSON-LD
    faq_jsonld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faqs]
    }
    
    article_jsonld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": meta_desc,
        "author": {"@type": "Organization", "name": "ComprimeFotos"},
        "publisher": {"@type": "Organization", "name": "ComprimeFotos", "url": "https://comprimefotos.com", "logo": {"@type": "ImageObject", "url": "https://comprimefotos.com/favicon.svg"}},
        "datePublished": "2026-09-18",
        "dateModified": "2026-09-18",
        "mainEntityOfPage": f"{SITE_URL}/blog/{slug}"
    }
    
    breadcrumb_jsonld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE_URL}/blog/"},
            {"@type": "ListItem", "position": 3, "name": title}
        ]
    }
    
    related_html = f'''
    <div class="related-section" style="margin-top: 48px; padding: 24px; background: #f8f9fa; border-radius: 12px;">
      <h3 style="margin-top: 0; color: #1a6b52; font-size: 1.2rem;">Herramienta recomendada</h3>
      <p style="margin: 12px 0;"><a href="{tool_path}" style="color: #1a6b52; font-weight: 600;">→ {tool_name}</a></p>
      <h3 style="margin-top: 24px; color: #1a6b52; font-size: 1.2rem;">Artículos relacionados</h3>
      <ul style="list-style: none; padding: 0; margin: 12px 0;">
        <li style="margin: 8px 0;"><a href="/blog/como-comprimir-imagenes-para-whatsapp" style="color: #1a6b52; text-decoration: none;">→ Comprimir imágenes para WhatsApp</a></li>
        <li style="margin: 8px 0;"><a href="/blog/jpg-vs-png-cual-ocupa-menos" style="color: #1a6b52; text-decoration: none;">→ JPG vs PNG: ¿Cuál ocupa menos?</a></li>
      </ul>
    </div>
'''
    
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

print("=" * 60)
print("Generating blogs 11-20 for comprimefotos.com")
print("=" * 60)

success = 0
for i, topic in enumerate(BLOG_TOPICS):
    print(f"\n[{i+1}/10] Generando: {topic['slug']}")
    
    filepath = BLOG_DIR / f"{topic['slug']}.html"
    if filepath.exists():
        print(f"  SKIP (already exists)")
        continue
    
    prompt = f"""Escribe un artículo de blog completo en español sobre: {topic['topic']}

Requisitos:
- Al menos 1200 palabras
- Estructura con 4-6 secciones
- Incluye 4 preguntas frecuentes (FAQ) al final
- Tono natural, útil, como un blog de fotografía
- Optimizado para SEO
- NO uses markdown
- Al final del artículo incluye:
PREGUNTAS FRECUENTES
Pregunta 1: ...
Respuesta: ...
Pregunta 2: ...
Respuesta: ...
Pregunta 3: ...
Respuesta: ...
Pregunta 4: ...
Respuesta: ...
"""
    
    content = call_deepseek(prompt, max_tokens=2500)
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
    
    html = build_blog_html(topic, content, faqs)
    filepath.write_text(html, encoding='utf-8')
    word_count = len(re.findall(r'\b\w+\b', content))
    print(f"  OK ({word_count} words, {len(faqs)} FAQs)")
    success += 1

print(f"\n{'=' * 60}")
print(f"Done: {success}/10 blogs generated")
