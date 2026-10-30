#!/usr/bin/env python3
"""IndexNow auto-submit for comprimefotos.com"""
import re
import json
import urllib.request
from pathlib import Path

SITE_HOST = "comprimefotos.com"
KEY = "comprimefotos2026indexnowkey7x4m2p8k"
KEY_LOCATION = f"https://{SITE_HOST}/{KEY}.txt"
SITEMAP_PATH = Path(__file__).parent / "sitemap.xml"

def get_urls_from_sitemap():
    """Extract all URLs from sitemap.xml"""
    content = SITEMAP_PATH.read_text(encoding='utf-8')
    urls = re.findall(r'<loc>([^<]+)</loc>', content)
    return urls

def submit_indexnow(urls):
    """Submit URLs to IndexNow API"""
    payload = {
        "host": SITE_HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        "https://api.indexnow.org/IndexNow",
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode('utf-8')
    except Exception as e:
        return None, str(e)

if __name__ == "__main__":
    print("=" * 60)
    print(f"IndexNow submit for {SITE_HOST}")
    print("=" * 60)
    
    urls = get_urls_from_sitemap()
    print(f"Found {len(urls)} URLs in sitemap")
    
    status, response = submit_indexnow(urls)
    
    if status == 200:
        print(f"✅ Success! HTTP {status}")
        print(f"   Submitted {len(urls)} URLs to IndexNow (Bing/Yandex/Seznam)")
    else:
        print(f"❌ Failed: HTTP {status}")
        print(f"   Response: {response}")
    
    print(f"\nKey location: {KEY_LOCATION}")
