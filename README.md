# 🦅 Claw Termux Agent (`claw-termux-agent`)

> **Autonomous Web Automation, Headless Scraping & AI Workflow Daemon Tuned for Termux & Mobile Linux**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Termux%20%7C%20Linux-orange.svg)]()

`claw-termux-agent` is an autonomous web scraping, web search, content extraction, and background monitoring agent CLI built specifically for mobile Termux and Linux environments.

---

## ✨ Features

- 🕷️ **Lightweight Web Scraper**: Fetches web pages, strips scripts/ads/formatting, and converts content into clean Markdown.
- 🔍 **Privacy-Preserving Web Search**: Executes queries without tracking and extracts top web search links with snippets.
- 🤖 **AI Content Summarizer**: Integrates with local Ollama (`qwen2.5`) or Gemini API to summarize web articles into executive 3-bullet briefings.
- 🔔 **Background Daemon Monitor**: Periodically monitors target websites and logs activities with Android `termux-notification` support.
- 💻 **Rich Terminal TUI**: Interactive command deck for mobile interaction.

---

## 🚀 Quick Start

### Installation

```bash
cd claw-termux-agent
pip install -e .
```

---

## 🛠️ Usage

### 1. Scrape a Webpage & Generate AI Briefing
```bash
clawagent scrape github.com/apravint
```

### 2. Autonomous Web Search
```bash
clawagent search "Termux AI developments 2026"
```

### 3. Trigger Background Monitor Task
```bash
clawagent monitor github.com/apravint/AI-DevPulse
```

### 4. View Daemon Logs
```bash
clawagent logs
```

### 5. Launch Interactive TUI Dashboard
```bash
clawagent interactive
# or simply run:
clawagent
```

---

## 🌲 Repository Structure

```text
claw-termux-agent/
├── clawagent/
│   ├── __init__.py
│   ├── cli.py         # Rich CLI & TUI dashboard
│   ├── scraper.py     # HTML scraper & Markdown parser
│   ├── searcher.py    # Autonomous web searcher
│   ├── daemon.py      # Background monitor & notification logger
│   └── llm.py         # LLM content summarizer bridge
├── requirements.txt
├── setup.py
└── README.md
```

---

## 📄 License

Distributed under the MIT License. Built by **Pravin Tamilan ([@apravint](https://github.com/apravint))**.
