import requests
from langchain_core.tools import tool
from typing import List
from time import time
# --- 1. GÜNÜN FIRSATLARI ---
@tool
def get_steam_specials(start_index: int = 0, end_index: int = 5):
    """
    Fetches 'Daily Deals', major discounts, and featured campaigns from the Steam homepage.
    Use this tool when the user asks for general discounts or "What's on sale?".

    Args:
        start_index (int): The starting index for the game list (e.g., 0).
        end_index (int): The ending index for the game list (e.g., 5).

    PAGINATION LOGIC:
    - First request: Use start_index=0, end_index=5.
    - If user asks for "more" or "other" games: INCREASE the indices (e.g., start_index=5, end_index=10).
    - Never repeat the same indices in the same conversation.
    """

    print("Steam specials tool çalışıyor")
    # 1. Veriyi Çek
    url = "https://store.steampowered.com/api/featuredcategories?cc=tr"
    try:
        response = requests.get(url)
        data = response.json()

        # 'specials' kategorisi genelde en iyi indirimlerdir
        specials = data.get("specials", {}).get("items", [])

        # --- SAYFALAMA MANTIĞI (PAGINATION) ---
        # Listeyi senin verdiğin parametrelere göre kesiyoruz
        # Eğer liste yetmezse (IndexError) boş döner, python bunu yönetir.
        selected_games = specials[start_index:end_index]

        if not selected_games:
            return "⚠️ Daha fazla öne çıkan indirim bulunamadı. (End of list)"

        results = []
        for item in selected_games:
            results.append({
                "oyun": item["name"],
                "eski_fiyat": item["original_price"] / 100,
                "yeni_fiyat": item["final_price"] / 100,
                "indirim": f"%{item['discount_percent']}",
                "steam_url": f"https://store.steampowered.com/app/{item['id']}"
            })

        return results

    except Exception as e:
        return f"Steam Specials API hatası: {str(e)}"

# --- 2. OYUN ARAMA VE FİYAT ---
@tool
def check_steam_price(game_name: str) -> str:
    """
    Checks the price of a SINGLE game on Steam.
    Input must be a simple string (game name).
    Example: "Elden Ring"
    """
    # İsim temizliği (Tırnak ve boşlukları at)
    global id_info
    clean_name = str(game_name).replace('"', '').replace("'", "").strip()

    print(f"\n🔎 FİYAT SORGUSU: {clean_name}")

    try:
        url = f"https://store.steampowered.com/api/storesearch/?term={clean_name}&l=turkish&cc=tr"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return f"⚠️ {clean_name}: Steam erişim hatası."

        data = response.json()

        if data["total"] == 0:
            print(" 🚫 BULUNAMADI")
            return f"🚫 {clean_name}: Steam'de bulunamadı."

        # Oyun bulundu, veriyi çekelim
        item = data["items"][0]
        title = item["name"]
        price_str = "Fiyat Bilgisi Yok"

        if "price" in item:
            id_info = item["id"]
            price_info = item["price"]
            final = price_info["final"] / 100
            currency = price_info["currency"]
            discount = 0

            price_str = f"{final} {currency}"
            if discount > 0:
                price_str += f" (🔥 %{discount} İNDİRİM!)"

        elif item.get("is_free", False):
            price_str = "Ücretsiz 🆓"

        print(f" ✅ {price_str}")
        return f"✅ {title}: {price_str}, id: {id_info}"

    except Exception as e:
        print(f" 💥 HATA: {e}")
        return f"❌ {clean_name}: Teknik hata ({str(e)})."



def check_steam_id(game_name: str) -> str:
    """
    Checks the price of a SINGLE game on Steam.
    Input must be a simple string (game name).
    Example: "Elden Ring"
    """
    # İsim temizliği (Tırnak ve boşlukları at)
    global id_info
    clean_name = str(game_name).replace('"', '').replace("'", "").strip()

    print(f"\n🔎 FİYAT SORGUSU: {clean_name}")

    try:
        url = f"https://store.steampowered.com/api/storesearch/?term={clean_name}&l=turkish&cc=tr"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return f"⚠️ {clean_name}: Steam erişim hatası."

        data = response.json()

        if data["total"] == 0:
            print(" 🚫 BULUNAMADI")
            return f"🚫 {clean_name}: Steam'de bulunamadı."

        # Oyun bulundu, veriyi çekelim
        item = data["items"][0]
        title = item["name"]
        price_str = "Fiyat Bilgisi Yok"

        if "price" in item:
            id_info = item["id"]
            price_info = item["price"]
            final = price_info["final"] / 100
            currency = price_info["currency"]
            discount = 0

            price_str = f"{final} {currency}"
            if discount > 0:
                price_str += f" (🔥 %{discount} İNDİRİM!)"

        elif item.get("is_free", False):
            price_str = "Ücretsiz 🆓"

        return id_info

    except Exception as e:
        print(f" 💥 HATA: {e}")
        return f"❌ {clean_name}: Teknik hata ({str(e)})."

# --- 3. İNCELEME VE PUAN ---
@tool
def get_steam_app_review(game_name: str):
    """
    If you want steam reviews use this tool and use game name for search
    """
    game_id = check_steam_id(game_name)
    print("Steam review tool çalışıyor")
    try:
        url = f"https://store.steampowered.com/appreviews/{game_id}?json=1&language=english"
        response = requests.get(url, timeout=10)
        data = response.json()

        item = data.get("query_summary")

        if not item:
            return "İnceleme bilgisi bulunamadı."

        return {
            "genel_durum": item.get("review_score_desc", "Bilinmiyor"),  # Örn: "Son Derece Olumlu"
            "toplam_inceleme": item.get("total_reviews"),
            "pozitif_sayisi": item.get("total_positive"),
            "negatif_sayisi": item.get("total_negative"),
            "puan_skoru": item.get("review_score")  # 0-10 arası gizli skor
        }

    except Exception as e:
        return f"İncelemeler alınırken hata oluştu: {str(e)}"