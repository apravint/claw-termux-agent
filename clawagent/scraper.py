"""
Web Scraper & Markdown Converter Engine
======================================
Extracts clean content, headers, links, and text from target URLs,
optimized for lightweight Termux environment.
"""

import re
import urllib.request
import urllib.parse
from typing import Dict, Any, List
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 ClawAgent/1.0"
}

def fetch_url(url: str, timeout: int = 15) -> str:
    """Fetch raw HTML content from a URL."""
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")

def extract_markdown(html_content: str, source_url: str = "") -> Dict[str, Any]:
    """Parse HTML content into clean structured markdown and metadata."""
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove script, style, nav, footer tags
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "svg"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled Page"

    # Extract headings
    headings = [h.get_text().strip() for h in soup.find_all(["h1", "h2", "h3"]) if h.get_text().strip()]

    # Extract all external links
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text().strip()
        if text and href.startswith("http"):
            links.append({"text": text[:40], "url": href})

    # Extract paragraphs and form clean markdown
    paragraphs = []
    for p in soup.find_all(["p", "article", "section"]):
        txt = p.get_text().strip()
        if len(txt) > 30 and txt not in paragraphs:
            paragraphs.append(txt)

    content_markdown = f"# {title}\n\n" + "\n\n".join(paragraphs[:15])

    return {
        "url": source_url,
        "title": title,
        "headings": headings[:10],
        "links": links[:10],
        "paragraph_count": len(paragraphs),
        "markdown": content_markdown,
        "character_count": len(content_markdown)
    }

def scrape_webpage(url: str) -> Dict[str, Any]:
    """Fetch and scrape webpage in a single step."""
    try:
        raw_html = fetch_url(url)
        return extract_markdown(raw_html, url)
    except Exception as e:
        return {
            "error": str(e),
            "url": url,
            "title": "Error Fetching Page",
            "markdown": f"Failed to fetch content from {url}: {str(e)}"
        }
