#!/usr/bin/env python3
"""批量修复 comprimefotos HTML 文件中的损坏标签和 emoji"""
import os
import glob

TOOLS_DIR = r"G:\comprimefotos\tools"

# 修复映射表：损坏文本 → 正确文本
FIXES = [
    # 损坏的 </span> 标签（少了 <）
    ("📷?/span>", "📷</span>"),
    ("📷/span>", "📷</span>"),
    ("— ?/span>", "→</span>"),
    ("é?/span>", "🖼️</span>"),
    ("¿?/span>", "🖼️</span>"),
    
    # 损坏的 </button> 标签
    ("é??/button>", "☰</button>"),
    
    # 损坏的 emoji（é 前缀是 UTF-8 多字节损坏残留）
    ("é🖼️", "🗜️"),
    ("é📁", "📁"),
    # 重度损坏的 emoji
    ("é¦æ«", "📄"),
    ("é¦æ§", "💧"),
    ("é¦æ»", "📐"),
    ("é¦æµ", "📋"),
    ("é¦å¸¹", "🖼️"),
    ("éå¦ç¬", "✂️"),
    ("é¦æ", "✂️"),
    
    # 损坏的 toast 消息
    ("'é?Conversión completada'", "'✅ Conversión completada'"),
    ("'é?Imagen descargada correctamente'", "'✅ Imagen descargada correctamente'"),
    ("'é?Imagen descargada — lista para enviar por WhatsApp'", "'✅ Imagen descargada — lista para enviar por WhatsApp'"),
    ("'é?Imagen descargada'", "'✅ Imagen descargada'"),
    ("'é?PDF descargado correctamente'", "'✅ PDF descargado correctamente'"),
    ("'é´?Comprimiendo...'", "'⏳ Comprimiendo...'"),
    
    # 损坏的 h1
    ("é📁 PDF a", "📁 PDF a"),
    
    # 损坏的 dropzone icon
    ('<span class="dropzone-icon">é¦æ«</span>', '<span class="dropzone-icon">📄</span>'),
    ('<span class="dropzone-icon">é¦æ§</span>', '<span class="dropzone-icon">🖼️</span>'),
    
    # 损坏的按钮文字
    ('é¦æµ Copiar texto', '📋 Copiar texto'),
    
    # 损坏的 WhatsApp 状态
    ("whatsappStatus.textContent = 'é?' + sizeMB", "whatsappStatus.textContent = '✅ ' + sizeMB"),
    
    # 损坏的 toast warning
    ("'é¦æ§ Primero sube una imagen'", "'⚠️ Primero sube una imagen'"),
    
    # 损坏的 PDF 处理图标
    ('<span style="font-size:3rem;">é¦æ«</span>', '<span style="font-size:3rem;">📄</span>'),
    ('<span style="font-size:3rem;">é🖼️</span>', '<span style="font-size:3rem;">🖼️</span>'),
    
    # quitar-fondo-fixed.html 的特殊乱码（可能是不同编码损坏）
    ("忙聼陇茅聰聰?/span>", "📷</span>"),
    ("茅娄聝忙聭聺", "🗜️"),
    ("茅娄聝忙聲聹", "📤"),
    ("茅娄聝忙聬录", "📁"),
    ("茅娄聝忙聼陇茅聰聰?/span>", "🖼️</span>"),
    ("茅聢芦?/span>", "→</span>"),
    ("茅聢陆?/button>", "☰</button>"),
    ("Men莽聟陇", "Menú"),
    ("im猫掳漏genes", "imágenes"),
    
    # === 第二轮新增修复 ===
    # PDF 提示文本损坏
    ("é©ç¸ç¬", "⚠️"),
    # 更多 toast
    ("'é?OCR completado'", "'✅ OCR completado'"),
    ("'é?Collage generado'", "'✅ Collage generado'"),
    ("'é?Collage descargado'", "'✅ Collage descargado'"),
    ("'é?Imagen cargada'", "'✅ Imagen cargada'"),
    ("'é?Firma generada'", "'✅ Firma generada'"),
    ("'é?Firma descargada'", "'✅ Firma descargada'"),
    # 按钮文字
    ('é?Generar collage', '🎨 Generar collage'),
    ("removeBtn.textContent = 'é?;", "removeBtn.textContent = '❌';"),
    ("✂️£é?Limpiar", "🧹 Limpiar"),
    # redimensionar 损坏的预设按钮
    ('é»è®¹ç¬ YouTube (1280èx720)', 'YouTube (1280×720)'),
    ('è«Mantener proporciónç»', '«Mantener proporción»'),
]

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    fixed_count = 0
    
    # 通用修复：任何 ?/span> 后面跟着不是数字/字母的（即损坏标签）
    # 更精确的做法是替换已知模式
    
    for broken, correct in FIXES:
        if broken in content:
            count = content.count(broken)
            content = content.replace(broken, correct)
            fixed_count += count
            print(f"  {filepath}: '{broken[:30]}...' → '{correct[:30]}...' x{count}")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ 已保存 ({fixed_count} 处修复)")
        return True
    else:
        print(f"  ⏭️ 无需修复")
        return False

def main():
    html_files = sorted(glob.glob(os.path.join(TOOLS_DIR, "*.html")))
    total = 0
    fixed_files = 0
    
    for f in html_files:
        if fix_file(f):
            fixed_files += 1
            total += 1
    
    print(f"\n总计: {fixed_files} 个文件已修复")

if __name__ == "__main__":
    main()
