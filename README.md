# 🎞️ OTT Release Tracker

A sleek Python GUI app that shows you the **latest movies and TV shows** released in the **past 7 days** on platforms like **Netflix**, **Amazon Prime**, **Hotstar**, and more — using the TMDb API.

---

## 🔍 What It Does

- Enter any OTT platform name (case-insensitive).
- See the latest content released this week.
- Get titles, ratings, release dates, and overviews.
- Smooth typewriter animation for a cooler experience.

---

## 🛠️ Tech Stack

- **Python**
- **Tkinter** (for GUI)
- **TMDb API** (for real-time content data)
- **Threading** (for async fetch)

---

## 💡 Key Features

- 🎬 Shows both Movies and TV Shows
- 🧠 Smart input handling (case-insensitive search)
- 🗓️ Filters results from only the **last 7 days**
- 🎨 Stylish UI with animated results
- 🌎 Works for Indian region (IN)

---

## ⚠️ Challenges Faced

- Making platform search **case-insensitive**
- Getting accurate releases within a 7-day window
- Display formatting to stay clean but informative

---

## 🚀 How to Run

```bash
pip install requests
python ott_tracker.py
