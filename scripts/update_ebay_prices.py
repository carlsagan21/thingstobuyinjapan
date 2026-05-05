#!/usr/bin/env python3
"""
Fetch current eBay listing prices for items in items.json using the Browse API.

Usage:
  1. Copy .env.example to .env and fill in your eBay API credentials
  2. pip install requests python-dotenv
  3. python scripts/update_ebay_prices.py [--dry-run] [--category CATEGORY]

The script searches eBay US for each item's English name, collects active
listing prices, and updates estimatedPriceUsd with the median price.
"""

import argparse
import base64
import json
import os
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
ITEMS_PATH = ROOT / "public" / "data" / "items.json"
ENV_PATH = ROOT / ".env"

EBAY_PRODUCTION_URL = "https://api.ebay.com"
EBAY_SANDBOX_URL = "https://api.sandbox.ebay.com"

# How many eBay results to fetch per item (max 200)
RESULTS_PER_ITEM = 50

# Minimum number of eBay listings to trust the median price
MIN_LISTINGS = 3

# Sleep between API calls to avoid rate limits (seconds)
API_DELAY = 0.5

# eBay search keywords mapped from item id → custom search query overrides.
# If an item id is listed here, this query is used instead of the English name.
# This is useful when the English name is too generic.
SEARCH_OVERRIDES: dict[str, str] = {
    "pokemon-tcg-jp-box": "Pokemon TCG Japanese Booster Box sealed",
    "nintendo-jp-limited": "Nintendo Switch Japan exclusive limited edition game",
    "sailor-pen": "Sailor Pro Gear fountain pen",
    "fuji-instax-jp": "Fujifilm Instax Mini Japan exclusive color",
    "skii-jp-set": "SK-II Japan set",
    "kitkat-japan": "KitKat Japan exclusive flavor box",
    "casio-gshock-jp": "G-Shock Japan exclusive limited model",
    "bandai-figure": "Bandai Tamashii Nations limited figure",
    "muji-jp-only": "Muji Japan exclusive",
    "uniqlo-collab": "Uniqlo UT Japan exclusive collaboration t-shirt",
    "hobonichi-techo": "Hobonichi Techo planner limited cover",
    "pilot-custom-fp": "Pilot Custom 823 fountain pen",
    "tombow-mono-set": "Tombow Mono limited set Japan",
    "ricoh-gr3": "Ricoh GR III camera",
    "sony-headphones-jp": "Sony WF-1000XM5",
    "grand-seiko-domestic": "Grand Seiko SBGA Japan",
    "seiko5-jp-limited": "Seiko 5 Japan limited exclusive",
    "shiseido-jp-only": "Shiseido Elixir Japan",
    "curel-jp-size": "Curel Japan moisturizer",
    "hadalabo-1l": "Hada Labo Premium lotion Japan",
    "onitsuka-jp-color": "Onitsuka Tiger Mexico 66 Japan exclusive",
    "bape-tokyo-only": "BAPE hoodie Japan exclusive Tokyo",
    "ghibli-store": "Studio Ghibli Japan exclusive goods",
    "sanrio-collab": "Sanrio Hello Kitty Japan exclusive",
    "good-smile-nendo": "Nendoroid limited exclusive Japan",
    "final-e5000": "Final Audio E5000",
    "jvc-fx1100": "JVC HA-FX1100",
    "ath-msr7b": "Audio Technica ATH-MSR7b",
    "sony-nw-a306": "Sony Walkman NW-A306",
    "balmuda-toaster": "Balmuda Toaster",
    "twinbird-grinder": "Twinbird CM-D457B coffee grinder",
    "olympus-pen-f": "Olympus PEN-F camera used",
    "iwatani-bo": "Iwatani cassette gas stove portable",
    "nintendo-3ds-ll-jp": "New 3DS LL Japan limited color",
    "ps5-jp-bundle": "PS5 Japan limited bundle",
    "yugioh-ocg-box": "Yu-Gi-Oh OCG Japanese Booster Box",
    "dragonball-fw": "Dragon Ball Fusion World Booster Box",
    "one-piece-tcg": "One Piece Card Game Japanese Booster Box",
    "atlus-famitsu-dx": "Atlus Famitsu DX Pack limited Persona",
    "splatoon-controller-jp": "Splatoon Pro Controller Japan",
    "famicom-retro": "Famicom console used Japan",
    "iroshizuku-50ml": "Pilot Iroshizuku ink 50ml",
    "sailor-studio-ink": "Sailor ink Studio",
    "platinum-3776": "Platinum 3776 Century fountain pen",
    "nakaya-custom": "Nakaya fountain pen urushi",
    "itoya-romeo3": "Itoya Romeo fountain pen",
    "midori-tn-starter": "Midori Travelers Notebook",
    "mitsubishi-kurutoga-roulette": "Kuru Toga Roulette mechanical pencil",
    "pilot-coleto-set": "Pilot Hi Tec C Coleto set",
    "stalogy-365": "Stalogy 365 notebook",
    "maruman-mnemosyne": "Maruman Mnemosyne notebook",
    "dhc-cleansing-oil": "DHC Deep Cleansing Oil 200ml",
    "anessa-uv": "Anessa Perfect UV Sunscreen",
    "biore-uv-aqua": "Biore UV Aqua Rich Watery Essence",
    "cure-aqua-gel": "Cure Natural Aqua Gel",
    "senka-perfect-whip": "Senka Perfect Whip face wash",
    "albion-skin-conditioner": "Albion Skin Conditioner",
    "decorte-aq": "Cosme Decorte AQ Meliority",
    "suqqu-brush": "SUQQU brush Japan",
    "shu-ultime8": "Shu Uemura ultime8 cleansing oil",
    "saborino-morning": "Saborino Morning Mask",
    "cdg-japan-store": "Comme des Garcons Japan exclusive",
    "visvim-jp": "Visvim Japan",
    "kapital-denim": "Kapital Century denim Japan",
    "wtaps-tokyo": "WTAPS Tokyo exclusive",
    "beams-japan-store": "Beams Japan exclusive",
    "yohji-ys": "Yohji Yamamoto Y's Japan",
    "nb-tokyo-design-studio": "New Balance Tokyo Design Studio",
    "buzzricksons-ma1": "Buzz Rickson MA-1 Japan",
    "tokyo-disney-merch": "Tokyo Disney exclusive Japan",
    "usj-mario": "USJ Super Nintendo World exclusive Japan",
    "jump-shop-tokyo": "Jump Shop exclusive Japan",
    "pokemon-center-plush": "Pokemon Center exclusive plush Japan",
    "premium-bandai-web": "Premium Bandai web exclusive",
    "gunpla-mg-limited": "Gundam Master Grade limited Gundam Base",
    "demon-slayer-fig": "Demon Slayer figure limited Japan Ichiban Kuji",
    "jjk-jump-shop": "Jujutsu Kaisen Jump Shop exclusive",
    "hololive-merch": "Hololive limited merchandise Japan",
    "ghibli-park": "Ghibli Park exclusive goods",
    "comiket-doujin": "Comiket exclusive goods Japan",
    "royce-nama": "Royce Nama chocolate Japan",
    "tokyo-banana-box": "Tokyo Banana box Japan",
    "yokumoku-cigare": "Yokumoku Cigare tin",
    "ippodo-matcha": "Ippodo matcha Japan",
    "pocky-jp-flavors": "Pocky Japan exclusive flavor",
    "calpis-concentrate": "Calpis concentrate Japan",
    "ichiran-takehome": "Ichiran Ramen take home set",
    "bourbon-alfort": "Bourbon Alfort Japan limited",
    "regional-senbei": "Japanese senbei regional limited box",
    "citizen-attesa-jp": "Citizen Attesa Japan",
    "seiko-presage-sakura": "Seiko Presage Japan limited",
    "seiko-prospex-jp": "Seiko Prospex Japan limited",
    "orient-star-jp": "Orient Star Japan",
    "kurono-tokyo": "Kurono Tokyo watch",
    "shun-classic": "Shun Classic santoku knife",
    "tojiro-dp": "Tojiro DP gyuto knife",
    "sakai-takayuki-damascus": "Sakai Takayuki Damascus knife",
    "iga-donabe": "Iga yaki donabe clay pot",
    "iwachu-tetsubin": "Iwachu Nambu cast iron teapot",
    "hario-v60-jp": "Hario V60 Japan exclusive color set",
}


