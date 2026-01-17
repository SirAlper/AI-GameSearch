from langchain_community.tools import TavilySearchResults  # Standart ve en kararlı kütüphane
from langchain_core.tools import tool
from src.steam_api import check_steam_price, get_steam_specials, get_steam_app_review

# 1. Motoru Hazırla (Gizli Değişken)
# Bunu modele vermeyeceğiz, sadece içeride kullanacağız.
_tavily_engine = TavilySearchResults(
    max_results=2,  # 5 yerine 2 sonuç getir (Yarı yarıya tasarruf)
    search_depth="basic",  # "advanced" yerine "basic" (Daha az veri, daha hızlı)
    include_raw_content=False,  # ASLA True yapma (Tüm HTML'i çeker)
    include_answer=True,  # Sadece Tavily'nin özetini al
    max_tokens=1000
    # Hatalı parametreleri engellemek için filtreleme yapıyoruz
)


# 2. Basit Wrapper (Modelin Göreceği Tek Şey)
@tool
def simple_web_search(query: str):
    """
    Perform a web search for game recommendations, reviews don't use for game prices and game id etc. this type information can be claimed by other tools.
    Useful for finding 'best indie games', 'underrated games', or checking reviews.

    Args:
        query (str): The search string. Example: "best steam games on sale"
    """
    # 1. Sorgu Temizliği
    clean_query = query.strip().strip('"').strip("'")
    print(f"🌍 Web Search Çalışıyor: {clean_query}")

    try:
        # 2. Motoru Çalıştır
        # TavilySearchResults, doğrudan {"query": ...} sözlüğünü kabul eder.
        return _tavily_engine.invoke({"query": clean_query})
    except Exception as e:
        return f"Arama sırasında hata oluştu: {str(e)}"


# 3. Listeyi Oluştur
ALL_TOOLS = [
    simple_web_search,
    check_steam_price,
    get_steam_specials,
    get_steam_app_review
]
TOOLS_BY_NAME = {tool.name: tool for tool in ALL_TOOLS}
