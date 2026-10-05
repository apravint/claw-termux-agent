"""
Claw Termux Agent CLI Runner
============================
Command-line interface and Rich TUI dashboard for mobile headless web scraping & AI daemon.
"""

import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

from clawagent.scraper import scrape_webpage
from clawagent.searcher import search_web
from clawagent.daemon import run_daemon_task, get_daemon_logs
from clawagent.llm import summarize_scraped_markdown

console = Console()

BANNER = """
[bold cyan]╔══════════════════════════════════════════════════════════════╗
║               [bold yellow]CLAW TERMUX AGENT v1.0.0[/bold yellow]                      ║
║  [dim]Autonomous Web Scraping & AI Automation for Termux[/dim]       ║
╚══════════════════════════════════════════════════════════════╝[/bold cyan]
"""

def print_banner():
    console.print(BANNER)

def cmd_scrape(url: str, summarize: bool = True):
    print_banner()
    with console.status(f"[bold yellow]Fetching & Extracting Web Content from: {url}...[/bold yellow]"):
        res = scrape_webpage(url)

    if "error" in res:
        console.print(f"[bold red]✖ Scraping Failed:[/bold red] {res['error']}")
        return

    table = Table(title="[bold green]Web Scraping Results[/bold green]", show_header=True)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="bold white")

    table.add_row("Page Title", res["title"])
    table.add_row("URL", res["url"])
    table.add_row("Headings Extracted", str(len(res["headings"])))
    table.add_row("Links Extracted", str(len(res["links"])))
    table.add_row("Total Characters", str(res["character_count"]))

    console.print(table)

    if summarize:
        with console.status("[bold yellow]Synthesizing AI Intelligence Briefing...[/bold yellow]"):
            briefing = summarize_scraped_markdown(res["title"], res["markdown"])
        console.print(Panel(briefing, title="[bold yellow]AI Executive Briefing[/bold yellow]", border_style="cyan"))

def cmd_search(query: str):
    print_banner()
    with console.status(f"[bold yellow]Searching Web for: '{query}'...[/bold yellow]"):
        results = search_web(query)

    table = Table(title=f"[bold cyan]Web Search Results for '{query}'[/bold cyan]", show_header=True)
    table.add_column("Title", style="bold yellow")
    table.add_column("URL", style="dim white")
    table.add_column("Snippet", style="white")

    for item in results:
        table.add_row(item["title"], item["url"], item["snippet"][:80] + "...")

    console.print(table)

def cmd_monitor(url: str):
    print_banner()
    console.print(f"[cyan]Registering autonomous background monitor for:[/cyan] [bold white]{url}[/bold white]")
    log = run_daemon_task(url)
    console.print(f"[bold green]✔ Background Task Logged:[/bold green] Status: {log['status']} | Chars: {log['char_count']}")

def cmd_logs():
    print_banner()
    logs = get_daemon_logs()

    table = Table(title="[bold magenta]Claw Agent Background Daemon Logs[/bold magenta]", show_header=True)
    table.add_column("Timestamp", style="dim white")
    table.add_column("Target URL", style="cyan")
    table.add_column("Page Title", style="yellow")
    table.add_column("Status", style="bold green")

    for l in reversed(logs):
        status_style = "bold green" if l["status"] == "SUCCESS" else "bold red"
        table.add_row(l["timestamp"], l["target_url"][:30], l["title"][:30], f"[{status_style}]{l['status']}[/{status_style}]")

    console.print(table)

def run_interactive():
    print_banner()
    while True:
        console.print("\n[bold cyan]Select Agent Action:[/bold cyan]")
        console.print("1. [yellow]Scrape Webpage & Generate AI Briefing[/yellow]")
        console.print("2. [yellow]Autonomous Web Search[/yellow]")
        console.print("3. [yellow]Trigger Background Web Monitor[/yellow]")
        console.print("4. [yellow]View Daemon Logs[/yellow]")
        console.print("5. [red]Exit[/red]")

        choice = Prompt.ask("Choose option", choices=["1", "2", "3", "4", "5"], default="1")

        if choice == "1":
            url = Prompt.ask("Enter URL to scrape (e.g. github.com/apravint)")
            cmd_scrape(url)
        elif choice == "2":
            q = Prompt.ask("Enter search query")
            cmd_search(q)
        elif choice == "3":
            url = Prompt.ask("Enter URL to monitor")
            cmd_monitor(url)
        elif choice == "4":
            cmd_logs()
        elif choice == "5":
            console.print("[bold green]Goodbye![/bold green]")
            break

def main():
    parser = argparse.ArgumentParser(description="Claw Termux Agent: Web Scraping & AI Automation")
    subparsers = parser.add_subparsers(dest="command")

    # Scrape
    sc_p = subparsers.add_parser("scrape", help="Scrape URL & generate AI briefing")
    sc_p.add_argument("url", help="Target URL")

    # Search
    se_p = subparsers.add_parser("search", help="Perform web search")
    se_p.add_argument("query", help="Search query")

    # Monitor
    mo_p = subparsers.add_parser("monitor", help="Run background monitor task")
    mo_p.add_argument("url", help="Target URL")

    # Logs
    subparsers.add_parser("logs", help="View daemon logs")

    # Interactive
    subparsers.add_parser("interactive", help="Launch interactive TUI dashboard")

    args = parser.parse_args()

    if args.command == "scrape":
        cmd_scrape(args.url)
    elif args.command == "search":
        cmd_search(args.query)
    elif args.command == "monitor":
        cmd_monitor(args.url)
    elif args.command == "logs":
        cmd_logs()
    elif args.command == "interactive" or len(sys.argv) == 1:
        run_interactive()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