# ---------------------------------------------------------------------------
# eBay API helpers
# ---------------------------------------------------------------------------


def get_base_url(env: str) -> str:
    """Return the eBay API base URL for the given environment."""
    return EBAY_SANDBOX_URL if env == "SANDBOX" else EBAY_PRODUCTION_URL


def get_access_token(client_id: str, client_secret: str, base_url: str) -> str:
    """Obtain an application access token via Client Credentials Grant."""
    url = f"{base_url}/identity/v1/oauth2/token"
    auth_str = f"{client_id}:{client_secret}"
    encoded = base64.b64encode(auth_str.encode()).decode()

    resp = requests.post(
        url,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encoded}",
        },
        data={
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope",
        },
        timeout=15,
    )

    if resp.status_code != 200:
        print(f"❌ Token request failed ({resp.status_code}): {resp.text}")
        sys.exit(1)

    token = resp.json()["access_token"]
    print(f"✅ Access token acquired (expires in {resp.json().get('expires_in', '?')}s)")
    return token


def search_ebay(
    token: str,
    base_url: str,
    query: str,
    limit: int = RESULTS_PER_ITEM,
) -> list[dict]:
    """Search eBay Browse API and return item summaries."""
    url = f"{base_url}/buy/browse/v1/item_summary/search"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
        "X-EBAY-C-ENDUSERCTX": "contextualLocation=country%3DUS",
    }
    params = {
        "q": query,
        "limit": str(min(limit, 200)),
        "filter": "buyingOptions:{FIXED_PRICE|AUCTION},priceCurrency:USD",
        "sort": "newlyListed",
    }

    resp = requests.get(url, headers=headers, params=params, timeout=15)

    if resp.status_code == 429:
        print("  ⏳ Rate limited, waiting 5s...")
        time.sleep(5)
        return search_ebay(token, base_url, query, limit)

    if resp.status_code != 200:
        print(f"  ⚠️  Search failed ({resp.status_code}): {resp.text[:200]}")
        return []

    data = resp.json()
    return data.get("itemSummaries", [])


