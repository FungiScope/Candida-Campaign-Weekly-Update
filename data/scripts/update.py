#!/usr/bin/env python3
import json, os, sys
from datetime import date

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "data.json")
COUNTRIES = ["Germany", "Spain", "Italy", "UK", "USA"]

def ask_date():
    today = date.today().isoformat()
    raw = input(f"Week date [YYYY-MM-DD] (default {today}): ").strip()
    if not raw:
        return today
    # basic validation
    try:
        y,m,d = map(int, raw.split("-"))
        _ = date(y,m,d)
    except Exception:
        print("Invalid date. Use YYYY-MM-DD.")
        sys.exit(1)
    return raw

def ask_int(prompt):
    while True:
        val = input(prompt).strip()
        if val == "":
            return 0
        try:
            n = int(val)
            if n < 0: raise ValueError()
            return n
        except ValueError:
            print("Please enter a non-negative integer (or leave blank for 0).")

def load_data():
    if not os.path.exists(DATA_PATH):
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("data.json is not valid JSON. Fix it or delete it to start fresh.")
            sys.exit(1)

def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

def main():
    print("=== Add weekly numbers ===")
    week = ask_date()
    print("Enter case numbers for each country (blank = 0):")
    countries_payload = {}
    for c in COUNTRIES:
        n = ask_int(f"  {c}: ")
        countries_payload[c] = n

    data = load_data()

    # replace if this week already exists; else append
    replaced = False
    for entry in data:
        if entry.get("date") == week:
            entry["countries"] = countries_payload
            replaced = True
            break
    if not replaced:
        data.append({"date": week, "countries": countries_payload})

    # sort by date ascending for cleanliness
    data.sort(key=lambda x: x.get("date",""))
    save_data(data)

    # Show a short summary
    total = sum(countries_payload.values())
    print(f"\nSaved week {week}. Total = {total}.")
    print(f"Updated {DATA_PATH}")
    print("Commit and push to publish via GitHub Pages.")

if __name__ == "__main__":
    main()
