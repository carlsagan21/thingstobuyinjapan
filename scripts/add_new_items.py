import json

items_path = "public/data/items.json"

with open(items_path, "r", encoding="utf-8") as f:
    items = json.load(f)

new_items = [
    {
        "id": "jnat-whetstone",
        "name": {
            "ko": "일본 천연 숫돌 (JNAT)",
            "en": "Japanese Natural Whetstone (JNAT)",
            "ja": "天然砥石"
        },
        "category": "kitchenware",
        "priceJpy": 7500,
        "estimatedPriceUsd": 150,
        "whereToBuy": {
            "ko": "도큐핸즈, 전통 철물점, 갓파바시 도구거리",
            "en": "Tokyu Hands, Traditional Hardware Stores, Kappabashi",
            "ja": "東急ハンズ、合羽橋道具街"
        },
        "notes": {
            "ko": "요리사와 목수들에게 인기가 엄청남. 무게가 무거우니 배송비 고려 필요.",
            "en": "Huge demand among chefs and woodworkers. Heavy item, so factor in shipping costs.",
            "ja": "料理人や大工に大人気。重いので送料に注意。"
        }
    },
    {
        "id": "city-pop-vinyl",
        "name": {
            "ko": "일본 시티팝 LP 바이닐",
            "en": "Japanese City Pop Vinyl Record",
            "ja": "シティ・ポップ レコード"
        },
        "category": "collectibles",
        "priceJpy": 2500,
        "estimatedPriceUsd": 75,
        "whereToBuy": {
            "ko": "디스크유니온, 타워레코드, 동네 중고 레코드점",
            "en": "Disk Union, Tower Records, Used Record Stores",
            "ja": "ディスクユニオン、タワーレコード、中古レコード店"
        },
        "notes": {
            "ko": "타케우치 마리야, 타카나카 마사요시 등의 오리지널 프레싱은 이베이에서 바로 팔림.",
            "en": "Original pressings of Mariya Takeuchi, Masayoshi Takanaka sell instantly on eBay.",
            "ja": "竹内まりや、高中正義などのオリジナル盤はeBayですぐ売れる。"
        }
    },
    {
        "id": "marugo-tabi-shoes",
        "name": {
            "ko": "마루고 타비 스니커즈",
            "en": "Marugo Tabi Sneakers",
            "ja": "丸五 足袋スニーカー"
        },
        "category": "fashion",
        "priceJpy": 5000,
        "estimatedPriceUsd": 75,
        "whereToBuy": {
            "ko": "작업복 전문점(워크맨 등), 마루고 직영점",
            "en": "Workman, Marugo Direct Stores",
            "ja": "ワークマン、丸五直営店"
        },
        "notes": {
            "ko": "발가락이 갈라진 독특한 디자인으로 해외 닌자/서브컬처 팬들에게 인기 폭발.",
            "en": "Split-toe design is hugely popular with ninja/subculture fans abroad.",
            "ja": "足袋デザインが海外の忍者・サブカルファンに大人気。"
        }
    },
    {
        "id": "japanese-chisel-yasuki",
        "name": {
            "ko": "야스키 하가네 조각도/끌",
            "en": "Yasuki Hagane Woodworking Chisel",
            "ja": "安来鋼 彫刻刀・鑿"
        },
        "category": "electronics",
        "priceJpy": 2000,
        "estimatedPriceUsd": 50,
        "whereToBuy": {
            "ko": "도큐핸즈, 전통 철물점",
            "en": "Tokyu Hands, Traditional Hardware Stores",
            "ja": "東急ハンズ、金物屋"
        },
        "notes": {
            "ko": "서양 도구보다 날카롭고 절삭력이 좋아 목공 매니아들의 고정 수요가 있음.",
            "en": "Sharper than Western tools; steady demand from woodworking enthusiasts.",
            "ja": "西洋の道具より切れ味が良く、木工愛好家の固定需要がある。"
        }
    },
    {
        "id": "edo-kiriko-glass",
        "name": {
            "ko": "에도 키리코 위스키 잔",
            "en": "Edo Kiriko Whiskey Glass",
            "ja": "江戸切子 グラス"
        },
        "category": "kitchenware",
        "priceJpy": 3500,
        "estimatedPriceUsd": 65,
        "whereToBuy": {
            "ko": "백화점 리빙관, 아사쿠사 전통공예품점",
            "en": "Department Stores, Asakusa Craft Shops",
            "ja": "百貨店、浅草の伝統工芸品店"
        },
        "notes": {
            "ko": "수제 컷팅 유리의 영롱함 덕분에 선물용이나 위스키 수집가들에게 인기.",
            "en": "Popular among whiskey collectors and for gifts due to beautiful hand-cut glass.",
            "ja": "手作りカットガラスの美しさから、ウイスキー収集家やギフトに人気。"
        }
    },
    {
        "id": "jubako-bento-box",
        "name": {
            "ko": "원목 쥬바코 (찬합) 도시락",
            "en": "Wooden Jubako Bento Box",
            "ja": "木製 重箱"
        },
        "category": "kitchenware",
        "priceJpy": 5500,
        "estimatedPriceUsd": 120,
        "whereToBuy": {
            "ko": "백화점, 로프트(LOFT), 전통 식기점",
            "en": "Department Stores, LOFT, Traditional Tableware Shops",
            "ja": "百貨店、LOFT、伝統食器店"
        },
        "notes": {
            "ko": "고급스러운 나무재질과 옻칠 마감이 서양인들에게 오리엔탈 인테리어/실사용으로 인기.",
            "en": "High-end wood and lacquer finish is popular for both use and Oriental decor.",
            "ja": "高級な木材と漆塗りが実用・インテリア両面で西洋人に人気。"
        }
    },
    {
        "id": "shodo-calligraphy-set",
        "name": {
            "ko": "일본 서예(쇼도) 세트",
            "en": "Japanese Shodo Calligraphy Set",
            "ja": "書道セット"
        },
        "category": "stationery",
        "priceJpy": 2000,
        "estimatedPriceUsd": 50,
        "whereToBuy": {
            "ko": "세카이도(Sekaido), 이토야(Itoya), 로프트",
            "en": "Sekaido, Itoya, LOFT",
            "ja": "世界堂、伊東屋、LOFT"
        },
        "notes": {
            "ko": "붓, 벼루, 먹물이 포함된 스타터 세트. 서양의 동양 아트 매니아들이 많이 찾음.",
            "en": "Starter set with brush, inkstone, and ink. Sought after by Oriental art enthusiasts.",
            "ja": "筆、硯、墨のセット。東洋アート愛好家によく売れる。"
        }
    }
]

# SEARCH_OVERRIDES update
overrides = {
    "jnat-whetstone": "Japanese Natural Whetstone JNAT",
    "city-pop-vinyl": "Japanese city pop vinyl record LP",
    "marugo-tabi-shoes": "Marugo Sneakers Tabi Sports Jog",
    "japanese-chisel-yasuki": "Japanese woodworking chisel Yasuki",
    "edo-kiriko-glass": "Japanese Kiriko Cut Glass Whiskey",
    "jubako-bento-box": "Jubako Bento Box Japanese Wooden",
    "shodo-calligraphy-set": "Japanese Calligraphy Shodo Brush Set"
}

items.extend(new_items)

with open(items_path, "w", encoding="utf-8") as f:
    json.dump(items, f, indent=2, ensure_ascii=False)
    f.write("\n")
    
print("Added 7 new trending items to items.json")
