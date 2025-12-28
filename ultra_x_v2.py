import requests
from rich.console import Console
from rich.prompt import Prompt
from datetime import datetime
import pyfiglet

console = Console()

# ===== BRANDING =====
APP = "ULTRA X"
OWNER = "@MTZ_ADMIN"
CHANNEL = "MINDSET TRADING ZONE"

# ===== BIG TITLE =====
banner = pyfiglet.figlet_format(APP)
console.print(f"[bold red]{banner}[/bold red]")
console.print("[cyan]FUTURE SIGNAL GENERATOR[/cyan]\n")

# ===== USER INPUT =====
pairs = Prompt.ask(
    "Enter OTC pairs (comma separated)",
    default="WIFUSD_otc,USDNGN_otc,USDCOP_otc"
)

start_time = Prompt.ask("Start Time (HH:MM)", default="23:03")
end_time = Prompt.ask("End Time (HH:MM)", default="23:59")
accuracy = int(Prompt.ask("Select Accuracy (60-90)", default="80"))

# ===== SIGNAL LIMIT LOGIC =====
signal_limit_map = {
    60: 45,
    65: 40,
    70: 35,
    75: 30,
    80: 25,
    85: 22,
    90: 12
}

max_signals = signal_limit_map.get(accuracy, 25)

start_t = datetime.strptime(start_time, "%H:%M").time()
end_t = datetime.strptime(end_time, "%H:%M").time()

# ===== MARKET CHECK =====
if not all(p.strip().lower().endswith("_otc") for p in pairs.split(",")):
    console.print("[red]❌ Only OTC market supported[/red]")
    exit()

# ===== INFO =====
console.print(
    f"[green]Market: OTC | Accuracy ≥ {accuracy}% | Max Signal: {max_signals}[/green]\n"
)

# ===== API CALL =====
url = (
    "https://quotexotc-futureapi.poghen-dx.workers.dev"
    f"/pairs={pairs}?start_time={start_time}&end_time={end_time}"
)

console.print("[yellow]Fetching signals...[/yellow]\n")
response = requests.get(url)
data = response.json()

console.print("[cyan]LIVE SIGNALS[/cyan]\n")

shown = 0

# ===== SIGNAL OUTPUT =====
if data.get("status") == "success":
    for s in data.get("signals", []):
        if shown >= max_signals:
            break

        sig_time = datetime.strptime(s["time"], "%H:%M").time()
        acc = int(s["accuracy"].replace("%", ""))

        if start_t <= sig_time <= end_t and acc >= accuracy:
            console.print(
                f"[bold green]{s['asset']}[/bold green]  "
                f"[white]{s['time']}[/white]  "
                f"[magenta]{s['direction'].lower()}[/magenta]  "
                f"[yellow]{acc}%[/yellow]"
            )
            shown += 1
else:
    console.print("[red]API ERROR[/red]")

# ===== FOOTER =====
console.print(f"\n[white]TOTAL SIGNAL: {shown}[/white]")
console.print(f"[cyan]OWNER   : {OWNER}[/cyan]")
console.print(f"[cyan]CHANNEL : {CHANNEL}[/cyan]")
console.print("[green]ULTRA X READY ✔[/green]")