def extract_prices(summaries: list[dict]) -> list[float]:
    """Extract USD prices from eBay item summaries."""
    prices: list[float] = []
    for item in summaries:
        price_info = item.get("price", {})
        currency = price_info.get("currency", "")
        value = price_info.get("value", "")

        if currency == "USD" and value:
            try:
                prices.append(float(value))
            except ValueError:
                continue
    return prices


def compute_median_price(prices: list[float]) -> float | None:
    """Return the median of prices, or None if insufficient data."""
    if len(prices) < MIN_LISTINGS:
        return None
    return round(statistics.median(prices))


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------


def load_items() -> list[dict]:
    """Load items from items.json."""
    with open(ITEMS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_items(items: list[dict]) -> None:
    """Save items back to items.json."""
    with open(ITEMS_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
        f.write("\n")


def build_query(item: dict) -> str:
    """Build a search query for the given item."""
    item_id = item["id"]
    if item_id in SEARCH_OVERRIDES:
        return SEARCH_OVERRIDES[item_id]
    # Fall back to the English name
    return item["name"]["en"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Update eBay prices for items.json")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print updates without writing to items.json",
    )
    parser.add_argument(
        "--category",
        type=str,
        default=None,
        help="Only update items in this category (e.g. 'watches', 'beauty')",
    )
    parser.add_argument(
        "--item",
        type=str,
        default=None,
        help="Only update a specific item by ID",
    )
    args = parser.parse_args()

    # Load env
    load_dotenv(ENV_PATH)
    client_id = os.getenv("EBAY_CLIENT_ID", "")
    client_secret = os.getenv("EBAY_CLIENT_SECRET", "")
    environment = os.getenv("EBAY_ENVIRONMENT", "PRODUCTION")

    if not client_id or not client_secret or "your_" in client_id:
        print("❌ Missing eBay API credentials.")
        print("   Copy .env.example to .env and fill in your Client ID and Secret.")
        print("   Get them at https://developer.ebay.com/my/keys")
        sys.exit(1)

    base_url = get_base_url(environment)
    print(f"🌐 Environment: {environment} ({base_url})")

    # Get token
    token = get_access_token(client_id, client_secret, base_url)

    # Load items
    items = load_items()
    print(f"📦 Loaded {len(items)} items from items.json\n")

    # Filter if needed
    target_items = items
    if args.category:
        target_items = [i for i in items if i["category"] == args.category]
        print(f"🔍 Filtering to category '{args.category}': {len(target_items)} items\n")
    if args.item:
        target_items = [i for i in items if i["id"] == args.item]
        print(f"🔍 Filtering to item '{args.item}': {len(target_items)} items\n")

    # Process
    updated = 0
    skipped = 0
    errors = 0
    results_log: list[dict] = []

    for idx, item in enumerate(target_items):
        query = build_query(item)
        old_price = item["estimatedPriceUsd"]

        print(f"[{idx + 1}/{len(target_items)}] {item['id']}")
        print(f"  Query: \"{query}\"")

        summaries = search_ebay(token, base_url, query)
        prices = extract_prices(summaries)

        if not prices:
            print(f"  ⚠️  No USD prices found ({len(summaries)} results)")
            skipped += 1
            time.sleep(API_DELAY)
            continue

        median = compute_median_price(prices)

        if median is None:
            print(f"  ⚠️  Too few listings ({len(prices)} < {MIN_LISTINGS})")
            skipped += 1
            time.sleep(API_DELAY)
            continue

        change = median - old_price
        pct = (change / old_price * 100) if old_price else 0
        arrow = "📈" if change > 0 else "📉" if change < 0 else "="

        print(f"  Listings: {len(prices)}, Range: ${min(prices):.0f}-${max(prices):.0f}")
        print(f"  Median: ${median} (was ${old_price}) {arrow} {change:+.0f} ({pct:+.1f}%)")

        results_log.append({
            "id": item["id"],
            "name": item["name"]["en"],
            "category": item["category"],
            "old_price": old_price,
            "new_price": median,
            "change": change,
            "listings_found": len(prices),
            "price_range": f"${min(prices):.0f}-${max(prices):.0f}",
        })

        if not args.dry_run and change != 0:
            item["estimatedPriceUsd"] = median
            updated += 1

        time.sleep(API_DELAY)

    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Summary: {updated} updated, {skipped} skipped, {errors} errors")
    print(f"   Total items processed: {len(target_items)}")

    if results_log:
        print("\n📋 Changes:")
        for r in sorted(results_log, key=lambda x: abs(x["change"]), reverse=True):
            if r["change"] != 0:
                arrow = "📈" if r["change"] > 0 else "📉"
                print(
                    f"  {arrow} {r['id']}: ${r['old_price']} → ${r['new_price']} "
                    f"({r['change']:+.0f}, {len(str(r['listings_found']))} listings, "
                    f"range {r['price_range']})"
                )

    if not args.dry_run and updated > 0:
        save_items(items)
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        print(f"\n✅ items.json updated ({updated} items) at {now}")
    elif args.dry_run:
        print("\n🔍 Dry run — no changes written.")
    else:
        print("\n✅ No price changes needed.")


if __name__ == "__main__":
    main()
