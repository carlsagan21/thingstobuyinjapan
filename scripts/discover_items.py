#!/usr/bin/env python3
"""
Discover popular Japanese items on eBay using the Browse API.
Searches multiple general queries and ranks items by frequency/price.
"""

import base64
import json
import os
import sys
import time
from collections import Counter
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

CLIENT_ID = os.getenv("EBAY_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET", "")
BASE_URL = "https://api.ebay.com"


def get_token():
    auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    r = requests.post(
        f"{BASE_URL}/identity/v1/oauth2/token",
        headers={"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Basic {auth}"},
        data={"grant_type": "client_credentials", "scope": "https://api.ebay.com/oauth/api_scope"},
        timeout=15,
    )
    return r.json()["access_token"]


def search(token, query, limit=50, sort="newlyListed"):
    r = requests.get(
        f"{BASE_URL}/buy/browse/v1/item_summary/search",
        headers={
            "Authorization": f"Bearer {token}",
            "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
            "X-EBAY-C-ENDUSERCTX": "contextualLocation=country%3DUS",
        },
        params={
            "q": query,
            "limit": str(limit),
            "filter": "priceCurrency:USD,buyingOptions:{FIXED_PRICE}",
            "sort": sort,
        },
        timeout=15,
    )
    if r.status_code != 200:
        print(f"  ⚠️ {r.status_code}: {r.text[:100]}")
        return [], 0
    data = r.json()
    total = data.get("total", 0)
    return data.get("itemSummaries", []), total


# Queries to search - broad Japanese product terms
QUERIES = [
    # General
    "Japan exclusive",
    "Japanese import authentic",
    "Made in Japan",
    "from Japan new",
    # Beauty & Health
    "Japanese skincare",
    "Japanese sunscreen",
    "Japanese eye drops",
    "Japanese supplement collagen",
    "Japanese hair care treatment",
    # Food & Drink
    "Japanese snack box",
    "Japanese candy assortment",
    "Japanese matcha green tea",
    "Japanese whisky glass",
    "Japanese rice seasoning furikake",
    "Japanese instant ramen variety",
    # Stationery & Art
    "Japanese washi tape",
    "Japanese calligraphy brush ink",
    "Japanese paper origami",
    # Kitchen & Home
    "Japanese knife gyuto",
    "Japanese whetstone sharpening",
    "Japanese cast iron teapot",
    "Japanese bento box",
    "Japanese ceramic plate",
    "Japanese incense",
    # Textiles
    "Japanese fabric furoshiki",
    "Japanese tenugui towel",
    "Imabari towel Japan",
    # Tools & Craft
    "Japanese woodworking chisel",
    "Japanese scissors professional",
    "Japanese garden tools",
    # Collectibles & Pop Culture
    "Ichiban Kuji figure Japan",
    "Gashapon capsule toy Japan",
    "Japanese city pop vinyl record",
    "Anime figure Japan exclusive",
    "Japanese trading card sleeves",
    # Fashion
    "Japanese selvedge denim",
    "Japanese leather wallet",
    "Japanese tabi shoes",
    # Electronics
    "Japanese mechanical keyboard",
    "Casio Japan domestic model",
]

def main():
    token = get_token()
    print(f"✅ Token acquired\n")

    all_items = []  # (query, title, price, category_path, total_results)

    for i, q in enumerate(QUERIES):
        print(f"[{i+1}/{len(QUERIES)}] \"{q}\"", end="")
        items, total = search(token, q, limit=20)
        print(f" → {total:,} total results, {len(items)} fetched")

        for item in items:
            price_val = float(item.get("price", {}).get("value", "0"))
            currency = item.get("price", {}).get("currency", "")
            title = item.get("title", "")
            cats = [c.get("categoryName", "") for c in item.get("categories", [])]
            cat_path = " > ".join(cats) if cats else "Unknown"

            if currency == "USD" and 5 <= price_val <= 2000:
                all_items.append({
                    "query": q,
                    "title": title,
                    "price": price_val,
                    "category": cat_path,
                    "leaf_category": cats[-1] if cats else "Unknown",
                })

        time.sleep(0.3)

    print(f"\n{'='*70}")
    print(f"📊 Total items collected: {len(all_items)}")

    # ── Analyze by eBay category ──
    cat_counter = Counter(item["leaf_category"] for item in all_items)
    print(f"\n🏷️  TOP 30 eBay Categories (by listing count):")
    for cat, count in cat_counter.most_common(30):
        avg_price = sum(i["price"] for i in all_items if i["leaf_category"] == cat) / count
        print(f"  {count:3d}x  ${avg_price:>7.0f} avg  │  {cat}")

    # ── Find items NOT in our current list ──
    # Load current items
    with open(ROOT / "public" / "data" / "items.json") as f:
        current = json.load(f)
    current_names = set()
    for item in current:
        current_names.add(item["name"]["en"].lower())
        current_names.add(item["id"])

    # ── Group by product type and find popular ones ──
    # Extract key product terms
    product_terms = Counter()
    for item in all_items:
        words = item["title"].lower().split()
        # Look for 2-3 word product descriptors
        for j in range(len(words) - 1):
            bigram = f"{words[j]} {words[j+1]}"
            if any(skip in bigram for skip in ["free ship", "brand new", "lot of", "set of", "us ship", "fast ship"]):
                continue
            product_terms[bigram] += 1
        if len(words) > 2:
            for j in range(len(words) - 2):
                trigram = f"{words[j]} {words[j+1]} {words[j+2]}"
                if any(skip in trigram for skip in ["free ship", "brand new", "lot of"]):
                    continue
                product_terms[trigram] += 1

    print(f"\n🔑 TOP 40 Product Terms (frequency):")
    for term, count in product_terms.most_common(40):
        if count >= 3:
            print(f"  {count:3d}x  {term}")

    # ── Suggest new items ──
    print(f"\n{'='*70}")
    print(f"💡 SAMPLE LISTINGS by Query (items we might want to add):\n")

    for q in QUERIES:
        q_items = [i for i in all_items if i["query"] == q]
        if not q_items:
            continue
        # Sort by price, take middle range
        q_items.sort(key=lambda x: x["price"])
        mid = len(q_items) // 2
        sample = q_items[max(0, mid-2):mid+3]
        if sample:
            avg = sum(i["price"] for i in q_items) / len(q_items)
            print(f"  📌 \"{q}\" ({len(q_items)} items, avg ${avg:.0f})")
            for s in sample[:3]:
                print(f"     ${s['price']:>7.0f}  {s['title'][:80]}")
            print()


if __name__ == "__main__":
    main()
