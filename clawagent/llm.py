"""
LLM Content Synthesizer & Agent Brain
======================================
Synthesizes scraped web markdown into concise intelligence briefings.
"""

import os
import urllib.request
import json

def summarize_scraped_markdown(title: str, markdown_content: str, provider: str = "auto") -> str:
    """Summarize web content into an executive intelligence report."""
    prompt = f"Analyze the following web content from '{title}' and generate a 3-bullet point executive summary:\n\n{markdown_content[:2500]}"

    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if provider == "gemini" or (provider == "auto" and gemini_key):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception:
            pass

    if provider in ("ollama", "auto"):
        try:
            url = "http://localhost:11434/api/generate"
            payload = {"model": "qwen2.5:1.5b", "prompt": prompt, "stream": False}
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("response", "").strip()
        except Exception:
            pass

    # Fallback heuristic summary
    lines = [l.strip() for l in markdown_content.split("\n") if len(l.strip()) > 40]
    bullets = lines[:3] if lines else ["Content fetched successfully."]
    return f"📌 **Executive AI Briefing for {title}:**\n" + "\n".join(f"• {b}" for b in bullets)
