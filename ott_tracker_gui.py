import tkinter as tk
from tkinter import ttk, messagebox
import requests
import datetime
from threading import Thread
import time

# 🔑 TMDB API key
TMDB_API_KEY = "f6a5fe67ba66b63db1ce69c0af4d20f6"

# 📅 Date range (today & last 7 days)
TODAY = datetime.date.today()
LAST_WEEK = TODAY - datetime.timedelta(days=7)

# 🎞️ Popular OTT platform names & aliases
PLATFORMS = [
    "Netflix",
    "Amazon Prime Video",
    "Disney+ Hotstar",
    "ZEE5",
    "Apple TV+"
]
ALIASES = {
    "netflix": "Netflix",
    "amazon prime video": "Amazon Prime Video",
    "prime video": "Amazon Prime Video",
    "prime": "Amazon Prime Video",
    "hotstar": "Disney+ Hotstar",
    "disney+ hotstar": "Disney+ Hotstar",
    "jiohotstar": "Disney+ Hotstar",
    "zee5": "ZEE5",
    "zee": "ZEE5",
    "apple tv+": "Apple TV+",
    "apple tv": "Apple TV+",
    "appletv": "Apple TV+"
}

############################
# 🔧  Helper functions     #
############################

def normalise_platform(name: str) -> str:
    """Return official platform name for any alias (case‑insensitive)."""
    return ALIASES.get(name.strip().lower(), name.strip())


def get_provider_id(name: str):
    """Query TMDB movie + tv provider endpoints to get provider id."""
    endpoints = [
        "watch/providers/movie",
        "watch/providers/tv"
    ]
    for ep in endpoints:
        url = (
            f"https://api.themoviedb.org/3/{ep}?api_key={TMDB_API_KEY}"
            "&language=en-US&watch_region=IN"
        )
        try:
            data = requests.get(url, timeout=10).json()
            for provider in data.get("results", []):
                if provider["provider_name"].lower() == name.lower():
                    return provider["provider_id"]
        except Exception as e:
            print("Provider fetch error:", e)
    return None


def get_recent_releases(provider_id: int, content_type: str):
    """Fetch last‑week releases for movie or tv."""
    base = (
        f"https://api.themoviedb.org/3/discover/{content_type}?api_key={TMDB_API_KEY}"
        "&language=en-US&sort_by=popularity.desc"
        f"&with_watch_providers={provider_id}&watch_region=IN"
    )
    if content_type == "movie":
        base += f"&release_date.gte={LAST_WEEK}&release_date.lte={TODAY}"
    else:
        base += f"&first_air_date.gte={LAST_WEEK}&first_air_date.lte={TODAY}"

    try:
        return requests.get(base, timeout=10).json().get("results", [])
    except Exception as e:
        print("Fetch error:", e)
        return []


def format_date(date_str: str) -> str:
    """Convert YYYY‑MM‑DD to DD/MM/YYYY."""
    try:
        y, m, d = date_str.split("-")
        return f"{d}/{m}/{y}"
    except ValueError:
        return "N/A"

# 💫 Typewriter effect

def type_text(widget: tk.Text, text: str, delay_ms: int = 15):
    widget.config(state="normal")
    for ch in text:
        widget.insert(tk.END, ch)
        widget.update()
        time.sleep(delay_ms / 1000)
    widget.insert(tk.END, "\n")
    widget.config(state="disabled")

######################################
# 🔎   Search + suggestion handlers  #
######################################

def update_suggestions(event=None):
    typed = platform_var.get().lower()
    suggestion_box.delete(0, tk.END)
    if not typed:
        return
    for item in PLATFORMS:
        if item.lower().startswith(typed):
            suggestion_box.insert(tk.END, item)
    suggestion_box.place(x=platform_entry.winfo_x(), y=platform_entry.winfo_y() + platform_entry.winfo_height())


def fill_from_suggestion(event):
    selection = suggestion_box.get(tk.ACTIVE)
    platform_var.set(selection)
    suggestion_box.delete(0, tk.END)
    suggestion_box.place_forget()


def search():
    def worker():
        raw_name = platform_var.get().strip()
        if not raw_name:
            messagebox.showwarning("Input Missing", "Please type an OTT platform name.")
            return

        platform_name = normalise_platform(raw_name)
        provider_id = get_provider_id(platform_name)
        if not provider_id:
            messagebox.showerror("Provider Not Found", f"No provider found for '{raw_name}'. Try another.")
            return

        movies = get_recent_releases(provider_id, "movie")
        shows = get_recent_releases(provider_id, "tv")

        results_text.config(state="normal")
        results_text.delete("1.0", tk.END)
        results_text.config(state="disabled")

        type_text(results_text, f"Latest on {platform_name}\n{'='*45}\n", delay_ms=12)

        # 🎬 Movies
        type_text(results_text, "\n🎬 Movies:\n", delay_ms=12)
        if movies:
            for m in movies[:5]:
                title = m.get("title", "Untitled")
                date = format_date(m.get("release_date", ""))
                rating = m.get("vote_average", "N/A")
                overview = m.get("overview", "No description available.")
                type_text(results_text, f"• {title} ({date})", 6)
                type_text(results_text, f"  ⭐ {rating}/10", 6)
                type_text(results_text, f"  {overview}\n", 6)
        else:
            type_text(results_text, "No new movies found.\n", 6)

        # 📺 TV Series
        type_text(results_text, "\n📺 TV Series:\n", delay_ms=12)
        if shows:
            for s in shows[:5]:
                title = s.get("name", "Untitled")
                date = format_date(s.get("first_air_date", ""))
                rating = s.get("vote_average", "N/A")
                overview = s.get("overview", "No description available.")
                type_text(results_text, f"• {title} ({date})", 6)
                type_text(results_text, f"  ⭐ {rating}/10", 6)
                type_text(results_text, f"  {overview}\n", 6)
        else:
            type_text(results_text, "No new TV shows found.\n", 6)

    suggestion_box.place_forget()
    Thread(target=worker, daemon=True).start()

###################
# 🌌 GUI setup    #
###################

root = tk.Tk()
root.title("🎞️ OTT Release Tracker")
root.geometry("900x620")
root.configure(bg="#1e1e2f")

style = ttk.Style(root)
style.configure("TLabel", foreground="white", background="#1e1e2f", font=("Segoe UI", 12))
style.configure("TButton", font=("Segoe UI", 11))

container = ttk.Frame(root)
container.pack(pady=20)

prompt_lbl = ttk.Label(container, text="Search OTT platform:")
prompt_lbl.grid(row=0, column=0, padx=10, pady=10)

platform_var = tk.StringVar()
platform_entry = ttk.Entry(container, textvariable=platform_var, width=32)
platform_entry.grid(row=0, column=1, padx=10)
platform_entry.bind("<KeyRelease>", update_suggestions)
platform_entry.focus()

search_btn = ttk.Button(container, text="Search", command=search)
search_btn.grid(row=0, column=2, padx=10)

# Suggestion Listbox (initially hidden)
suggestion_box = tk.Listbox(container, width=32, height=4, bg="white")
suggestion_box.bind("<ButtonRelease-1>", fill_from_suggestion)

results_text = tk.Text(root, wrap=tk.WORD, font=("Segoe UI", 11), bg="#2c2c3c", fg="white", state="disabled")
results_text.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

root.mainloop()
